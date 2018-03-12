package statistics

/**
  * \* Created with IntelliJ IDEA.
  * \* User: nyh
  * \* Date: 18-3-12
  * \* Time: 下午6:04
  * \* Description: 
  * \*/
object Correlation {
  def main(args: Array[String]): Unit = {
    val sc: SparkContext = new SparkContext()
    val seriesX: RDD[Double] = ... // a series
    val seriesY: RDD[Double] = ... // must have the same number of partitions and cardinality as seriesX
    // compute the correlation using Pearson's method. Enter "spearman" for Spearman's method. If a
    // method is not specified, Pearson's method will be used by default.
    val correlation: Double = Statistics.corr(seriesX, seriesY, "pearson")
    val data: RDD[Vector] = ... // note that each Vector is a row and not a column
    // calculate the correlation matrix using Pearson's method. Use "spearman" for Spearman's method.
    // If a method is not specified, Pearson's method will be used by default.
    val correlMatrix: Matrix = Statistics.corr(data, "pearson")
  }
}
