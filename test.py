import csv
import numpy as np
import pandas as pd
import time
import ALS_recommendation as als
import Cosine_Similarity as cos
import Moviesforpersonality as Mp
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




uid = 1281563425377910
def GetRecommendations(UID):
    print(str(UID))
    alsresult = als.getALSReco(UID)
    time.sleep(45)
    cosresult = cos.get_similar_movies(9)
    Mpresult = Mp.recoMovies(UID)
    print("***************************final *********************************")
    print(alsresult)
    print(cosresult)
    print(Mpresult)



GetRecommendations(uid)
