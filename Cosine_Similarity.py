import pandas as pd
from scipy import sparse
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist, jaccard
from sklearn.feature_extraction.text import TfidfVectorizer
#################################################################################################
path = "D:\\final year project\Datasets\\Movies.csv"
path.encode('utf-8').strip()
moviesWithoutIndex = pd.read_csv(r"C:\Users\HP ITFAC\Desktop\FYP\datasets\inputs\Movies.csv",header=0,encoding = 'unicode_escape')
movies = moviesWithoutIndex.set_index('movieId')
col_one_list = moviesWithoutIndex['movieId'].tolist()

# Normalize ratings data
movieratingsOnly =moviesWithoutIndex[["R1","R2","R3","R4","R5","hype"]]
x = movieratingsOnly.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
movieratingsOnly = pd.DataFrame(x_scaled)
movieratingsOnly.columns = ["R1","R2","R3","R4","R5","hype"]
movieratingsOnly.info()
moviesWithoutIndex.drop(labels = ["R1","R2","R3","R4","R5","hype"],axis = 1,inplace = True)
movieratingsOnly['movieId'] = moviesWithoutIndex['movieId']
moviesDf = pd.merge( moviesWithoutIndex, movieratingsOnly, left_on='movieId', right_on='movieId')

############################################################

def getGenreSimilarity():
    corpus = moviesWithoutIndex["genres"].tolist()
    # print(corpus)
    vect = TfidfVectorizer(min_df=1, stop_words="english")
    tfidf = vect.fit_transform(corpus)
    pairwise_similarity = tfidf * tfidf.T

    item_similarity_df = pd.DataFrame(pairwise_similarity.toarray(), index= col_one_list, columns=col_one_list)
    # print(item_similarity_df)
    return item_similarity_df

#################################################################################################

def getFeatureSimilarity():
    print(movies)
    del movies['title']
    del movies['genres']
    movies.fillna(0)
    print(movies.count())

    def standardize(row):
        new_row = (row - row.mean() )/ (row.max() - row.min())
        return new_row

    movies_std = movies.apply(standardize)
    print(movies_std)
    item_similarity = cosine_similarity(movies_std)
    # print("************************************")
    #print(item_similarity)
    print(movies.columns)
    col_one_list = moviesWithoutIndex['movieId'].tolist()
    print(col_one_list)


    item_similarity_df = pd.DataFrame(item_similarity, index=col_one_list, columns=col_one_list)
    print(item_similarity_df)
    return item_similarity_df



def get_similar_movies(mid):
    item_similarity_df = getFeatureSimilarity()
    genre_similarity_df = getGenreSimilarity()
    itemsimilar_score = item_similarity_df[mid]
    genresimilar_score = genre_similarity_df[mid]
    data = {'itemsimilar_score': [], "genresimilar_score": [],"MId": []}
    simScore = pd.DataFrame(data)
    simScore["itemsimilar_score"] = itemsimilar_score
    simScore["genresimilar_score"] = genresimilar_score
    simScore["MId"] =col_one_list
    simScore = simScore.sort_values(by='itemsimilar_score', ascending=False)
    simScore = simScore.head(10)
    simScore = simScore.sort_values(by='genresimilar_score', ascending=False)
    # similar_score = itemsimilar_score.sort_values(ascending= False)
    return simScore


#print("recommended movies ")
print(get_similar_movies(13))
# featuer = getFeatureSimilarity()
# genr = getGenreSimilarity()
# print(featuer)
# print(genr)
