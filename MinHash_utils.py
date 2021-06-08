import pickle as pkl
import os
import csv
import enchant
import wordninja
import re
import math
from nltk import ngrams
import itertools
from collections import OrderedDict
import random
from itertools import islice


def get_dic_of_common_windows_software_names():
    common_software_names_words = get_common_software_words()
    required_s_names = get_required_s_names()
    print('required_s_names length = ' + str(len(required_s_names)))
    d = get_enchant()
    dic_of_softwares = {}
    f = open("/DATA/Ofir/Common_Windows_softwares_new.txt", "r")
    for software_name in f:
        processed_software_name = remove_common_words(pre_process_software_name(software_name),
                                                      common_software_names_words)
        if processed_software_name in required_s_names:
            dic_of_softwares[processed_software_name] = software_name
    # add edited s_name to s_names dict
    for s_name in required_s_names.keys():
        if s_name not in dic_of_softwares:
            dic_of_softwares[s_name] = s_name
    return dic_of_softwares
    
def get_common_software_words():
    common_words = {}
    with open('/DATA/Ofir/most_commom_words.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            common_words[row[0]] = row[1]
    return common_words


def get_required_s_names():
    required_s_names = {}
    f = open("/DATA/Ofir/s_names_dict.txt", "r")
    for software_name in f:
        required_s_names[software_name.replace('\n', '')] = 1
    return required_s_names
    
    
def get_all_3_grams_list():
    all_3_grams_list = [''.join(x) for x in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=3)]
    three_grams = {}
    for three_gram in all_3_grams_list:
        three_grams[three_gram] = {}
    return three_grams    
    
    
def init_three_grams_dic(three_grams_dic, dic_of_softwares):
    for software_name in dic_of_softwares.keys():
        for software_name_3_gram in get_3_grams(software_name):
            if software_name_3_gram in three_grams_dic:
                three_grams_dic[software_name_3_gram][software_name] = 1

    three_grams_dic = OrderedDict(sorted(three_grams_dic.items(), key=lambda kv: kv[0]))


def get_three_gram_to_hash_values_dic(three_grams_dic):
    three_grams_dic_length = len(three_grams_dic)
    coeffA = pickRandomCoeffs(100, three_grams_dic_length)
    coeffB = pickRandomCoeffs(100, three_grams_dic_length)
    three_gram_to_hash_values_dic = {}
    x = 0
    for three_gram in three_grams_dic.keys():
        three_gram_to_hash_values_dic[three_gram] = {}
        for i in range(0, 100):
            a = coeffA[i]
            b = coeffB[i]
            three_gram_to_hash_values_dic[three_gram]['h_' + str(i)] = h(a, x, b, three_grams_dic_length)
        x += 1
    return three_gram_to_hash_values_dic


def init_signature_matrix(dic_of_softwares):
    inf = math.inf
    signature_matrix = {}
    for i in range(0, 100):
        signature_matrix[i] = {}
        for software_name in dic_of_softwares.keys():
             signature_matrix[i][software_name] = inf
    return signature_matrix

def eval_signature_matrix(signature_matrix, sorted_three_grams_dic, three_gram_to_hash_values_dic):
    for three_gram, software_names in sorted_three_grams_dic.items():
        for software_name in software_names.keys():
            for i in range(0, 100):
                signature_matrix[i][software_name] = min(signature_matrix[i][software_name], three_gram_to_hash_values_dic[three_gram]['h_' + str(i)])

def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}


def build_LSH_buckets(signature_matrix, dic_of_softwares):
    #LSH - banding b = 25, r = 4
    buckets = {}
    i = 1
    for band in chunks(signature_matrix, 4):
        band_index = 'band_' + str(i)
        buckets[band_index] = {}
        for software_name in dic_of_softwares.keys():
            sig = []
            for h in band.keys():
                sig.append(str(band[h][software_name]) + '_')
            if ''.join(sig) in buckets[band_index]:
                buckets[band_index][''.join(sig)][software_name] = 1
            else:
                buckets[band_index][''.join(sig)] = {software_name : 1}
        i += 1
    return buckets

def save(LSH_buckets, signature_matrix, three_gram_to_hash_values_dic):
    pkl.dump(LSH_buckets, open('/DATA/Ofir/minhash/LSH_buckets.pkl', 'wb'))
    pkl.dump(signature_matrix, open('/DATA/Ofir/minhash/signature_matrix.pkl', 'wb'))
    pkl.dump(three_gram_to_hash_values_dic, open('/DATA/Ofir/minhash/three_gram_to_hash_values_dic.pkl', 'wb'))


def prepaere_csv_files_per_band(LSH_buckets):
    csv_columns = ['sig', 'bucket', 'bucket size']
    for band, bucket in LSH_buckets.items():
        with open('/DATA/Ofir/minhash/bands' + band + '.csv', 'w') as f:
            f.write(str(csv_columns) + '\n')
            for sig, s_names in bucket.items():
                f.write("%s,%s, %s\n" % (str(sig), list_to_str(list(s_names.keys())), str(len(s_names))))


def list_to_str(lst):
    ans = ''
    for el in lst:
        ans += str(el) + ' : '
    return ans