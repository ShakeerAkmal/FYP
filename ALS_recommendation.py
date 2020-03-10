from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.sql.types import DecimalType
from pyspark.sql.types import DoubleType
import pandas as pd

# from pyspark.sql.functions import col


spark = SparkSession.builder.appName('Recommendation_system').getOrCreate()

df = spark.read.csv("C:\\Users\HP ITFAC\\Desktop\\FYP\\datasets\\MovieManytoMany_dataframe.csv")
df = df.withColumnRenamed("_c0", "UID").withColumnRenamed("_c1", "MID").withColumnRenamed("_c2",
                                                                                             "score").withColumnRenamed(
    "_c3", "score")
# df.show(100,truncate=True)

nd = df.select(df['UID'], df['MID'], df['score'])

nd.show()
# data frame is ok now
# transform the dataset to int values
indexer = [StringIndexer(inputCol=column, outputCol=column + "_index") for column in
           list(set(nd.columns) - set(['score']))]
pipeline = Pipeline(stages=indexer)
transformed = pipeline.fit(nd).transform(nd)

changedTypedf = transformed.withColumn("score", transformed["score"].cast(DoubleType()))
transformed = changedTypedf
transformed.printSchema()
transformed.show()
trans = transformed.toPandas()

# split traing and test dataset
(training, test) = transformed.randomSplit([0.8, 0.2])

# fit dataset to als
als = ALS(maxIter=5, regParam=0.09, rank=25, userCol="UID_index", itemCol="MID_index", ratingCol="score",
          coldStartStrategy="drop", nonnegative=True)
model = als.fit(training)

# evaluate model
evaluator = RegressionEvaluator(metricName="rmse", labelCol="score", predictionCol="prediction")
predictions = model.transform(test)
rmse = evaluator.evaluate(predictions)
print("RMSE=" + str(rmse))
predictions.show()

#user_recs = model.recommendForAllUsers(50).show(10)

dataset = model.recommendForAllUsers(50).toPandas()
dataset1 = predictions.toPandas()


dataset1.query('UID==1413737972090633.0').head()
result = pd.merge( dataset, dataset1, left_on='UID_index', right_on='UID_index')
result.query('UID==1413737972090633.0').head()
recos = result['recommendations'].iloc[0]
reco = str(recos)
MID_indexList = []
ratingList = []
aa = reco.replace('[', '')
moviestr3 = aa.replace("]", "")
moviestr0 = moviestr3.replace("(", "")
moviestr2 = moviestr0.replace("rating=", "")
moviestr1 = moviestr2.replace("RowMID_index=", "")
moviestr = moviestr1.split('),')
# print(moviestr)
for i in moviestr:
    # print(i)
    rates = i.replace(")", "")
    score = rates.split(',')
    MID_indexList.append(score[0])
    ratingList.append(score[1])


data = {'MID_index': [], "rating": []}
recoDF = pd.DataFrame(data)
recoDF["MID_index"] = MID_indexList
recoDF["rating"] = ratingList

recoDF["MID_index"] = pd.to_numeric(recoDF["MID_index"])
recoDF["rating"] = pd.to_numeric(recoDF["rating"])

tran = trans[['MID_index','MID']]
Finalresult = pd.merge( recoDF, trans, left_on='MID_index', right_on='MID_index')
Finalresult = Finalresult[['MID_index','rating']]
Finalresult.drop_duplicates(keep=False,inplace=True)

print("*******************************************************************************************")
print(Finalresult)






