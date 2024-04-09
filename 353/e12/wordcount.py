import string, re
import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation




def main(in_directory, out_directory):
    df = spark.read.text(in_directory)
    df = df.select(functions.split(df.value, wordbreak, -1).alias('word'))
    df = df.select(functions.explode(df.word).alias('word'))
    df = df.select(functions.lower(df.word).alias('word'))
    df = df.groupby(df.word).count()
    df = df.orderBy(['count', 'word'], ascending=False)
    df = df.where(df.word != '')
    df.show()

    df.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)