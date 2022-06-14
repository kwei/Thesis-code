# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')

import cvxpy as cp
import csv
import numpy as np
import math

global envName
envName = ""

from progressbar import *
widgets = ['Progress: ',Percentage(), ' ', Bar('█')]

def setSOCPEnv(_envName):
  global envName
  if _envName == "sdp":
    envName = "sdp"
  elif _envName == "socp":
    envName = "socp"
  elif _envName == "3d_mj":
    envName = "3d_mj"
  elif _envName == "differentUAV":
    envName = "differentUAV"
  elif _envName == "differentUAV_ALLSamples":
    envName = "differentUAV_ALLSamples"
  elif _envName == "sdp_realRSS":
    envName = "sdp_realRSS"
  else:
    envName = ""
  # print(envName)
    
class SOCP():
  def __init__(self):
    self._var_t = None
    self._var_p = None
    self._constraint = None


  def buildConstraint(self, targets, anchors, pathLossModel):
    if (not envName == "")and (not envName == "3d_mj"):
      env =  __import__('utils.env_'+envName, fromlist=['env']).env
    else:
      env =  __import__('utils.env'+envName, fromlist=['env']).env
    soc_constraints = []
    for i, target_i in enumerate(targets):
      for j, target_j in enumerate(targets):
        if not target_i.id == target_j.id:
          rss = target_i.searchRSSById(target_j.id)
          d = pathLossModel.estimateDistance(target_i.power, rss)
          soc_constraints.append(cp.SOC([d] @ self._var_t, self._var_p[i] - self._var_p[j]))

      for anchor in anchors:
        rss = target_i.searchRSSById(anchor.id)
        d = pathLossModel.estimateDistance(target_i.power, rss)
        soc_constraints.append(cp.SOC([d] @ self._var_t, self._var_p[i] - np.array(anchor.observedPosition)))

    self._constraint = soc_constraints

  def doSolve(self, log):
    if (not envName == "")and (not envName == "3d_mj"):
      env =  __import__('utils.env_'+envName, fromlist=['env']).env
    else:
      env =  __import__('utils.env'+envName, fromlist=['env']).env
    prob = cp.Problem(cp.Minimize(self._var_t), self._constraint + [p[2]>=0 for p in self._var_p] )
    prob.solve(verbose=log)

  @property
  def var_t(self):
    return self._var_t

  @property
  def var_p(self):
    return self._var_p

  @var_t.setter
  def var_t(self, t):
    self._var_t = t

  @var_p.setter
  def var_p(self, p):
    self._var_p = p


def calculateSOCP(groupListSamples, UAVsSamples, pathLossModel, savePath=None):
  if not envName == "" :
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env

  socpResultSamples = {}
  for sample, groupList in groupListSamples.items():
    socp = SOCP()
    socp.var_t = cp.Variable(1)
    socp.var_p = [cp.Variable(env.DIMENSION) for i in range(env.N_ngps)]

    targets = []
    for uavIndex, uav in UAVsSamples[sample].items():
      if uav.observedPosition is None:
        targets.append(uav)
    results = []
    for groupSize, groups in groupList.items():
      for iGroup, group in enumerate(groups):
        print("█", end='')
        anchors = []
        for i in group:
          anchors.append(UAVsSamples[sample][i])

        socp.buildConstraint(targets, anchors, pathLossModel)
        socp.doSolve(log=False)
        results.append([socp.var_p[i].value for i in range(env.N_ngps)])
        sys.stdout.flush()
    socpResultSamples[sample] = results
    print()

  socpResultSamples_reform = {}
  for sample, socpResult in socpResultSamples.items():
    socpResult_uav = []
    for i in range(np.array(socpResult).shape[1]):
      temp = []
      for j in range(np.array(socpResult).shape[0]):
        temp.append(socpResult[j][i])
      socpResult_uav.append(temp)
    socpResultSamples_reform[sample] = socpResult_uav

  if savePath:
    for j in range(env.N_ngps):
      with open(savePath+"/position_{}.csv".format(j), "w") as _csv:
        for i in range(len(socpResultSamples_reform.keys())):
          csvWriter = csv.writer(_csv, delimiter=',')
          csvWriter.writerows(socpResultSamples_reform[i][j])
  
  return socpResultSamples_reform