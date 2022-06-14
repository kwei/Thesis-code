# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')
from itertools import combinations
import numpy as np

envName = ""
def setCombinationSetEnv(_envName):
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

def getCombinationSetEnv():
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  print(env.N_ngps)

def generateCombination(uavs, groupSize):
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  groupingCandidates = []
  for id, uav in uavs.items():
    if uav.observedPosition is not None:
      groupingCandidates.append(id)
  return list (map(lambda x: list (x), list (combinations(groupingCandidates, groupSize))))

def combinationSet(UAVsSamples):
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  groupListSamples = {}
  for sample, UAVs in UAVsSamples.items():
    temp = {}
    for groupSize in range(env.groupSizeFrom, env.N_gps+1):
      groupList = generateCombination(UAVs, groupSize)
      temp[groupSize] = groupList
    groupListSamples[sample] = temp
  return groupListSamples

def groupingFromSet(candidates):
  if (not envName == "") and (not envName == "3d_mj"):
    env =  __import__('utils.env_'+envName, fromlist=['env']).env
  else:
    env =  __import__('utils.env'+envName, fromlist=['env']).env
  groupList = {}
  for groupSize in range(env.groupSizeFrom, env.N_gps+1):
    groupList[groupSize] = list (map(lambda x: list (x), list (combinations(candidates, groupSize))))
  return groupList