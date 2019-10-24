
import numpy as np
import pandas as pd

import os

from kmodes import kmodes
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.cluster import MiniBatchKMeans
import csv
from datetime import datetime
import time
import sys
from sklearn import metrics
from sklearn.metrics import pairwise_distances


class Clustering():

	# obs:
	# mode = compare_k -> usa metric para decidir qual o melhor k, sendo n_clusters o valor maximo de k a ser testado
	# mode = fixed_k -> usa n_clusters como k fixo
	def __init__(self, df, n_clusters=20,  mode="compare_k", metric="calinski_harabaz", algorithm="kmeans"):
		self.df = df
		self.n_clusters = n_clusters
		self.metric = metric
		self.algorithm = algorithm
		self.mode = mode
		self.max_lines = 800000
		print df


	def clusterize (self):
		best_score = -1
		best_labels = []
		best_k = 0

		if self.mode == "compare_k":
			for k in range(2,self.n_clusters+1):
				classifier = self.return_classifier(k).fit(self.df)
				score = self.return_metric(classifier.labels_)
				if best_score < score:
					best_labels = classifier.labels_
					best_score = score
					best_k = k
				print ("For k = {} the {} is = {}".format(k, self.metric,score))
			print ("Best k was %d with score %.3f"%(best_k,best_score))

		else:
			classifier = self.return_classifier(self.n_clusters).fit(self.df)
			best_labels = classifier.labels_
			best_k = self.n_clusters
		return best_labels, best_k

	def return_classifier(self, k):
		if self.algorithm == "kmodes":
			return kmodes.KModes(n_clusters=k, init='Huang', n_init=1, verbose=1)
		elif self.algorithm == "kmeans":
			if len(self.df) > self.max_lines:
				return MiniBatchKMeans(n_clusters=k, random_state=1)
			else:
				return KMeans(n_clusters=k, random_state=1)

	def return_metric (self, labels):
		if self.metric=="calinski_harabaz":
			return metrics.calinski_harabaz_score(self.df, labels)
		elif self.metric=="silhouette":
			return metrics.silhouette_score(self.df, labels, metric='euclidean',sample_size=20000)
