import ClusterPersonality as clus
import pandas as pd
import numpy as np

def recoMovies(uid):
    cluster = clus.getCluster(uid)
    print("*********************************************************************************")
    print(str(cluster))
    print("*********************************************************************************")
    clusterSimilarityData = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\MoviesWithClusterSim.csv')
    genreWeights = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\genreWeightForClusters.csv')


    # In[102]:
    clusterSimilarityData.head()
    genreWeights.head(15)

    # In[105]:
    if(cluster == 1):
        sortedByCluster = clusterSimilarityData.sort_values(by='cl1', ascending=False)
        top10 = sortedByCluster.head(10)
        print("Cl 1")

    if (cluster == 2):
        sortedByCluster = clusterSimilarityData.sort_values(by='cl2', ascending=False)
        top10 = sortedByCluster.head(10)
        print("Cl 2")

    if (cluster == 3):
        sortedByCluster = clusterSimilarityData.sort_values(by='cl3', ascending=False)
        top10 = sortedByCluster.head(10)
        print("Cl 3")

    if (cluster == 4):
        sortedByCluster = clusterSimilarityData.sort_values(by='cl4', ascending=False)
        top10 = sortedByCluster.head(10)
        print("Cl 4")

    # In[106]:

    top10.head()
    # In[109]:
    weights = genreWeights.query('cluster=='+str(cluster))
    # In[135]:
    newDF = pd.DataFrame({'movieId':[],'genreScore':[]})
    for index, row in top10.iterrows():
        genres = row['genres']
        genresstr = str(genres)
        genresarr = genresstr.split(' ')
        idnum = row['movieId']
        totalscore = 0.0
        for i in genresarr:
            gen = str(i)
            scorerow = weights.query('genre == "'+gen+'"')
            score = scorerow["genreWeight"]
            try:
                totalscore = float(score) + totalscore
            except:
                totalscore = 0 + totalscore

        newDF = newDF.append({'movieId':idnum,'genreScore':totalscore} , ignore_index=True)
    newDF.head(10)
    # In[136]:
    finalDF = newDF.sort_values(by='genreScore', ascending=False)
    return (finalDF)

uid4 = 845762529201263
uid = 1281563425377910
uid3 = 1084806141905552
uid2 = 1108136359517809
# result = recoMovies(uid2)
# print(result)


