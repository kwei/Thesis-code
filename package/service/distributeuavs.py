# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')

from model.uav import UAV, setUAVEnv
import importlib

envName = ""

def setDistributeUavsEnv(_envName):
  global envName
  if _envName == "sdp":
    envName = "sdp"
  if _envName == "3d_mj":
    envName = "3d_mj"
  if _envName == "differentUAV":
    envName = "differentUAV"
  if _envName == "differentUAV_ALLSamples":
    envName = "differentUAV_ALLSamples"
  if _envName == "sdp_realRSS":
    envName = "sdp_realRSS"

def TestEnv():
  print("envName",envName)
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  print(env.N)

import pickle
import numpy as np

def distributeUAVs():
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  setUAVEnv(envName)
  UAVs = {}
  # 3-D
  if env.DIMENSION == 3:
    xList = np.random.choice(np.arange(0.0, env.X_RANGE+0.0), env.N, replace=False)
    yList = np.random.choice(np.arange(0.0, env.Y_RANGE+0.0), env.N, replace=False)
    zList = np.random.choice(np.arange(env.UAV_LOWEST_HEIGHT+0.0, env.Z_RANGE+0.0), env.N, replace=False)
    positionList = [xList, yList, zList]
  # 2-D
  elif env.DIMENSION == 2:
    xList = np.random.choice(np.arange(0.0, env.X_RANGE+0.0), env.N, replace=False)
    yList = np.random.choice(np.arange(0.0, env.Y_RANGE+0.0), env.N, replace=False)
    positionList = [xList, yList]
  else:
    raise Exception("Dimension Error")
  
  for uavIndex in range(env.N):
    position = []
    for d in range(env.DIMENSION):
      position.append(positionList[d][uavIndex])
    
    realPosition = position
    observedPosition = position
    uav = UAV(uavIndex, realPosition, observedPosition)
    UAVs[uavIndex] = uav
  return UAVs

def createUAVsSamples(pathLossModel, savePath):
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  UAVsSamples = {}
  for sample in range(env.SAMPLES):
    uavIndexes_withoutGPS = np.random.choice(env.N, env.N_ngps, replace=False)
    UAVs = distributeUAVs()
    for id in uavIndexes_withoutGPS:
      UAVs[id].observedPosition = None
    UAVsSamples[sample] = UAVs
  
  for sample, UAVS in UAVsSamples.items():
    # UAV j obtain the RSS from UAV i.
    for i, uav_i in UAVS.items():
      for j, uav_j in UAVS.items():
        if not i == j:
          realDistance_ij = np.linalg.norm(np.array(uav_i.realPosition) - np.array(uav_j.realPosition))
          rss = pathLossModel.estimateRSS(uav_i.power, realDistance_ij)
          uav_i.collectRSS(j, rss)
  
  f = open(savePath+"/UAVsSamples.pkl", "wb")
  pickle.dump(UAVsSamples, f)
  f.close()

  return UAVsSamples