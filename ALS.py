################################ This is not working
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder
from pyspark.sql.types import DecimalType

sc = SparkContext(master="local", appName="test")
sqlContext = SQLContext(sc)
print(sqlContext)

sc.setCheckpointDir('checkpoint')


df = sqlContext.read.csv("D:\\final year project\Datasets\\UserMovies.csv")
df2 = df.withColumnRenamed("_c0" ,"AUTHID").withColumnRenamed("_c1" ,"UID").withColumnRenamed("_c2"
                                                                                              ,"MID").withColumnRenamed \
    ("_c3" ,"Watched")
df2.printSchema()

df2 = df2.withColumn("UID" ,df2["UID"].cast(DecimalType()))
df2 = df2.withColumn("MID" ,df2["MID"].cast(DecimalType()))
df2 = df2.withColumn("Watched" ,df2["Watched"].cast(DecimalType()))


df2.printSchema()
df2.show()

# Create test and train
(training, test) = df2.randomSplit([0.2 ,0.8])
print(test.count())
print(training.count())

# Create ALS Model
als = ALS(userCol="UID", itemCol="MID", ratingCol="Watched", coldStartStrategy="drop", nonnegative= True)

# tune model using paramGridBuilder
param_grid = ParamGridBuilder()\
            .addGrid(als.rank, [12 ,13 ,14])\
            .addGrid(als.maxIter, [18 ,19 ,20])\
            .addGrid(als.regParam, [.17 ,.18, .19])\
            .build()

# Define evaluator as RMSE
evaluater = RegressionEvaluator(metricName="rmse", labelCol="Watched", predictionCol="prediction")

# build cross validation using TrainValidationSplit

tvs = TrainValidationSplit(
    estimator= als,
    estimatorParamMaps= param_grid,
    evaluator= evaluater
)
print("task 1 done")

# fit ALS model to training data
model = tvs.fit(training)
print("task 2 done")

# extract best model from the tuning exerecise using ParamGridBuilder
best_model = model.bestModel

# generate predictions and eevaluate using RMSE
predictions = best_model.transform(test)
rmse = evaluater.evaluate(predictions)

# evaluation metrics and model parameters
print("RMSE " +str(rmse))
print("Best Model")
print("Rank :"), best_model.rank
print("MaxIter: "), best_model._java_obj.parent().getMaxIter()
print("Regparam: "), best_model._java_obj.parent().getRegParam()


print(predictions.sort("UID", "Watched"))
