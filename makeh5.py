import sys
sys.path.append('/skku/skku01/gpt/src')
import h5py
import numpy as np
import tokenization as tk
import argparse
import re

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--txt', metavar='txtFile', type=str)
parser.add_argument('--hdf5', metavar='hdf5File', type=str)
parser.add_argument('--category', metavar='fileCat', type=int)
args = parser.parse_args()

txt_list = []
finalList = []
txt_list = args.txt.split(',')
f = h5py.File(args.hdf5,'w')
textCategory = '/category/'+str(args.category)

def makeArray(file_name):
        txtFile = open(file_name, 'r', encoding = 'utf-8')
        txtLine = ""
        for i in txtFile:
                txtLine = i.split('\n')
                for j in txtLine:
                        txtLine = txtLine + j
        print(txtLine)
        # 저장할 hdf5파일
        hdf5File = args.hdf5
        dictionary = tk.load_vocab("/skku/skku01/gpt/models/345K/vocab.txt")

        basic = tk.BasicTokenizer()

        wordTok = tk.WordpieceTokenizer(dictionary)

        tokenList = []
        tok = wordTok.tokenize(txtLine)
        for j in tok:
                if j =='[UNK]':
                        continue;
                tokenList.append(dictionary[j])
        finalElement=np.array(tokenList, dtype = np.int32)
        finalList.append(finalElement)
        txtFile.close()

def main():
        for i in txt_list:
                makeArray(i)
        finalArr = np.array(finalList)
        print(finalArr.shape)
        f.create_group('/category')
        dt = h5py.special_dtype(vlen = np.int32)
        f.create_dataset(textCategory,data=finalArr,dtype=dt,chunks=True)
        f.close()

if __name__== '__main__':
        main()
