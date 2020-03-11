import pandas as pd
import numpy as np
import glob
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt


dataset = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\inputs\IdAndMoviesv6.csv')
dataset.drop(labels = ['id.1','movie_list','O_Actual','C_Actual','E_Actual','A_Actual','N_Actual'],axis = 1,inplace = True)
completeDataset = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\inputs\IdAndMoviesv6.csv')
completeDataset.drop(labels = ['id.1','movie_list','O_Actual','C_Actual','E_Actual','A_Actual','N_Actual'],axis = 1,inplace = True)
UIDs = completeDataset["id"]
# In[8]:
def getCluster(uid):
    UidList = dataset["id"]
    dataset.drop(labels = ['id'],axis = 1,inplace = True)
    dataset.head()
    print(completeDataset)

    result = completeDataset.query('id=='+str(uid)).head()
    result.drop(labels=['id'], axis=1, inplace=True)
    print(result)
    featureList = result.iloc[0]
    print(type(featureList))
    personalityScoreArray = featureList.values
    print(personalityScoreArray)


    dataset1_standardized = dataset
    # find the appropriate cluster number
    plt.figure(figsize=(10, 8))
    from sklearn.cluster import KMeans
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        kmeans.fit(dataset1_standardized)
        wcss.append(kmeans.inertia_)
    plt.plot(range(1, 11), wcss)
    plt.title('The Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()


    dataset1 = dataset
    # Fitting K-Means to the dataset
    kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
    y_kmeans = kmeans.fit_predict(dataset1_standardized)
    #beginning of  the cluster numbering with 1 instead of 0
    y_kmeans1=y_kmeans
    y_kmeans1=y_kmeans+1
    # New Dataframe called cluster
    cluster = pd.DataFrame(y_kmeans1)
    # Adding cluster to the Dataset1
    dataset1['cluster'] = cluster
    dataset1['UID'] = UIDs
    filename = 'C:\\Users\HP ITFAC\Desktop\FYP\datasets\\UserClusters.csv'

    # Use this function to search for any files which match your filename
    files_present = glob.glob(filename)

    # if no matching files, write to csv, if there are matching files, print statement
    if not files_present:
        dataset1.to_csv(r'C:\Users\HP ITFAC\Desktop\FYP\datasets\UserClusters.csv', index=None, header=True)
    else:
        print('This file already exists!')

    #Mean of clusters
    kmeans_mean_cluster = pd.DataFrame.round(dataset1.groupby('cluster').mean(),1)
    kmeans_mean_cluster


    dataset1.head()


    print(dataset1)


    # In[17]:


    correct = 0
    X = personalityScoreArray

    predict_me = np.array(X)
    print(predict_me)
    predict_me = predict_me.reshape(-1, 5)
    prediction = kmeans.predict(predict_me)
    print(predict_me)
    clusterVal = prediction[0]+1
    return (clusterVal)




