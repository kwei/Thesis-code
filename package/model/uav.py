# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')

envName = ""
def setUAVEnv(_envName):
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
    
class UAV():
  def __init__(self, id, realPosition, observedPosition):
    if (not envName == "") and (not envName == "3d_mj"):
      env =  __import__('utils.env_'+envName, fromlist=['env']).env
    else:
      env =  __import__('utils.env'+envName, fromlist=['env']).env
    self._id = id
    self._power = env.UAV_TRANSMISSION_POWER
    self._realPosition = realPosition
    self._observedPosition = observedPosition
    self._rssVector = {}
  
  def searchRSSById(self, id):
    return self._rssVector[id]
  
  @property
  def id(self):
    return self._id

  @property
  def power(self):
    return self._power

  @power.setter
  def power(self,power):
    self._power = power

  @property
  def rssVector(self):
    return self._rssVector
  
  def collectRSS(self, index, rss):
    self._rssVector[index] = rss
  
  @property
  def realPosition(self):
    return self._realPosition
  
  @property
  def observedPosition(self):
    return self._observedPosition
  
  @observedPosition.setter
  def observedPosition(self, observedPosition):
    self._observedPosition = observedPosition

if __name__ == '__main__':
  uav_id = 0
  uav_realPosition = [5, 4, 87]
  uav_observedPosition = [6, 4, 87]
  uav = UAV(uav_id, uav_realPosition, uav_observedPosition)

  for id in range(1, 5):
    rss = -52+id*2
    uav.collectRSS(id, rss)
  
  print(uav.__dict__)
  print(uav.searchRSSById(3))