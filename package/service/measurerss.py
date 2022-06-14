# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')

import numpy as np

envName = ""
def setMeasuerRssEnv(_envName):
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

def measureRSS(UAVsSamples, pathLossModel):
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  for sample, UAVS in UAVsSamples.items():
    # UAV j obtain the RSS from UAV i.
    for i, uav_i in UAVS.items():
      for j, uav_j in UAVS.items():
        if not i == j:
          # print(uav_i.id, uav_j.id)
          realDistance_ij = np.linalg.norm(np.array(uav_i.realPosition) - np.array(uav_j.realPosition))
          rss = pathLossModel.estimateRSS(uav_i.power, realDistance_ij)
          uav_i.collectRSS(j, rss)