# -*- coding: utf-8 -*-


"""final_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HCzH0imTbXz7RXZx7VaztDUrNB_VVJP5
"""

from math import nan
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import sys
# import urllib.request
from konlpy.tag import Okt
# from tqdm import tqdm

import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from hanspell import spell_checker

import kss
from more_itertools import locate

"""# **전처리**"""

# 중복 제거

def duplicatesRemove(data) :
  data.drop_duplicates(subset = ['광고내용'], inplace=True) # document 열에서 중복인 내용이 있다면 중복 제거
  data['광고내용'] = data['광고내용'].str.replace("[^가-힣 ]","") # 정규 표현식 수행
  data['광고내용'] = data['광고내용'].str.replace('^ +', "") # 공백은 empty 값으로 변경
  data['광고내용'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경

  data = data.dropna(how='any') # Null 값 제거

  data.reset_index(drop=True, inplace=True)

  print('전처리 후 데이터 수 :',len(data))

  return data

#hanspell 맞춤법 검사

def spellcheck(data):
  data['hanspell']=''
  for i in range(len(data)):
    spelled_sent = spell_checker.check(data["광고내용"][i])
    data['hanspell'][i] = spelled_sent.checked
  data.drop("광고내용", axis = 1, inplace = True)
  data = data[['hanspell','label']]
  data.rename(columns={'hanspell':'광고내용'}, inplace = True)
  return data

#토큰화+불용어제거
def ko_processing(df):
  stopwords = ['수','로','로부터','되다','다','든지','께','께서', '이라고','이다','것','의','가','하고','하고는','이','은','이므로','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을']
  #stopwords = ['되다','인', '줄', '되어다', '것', '이라고','께','께서','든','든지','로','더러','며','만은','조차','처럼','한테','하고','하고는','커녕','나','이다','지요','이므로','있다','이다','의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을']
  okt = Okt()
  df['ko_processing'] = np.nan
  df["ko_processing"] = df["ko_processing"].astype(object)

  X = []
  for sentence in df['광고내용']:
      tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
      stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
      X.append(stopwords_removed_sentence)

  #ko_procssing
  for i in range(len(df)):
      df['ko_processing'][i]=X[i][:]
  df = df.dropna(how='any') # Null 값 제거
  return df

"""# **train/test**"""

#정수 인코딩
def processing(df):
  df["processing"] = np.nan
  df["processing"] = df["processing"].astype(object)


  X = df['ko_processing'].to_list()
  processing = tokenizer.texts_to_sequences(X)

  #procssing
  for i in range(len(df)):
    df['processing'][i]=processing[i][:]
  
  df = df.dropna(how='any') # Null 값 제거
  return df

"""# **패딩**"""


"""# **모델링**"""

# from tensorflow.keras.layers import Embedding, Dense, LSTM
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import load_model
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import numpy as np
import pandas as pd
# from keras import models, layers
# from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


"""# **모델 부르기**"""


MODEL_NAME = 'model/diamond_model.h5'

from tensorflow.keras.models import Sequential

from keras.models import load_model

loaded_model = load_model(MODEL_NAME)

import pickle
with open('model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

con = np.load('model/con_save.npy')
word_index = [row[0] for row in con]
word_index = list(map(int, word_index))

names = [weight.name for layer in loaded_model.layers for weight in layer.weights]
weights = loaded_model.get_weights()

kernel_weights = weights[0]
recurrent_kernel_weights = weights[1]
bias = weights[2]

n = 1
units = 106  # LSTM layers  

Wi = kernel_weights[:, 0:units]
Wf = kernel_weights[:, units:2 * units]
Wc = kernel_weights[:, 2 * units:3 * units]
Wo = kernel_weights[:, 3 * units:]


Ui = recurrent_kernel_weights[:, 0:units]
Uf = recurrent_kernel_weights[:, units:2 * units]
Uc = recurrent_kernel_weights[:, 2 * units:3 * units]
Uo = recurrent_kernel_weights[:, 3 * units:]


bi = bias[0:units]
bf = bias[units:2 * units]
bc = bias[2 * units:3 * units]
bo = bias[3 * units:]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tokenizing(df):
  X = []
  for sen in df['processing']:
      word_arr =[]
      for word in sen:
          if word in word_index:
              word_arr.append(float(con[con[:,0] ==word,1]))
          else:
              word_arr.append(0)

      [word_arr.insert(0,0) for i in range(106-len(word_arr))]
      X.append(word_arr)

  X = pd.DataFrame(X)
  X = X.loc[:,:105]
  X= X.to_numpy()
  X = X.reshape(-1,106,1)
  X.shape
  return X

import matplotlib.font_manager as fm
# from matplotlib import rc
path = 'C:/Users/USER/diamond_web/model/NanumGothicBold.ttf'
best_font = fm.FontProperties(fname=path, size=50).get_name()
plt.rc('font', family=best_font)




def make_plot(test_df, test_li, number, standard_score):
    
    ht_1 = np.zeros(n * units).reshape(n, units)
    Ct_1 = np.zeros(n * units).reshape(n, units)

    h_t_value = []
    influence_h_t_value = []
    #test_li=test_li[0] #이중리스트로 변환

    for t in range(0, len(test_li[number,:])):
        xt = np.array(test_li[number,t])
        ft = sigmoid(np.dot(xt, Wf) + np.dot(ht_1, Uf) + bf)  # forget gate

        influence_ft = (np.dot(ht_1, Uf))/(np.dot(xt, Wf) + np.dot(ht_1, Uf) + bf) * ft

        it = sigmoid(np.dot(xt, Wi) + np.dot(ht_1, Ui) + bi)  # input gate
        influence_it = (np.dot(ht_1, Ui))/(np.dot(xt, Wi) + np.dot(ht_1, Ui) + bi) * it

        ot = sigmoid(np.dot(xt, Wo) + np.dot(ht_1, Uo) + bo)  # output gate
        influence_ot = np.dot(ht_1, Uo) / (np.dot(xt, Wo) + np.dot(ht_1, Uo) + bo) * ot

        gt =  np.tanh(np.dot(xt, Wc) + np.dot(ht_1, Uc) + bc)
        influence_gt =np.dot(ht_1, Uc) / (np.dot(xt, Wc) + np.dot(ht_1, Uc) + bc) * gt

        Ct = ft * Ct_1 + it * gt
        influence_ct = influence_ft * Ct_1 + influence_it * influence_gt
        ht = ot * np.tanh(Ct)
        influence_ht = influence_ot * (influence_ct/Ct) * ht

        influence_h_t_value.append(influence_ht)

        ht_1 = ht  # hidden state, previous memory state
        Ct_1 = Ct  # cell state, previous carry state

        h_t_value.append(ht)

    influence_h_t_value.append(h_t_value[-1])
    for i in range(len(influence_h_t_value)-1,0,-1):
        influence_h_t_value[i] = influence_h_t_value[i] - influence_h_t_value[i-1]

    influence_h_t_value = influence_h_t_value[1:]
    impact_columns = np.dot(influence_h_t_value,weights[3]) + (weights[4]/units)
    print("\n문장 : " , test_df.loc[number, '문장'])
    
    #score = loaded_model.predict(test_li[number:number+1])[0][0]
    score = loaded_model.predict(test_li[number:number+1])[0][0]
    test_df.loc[number,"score"] = score
    if score > standard_score:
        ment = "PASS SENTENCE"
        b_color = 'azure' #green일 경우 허용 0.5넘었을 때
        t_color = "mediumblue"
    else:
        ment = "DANGER SENTENCE"
        b_color ='mistyrose'
        t_color = "red"

    # fig = plt.figure(figsize=(15,3),facecolosr=b_color)
    for k in range(len(test_df.loc[number,'ko_processing'])):
        s = test_df.loc[number,'ko_processing'][k]
        k1=len(impact_columns)+k-len(test_df.loc[number,'ko_processing'])
        va = round(float(impact_columns[k1][0][0]),2)
    #     if va > 0.5:
    #         font1 = {'family':best_font,
    #             'color':  'darkblue',
    #             'weight': 'normal',
    #             'size': 16}
    #     elif va< -0.3:
    #         font1 = {'family':best_font,
    #             'color':  'red',
    #             'weight': 'normal',
    #             'size': 16}

    #     else:
    #         font1 = {'family':best_font,
    #             'color':  'black',
    #             'weight': 'normal',
    #             'size': 16}


    #     if k < 17:
    #         plt.rcParams['axes.unicode_minus'] =False
    #         plt.rc('font', family='NanumGothic')
    #         plt.text(s=s, x=k*0.7, y=0,fontdict=font1,va='center',ha='center')
    #         plt.text(s=va,x=k*0.7, y=-0.1,fontdict=font1,va='center',ha='center')
    #     elif k < 34:
    #         plt.rcParams['axes.unicode_minus'] =False
    #         plt.rc('font', family='NanumGothic')
    #         plt.text(s=s, x=k*0.7 - 17*0.7, y=-0.2,fontdict=font1,va='center',ha='center')
    #         plt.text(s=va,x=k*0.7- 17*0.7, y=-0.3,fontdict=font1,va='center',ha='center')
    #     else:
    #         plt.rcParams['axes.unicode_minus'] =False
    #         plt.rc('font', family='NanumGothic')
    #         plt.text(s=s, x=k*0.7 - 34*0.7, y=-0.4,fontdict=font1,va='center',ha='center')
    #         plt.text(s=va,x=k*0.7- 34*0.7, y=-0.5,fontdict=font1,va='center',ha='center')   

    # plt.xlim(0,8)
    # plt.ylim(-0.5,0.1)
    # plt.axis('off')
    # plt.title(ment, size = 20, color = t_color, pad = 15)
    # plt.show()
    print("문장별 위험도 : {:.3f}".format(1-score))
 






def ad_predict(ad):
  #문장 분리
  danger_index=[]
  li = []
  danger_value =[]
  splited_ad=kss.split_sentences(ad)
  #맞춤법+전처리
  
  #채현추가
  for sent in splited_ad:
    spelled_sent = spell_checker.check(sent)
    sent = spelled_sent.checked
    sent = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', sent)
    li.append(sent)

  #여기까지채현추가


  ad_df = pd.DataFrame({"광고내용":li})
  ad_df = ko_processing(ad_df) # 단어 쪼갠 것
  ad_df = processing(ad_df)   # 단어 정수인덱싱

  ad_df['score'] = np.nan
  ad_df["score"] = ad_df["score"].astype(float)
  ad_df.rename(columns = {'광고내용':'문장'}, inplace = True)

  #토큰화
  input = tokenizing(ad_df) # 단어가중치
  print("광고 내 문장")
  num = 1
  for sen in ad_df['문장']:
    print("문장"+str(num)+" : " + sen)
    num += 1

  #문장이 2개 이상
  if len(ad_df)>1:
    #모델 예측
    print("\n\n문장 별 예측 결과")
    for i in range(len(ad_df)):
      make_plot(ad_df, input, i, 0.5)



    danger_index = list(locate(ad_df['score'], lambda x: x < 0.5))
    print(danger_index)
    #score
    danger = ad_df.loc[ad_df['score']<0.5].copy()
    danger.rename(columns = {'문장':'위험 문장'}, inplace = True)
    danger.rename(columns = {'score':'위험도'}, inplace = True)
    danger = danger.reset_index(drop=True)
    safety = ad_df.loc[ad_df['score']>=0.5].copy()  

    if len(danger)!=0:
      danger['위험도'] = 1-danger['위험도']
      print("\n최종 예측 결과 : 다음 문장 때문에 해당 광고는 {:.2f}% 확률로 허위광고입니다.\n".format((danger['위험도'].mean()) * 100))
      # 위험도가 기준 이상인 문장의 인덱스
      for i in range(len(danger)):
        
        if 0.5 < danger.loc[i,"위험도"]:
          danger_value.append(danger.loc[i, "위험도"])
      sys.displayhook(danger.loc[:,['위험 문장', '위험도']])
      # 문장 길이, 허위/허용, 확률, 문장단위 분류리스트, 위험문장의 인덱스,위험문장의 위험도값
      return [ len(ad_df), "허위", round((danger['위험도'].mean()) * 100, 2), splited_ad, danger_index, danger_value]

    else:
      print("\n최종 예측 결과 : 해당 광고는 {:.2f}% 확률로 허용광고입니다.\n".format(safety['score'].mean() * 100))
      # 문장 길이, 허용/허위, 확률, 문장단위 분류리스트, 위험문장 인덱스 X, 위험문장의 위험도값 X
      return [ len(ad_df), "허용", round((safety['score'].mean()) * 100, 2), splited_ad, nan, nan ]

  #문장이 1개
  else:
    print("\n\n문장 별 예측 결과")
    make_plot(ad_df, input,0, 0.5)
    ad_df = ad_df.reset_index(drop=True)
    if(ad_df.loc[0,'score'] > 0.5):
      print("\n최종 예측 결과 : 해당 광고는 {:.2f}% 확률로 허용광고입니다.\n".format(ad_df['score'][0] * 100))
      # 문장 길이, 허위/허용, 확률, 문장단위 분류리스트, 위험문장의 인덱스,위험문장의 위험도값
      return[len(ad_df),"허용",round(ad_df['score'][0] * 100, 2), splited_ad, 0, danger_index ]
    else:
      ad_df['score'] = 1-ad_df['score']
      print("\n최종 예측 결과 : 다음 문장 때문에 해당 광고는 {:.2f}% 확률로 허위광고입니다.\n".format((ad_df['score'][0]) * 100))
      ad_df.rename(columns = {'문장':'위험 문장'}, inplace = True)
      ad_df.rename(columns = {'score':'위험도'}, inplace = True)
      sys.displayhook(ad_df.loc[:,['위험 문장', '위험도']])
      # 문장 길이, 허용/허위, 확률, 문장단위 분류리스트, 위험문장 인덱스 X, 위험문장의 위험도값 X
      return [len(ad_df),"허위",round((ad_df['위험도'][0]) * 100, 2), splited_ad, nan, nan ]



  # 허용 결과물: 퍼센트(1), 문장 별 예측결과(문장 수) -> 클릭 시 
  # 허위 결과물: 퍼센트(1), 문장 별 예측결과(문장 수)[리스트로], 가장 큰 위험 문장 인덱스

if __name__ == '__main__':
  # print(typekss.split_sentences("벌들은 프로폴리스를 벌집 출입구에 발라 외부로부터 바이러스나 세균의 유입을 막습니다. 효소는 생체반응을 조절하는 단백질이며 생명 유지를 위한 필수적인 물질입니다. 효소는 식품으로부터 섭취한 탄수화물 지방 단백질을 분해하여 소화에 도움을 주는 건강기능식품입니다. 정상 성인은 수면시작 후 80~100분에 첫 번째 비렘수면이 나타나며 그 이후에 렘수면과 비렘수변이 약 90분 주기로 4~6회 반복됩니다.")
  ad_predict("벌들은 프로폴리스를 벌집 출입구에 발라 외부로부터 바이러스나 세균의 유입을 막습니다. 효소는 생체반응을 조절하는 단백질이며 생명 유지를 위한 필수적인 물질입니다. 효소는 식품으로부터 섭취한 탄수화물 지방 단백질을 분해하여 소화에 도움을 주는 건강기능식품입니다. 정상 성인은 수면시작 후 80~100분에 첫 번째 비렘수면이 나타나며 그 이후에 렘수면과 비렘수변이 약 90분 주기로 4~6회 반복됩니다.")