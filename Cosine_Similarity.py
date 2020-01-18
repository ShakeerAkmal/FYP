import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist, jaccard
from sklearn.feature_extraction.text import TfidfVectorizer
#################################################################################################
path = "D:\\final year project\Datasets\\Movies.csv"
path.encode('utf-8').strip()
moviesWithoutIndex = pd.read_csv("D:\\final year project\Datasets\\MoviesMini.csv",header=0,encoding = 'unicode_escape')
movies = moviesWithoutIndex.set_index('movieId')
col_one_list = moviesWithoutIndex['movieId'].tolist()

def getGenreSimilarity():
    corpus = moviesWithoutIndex["genres"].tolist()
    print(corpus)
    vect = TfidfVectorizer(min_df=1, stop_words="english")
    tfidf = vect.fit_transform(corpus)
    pairwise_similarity = tfidf * tfidf.T

    item_similarity_df = pd.DataFrame(pairwise_similarity.toarray(), index= col_one_list, columns=col_one_list)
    print(item_similarity_df)
    return item_similarity_df

#################################################################################################
#https://www.youtube.com/watch?v=3ecNC-So0r4

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
    print("************************************")
    #print(item_similarity)
    print(movies.columns)
    col_one_list = moviesWithoutIndex['movieId'].tolist()
    print(col_one_list)


    item_similarity_df = pd.DataFrame(item_similarity, index=col_one_list, columns=col_one_list)
    print(item_similarity_df)
    return item_similarity_df



def get_similar_movies(mid):
    item_similarity_df = getFeatureSimilarity()
    similar_score = item_similarity_df[mid]
    similar_score = similar_score.sort_values(ascending= False)
    return similar_score


#print("recommended movies ")
#print(get_similar_movies(2))
featuer = getFeatureSimilarity()
genr = getGenreSimilarity()
print(featuer)
print(genr)
