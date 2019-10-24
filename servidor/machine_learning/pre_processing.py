 # -*- coding: utf-8 -*-
from static_beacons import StaticBeacons
from collections import deque
import pandas as pd
import numpy as np
import re
from itertools import *
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import VarianceThreshold
from sklearn import random_projection
from sklearn.cluster import FeatureAgglomeration


'''


'''


# remove as linhas zeradas
def removeZeroLines (df):
	df = df[(df.T != 0).any()]
	return df[(df.T != -1).any()]

# remove os espacos extras nos nomes das colunas
def removeWhiteSpaces(df):
	return df.rename(columns=lambda x: x.strip())

# encontra a primeira coluna que nao corresponde a um MAC address
def macRegex (df):
	for column in list(df):
		if not re.search('(\w{2}:{1}){5}(\w{2})$', column):
			return column


def column_wifi(df):
	list_features = list(df)
	if list_features[-1] == "sensorhub":
		return list_features[-2]
	elif list_features[-1] == "battery":
		return list_features[-3]
	else:
		return list_features[-1]

class PreProcessing():

	dic = {"all":1, "simple":0, "pca":2, "agglomeration":3}

	# df -> dataframe
	# norm -> False -> df sera utilizado sem normalizacao
	#		-> True -> df sera normalizado
	# model -> tipo de modelo para selecao de features (all, simple, ...)
	# features -> "b" -> somente beacons serao considerados features
	#           -> "b,w" -> beacons e wifi serao considerados features
	# to_binary -> False -> df ja esta binaria
	#            -> Valor -> valor minino considerado como 1 na hora de binarizar a matriz
	def __init__(self,df,norm=False,model="all",features="b",to_binary=False):

		# remove os espacos extras nos nomes das colunas
		df = removeWhiteSpaces(df)
        # sensorhub
		try:
			self.sensorhub = df.loc[:,'sensorhub']
		except Exception:
			pass

		# Bluetooth
		try:
			self.beacons = df.loc[:,:macRegex(df)]
			self.beacons = self.beacons.iloc[:, :-1]
			self.beacons = removeZeroLines(self.beacons)
		except Exception:
			pass

		# Wifi
		try:
			self.wifi = df.loc[:,macRegex(df):column_wifi(df)]
			self.wifi = self.wifi.iloc[:, :-1]
			self.wifi = removeZeroLines(self.wifi)
		except Exception:
			pass

		# battery
		try:
			self.batery = df.loc[:,'battery']
		except Exception:
			pass

		self.norm=norm
		self.model=self.dic[model]
		self.to_binary = to_binary
		print ("modelo : "+model)




	def build (self):

		my_df = None

		# FEATURES
		# beacons como features
		try:
			my_df = pd.concat([my_df,self.beacons.astype(int)], axis=1)
		except Exception as e:
			pass
		try:
			my_df = pd.concat([my_df.astype(int),self.wifi.astype(int)], axis=1)
		except Exception as e:
			pass

		my_df = my_df.fillna(0.0).astype(int)

		# MODELS
		# modelo all -> todos os beacons serao utilizados
		if self.model == 1:
			pass

		# modelo simple -> deixa so os beacons fixos hardcoded
		elif self.model == 0:
			# retorna o conjunto de colunas que sao os beacons hardcoded
			static_beacons = StaticBeacons().build(my_df)
			my_df = my_df[static_beacons]
			my_df = removeZeroLines(my_df)





		# # TRANSFORMACAO PARA BINARIO
		# # TODO colocar isso antes ou depois da aplicacao do modelo?
		# if self.to_binary:
		# 	my_df = df > self.to_binary
		# 	my_df = df.astype(int)
		# # caso contrario, matriz assume-se que matriz ja esta binaria
        #

		# NORMALIZACAO
		# normaliza a matriz
		# nao existe csv de matriz normalizada
		if self.norm == True:
			my_df = Normalization(my_df, self.sensorhub,self.batery).build()
		# caso contrario, ja existia csv de matriz normalizada, e normalized eh esta matriz
		# ou nao havera nenhum tipo de normalizacao

        #
		# # modelo PCA -> descarta as features de menor importancia
		# if self.model == 2:
		# 	# descartar features com menos de 80% de variancia
		# 	pca = PCA(n_components=0.9, svd_solver='full')
		# 	array = pca.fit_transform(my_df)
		# 	my_df = pd.DataFrame(array, index=list(my_df.index))
        #
        #
		# # modelo feature agglomeration -> aglomera features muito parecidas
		# #TODO precisa dar o  numero de clusters:
		# # talvez rodar a clusterizacao com todas as features, depois voltar e reduzir com esse numero de clusters
		# elif self.model == 3:
		# 	agglo = FeatureAgglomeration(connectivity=connectivity,
        #                              n_clusters=32)
		# 	agglo.fit(my_df)
		# 	array = agglo.transform(my_df)
		# 	my_df = pd.DataFrame(array, index=list(my_df.index))


		return my_df


	# retorna o df de modalities, se existir
	# retorna uma coluna variando de 0 a 3 de acordo com o modality
	def get_modalities(self):
		try:
			return self.modality.idxmax(axis=1).astype('category').cat.codes
		except Exception:
			return None





class Normalization():

	my_buffer = deque(maxlen=10)
	my_buffer_time = deque(maxlen=10)

	def __init__(self,df,sensorhub,battery):
		self.df=df
		self.sensorhub = sensorhub
		self.battery = battery
		self.timestamp  = list(df.index)


	# def set_buffer(self, line):
	# 	self.my_buffer.append(line)
	# 	if len(self.my_buffer) >= 10:
	# 		self.my_buffer.remove(self.my_buffer[0])

	def build_line (self,time, line):
		merge_lines = line
		for i, i_line in enumerate(reversed(self.my_buffer)):
			if self.my_buffer_time[i]+10 > time:
				for indx, item in enumerate(i_line):
					if item == 1:
						merge_lines[indx] = 1

		return merge_lines




	def build (self):
		i = 0
		first_stop = False
		signature = None
		print ("group and fill")
		print ('initial shape {}'.format(self.df.shape))
		filled = None
		index = None

		loop_stopped = False
		time_loop_stopped = 0
		my_line_loop_stopped = []

		mycount = 0
		for timestamp_line, row in self.df.iterrows():

			mycount+=1

			print timestamp_line
			if loop_stopped:
				if timestamp_line in self.sensorhub.index:
					print type(self.sensorhub.loc[timestamp_line]), "tipo"
					print self.sensorhub.loc[timestamp_line], "valor"
					print self.sensorhub.loc[timestamp_line] == 1, "condicao"
					if self.sensorhub.loc[timestamp_line] != 1:
						for gap in xrange(0,timestamp_line - time_loop_stopped,10):
							self.df.loc[time_loop_stopped+gap] = my_line_loop_stopped
						loop_stopped = False
			else:
				if timestamp_line in self.sensorhub.index:
					print type(self.sensorhub.loc[timestamp_line]), "tipo"
					print self.sensorhub.loc[timestamp_line], "valor"
					print self.sensorhub.loc[timestamp_line] == 1, "condicao"
					if self.sensorhub.loc[timestamp_line] == 1:
						loop_stopped = True
						time_loop_stopped = timestamp_line
						my_line_loop_stopped = self.build_line(timestamp_line, row)
					else:
						self.my_buffer_time.append(timestamp_line)
						self.my_buffer.append(row)




			# USER esta stopped
			# S = 0 -> S = 1
			# if self.modality.loc[row.name,'stopped'] == 1 and first_stop == False:
			# 	first_stop = True
			# 	# group the last 5 seconds of signatures
			# 	signature, calls = self.group(i,5,0)
			# 	# calls guarda quantas timestamps pra cima devem ser atualizadas com a nova signature
			# 	calls += 1
			# 	signature = signature.astype(int)
            #
			# 	# preenche as assinaturas anteriores
			# 	self.fill_previous(calls, signature, i)
            #
			# # Micromovimentos
			# # **** so importam os que estao na matriz so com os beacons
			# # S = 1 -> S = 1
			# if self.modality.loc[row.name,'stopped'] == 1  and first_stop == True:
			# 	ind, fil = self.fill(self.timestamp[i],signature)
			# 	try:
			# 		index = np.concatenate((index, ind), axis=0)
			# 		filled = np.concatenate((filled, fil), axis=0)
            #
			# 	except :
			# 		index = ind
			# 		filled = fil
            #
			# 	self.df.iloc[i] = signature
            #
			# # User nao esta mais stopped
			# # S = 1 -> S = 0
			# elif self.modality.loc[row.name,'stopped'] == 0 and first_stop == True:
            #
			# 	# muito lento
			# 	#filled_df = filled_df.append(self.fill(self.timestamp[i],signature))
			# 	#filled_df = pd.concat([filled_df,self.fill(self.timestamp[i],signature)])
			# 	# usa muita memoria
			# 	#self.df = self.df.append(self.fill(self.timestamp[i],signature))
			# 	#self.df = pd.concat([self.df,self.fill(self.timestamp[i],signature)])
			# 	ind, fil = self.fill(self.timestamp[i],signature)
			# 	try:
			# 		index = np.concatenate((index, ind), axis=0)
			# 		filled = np.concatenate((filled, fil), axis=0)
            #
			# 	except :
			# 		index = ind
			# 		filled = fil
            #
            #
			# 	first_stop = False
            #
            #
			# i+=1
            #


		print "loop = ",mycount
		print ("end of group and fill")
		# TODO aqui gasta muita memoria, momentaneamente
		# filled_df = pd.DataFrame(filled, index=index, columns=list(self.df))
		filled_df = self.df
		# filled_df = filled_df.groupby(filled_df.index).first()
		filled_df.sort_index(inplace=True)

		print ('final shape {}'.format(filled_df.shape))

		return filled_df




	def group (self,i,acc, calls):

		if i <= 0:
			return self.df.iloc[i,:], calls
		diff = int(self.timestamp[i])-int(self.timestamp[i-1])
		if diff > acc:
			return self.df.iloc[i,:], calls
		if diff == acc:
			return np.logical_or(self.df.iloc[i,:],self.df.iloc[i-1,:]), calls

		new_result, new_calls = self.group(i-1,acc-diff,calls+1)
		return np.logical_or(self.df.iloc[i,:], new_result), new_calls

	# coloca a nova signature nas timestamps anteriores e na atual
	def fill_previous (self, n, signature, index):
		self.df.iloc[index] = signature
		for j in range (n):
			self.df.iloc[index-j] = signature




	def fill(self,end,signature):

		index = []
		# fill de 2 em 2 segundos
		# constroi as novas timestamps
		while signature.name+2 < end:
			# add 2 na timestamp
			signature.name = signature.name + 2
			index.append(signature.name)

		# constroi de uma vez o 2d array com as signatures
		filled = np.zeros((len(index), len(signature)))
		filled[:,:] = np.array(signature)
		#filled = pd.DataFrame(signature, index=index, columns=list(self.df))
		return index, filled
