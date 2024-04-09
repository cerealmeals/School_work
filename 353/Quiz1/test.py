import sys
from pyspark.sql import SparkSession, functions, types, Row
from pyspark import RDD
import re
from math import sqrt

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


def main(in_directory, out_directory):
    df = spark.read.json(in_directory)






if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
