# -*- coding: utf-8 -*-
import os
import re
import math
from pprint import pprint
import MeCab
import numpy as np
import gensim
import itertools
import pandas as pd
import scipy.spatial.distance as distance
from scipy.cluster.hierarchy import dendrogram, linkage

# 実行ファイルパスを取得
execPath = os.path.dirname(__file__)
# 学習済みベクターモデルの読込
model = gensim.models.doc2vec.Doc2Vec.load(execPath + "/gensimModel/jawiki.doc2vec.dbow300d.model")
# MeCab辞書読込
mt = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

# 問題文正規化
def regulateQuestion(q):
  q = q.translate(str.maketrans({'（':'(','）':')'}))
  q = re.sub('\([\u3041-\u309F・]+\)','',q)
  q = re.sub('[?？]','',q)
  return q

# コサイン類似度を得る
def cosSim(v1, v2):
  """ コサイン類似度を得る
  Args: v1(np.Array), v2(np.Array): ベクトル(同次元)
  Returns: float: 類似度(-1～1)
  """
  return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 分かち書きする
def tokenize(text):
    wakati = MeCab.Tagger("-O wakati")
    wakati.parse("")
    return wakati.parse(text).strip().split()

# 問題文から問題ベクターを得る
def getVector(text):
  """問題文から問題ベクターを得る
  Args: text(str): 問題文
  Returns: np.Array: 問題文ベクター
  """
  return model.infer_vector(tokenize(text))

# 問題ベクター間距離関数
def getDistance(v1, v2):
  """問題ベクター間距離関数
  Args: v1(np.Array), v2(np.Array): 問題文ベクター
  Returns: float: 距離
  """
  return 1 - cosSim(v1, v2)

# テキスト樹形図出力
def getTextDendrogram(num, indent, Z, questions, n):
  """テキスト樹形図出力
  Args: num(float): 枝番号
        indent: 表示する樹形
        Z: クラスタリング結果
        questions(list): 問題文リスト
        n(int): 問題数
  Returns: list: 樹形図（上から順の1行毎リスト）
  """
  if(num < n):
    return [indent + str(int(num)) + "." + questions[int(num)]]
  else:
    branchChars = "①②③④⑤⑥⑦⑧⑨"
    branchRank = int(n*2-num-1)
    if branchRank <= len(branchChars):
      branchChar = branchChars[branchRank-1]
    else:
      branchChar = "┬"
    return getTextDendrogram(Z[int(num-n), 0], indent+branchChar, Z, questions, n) \
         + getTextDendrogram(Z[int(num-n), 1], re.sub("[┬"+branchChars+"]","│",indent).replace("└","　")+"└", Z, questions, n)

# 最遠配置リストを得る
def scatterQuestion(num, Z, dMatrix, n):
  """最遠配置リストを得る
  Args: num(float): 枝番号
        Z: クラスタリング結果
        dMatrix: 距離マトリクス
        n(int): 問題数
  Returns: list: 最遠配置リスト
  """
  if(num < n):
    return [int(num)]
  else:
    v1 = scatterQuestion(Z[int(num-n), 0], Z, dMatrix, n)
    v2 = scatterQuestion(Z[int(num-n), 1], Z, dMatrix, n)
    i1 = 1
    i2 = 1
    d = 1.0 / (2.0 * (len(v1) + 1) * (len(v2) + 1))

    # 2つのリストの間で最も近い要素のインデックスを取得する
    dMatrixv1v2 = dMatrix[np.ix_(v1, v2)]
    # print(dMatrixv1v2)
    minIndex = np.unravel_index(np.argmin(dMatrixv1v2),  dMatrixv1v2.shape)
    minIndexv1 = minIndex[0]
    minIndexv2 = minIndex[1]
    # v1は当該要素が先頭に来るよう要素を移動
    v1 = v1[minIndexv1:] + v1[0:minIndexv1]
    # v2は当該要素が真ん中に来るよう要素を移動
    v2LenHalf = int((len(v2)+1)/2)
    v2 = v2[minIndexv2:] + v2[0:minIndexv2]
    v2 = v2[v2LenHalf:]  + v2[0:v2LenHalf]

    returnList = []
    while i1 <= len(v1) or i2 <= len(v2):
      if (i1 / (len(v1)+1)) > (i2 / (len(v2)+1) + d):
        returnList.append(v2[i2-1])
        i2 += 1
      else:
        returnList.append(v1[i1-1])
        i1 += 1
    return returnList

