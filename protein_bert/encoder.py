import pandas as pd
import proteinbert

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


csv_file_path = "/home/meng/sst-project/protein_bert/fasta.csv"

# csv_handle = open(csv_file_path,"r")

# csv_content = csv_handle.readlines()

# prot_list = []
# name_list = []

# for line in csv_content:
#     data_line = line[:-1].split(",")
#     name = data_line[0]
#     prot_sequence = data_line[1]

#     name_list.append(name)
#     prot_list.append(prot_sequence)

# csv_handle.close()
# data_set = pd.DataFrame(prot_list)

input_set = pd.read_csv(csv_file_path).dropna().drop_duplicates()

# print(input_set)

seqs = input_set['seq']
raw_Y = input_set['label']

dataset = pd.DataFrame({'seq': seqs, 'raw_Y': raw_Y})
# dataset = filter_dataset_by_len(dataset, seq_len = seq_len, dataset_name = dataset_name, verbose = verbose)
seqs = dataset['seq']
raw_Y = dataset['raw_Y']




create_model_function = proteinbert.conv_and_global_attention_model.create_model
model,encoder = proteinbert.load_pretrained_model_from_dump("/home/meng/proteinbert_models/epoch_92400_sample_23500000.pkl",create_model_function)
# print(encoder)


X = encoder.encode_X(seqs, 5300)
encode_result = X[0]

dfarray = np.array(encode_result)

n_clusters = 2

kmeans = KMeans(n_clusters=int(n_clusters)).fit(dfarray)
y_pred = kmeans.predict(dfarray)

result_dict = {}
for result in y_pred:
    if result not in result_dict.keys():
        result_dict[result] = 1
    else:
        result_dict[result] = result_dict[result] + 1
print(result_dict)
# for element in X[1][1]:
#     print(sum(element))