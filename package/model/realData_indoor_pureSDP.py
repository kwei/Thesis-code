# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')

import cvxpy as cp
import csv
import numpy as np
import math
import pickle

global envName
envName = ""

from progressbar import *
widgets = ['Progress: ',Percentage(), ' ', Bar('█')]

def setSDPEnv(_envName):
  global envName
  envName = "sdp_realRSS"
  # if _envName == "sdp":
  #   envName = "sdp"
  # if _envName == "3d_mj":
  #   envName = "3d_mj"
  # if _envName == "differentUAV":
  #   envName = "differentUAV"
  # if _envName == "differentUAV_ALLSamples":
  #   envName = "differentUAV_ALLSamples"
  # if _envName == "sdp_realRSS":
  #   envName = "sdp_realRSS"
  # print(envName)
    
class SDP():
  def __init__(self):
    self._var_SDPt = None
    self._var_p = None
    self._constraint = None
    with open(rootpath+"/datas/realRSSMeasurements/suitablePower.pkl", "rb") as f:
      self._suitablePower = pickle.load(f)


  def buildConstraint(self, targets, anchors, pathLossModel):
    if (not envName == "")and (not envName == "3d_mj"):
      env =  __import__('utils.env_'+envName, fromlist=['env']).env
    else:
      env =  __import__('utils.env'+envName, fromlist=['env']).env
    soc_constraints = []
    for i, target_i in enumerate(targets):

      for anchor in anchors:
        rss = target_i.searchRSSById(anchor.id)
        # print(target_i.id, anchor.id)
        d = pathLossModel.estimateDistance(self._suitablePower[target_i.id-1][anchor.id-1], rss)
        xi = np.array([anchor.observedPosition]).T
        I = np.identity(3)

        firstRow = np.concatenate((I, (-xi)), axis=1)
        secondRow = np.concatenate((-(xi.T), xi.T @ xi), axis=1)
        Ai = np.concatenate((firstRow,secondRow), axis=0)

        soc_constraints.append(cp.trace(Ai @ self._var_p[i]) * math.pow(10,rss/10)/math.pow(10,(anchor.power-40)/10) - 1 <= self._var_SDPt )
        soc_constraints.append(cp.trace(Ai @ self._var_p[i]) * math.pow(10,rss/10)/math.pow(10,(anchor.power-40)/10) - 1 >= -self._var_SDPt )
        soc_constraints.append(self._var_p[i][-1][-1] == 1)

    self._constraint = soc_constraints

  def doSolve(self, log):
    if (not envName == "")and (not envName == "3d_mj"):
      env =  __import__('utils.env_'+envName, fromlist=['env']).env
    else:
      env =  __import__('utils.env'+envName, fromlist=['env']).env
    prob = cp.Problem(cp.Minimize(self._var_SDPt), self._constraint)
    prob.solve(verbose=log)


  @property
  def var_SDPt(self):
    return self._var_SDPt

  @property
  def var_p(self):
    return self._var_p

  @var_p.setter
  def var_p(self, p):
    self._var_p = p

  @var_SDPt.setter
  def var_SDPt(self, t):
    self._var_SDPt = t


def calculateSDP(groupListSamples, UAVsSamples, pathLossModel, savePath=None):
  if not envName == "" :
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  # print("[calculateSDP] envName: ", envName)
  # print("[calculateSDP] env.N", env.N)
  sdpResultSamples = {}
  for sample, groupList in groupListSamples.items():
    # print("#{}".format(sample), end='')
    sdp = SDP()
    sdp.var_SDPt = cp.Variable(1)
    sdp.var_p = [cp.Variable((env.DIMENSION+1, env.DIMENSION+1), symmetric=True) for i in range(env.N_ngps)]

    targets = []
    for uavIndex, uav in UAVsSamples[sample].items():
      if uav.observedPosition is None:
        targets.append(uav)
    results = []
    for groupSize, groups in groupList.items():
      for group in groups:
        print("█", end='')
        anchors = []
        for i in group:
          anchors.append(UAVsSamples[sample][i])

        sdp.buildConstraint(targets, anchors, pathLossModel)
        sdp.doSolve(log=False)
        results.append([sdp.var_p[i].value[-1][:3] for i in range(env.N_ngps)])
        sys.stdout.flush()
    sdpResultSamples[sample] = results
    print()

  # print(np.array(sdpResultSamples[0]).shape)

  sdpResultSamples_reform = {}
  for sample, socpResult in sdpResultSamples.items():
    socpResult_uav = []
    for i in range(np.array(socpResult).shape[1]):
      temp = []
      for j in range(np.array(socpResult).shape[0]):
        temp.append(socpResult[j][i])
      socpResult_uav.append(temp)
    sdpResultSamples_reform[sample] = socpResult_uav
  
  # print(np.array(sdpResultSamples_reform[0]).shape)

  if savePath:
    for j in range(env.N_ngps):
      with open(savePath+"/position_{}.csv".format(j), "w") as _csv:
        for i in range(len(sdpResultSamples_reform.keys())):
          csvWriter = csv.writer(_csv, delimiter=',')
          csvWriter.writerows(sdpResultSamples_reform[i][j])
  
  return sdpResultSamples_reform