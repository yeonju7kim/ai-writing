import os.path

import h5py
# import tensorflow_text.tools.wordpiece_vocab as tk
import numpy as np
from tensorflow_text.python.ops.wordpiece_tokenizer import *
import tensorflow as tf
# import tokenization as tk

def load_vocab(filename):
	vocab_dict = {}
	vocab_list = []
	line_num = 0
	with open(filename, 'r', encoding='utf8', newline='\n') as fp:
		# vocab_dict[line_num] = fp.read()
		# line_num = line_num + 1
		vocab_list = fp.read().split('\n')
		for vocab in vocab_list:
			vocab_dict[line_num] = vocab
			line_num = line_num + 1
	return vocab_dict

def make_tokenizer(filename):
	dictionary = load_vocab(filename)
	wordTok = WordpieceTokenizer(filename)
	return wordTok

def read_h5py(filename):
	f = h5py.File(filename, 'r')
	return f[[key for key in f.keys()][0]]

def main():
	tokenizer = make_tokenizer("models/345K/vocab.txt")
	raw_data = read_h5py('data/news_sample.hdf5')
	line_list = []
	for i in range(len(raw_data['0'])):
		line_list.append(raw_data['0'][i])
	line_tensor = tf.convert_to_tensor(line_list)
	print(tokenizer.detokenize(line_tensor))

if __name__ == '__main__':
	main()