#!/usr/bin/env python
#--coding:utf-8--

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/mw/Dropbox (MIT)/02 Vector files/Kphaffii SnapGene/Protein Files/protana_processed.csv')
dfarray = np.array(df)
print(dfarray)
n_clusters = 2
kmeans = KMeans(n_clusters=int(n_clusters)).fit(dfarray)
y_pred = kmeans.predict(dfarray)
centroids = kmeans.cluster_centers_

# principle component analysis on the input data
pca = PCA(n_components=2)
pca.fit(dfarray)
X_tf = pca.transform(dfarray)
c_tf = pca.transform(centroids)

# use the first two PCs to visualize clustering 
plt.scatter(X_tf[:,0],X_tf[:,1],c=y_pred)
plt.scatter(c_tf[:,0],c_tf[:,1],c='red')
plt.show