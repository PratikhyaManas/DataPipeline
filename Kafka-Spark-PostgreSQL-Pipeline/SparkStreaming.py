from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Spark Stream").master("local[*]").getOrCreate()

kafka_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers","localhost:9092").option("subscribe", "RpiValueKafka").load()
kafka_df_1 = kafka_df.selectExpr("CAST(value AS STRING)")

kafka_df_2 = kafka_df_1.withColumn("body", regexp_replace(kafka_df_1.value, "\"", ""))
kafka_df_3 = kafka_df_2.withColumn("body_1", split(kafka_df_2.body, ","))
kafka_df_4 =kafka_df_3.withColumn("Timestamp", col("body_1").getItem(0)).withColumn("Device_Name", col("body_1").getItem(1)).withColumn("Temperature", col("body_1").getItem(2).cast("Double")).withColumn("Humidity", col("body_1").getItem(3).cast("Double")).withColumn("Pressure", col("body_1").getItem(4).cast("Double")).withColumn("WaterLevel", col("body_1").getItem(5).cast("Double")).drop("body_1", "body","value")

kafka_df_4.printSchema()

df_window = kafka_df_4.groupBy(window(kafka_df_4.Timestamp, "5 seconds"),"Device_Name").mean().orderBy("window")
df_window.printSchema()


df_window_1 = df_window.select(col("window.start").alias("StartTime"),col("window.end").alias("EndTime"), "Device_Name",col("avg(Temperature)").alias("Avg_Temperature"),col("avg(Humidity)").alias("Avg_Humidity"),col("avg(Pressure)").alias("Avg_Pressure"),col("avg(WaterLevel)").alias("Avg_WaterLevel"))

df_window_1.printSchema()

df_window_1.writeStream.format("console").outputMode("complete").option("truncate","false").start()

import psycopg2
class AggInsertPostgres:
    def process(self, row):
        StartTime = str(row.StartTime)
        EndTime = str(row.EndTime)
        Device_Name = row.Device_Name
        Temperature = row.Avg_Temperature
        Humidity = row.Avg_Humidity
        Pressure = row.Avg_Pressure
        WaterLevel = row.Avg_WaterLevel
        try:
            connection = psycopg2.connect(user="postgres",
            password="postgres",
            host="192.168.99.100",
            port="5432",
            database="Spark Database")
            cursor = connection.cursor()
            sql_insert_query = """ INSERT INTO agg_rpy (StartTime, EndTime, Device_Name,Avg_Temperature, Avg_Humidity, Avg_Pressure, Avg_WaterLevel)VALUES ('%s', '%s', '%s', %d, %d, %d, %d) """ % (StartTime, EndTime,Device_Name, Temperature, Humidity,Pressure, WaterLevel)
            print("\n sql_insert_query",sql_insert_query)
            result = cursor.execute(sql_insert_query)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into agg_rpy table")

            except(Exception, psycopg2.Error) as error:\
                print("Failed inserting record into table {}".format(error))
            finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

df_window_1.writeStream.format("console").outputMode("complete").option("truncate","false").start()

df_window_1.writeStream.outputMode("complete").foreach(AggInsertPostgres()).start()

kafka_df_4.writeStream.format("console").outputMode("update").option("truncate","false").start().awaitTermination()



