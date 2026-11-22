from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import functions as F

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

spark.conf.set("spark.sql.catalog.lakehouse", "org.apache.iceberg.spark.SparkCatalog")
spark.conf.set("spark.sql.catalog.lakehouse.type", "hadoop")
spark.conf.set("spark.sql.catalog.lakehouse.warehouse", "s3a://ucv-data-platform/products")

hconf = sc._jsc.hadoopConfiguration()
hconf.set("fs.s3a.endpoint", "http://floci:4566")
hconf.set("fs.s3a.path.style.access", "true")
hconf.set("fs.s3a.connection.ssl.enabled", "false")
hconf.set("fs.s3a.access.key", "test")
hconf.set("fs.s3a.secret.key", "test")
hconf.set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")

df = spark.table("lakehouse.silver.products")

print("VALIDACION DE PRODUCTOS")
df.agg(
    F.count("*").alias("total_productos"),
    F.sum(F.when(F.col("product_id").isNull(), 1).otherwise(0)).alias("product_id_nulos"),
    F.sum(F.when(F.col("price").isNull() | (F.col("price") <= 0), 1).otherwise(0)).alias("precios_invalidos")
).show()

print("VALIDACION DE DUPLICADOS")
duplicados = df.groupBy("product_id").count().filter(F.col("count") > 1)

print("Cantidad de product_id duplicados:", duplicados.count())
duplicados.show(truncate=False)
print("LECTURA DE TABLAS ICEBERG")

silver = spark.table("lakehouse.silver.products")
gold = spark.table("lakehouse.gold.product_category_summary")

print("Registros Silver:", silver.count())
silver.show(5, truncate=False)

print("Registros Gold:", gold.count())
gold.show(5, truncate=False)
spark.stop()
