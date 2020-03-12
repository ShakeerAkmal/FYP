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


def GetRecommendations(UID):
    IsExists = IsUserExists(UID)
    if IsExists:
        print(str(UID))
        Mid = getUserMovies(UID)
        if len(Mid) == 0:
            print('the list is empty')
            Mpresult = Mp.recoMovies(UID)
            print(Mpresult)
        else:
            alsresult = als.getALSReco(UID)
            time.sleep(45)
            cosineResult = []
            for i in Mid:
                cosresult = cos.get_similar_movies(float(i))
                cosineResult.append(cosresult)
            Mpresult = Mp.recoMovies(UID)
            print("***************************final *********************************")
            print(alsresult)
            print(cosineResult)
            print(Mpresult)
    else:
        print("User does not exists")


def IsUserExists(UID):
    completeDataset = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\inputs\IdAndMoviesv6.csv')
    result = completeDataset.query('id==' + str(UID)).head()
    id = result["id"].values
    try:
        x = id[0]
        isUser = True
    except:
        x=0
        isUser = False
    return x


def getUserMovies(UID):
    m2mDataset = pd.read_csv(r"C:\Users\HP ITFAC\Desktop\FYP\datasets\MovieManytoMany_dataframe.csv",header=None,encoding = 'unicode_escape')
    m2mDataset.columns = ["UID", "movieId", "rating"]
    result = m2mDataset.query('UID==' + str(UID)).head()
    id = result["movieId"].values
    return (id)


uid = 1281563425377910
GetRecommendations(uid)
