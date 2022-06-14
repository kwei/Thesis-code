class env():
  # Total UAVs
  N=16                
  # Malicious UAVs
  N_f=1               
  # UAVs with GPS
  N_gps = N//2        
  # UAVs without GPS
  N_ngps = N - N_gps  
  # UAVs with Good GPS
  N_t=N_gps-N_f       

  # Environment Size
  X_RANGE=1000
  Y_RANGE=1000
  Z_RANGE=1000

  # Scenario Dimension
  DIMENSION = 2
  # Training Samples
  SAMPLES = 100
  LOAD_SAMPLES_FOR_AE = 100
  # Combination size
  COMBINATION_SIZE = 2
  # Anomaly amount
  ANOMALY_AMOUNT = 1

  noiseMean = 0
  noiseDeviation = 0.1

  groupSizeFrom = 5

  ## UAV parameters
  # UAV transmission power in dBm (100 mW)
  UAV_TRANSMISSION_POWER = 20
  # UAV's lowest flying height (m)
  UAV_LOWEST_HEIGHT = 100

  ## Path Loss Model parameters
  # Reference distance (m)
  REFERENCE_DISTANCE = 1
  # Reference Path Loss
  REFERENCE_PL = 40
  # Defualt Path Loss Exponent (free space)
  PLE = 2

  # Traing and testing percentage
  TEST_PERCENTAGE = 0.1


  # VAE training parameter
  batch_size = 2048*4
  latent_dim = 32
  intermediate_dim = 64
  final_dim = 32
  epochs = 100
  epsilon_std = 1.0


  ## Q Learning parameters
  # Learning rate
  learningRate = 1e-4
  # Discount lambda
  discountLambda = 0.001
  # exploration rate
  explorationRate = 0.1


