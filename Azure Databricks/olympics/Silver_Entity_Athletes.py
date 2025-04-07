# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df = spark.read.format("parquet")\
    .load("abfss://bronze@olympicsprojectgkdl.dfs.core.windows.net/athletes")

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.fillna({"birth_place":"xyz", "birth_country":"abc","residence_place":"unknown","residence_country":"aaa"})

# COMMAND ----------

display(df)

# COMMAND ----------

df_filtered = df.filter((col('current')==True) & (col('name').isin('GALSTYAN Slavik','HARUTYUNYAN Arsen','SEHEN Sajjad')))

# COMMAND ----------

display(df_filtered)

# COMMAND ----------

df = df.withColumn('height',col('height').cast(FloatType()))\
    .withColumn('weight',col('weight').cast(FloatType()))

display(df)

# COMMAND ----------

df_sorted = df.sort('height','weight',ascending=[0,1]).filter(col('weight')>0)
df_sorted.display()

# COMMAND ----------

df_sorted = df_sorted.withColumn('nationality',regexp_replace('nationality','United States','US'))

display(df_sorted)

# COMMAND ----------

df.groupBy('code').agg(count('code').alias('total_count')).filter(col('total_count')>1).display()

# COMMAND ----------

df_sorted = df_sorted.withColumnRenamed('code', 'athlete_id')
df_sorted.display()

# COMMAND ----------

df_sorted = df_sorted.withColumn('occupation', split('occupation',','))
display(df_sorted)

# COMMAND ----------

df_sorted.columns

# COMMAND ----------

df_final = df_sorted.select('athlete_id',
 'current',
 'name',
 'name_short',
 'name_tv',
 'gender',
 'function',
 'country_code',
 'country',
 'country_long',
 'nationality',
 'nationality_long',
 'nationality_code',
 'height',
 'weight')

# COMMAND ----------

display(df_final)

# COMMAND ----------

df_final.write.format("delta")\
    .mode("append")\
        .option("path","abfss://silver@olympicsprojectgkdl.dfs.core.windows.net/athletes")\
            .saveAsTable("olympics.silver.athletes")

# COMMAND ----------

