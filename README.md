# 碩論程式碼文件整理

* #### 檔案說明
1. envModification：安裝 CVXPY 所需相關套件
（本地安裝時才需要）
2. codes：碩論程式碼
（.ipynb 在 Google Colaboratory 上運行無須額外安裝套件）
3. package：程式所需模組
4. GPSMeasurement.txt：GPS量測原始數據
5. GPSMeasurement2.txt：GPS量測原始數據

* #### 執行流程
1. 生成訓練與測試資料(含錨點分組)
anomolySDSOCPgenerator.ipynb
anomolyPCAgenerator.ipynb
anomolyMDSgenerator.ipynb

2. #### 訓練模型
VAE_NOanchor.ipynb
VAE_NOanchorPCA.ipynb
VAE_NOanchorMDS.ipynb
AE_NOanchor.ipynb

3. #### 測試模型並選取最佳錨點(含FKP)
VAE_ALLSAMPLE_anomalyDetect_NoKL.ipynb
VAE_ALLSAMPLE_anomalyDetect_NoKLPCA.ipynb
VAE_ALLSAMPLE_anomalyDetect_NoKLMDS.ipynb

4. #### 計算定位結果與繪製定位結果圖
Localization_afterAnomalyDetectionSD-SOCP.ipynb
Localization_afterAnomalyDetectionSDP.ipynb
Localization_afterAnomalyDetectionSOCP.ipynb

5. #### 繪製各項結果圖
result.ipynb
drawHistOfDifferentPreprocess.ipynb
MSE_Difference_of_5DimensionReductionMethod.ipynb
AE_VAE_comparison.ipynb
localizationResultComparison.ipynb

* #### 安裝環境（安裝 CVXPY 於 Windows 環境中的 Anaconda）
1.	Install wheels from the [Unofficial Windows Binaries for Python Extension Packages]( https://www.lfd.uci.edu/~gohlke/pythonlibs/#cvxpy )<br>
　a.	pip install numpy-1.19.5+vanilla-cp37-cp37m-win_amd64.whl<br>
　b.	pip install scipy-1.6.0-cp37-cp37m-win_amd64.whl<br>
　c.	pip install cvxopt-1.2.5-cp37-cp37m-win_amd64.whl<br>
　d.	pip install scs-2.1.2-cp37-cp37m-win_amd64.whl<br>
　e.	pip install ecos-2.0.7.post1-cp37-cp37m-win_amd64.whl<br>
　f.	pip install cvxpy-1.1.7-cp37-cp37m-win_amd64.whl<br>

其餘套件：(Google Colaboratory 上直接 import 就可以用)
1.	itertools
2.	sys
3.	pickle
4.	numpy
5.	math
6.	csv
7.	matplotlib.pyplot
8.	random
9.	keras
10.	keras.layers
11.	keras.models

* #### 程式檔案說明
---
格式如下：
程式檔案名稱（在codes資料夾內）
1. 用途介紹
2. 所需檔案與說明<br>
　a. 檔案一：說明<br>
　b. 檔案二：說明<br>
3. 生成檔案與說明<br>
　a. 檔案一：說明<br>
　b. 檔案二：說明<br>
---

**AE_VAE_comparison.ipynb**
1.	用途介紹：繪製AE與VAE模型在異常偵測上的比較圖
2.	所需檔案與說明<br>
　a.	/datas/anomalySDPResult/done0804_500-1000/result0722_AE_V2.csv：AE的異常偵測結果，包含Precision、Recall and F1 score<br>
　b.	/datas/anomalySDPResult/done0804_500-1000/result0722_VAE_V2.csv：VAE的異常偵測結果，包含Precision、Recall and F1 score<br>
3.	生成檔案與說明<br>
　a.	anomaly_detection_comparison_AE_VAE_Precision.eps：AE與VAE的Precision圖<br>
　b.	anomaly_detection_comparison_AE_VAE_Recall.eps：AE與VAE的Recall圖<br>
　c.	anomaly_detection_comparison_AE_VAE_F1Score.eps：AE與VAE的F1 score圖<br>

**anomolyMDSgenerator.ipynb**
1.	用途介紹：生成經過MDS降維處理的訓練與測試資料
2.	所需檔案與說明<br>
　a.	/datas/uavPosition/300_0706/deviation/<填入deviation>/UAVsSamples.pkl：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	/test_position<填入定位目標序號>_pickerror<填入異常無人機數量>_deviation<填入deviation>_100.csv：經過MDS降維處理的測試資料<br>

**anomolyPCAgenerator.ipynb**
1.	用途介紹：生成經過PCA降維處理的訓練與測試資料
2.	所需檔案與說明<br>
　a.	/datas/uavPosition/300_0706/done_deviation/<填入deviation>/UAVsSamples.pkl：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	/test_position<填入定位目標序號>_pickerror<填入異常無人機數量>_deviation<填入deviation>_100.csv：經過PCA降維處理的測試資料<br>

**anomolySDSOCPgenerator.ipynb**
1.	用途介紹：生成經過SDSOCP降維處理的訓練與測試資料
2.	所需檔案與說明<br>
　a.	/datas/uavPosition/300_0706/done_deviation/<填入deviation>/UAVsSamples.pkl：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	/test_position<填入定位目標序號>_pickerror<填入異常無人機數量>_deviation<填入deviation>_300.csv：經過SDSOCP降維處理的測試資料<br>

**drawHistOfDifferentPreprocess.ipynb**
1.	用途介紹：統整並計算不同降維方法經過VAE後的異常偵測表現（印出數值）
2.	所需檔案與說明<br>
　a.	/drawHistOfDifferentPreprocessDataMDS.csv：基於MDS的異常偵測數值（TP, FP, TN, and FN）<br>
　b.	/drawHistOfDifferentPreprocessDataPCA.csv：基於PCA的異常偵測數值（TP, FP, TN, and FN）<br>
　c.	/drawHistOfDifferentPreprocessDataSDSOCP.csv：基於SDSOCP的異常偵測數值（TP, FP, TN, and FN）<br>
3.	生成檔案與說明<br>
　a.	無<br>

**Localization_afterAnomalyDetectionSD-SOCP.ipynb**
1.	用途介紹：生成經過異常偵測前後的SDSOCP定位誤差RMSE
2.	所需檔案與說明<br>
　a.	/datas/anomalySDPResult/0808_3_v2/UAVsSamples_pick<填入異常無人機數量>div<填入deviation>_300.npy：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	0804_before_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測前的SDSOCP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　b.	0804_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測後的SDSOCP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　c.	0804_before_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測前的SDSOCP定位誤差RMSE(誤差偏移量平均值為700)<br>
　d.	0804_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測後的SDSOCP定位誤差RMSE(誤差偏移量平均值為700)<br>

**MSE_Difference_of_5DimensionReductionMethod.ipynb**
1.	用途介紹：繪製REs圖
2.	所需檔案與說明<br>
　a.	無（在程式內部貼上數值）<br>
3.	生成檔案與說明<br>
　a.	anomaly_detection_reconstruction_error_03_3anomaly.eps：deviation 0.3 的REs圖<br>
　b.	anomaly_detection_reconstruction_error_3_3anomaly.epsdeviation 3 的REs圖<br>

**Localization_afterAnomalyDetectionSDP.ipynb**
1.	用途介紹：生成經過異常偵測前後的SDP定位誤差RMSE
2.	所需檔案與說明<br>
　a.	/datas/anomalyNewSDPResult/0810_v2/UAVsSamples_pick<填入異常無人機數量>div<填入deviation>_300.npy：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	0808_3_before_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測前的SDP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　e.	0808_3_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測後的SDP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　f.	0808_3_before_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測前的SDP定位誤差RMSE(誤差偏移量平均值為700)<br>
　g.	0808_3_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測後的SDP定位誤差RMSE(誤差偏移量平均值為700)<br>

**Localization_afterAnomalyDetectionSOCP.ipynb**
1.	用途介紹：生成經過異常偵測前後的SOCP定位誤差RMSE
2.	所需檔案與說明<br>
　a.	/datas/anomalySOCPResult/1125_v2/UAVsSamples_pick<填入異常無人機數量>div<填入deviation>_300.npy：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	1213_before_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測前的SOCP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　b.	1213_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測後的SOCP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　c.	1213_before_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測前的SOCP定位誤差RMSE(誤差偏移量平均值為700)<br>
　d.	1213_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測後的SOCP定位誤差RMSE(誤差偏移量平均值為700)<br>

**ParsingGPSMeasurement.ipynb**
1.	用途介紹：解析GPS量測資料
2.	所需檔案與說明<br>
　a.	/datas/realGPSMeasurements/gpsMeasurement_test.txt：GPS量測結果<br>
3.	生成檔案與說明<br>
　a.	normal_GPS_drifting.html：正常GPS偏移圖<br>
　b.	anomaly_GPS_drifting.html：異常GPS偏移圖<br>

**AE_NOanchor.ipynb**
1.	用途介紹：訓練AE
2.	所需檔案與說明<br>
　a.	/datas/anomalySDPResult/done0808_3/test_position<填入定位目標序號>_pickerror0_deviation<填入deviation>_300.csv：SDSOCP定位結果<br>
　b.	/datas/uavPosition/300_0706/done_deviation/<填入deviation>/UAVsSamples.pkl：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	AENoanchorModel_8UAV_8uUAV_div <填入deviation>：儲存模型<br>

**localizationResultComparison.ipynb**
1.	用途介紹：繪製定位誤差圖
2.	所需檔案與說明<br>
　a.	1213_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測後的SOCP定位誤差RMSE(誤差偏移量平均值為700)<br>
　b.	0808_3_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測後的SDP定位誤差RMSE(誤差偏移量平均值為700)<br>
　c.	0804_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測後的SDSOCP定位誤差RMSE(誤差偏移量平均值為700)<br>
　d.	1213_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測後的SOCP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　e.	0808_3_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測後的SDP定位誤差RMSE(誤差偏移量平均值為1200)<br>
　f.	0804_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE_v2.pkl：異常偵測後的SDSOCP定位誤差RMSE(誤差偏移量平均值為1200)<br>
3.	生成檔案與說明<br>
　a.	localization_error_comparison_SOCP_SDP_SDSOCP_RMSE.eps：定位誤差圖(誤差偏移量平均值為700)<br>
　b.	localization_error_comparison_SOCP_SDP_SDSOCP_RMSE_1200.eps：定位誤差圖(誤差偏移量平均值為1200)<br>

**VAE_NOanchor.ipynb**
1.	用途介紹：訓練VAE for SDSOCP
2.	所需檔案與說明<br>
　a.	/datas/anomalySDPResult/done0808_3/test_position<填入定位目標序號>_pickerror0_deviation<填入deviation>_300.csv：SDSOCP定位結果<br>
　b.	/datas/uavPosition/300_0706/done_deviation/<填入deviation>/UAVsSamples.pkl：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	V2_VAENoanchorModel_300sample_8UAV_8uUAV_div<填入deviation>：儲存模型<br>

**VAE_NOanchorMDS.ipynb**
1.	用途介紹：訓練VAE for MDS
2.	所需檔案與說明<br>
　a.	/datas/anomalyNewSDPResult/0811_MDS/test_position<填入定位目標序號>_pickerror0_deviation<填入deviation>_300.csv：MDS降維結果<br>
　b.	/datas/uavPosition/300_0706/done_deviation/<填入deviation>/UAVsSamples.pkl：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	VAENoanchorMDSModel_300sample_8UAV_8uUAV_div<填入deviation>：儲存模型<br>

**VAE_NOanchorPCA.ipynb**
1.	用途介紹：訓練VAE for PCA
2.	所需檔案與說明<br>
　a.	/datas/anomalyNewSDPResult/0817_PCA/test_position<填入定位目標序號>_pickerror0_deviation<填入deviation>_300.csv：PCA降維結果<br>
　b.	/datas/uavPosition/300_0706/done_deviation/<填入deviation>/UAVsSamples.pkl：讀取無人機群樣本<br>
3.	生成檔案與說明<br>
　a.	VAENoanchorModel_300sample_8UAV_8uUAV_div<填入deviation>：儲存模型<br>

**VAE_ALLSAMPLE_anomalyDetect_NoKL.ipynb**
1.	用途介紹：計算SDSOCP經過VAE的異常偵測數值（TP, FP, TN, and FN）
2.	所需檔案與說明<br>
　a.	/datas/trainingModel/V2_VAENoanchorModel_300sample_8UAV_8uUAV_div<填入deviation>：VAE模型<br>
　b.	/datas/anomalySDPResult/0808_3_v2/UAVsSamples_pick<填入異常無人機數量>div<填入deviation>_300.npy：讀取無人機群樣本<br>
　c.	/datas/anomalySDPResult/0808_3_v2/test_position<填入定位目標序號>_pickerror<填入異常無人機數量>_deviation<填入deviation>_300.csv：SDSOCP定位結果<br>
3.	生成檔案與說明<br>
　a.	0808_3_100sample_<填入異常無人機數量>anomaly_<填入deviation>div_SelectedAnchors_VAE_v2.pkl：挑選過後的錨點<br>
　b.	/datas/anomalySDPResult/0808_3_v2/result.csv：異常偵測結果（TP, FP, TN, and FN）<br>

**VAE_ALLSAMPLE_anomalyDetect_NoKLMDS.ipynb**
1.	用途介紹：計算MDS經過VAE的異常偵測數值（TP, FP, TN, and FN）
2.	所需檔案與說明<br>
　a.	/datas/trainingModel/VAENoanchorMDSModel_300sample_8UAV_8uUAV_div<填入deviation>：VAE模型<br>
　b.	/datas/anomalyNewSDPResult/0811_MDS/UAVsSamples_pick<填入異常無人機數量>div<填入deviation>_300.npy：讀取無人機群樣本<br>
　c.	/datas/anomalyNewSDPResult/0811_MDS/test_position<填入定位目標序號>_pickerror<填入異常無人機數量>_deviation<填入deviation>_100.csv：MDS降維結果<br>
3.	生成檔案與說明<br>
　a.	100sample_<填入異常無人機數量>anomaly_<填入deviation>div_SelectedAnchors_VAE.pkl：挑選過後的錨點<br>
　b.	/datas/anomalyNewSDPResult/0811_MDS/result.csv：異常偵測結果（TP, FP, TN, and FN）<br>

**VAE_ALLSAMPLE_anomalyDetect_NoKLPCA.ipynb**
1.	用途介紹：計算PCA經過VAE的異常偵測數值（TP, FP, TN, and FN）
2.	所需檔案與說明<br>
　a.	/datas/trainingModelPCA/VAENoanchorModel_300sample_8UAV_8uUAV_div<填入deviation>：VAE模型<br>
　b.	/datas/anomalyNewSDPResult/0817_PCA/UAVsSamples_pick<填入異常無人機數量>div<填入deviation>_300.npy：讀取無人機群樣本<br>
　c.	/datas/anomalyNewSDPResult/0817_PCA/test_position<填入定位目標序號>_pickerror<填入異常無人機數量>_deviation<填入deviation>_100.csv：PCA降維結果<br>
3.	生成檔案與說明<br>
　a.	100sample_<填入異常無人機數量>anomaly_<填入deviation>div_SelectedAnchors_VAE.pkl：挑選過後的錨點<br>
　b.	/datas/anomalyNewSDPResult/0817_PCA/result.csv：異常偵測結果（TP, FP, TN, and FN）<br>

**result.ipynb**
1.	用途介紹：繪製異常偵測前後的定位誤差CDF
2.	所需檔案與說明<br>
　a.	/datas/localizationResult/0804_before_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測前的定位誤差<br>
　b.	/datas/localizationResult/0804_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：異常偵測後的定位誤差<br>
3.	生成檔案與說明<br>
　a.	localization_error_CDF_RMSE_<填入deviation>.eps：定位誤差CDF<br>

**localizationResultComparison.ipynb**
1.	用途介紹：繪製 SD/SOCP、SDP 和 SOCP 的定位誤差圖
2.	所需檔案與說明<br>
　a.	/datas/localizationResult/1213_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：SOCP 的定位誤差<br>
　b.	/datas/localizationResultSDP/0808_3_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：SDP 的定位誤差<br>
　c.	/datas/localizationResult/0804_after_localization_RMSE<填入deviation>_<填入異常無人機數量>_VAE.pkl：SD/SOCP 的定位誤差<br>
3.	生成檔案與說明<br>
　a.	localization_error_comparison_SOCP_SDP_SDSOCP_RMSE.eps：定位誤差比較圖<br>
