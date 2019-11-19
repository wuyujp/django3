# -*- coding: utf-8 -*-
from mysite.settings import BASE_DIR

import glob
import csv
import pandas as pd
import os
from statistics import mean
inputPath=os.path.join(BASE_DIR, "myhp/data/WikiName/*.csv")
# xlsxからLiseNameを重複しないように抽出、csvに保存する
# 常に省略しないprint
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199
wikiNames = []
Languages = []
def getNames ():
	header = ['Name', 'Language']
	df =pd.DataFrame(columns=header)
	# NameとLanguageのみを抽出
	for file in glob.glob(inputPath):
		print(file)
		language = re.findall('Name(.)(.*)Name.csv', file)[0][1]
		df = pd.read_csv(file, header = 0, dtype=str, encoding="utf-8",sep='\t', error_bad_lines=False)
		wikiNames.append(df)
		Languages.append(language)

import re
import math
#記号区切り、リストに単語を格納して返す
def getWordListBySymbol (text):
	return list(filter(lambda str:str != '', re.split(r'[･,-\.\'\s0-9#$%&!?*+/;:()<=>@^\[\]\\_{|}~"]', text)))
### リストデータtext1と入力データtext2のレーベンシュタイン距離（編集距離）
import Levenshtein
def getLevenshteinDistance (text1, text2):
	return Levenshtein.distance(text1, text2)


def predictEditDistance(text):
	# リスト形式への変換
	nameList = getWordListBySymbol(text)
	resultList = []
	for name in nameList:
		length = len(name)
		nameScoreList = {}
		initial = name[:1]
		for wikiName, language in zip(wikiNames, Languages):
			resultSeries = wikiName[initial].dropna().str.upper().apply(getLevenshteinDistance, text2=name)
			#print(resultSeries)
			if not resultSeries.empty:
				nameScoreList[language]=resultSeries.min() * math.sqrt(length)
				#nameScoreList.append(resultSeries.min() * math.sqrt(length))
			else :
				nameScoreList[language]=length*2
				#nameScoreList.append(length*2)
		resultList.append(nameScoreList)
	return resultList


def predictLanguage(text):

	getNames()
	text = text.upper()
	resultList = predictEditDistance(text)
	finalresult = dict(zip(Languages, [0] * 5))
	for result in resultList:
		for language in Languages:
			finalresult[language] = finalresult[language] + result[language]
	if mean(finalresult.values()) != 0:
		return min(finalresult.items(), key=lambda x:x[1])[0], '{:.2%}'.format(1-min(finalresult.values())/mean(finalresult.values()))
	else :
		return "分からない～", "50%"

print(predictLanguage("WUYU"))