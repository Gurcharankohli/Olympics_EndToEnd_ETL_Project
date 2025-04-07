# Databricks notebook source
# MAGIC %md
# MAGIC ## Dynamic Data Reading

# COMMAND ----------

# MAGIC %md
# MAGIC ### Parameters

# COMMAND ----------

dbutils.widgets.text("source_container","")
dbutils.widgets.text("sink_container","")
dbutils.widgets.text("folder","")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fetching Parameters

# COMMAND ----------

source_container = dbutils.widgets.get("source_container")
sink_container = dbutils.widgets.get("sink_container")
folder = dbutils.widgets.get("folder")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Paramterizing Code

# COMMAND ----------

df_events = spark.read.format("parquet")\
                   .load(f"abfss://{source_container}@olympicsprojectgkdl.dfs.core.windows.net/{folder}") 

# COMMAND ----------

df_events.display()

# COMMAND ----------

df_events.write.format("delta")\
    .mode("append")\
        .option("path",f"abfss://{sink_container}@olympicsprojectgkdl.dfs.core.windows.net/{folder}")\
            .saveAsTable(f"olympics.{sink_container}.{folder}")