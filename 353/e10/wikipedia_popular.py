import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


comments_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('page_name', types.StringType()),
    types.StructField('visits', types.LongType()),
    types.StructField('bytes', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    pages = spark.read.option("delimiter", " ").csv(in_directory, schema=comments_schema)
    pages.show(); return


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)