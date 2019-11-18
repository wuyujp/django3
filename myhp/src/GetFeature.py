# -*- coding: utf-8 -*-

### 半角に変換
### 入力が全部半角であれば不要
import mojimoji
def hanKakuChange (text):
	return mojimoji.zen_to_han(text)

### 文字種変換
import re
def charChange (text):
	#大文字に統一
	text = text.upper()
	#\,\.\-\'\&\;\(\)と数字以外の記号を全部スペースとするす
	hanSymbol = r'[#$%!?*+/:<=>@^\[\]\\_{|}~"]'
	return(re.sub(hanSymbol, " ", text))

### 桁数取得
def getLen (text):
	return len(text)

### 単語数（記号+スペース区切り）
import re
def getWordNumberBySymbol (text):
	afterList = list(filter(lambda str:str != '', re.split(r'[･,-\.\'\s]', text)))
	#print(afterList)
	return len(afterList)

### 単語数（スペース区切り）
def getWordNumberBySpace (text):
	#print(text.split())
	return len(text.split())

### リストデータtext1と入力データtext2の近似度
import difflib
def getSequenceMatcherDistance (text1, text2):
	return difflib.SequenceMatcher(None, text1, text2).ratio()

### リストデータtext1と入力データtext2のレーベンシュタイン距離（編集距離）
import Levenshtein
def getLevenshteinDistance (text1, text2):
	return Levenshtein.distance(text1, text2)

### リストデータtext1と入力データtext2の最長一致桁数Overlap
import difflib
def getOverlap(text1, text2):
	s = difflib.SequenceMatcher(None, text1, text2)
	pos_a, pos_b, size = s.find_longest_match(0, len(text1), 0, len(text2)) 
	return len(text1[pos_a:pos_a+size])

### 発音近似距離
from pyphonetics import RefinedSoundex 
def getPyphoneticsDis(text1, text2):
	try : 
		return RefinedSoundex().distance(text1, text2)
	except IndexError:
		return -1

### 発音近似のキャラクタ数の差の合計
## 例：TDの差はキャラクタTの差+Dの差の合計値になる
def getCharCount(text1, text2, str1, str2):
	return(abs(text1.count(str1) - text2.count(str1)) + abs(text1.count(str1) - text2.count(str1)))

### 入力データtext1とマッチ文字列text2のヒット開始単語位置
def getStartPos(text1, text2):
	try :
		if text1:
			return text1.index(text2)
		else:
			return -1
	except ValueError:
		return -1

### 入力データtext1とマッチ文字列text2のヒット終了単語最後まで位置
def getEndPos(text1, text2):
	try :
		if text1:
			return len(text1) - text1.index(text2) - len(text2)
		else:
			return -1
	except ValueError:
		return -1

#####言語判断為の特徴抽出定義
# 他言語eを統一する
def replaceChar (text):
	afterText = text.replace('É', 'E').replace('é', 'E').replace('È', 'E')
	return afterText

# とある記号出現回数の統計
def getSymbolCount(text, symbol):
	if text :
		return text.count(symbol)
	else :
		return 0

# 各単語数の桁数の平均
from statistics import mean
def getWordsAvgLen(wordList):
	if len(wordList) ==0:
		return None
	else:
		return mean(map(len, wordList))

#各単語数の桁数の標準差
#長さが1の場合は-1を返す
from statistics import stdev
def getWordsStand(wordList):
	if len(wordList) >1 :
		return stdev(map(len, wordList))
	else:
		return -1

# 単語の有り無しを返却する関数
# 戻り値は1,0
def getExists(wordList, text):
	return (1 if (text in wordList) else 0)

# 単語の出現回数を返却する関数
def getWordCount(wordList, text):
	return wordList.count(text)

# 単語の含むかどうかを返却する関数
# 戻り値は1,0
def getContains(text, text2):
	return (1 if (text2 in text) else 0)

# リスト版の発音近似度、最小値を返す
from statistics import stdev
def getListPyphoneticsDis(wordList, text):
	disList = []
	if len(wordList) ==0:
		return None
	else:
		for word in wordList:
			disList.append(getPyphoneticsDis(word, text))
		return min(disList)
	# ↓これ一個目の値がおかしくなる？
	#return min(list(map(getPyphoneticsDis, wordList, text)))

# 区切り結合後の編集距離
def getPerfectLevenDistance(text1, text2):
	#結合
	text1 = re.sub(r'[･,-\.\'\s0-9#$%&!?*+/;:()<=>@^\[\]\\_{|}~"]', "", text1)
	text2 = re.sub(r'[･,-\.\'\s0-9#$%&!?*+/;:()<=>@^\[\]\\_{|}~"]', "", text2)
	return getLevenshteinDistance(text1, text2)

# 日本語か漢字かを判断する
# 戻り値はTure, Flase
def is_japanese(str):
    return True if re.search(r'[㈲ぁ-んァ-ン\u4E00-\u9FD0]', str) else False 

import re
#記号区切り、リストに単語を格納して返す
def getWordListBySymbol (text):
	return list(filter(lambda str:str != '', re.split(r'[･,-\.\'\s0-9#$%&!?*+/;:()<=>@^\[\]\\_{|}~"]', text)))

# リスト中重複要素があるか
def hasDuplicateWord (wordList):
	# 1桁の単語を除く
	wordList = [word for word in wordList if len(word) > 2]
	return len(wordList) != len(set(wordList))

# 数字があるかを判断する
# 戻り値はTure, Flase
import re
def numberCount(str):
    return len(re.findall(r'[0-9]', str))

# イニシャルの数を返却する
# 1桁文字は必須とするが、/.ピリオドは必須としない
# 文字指定もできる、指定しない場合は全文字
import re
def getInitialCount(str, letter):
	if letter == None:
		return len(re.findall(r' [A-Z](\.)? ', str)) + len(re.findall(r' [A-Z](\.)?$', str))
	if letter == 'M':
		return len(re.findall(r' [M](\.)? ', str)) + len(re.findall(r' [M](\.)?$', str))

'''ここからは簡単なUT
print(hanKakuChange("えeeえ１２12"))
print(charChange("A,.'-*!?0123#$%&!?*+/;:()<=>\[]@^_{|}~+a"))
print(getLen("BDUL, JAN KABIR MOHAMMAD"))
print(getWordNumberBySymbol("BDUL, JAN KABIR MOHAMMAD"))
print(getWordNumberBySpace("BDUL, JAN KABIR MOHAMMAD"))
print(getSequenceMatcherDistance("BDUL, JAN KABIR MOHAMMAD", "ABDUL, JAN KABIR MOHAMMAD"))
print(getPerfectLevenDistance("BDUL, JAN KABIR MOHAMMAD", "ABDUL; JAN KABIR MOHAMMAD"))
print(getLevenshteinDistance("BDUL, JAN KABIR MOHAMMAD", "ABDUL; JAN KABIR MOHAMMAD"))
print(getOverlap("BDUL, JAN KABIR MOHAMMAD", "ABDUL, JAN KABIR NOHAMMAD"))
print(getCharCount("BDUL, JAN KABIR MOHAMMAD", "T", "D"))
print(getStartPos("BDUL, JAN KABIR MOHAMMAD", "JAN KABIR MOHAMMAD"))
print(getEndPos("BDUL, JAN KABIR MOHAMMAD", "JAN KABIR MOHAMM"))
print(getPyphoneticsDis("BDUL, JAN KABIR MOHAMMAD", "JAN KABIR MOHAMMAD"))


print(getSymbolCount("BDUL, JAN, KABIR, MOHAMMAD", "."))
print(getWordsAvgLen(['BDUL', 'JAN', 'KABIR', 'MOHAMMADAA']))
print(getWordsStand(['BDUL', 'JAN', 'KABIR', 'MOHAMMADAA']))
print(getExists(['BDUL', 'JAN', 'KABIR', 'MOHAMMADAA'], 'JA'))
print(getContains("BDUL, JAN, KABIR, MOHAMMAD", "HAMMB"))
print(getListPyphoneticsDis(['BDUL', 'JAN', 'KABIR', 'MOHAMMADAA'], "MOHAMMATAAAA"))
print(getStartPos("BDUL, JAN KABIR MOHAMMAD", "JJJJ"))

print(hasDuplicateWord(['A', 'A', 'BC', 'BC']))
print(is_japanese('あ123'))
print(hasNumber('あ'))
print(getInitialCount("BDUL,  M.  A.. JAN KABIR MOHAMMAD M", 'M'))
print(numberCount('1234asd'))
'''

