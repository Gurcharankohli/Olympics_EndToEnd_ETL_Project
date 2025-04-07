# Databricks notebook source
# MAGIC %md
# MAGIC ## Silver Notebook

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading NOCS Data

# COMMAND ----------

df = spark.read.format("csv")\
           .option("header","True")\
               .option("inferSchema","True")\
                   .load("abfss://bronze@olympicsprojectgkdl.dfs.core.windows.net/nocs") 

# COMMAND ----------

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **Dropping the column**

# COMMAND ----------

df=df.drop('country')

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df = df.withColumn('tag',split(col('tag'),'-')[0])

# COMMAND ----------

df.write.format("delta")\
        .mode("append")\
            .option("path","abfss://silver@olympicsprojectgkdl.dfs.core.windows.net/nocs")\
            .saveAsTable("olympics.silver.nocs")

# COMMAND ----------

