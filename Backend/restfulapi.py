from flask import Flask, request
from flask_restful import Resource, Api

import sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

import socket



def resultcovid():

    covid = pd.read_csv('coviddata.csv', engine = 'python')
    #print (covid.info())

    #print(covid.head())

    covid_variables = covid.drop(['id'], axis = 1)

    #print(covid_variables.head())

    covid_norm = (covid_variables-covid_variables.min())/(covid_variables.max()-covid_variables.min())

    #print(covid_norm)

    X_prime = covid_norm.ix[:,(0,1,2,3,4,5,6,7)].values
    #print(X_prime[0])

    Y = covid_norm.ix[:,(8)].values

    X = preprocessing.scale(X_prime)
    #print(X[0])


    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = .33, random_state = 17)
    knn = KNeighborsClassifier(n_neighbors=7)
    knn.fit(X_test,Y_test)
    porcentaje = knn.score(X_train,Y_train)
    print(porcentaje)

    mi_socket = socket.socket()
    mi_socket.connect(('localhost',8000))

    mi_socket.send(b'hello')
    
    mi_socket.close()

    
    return porcentaje*100





app = Flask(__name__)
api = Api(app)





class Covid(Resource):
    def get(self):
        rpta = resultcovid()
        print("Su resultado es: ",rpta)
        return [{'porcentaje': str(rpta)}]

    def post(self):
        arr = []
        some_json = request.get_json()
        arr.append(float(some_json['v1']))
        arr.append(float(some_json['v2']))
        arr.append(float(some_json['v3']))
        arr.append(float(some_json['v4']))
        arr.append(float(some_json['v5']))
        arr.append(float(some_json['v6']))
        arr.append(float(some_json['v7']))
        arr.append(float(some_json['v8']))
        
        print(arr)

        covid = pd.read_csv('coviddata.csv', engine = 'python')
        #print (covid.info())

        #print(covid.head())

        covid_variables = covid.drop(['id'], axis = 1)

        #print(covid_variables.head())

        covid_norm = (covid_variables-covid_variables.min())/(covid_variables.max()-covid_variables.min())

        #print(covid_norm)

        X_prime = covid_norm.ix[:,(0,1,2,3,4,5,6,7)].values
        #print(X_prime[0])

        Y = covid_norm.ix[:,(8)].values

        X = preprocessing.scale(X_prime)
        #print(X[0])


        X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = .33, random_state = 17)
        knn = KNeighborsClassifier(n_neighbors=int(some_json['kvariable']))
        knn.fit(X_test,Y_test)
        arrsca = preprocessing.scale(arr)
        rpta = knn.predict([arrsca])
        print(rpta[0]) 


        return {'devoresultado': str(rpta[0])},201

api.add_resource(Covid, '/api/covid')

if __name__ == '__main__':
    app.run(debug=True)