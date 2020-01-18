# https://medium.com/@patelneha1495/recommendation-system-in-python-using-als-algorithm-and-apache-spark-27aca08eaab3
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.sql.types import DecimalType
from pyspark.sql.types import DoubleType

# from pyspark.sql.functions import col


spark = SparkSession.builder.appName('Recommendation_system').getOrCreate()

df = spark.read.csv("D:\\final year project\Datasets\\UserMovies.csv")
df = df.withColumnRenamed("_c0", "AUTHID").withColumnRenamed("_c1", "UID").withColumnRenamed("_c2",
                                                                                             "MID").withColumnRenamed(
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

user_recs = model.recommendForAllUsers(20).show(10)
