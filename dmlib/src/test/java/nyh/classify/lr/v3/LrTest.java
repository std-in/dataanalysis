package nyh.classify.lr.v3;

import java.util.List;

public class LrTest {

    /**
     * @param args
     */
    public static void main(String[] args) {
        // TODO Auto-generated method stub
//      String fileName = "logisticaps.csv";
//      boolean isEnd = true;
//      int size = 12;
        String fileName = "logistic1.csv";
        boolean isEnd = true;
        int size = 2;
//      String fileName = "binary.csv"; logisticaps
//      boolean isEnd = false;
//      int size = 3;
        double rate = 0.001;
        int limit = 9000;
        boolean isGD = true;
        Logistic logistic = new Logistic(size,rate,limit);
        logistic.train(fileName, isEnd,isGD);
        ReadData readData = new ReadData();
        List<Instance> data = readData.readDataSet(fileName, isEnd);
        double acc = logistic.accuracyRate(data);
        System.out.println("正确率："+acc);
        double w[] = logistic.getWeights();
        for(int i=0;i<w.length;i++){
            System.out.println(w[i]+"\t");
        }
    }

}
