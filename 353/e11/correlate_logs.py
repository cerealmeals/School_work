import sys
from pyspark.sql import SparkSession, functions, types, Row
from pyspark import RDD
import re
from math import sqrt

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        
        return Row(hostname=m[1], bytes=int(m[2]))
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)

    return log_lines.map(line_to_row).filter(not_none)
    # TODO: return an RDD of Row() objects


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    logs.cache()

    count = logs.groupby('hostname').count().withColumnRenamed('count', 'x')
    sums = logs.groupby('hostname').sum('bytes').withColumnRenamed('sum(bytes)', 'y')

    to_calculate = count.join(sums, on='hostname')
    to_calculate = to_calculate.withColumn('x2', (to_calculate['x'] * to_calculate['x']))
    to_calculate = to_calculate.withColumn('y2', to_calculate['y'] * to_calculate['y'])
    to_calculate = to_calculate.withColumn('xy', to_calculate['y'] * to_calculate['x'])
    
    to_calculate.cache()

    n = to_calculate.count()

    all_sums = to_calculate.groupby().sum().first()

    sum_x = all_sums[0]
    sum_y = all_sums[1]
    sum_x2 = all_sums[2]
    sum_y2 = all_sums[3]
    sum_xy = all_sums[4]
    

    # to_calculate.show(); return
    # TODO: calculate r.
    # print(to_calculate.corr('x','y'))

    r = (n*sum_xy - sum_x*sum_y)/(sqrt(n*sum_x2 - sum_x**2)*sqrt(n*sum_y2-sum_y**2))
    


    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
