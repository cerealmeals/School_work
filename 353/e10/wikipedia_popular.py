import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


comments_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('visits', types.LongType()),
    types.StructField('bytes', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])

def filename_to_date_hour(string):
    output = string[-18:-7]
    #output = output[:len(output)-4]
    return output


def main(in_directory, out_directory):
    pages = spark.read.option("delimiter", " ").csv(in_directory, schema=comments_schema).withColumn('filename', functions.input_file_name())

    pages = pages.where(pages.language == 'en')
    pages = pages.where(pages.title != 'Main_Page')
    Specials = pages.where((pages.title.startswith('Special:')))

    pages = pages.subtract(Specials)
    
    file_to_date = functions.udf(filename_to_date_hour, returnType=types.StringType())

    pages = pages.withColumn('filename', file_to_date(pages.filename))
    pages = pages.drop('bytes').drop('language')

    groups = pages.groupby('filename').max('visits')
    groups 

    groups.write.csv(out_directory, mode='overwrite')
    groups.show(); return




if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)