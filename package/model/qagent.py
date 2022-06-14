# -*- coding: utf-8 -*-
rootpath = '/content/drive/Shareddrives/KW phase1 repo'

import sys
sys.path.append(rootpath+'/package')
from utils.env import env
from service.combinationset import groupingFromSet
from model.sdp import calculateSDP
from model.pathlossmodel import PathLossModel, NoiseMaker

import numpy as np
from scipy.special import comb, perm

MSE = lambda x,y: np.mean(np.square(np.array(x)-np.array(y)), axis=1)
def KL(a, b):
    size = min(len(a),len(b))
    a = np.asarray(a[:size], dtype=np.float)
    b = np.asarray(b[:size], dtype=np.float)
    return np.sum(np.where(a != 0, a * np.log(a / b), 0))

def swapFunc(j, X, shapeOfX, targetReformSlice):
  for sample in range(shapeOfX[1]): #sample
    temp = []
    for i in range(shapeOfX[0]):
      temp.append(X[i][sample][j])
    targetReformSlice.append(temp)

# def detectAnomaly(mse):
#   trainingMean = 0.07640376
#   trainingStd = 0.01239504
#   upperBound = trainingMean + trainingStd*2
#   lowerBound = trainingMean - trainingStd*2
#   print("MSE of testing: ", np.mean(mse))
#   if np.mean(mse) >= lowerBound and np.mean(mse) <= upperBound:
#     return False
#   else:
#     return True
def detectAnomaly(kl):
  if np.isnan(kl):
    return True
  elif kl<0 :
    return True
  else:
    return False

class QAgent():
  def __init__(self, states, actions, UAVsSamples):
    self._learningRate = env.learningRate
    self._discountLambda = env.discountLambda
    self._epsilon = env.explorationRate
    self._states = states
    self._actions = actions
    self._table = np.zeros((len(self._states), len(self._actions)))
    self._currentState = np.random.choice(self._states)
    self._sdpResultsDatas = {}
    self._currentAction = None
    self._nextState = None
    self._UAVsSamples = UAVsSamples

    self._pathLossModel = PathLossModel()
    self._pathLossModel.noiseMaker = NoiseMaker(mean = env.noiseMean, deviation = env.noiseDeviation)

  def generateSdpResultsDatas(self):
    print("generateSdpResultsDatas")
    for iState, state in enumerate(self._states):
      groupListSamples = {0:groupingFromSet(state)}
      print("iState",iState)
      self._sdpResultsDatas[iState] = calculateSDP(groupListSamples, self._UAVsSamples, self._pathLossModel)

  def step(self, vae):
    # 1. 確認當前state (踢掉人後的組)
    # 2. 根據state中的group內成員，重新grouping出各種groups
    # 3. 計算SDP
    # 4. 讀取SDP結果並reshape成VAE的input size
    # 5. testResult = vae.predict(test)
    # 6. mse = MSE(testResult, test)
    # 7. if (detectAnomaly(mse)) -> penalty
    # 8. reward = rewardFunc(len(當前state), penalty)
    # 9. 根據action (踢掉的人)列出所有groups，從中透過Q table選擇或是有機率 (self._epsilon) 會選擇不同的group，變成下一個state
    # 10. self._nextState 更新
    # 11. return reward
    # print("1")
    stateIndex = self._states.index(self._currentState)
    _sdpResultsDatas = self._sdpResultsDatas[stateIndex]
    groupSize = np.array(_sdpResultsDatas[0]).shape[1]
    # for i in np.arange(env.groupSizeFrom, env.N_ngps+1,1):
    #   groupSize += comb(env.N_ngps,i)
    # groupSize = int(groupSize)

    rawDatas = []
    ReadSampleSize = 1
    # print(np.array(_sdpResultsDatas[0]).shape)
    # print(groupSize)
    # print("2")
    for i in range(env.N_ngps):
      temp = []
      for j in range(ReadSampleSize):
        # print(i, j)
        temp.append(_sdpResultsDatas[0][i][j*groupSize : j*groupSize+groupSize])
      rawDatas.append(temp)

    _anchorSamples = []
    anchorSamples = []
    for sample in range(ReadSampleSize):
      temp = []
      for id, uav in self._UAVsSamples[sample].items():
        if not uav.observedPosition == None:
          temp.append([uav.observedPosition for i in range(groupSize)])
      _anchorSamples.append(temp)
    for i in range(env.N_gps):
      temp = []
      for sample in range(ReadSampleSize):
        temp.append(_anchorSamples[sample][i])
      anchorSamples.append(temp)
    
    list (map(lambda i: rawDatas.append(anchorSamples[i]), range(env.N_gps)))

    # print("rawDatas: ", np.array(rawDatas).shape)
    # print("3")
    dualGroupingTestingData = []
    for i in range(env.N):
      testingS = []
      for j in range(np.array(rawDatas).shape[1]):
        temp = []
        for index_1, e1 in enumerate(rawDatas[i][j]):
          for index_2, e2 in enumerate(rawDatas[i][j]):
            # print(len(rawDatas[i][j]))
            if not index_1 == index_2:
              temp.append([e1, e2])
            if len(rawDatas[i][j]) == 1:
              temp.append([e1, e2])
        testingS.append(temp)
      dualGroupingTestingData.append(testingS)

    _testingDataShape= np.array(dualGroupingTestingData).shape
    # print("_testingDataShape: ", _testingDataShape)
    _reshapeTestingData = []
    # print("4")
    list (map(lambda _sample: swapFunc(_sample, dualGroupingTestingData, _testingDataShape, _reshapeTestingData), range(_testingDataShape[2])))
    
    _reshapeTestingData = np.array(_reshapeTestingData).astype('float32')
    # print(_reshapeTestingData)
    VAETestingData = _reshapeTestingData.reshape(len(_reshapeTestingData), np.prod(_reshapeTestingData.shape[1:]))

    data_min = 0
    data_max = max(max(env.X_RANGE,env.Y_RANGE),env.Z_RANGE)

    normalizeVAETestingData = (VAETestingData-data_min)/(data_max - data_min)
    normalizeVAETestingData = normalizeVAETestingData.astype('float32')

    # print("5")
    vaeOutput = vae.predict(normalizeVAETestingData, batch_size = 2048*4)
    # print("6")
    print("KL",KL(vaeOutput,normalizeVAETestingData))
    mse = MSE(vaeOutput, normalizeVAETestingData)
    # if (detectAnomaly(mse)):
    if (detectAnomaly(KL(vaeOutput,normalizeVAETestingData))):
      penalty = -10
    else:
      penalty = 0
    reward = (len(self._currentState)/len(self._states))*1  + penalty*1
    return reward

  
  def chooseAction(self):
    if np.random.rand() < self._epsilon:
      action = np.random.choice(self._actions)
      self._currentAction = action
    else:
      print("currentState: ", self._currentState)
      stateIndex = self._states.index(self._currentState)
      print("stateIndex: ", stateIndex)
      state_action = self._table[stateIndex]
      print("state_action: ", state_action)
      # print(np.argmax(state_action, axis=0))
      if all(v == 0 for v in state_action):
        action = np.random.choice(self._actions)
      else:
        action = self._actions[np.argmax(state_action, axis=0)]
      self._currentAction = action
      print("next action: ", self._currentAction)
    return action


  def updateQtable(self, reward):
    stateIndex = self._states.index(self._currentState)
    actionIndex = self._actions.index(self._currentAction)
    # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
    q_value = self._table[stateIndex][actionIndex]
    self._table[stateIndex][actionIndex] = q_value + self._learningRate*(reward + self._discountLambda*np.max(self._table[stateIndex][:]) - q_value)
    self._currentState = self._nextState
    self._nextState = None

  @property
  def sdpResultsDatas(self):
    return self._sdpResultsDatas

  @property
  def discountLambda(self):
    return self._discountLambda

  @property
  def learningRate(self):
    return self._learningRate

  @property
  def actions(self):
    return self._actions

  @property
  def currentState(self):
    return self._currentState
  
  @property
  def currentAction(self):
    return self._currentAction

  @property
  def nextState(self):
    return self._nextState

  @property
  def table(self):
    return self._table

  @property
  def states(self):
    return self._states

  @property
  def UAVsSamples(self):
    return self._UAVsSamples

  @sdpResultsDatas.setter
  def sdpResultsDatas(self,sdpResultsDatas):
    self._sdpResultsDatas = sdpResultsDatas

  @learningRate.setter
  def learningRate(self, learningRate):
    self._learningRate = learningRate

  @discountLambda.setter
  def discountLambda(self, discountLambda):
    self._discountLambda = discountLambda

  @actions.setter
  def actions(self, actions):
    self._actions = actions

  @currentState.setter
  def currentState(self, currentState):
    self._currentState = currentState
  
  @currentAction.setter
  def currentAction(self, currentAction):
    self._currentAction = currentAction

  @nextState.setter
  def nextState(self, nextState):
    self._nextState = nextState

  @table.setter
  def table(self, table):
    self._table = table

  @states.setter
  def states(self, states):
    self._states = states
  
  @UAVsSamples.setter
  def UAVsSamples(self, UAVsSamples):
    self._UAVsSamples = UAVsSamples

