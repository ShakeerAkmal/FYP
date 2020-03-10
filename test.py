import csv
import numpy as np
import pandas as pd
#import ALS as als
# import ALS_recommendation as als2
import Cosine_Similarity as cos
#import ClusterPersonality as cluster
import sys, getopt, pprint
from pymongo import MongoClient
#CSV to JSON Conversion
csvfile = open('D:\\final year project\Datasets\mypersonality_final.csv', 'r')
reader = csv.DictReader( csvfile )
mongo_client=MongoClient()
db=mongo_client.recommendation
db.personality.drop()


def insertMoviesToDb():
    movies = pd.read_csv('D:\\final year project/sample.movie.csv')
    db.Movie.insert_many(movies.to_dict('records'))
    #print(movies)

def insertUsersToDb():

    users = pd.read_csv('D:\\final year project\Datasets\mypersonality_final.csv')
    id = np.asarray([1])
    a_l = id.tolist()

    i=1
    while i < 250:
        a_l.insert(i, i+1)
        i += 1
    id = np.asarray(a_l)
    users['userId'] = id
    print(users)
    db.User.insert_many(users.to_dict('records'))

#insertUsersToDb()

#als2
#cos
#cluster