# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')
envName = ""
def setPathLossModelEnv(_envName):
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


import math
import numpy as np

class PathLossModel():
  def __init__(self):
    if (not envName == "") and (not envName == "3d_mj"):
      env =  __import__('utils.env_'+envName, fromlist=['env']).env
    else:
      env =  __import__('utils.env'+envName, fromlist=['env']).env
    self._refDistance = env.REFERENCE_DISTANCE
    self._refPL = env.REFERENCE_PL
    self._noiseMaker = 0
    self._ple = env.PLE

  def estimateRSS(self, txPower, distance):
    return txPower-self._refPL+self._noiseMaker.noise()-(10*self._ple*math.log10(distance/self._refDistance))

  def estimateDistance(self, txPower, rss):
    return self._refDistance*math.pow(10, ((txPower-self._refPL) - rss)/(10*(self._ple)))

  @property
  def noise(self):
    return self._noiseMaker.noise()

  @property
  def ple(self):
    return self._ple

  @property
  def noiseMaker(self):
    return self._noiseMaker

  @noise.setter
  def noiseMaker(self, noiseMaker):
    self._noiseMaker = noiseMaker

  @ple.setter
  def ple(self, ple):
    self._ple = ple

class NoiseMaker():
	def __init__(self, mean = 0, deviation = 1):
		self._mean = mean
		self._deviation = deviation

	def noise(self):
		return np.random.normal(self._mean, self._deviation)

if __name__ == '__main__':
  pathLossModel = PathLossModel()
  pathLossModel.noiseMaker = NoiseMaker(mean = env.noiseMean, deviation = env.noiseDeviation)

  rss = pathLossModel.estimateRSS(txPower=env.UAV_TRANSMISSION_POWER, distance=20)
  print("Distance {} m -> RSS: {} dBm".format(20, rss))
  d = pathLossModel.estimateDistance(txPower=env.UAV_TRANSMISSION_POWER, rss=rss)
  print("RSS: {} dBm -> Distance: {} m".format(rss, d))