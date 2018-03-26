import org.apache.spark.mllib.linalg.{Vector, Vectors, Matrix}
import org.apache.spark.mllib.stat.Statistics
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession

/**
  * \* Created with IntelliJ IDEA.
  * \* User: nyh
  * \* Date: 18-3-13
  * \* Time: 下午12:42
  * \* Description:
  * \*/
object Correlation {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder
      .appName("CorrelationExample")
      .master("local[2]")
      .getOrCreate()
    import spark.implicits._

    val test1 = Seq(1.0, 2.0, 3.0, 4.0)
    val test2 = Seq(5.0, 10.0, 15.0, 21.0)

    val seriesX: RDD[Double] = spark.sparkContext.parallelize(test1)
    // must have the same number of partitions and cardinality as seriesX
    val seriesY: RDD[Double] = spark.sparkContext.parallelize(test2)
//    compute the correlation using Pearson's method. Enter "spearman" for Spearman's method. If a
//      method is not specified, Pearson's method will be used by default.
    val correlation: Double = Statistics.corr(seriesX, seriesY, "pearson")
    print(correlation)

    // note that each Vector is a row and not a column
    val test3 = Seq(Vectors.dense(1, 2, 3, 4), Vectors.dense(5, 10, 15, 20), Vectors.dense(100, 75, 50, 25))
    val data: RDD[Vector] = spark.sparkContext.parallelize(test3)
    // calculate the correlation matrix using Pearson's method. Use "spearman" for Spearman's method.
    // If a method is not specified, Pearson's method will be used by default.
    val correlMatrix: Matrix = Statistics.corr(data, "pearson")
    print(correlMatrix)
  }
}
