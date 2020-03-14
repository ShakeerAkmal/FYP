import csv
import numpy as np
import pandas as pd
import time
import ALS_recommendation as als
import Cosine_Similarity as cos
import Moviesforpersonality as Mp
import sys, getopt, pprint
from pymongo import MongoClient
import csv
import statistics

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
            Mpresult.columns = ['MID', 'rating']
            # print(Mpresult)
            # return ([],[],Mpresult)
            return (Mpresult)
        else:
            alsresult = als.getALSReco(UID)
            # time.sleep(45)
            cosineResult = []
            for i in Mid:
                cosresult = cos.get_similar_movies(float(i))
                cosineResult.append(cosresult)
            Mpresult = Mp.recoMovies(UID)
            result = pd.concat(cosineResult)
            cosFinal = result[["MId","itemsimilar_score"]]
            cosFinal.columns = ['MID', 'rating']
            Mpresult.columns = ['MID', 'rating']
            alsresult['rating'] = alsresult['rating'].apply(lambda x: x * 0.195)
            cosFinal['rating'] = cosFinal['rating'].apply(lambda x: x * 0.294)
            Mpresult['rating'] = Mpresult['rating'].apply(lambda x: x * 0.511)


            # print (alsresult)
            # print(cosFinal)
            # print(Mpresult)
            finalScores = pd.concat([alsresult,cosFinal,Mpresult], ignore_index=True)
            data = {'MID': [], "rating": []}
            NewDF = pd.DataFrame(data)
            for index, row in finalScores.iterrows():
                Movieid = row['MID']
                rating = row['rating']
                if Movieid in Mid:
                    print(Movieid)
                    print(Mid)
                else:
                    NewDF = NewDF.append({'MID': Movieid, "rating": rating}, ignore_index=True)
            # Create DataFrame
            sorted = NewDF.sort_values(by='rating', ascending=False)
            final = sorted.head(10)
            row_list = final
            row_list["UID"] = str(UID)+"x"
            row_list.to_csv(r'C:\Users\HP ITFAC\Desktop\FYP\datasets\result10.csv',index=None, header=False,float_format='%.18f')

            Movies = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\inputs\Movies.csv')
            # uid = 1108136359517809
            finalResult = pd.merge(final, Movies, left_on='MID', right_on='movieId')
            # return (alsresult,result,Mpresult)
            print("************************************************final ************************************************")

            print(finalResult[['MID','rating','title']])
            print("******************************************************************************************************")

            return (final)
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
uid4 = 845762529201263
uid = 1281563425377910
uid3 = 1084806141905552
uid2 = 1108136359517809
uid5 =656302011806663
uid6 =2361065527260956
uid7 =3405381112870618
uid8 =1108136359517809
uid9 =2287775961336722
uid10 =2515900458653709
uid11=1413737972090633
uid12 =2229047854070676
uid13=2459148220983721





uid000 =2673067859457596
# x = GetRecommendations(uid000)
# print("*************************************final ***********************************")
# print("Standard Deviation of x is % s "% (statistics.stdev(x["rating"])))
# print("Standard Deviation of y is % s "% (statistics.stdev(y["itemsimilar_score"])))
# print("Standard Deviation of z is % s "% (statistics.stdev(z["genreScore"])))

# GetRecommendations(uid000)
# 885419185249490
#3447481625293846
# 581752609335445
# 3347102761973301
#1081082628933186
# 2511294662228557
# 1833507973450442
# 2340811559543820
# 1084806141905552
#1281563425377910
#1108136359517809
#845762529201263
#656302011806663
#845762529201263
#1255945248128127
#2650774725248679
#1974273129343556
# 966095950450635
# 1467433210100613
# 2545605765710163