package nyh.classify.lr.v3;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ReadData {
    public List<Instance> readDataSet(String fileName,boolean isEnd){

        List<Instance> data = new ArrayList<Instance>();
        FileReader fileReader = null;
        try {
            fileReader = new FileReader(fileName);
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        BufferedReader br = new BufferedReader(fileReader);
        String row = new String();

        try {
            while((row=br.readLine())!=null){
                String[] A = row.split(",");
                double[] x = getDoubleArray(A,isEnd);
                double label = 0;
                if(isEnd)
                    label = Double.parseDouble(A[A.length-1]);
                else
                    label =  Double.parseDouble(A[0]);
                data.add(new Instance(label,x));
            }
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return data;
    }
    public double[] getDoubleArray(String[] A,boolean isEnd){
        double[] X = new double[A.length];
        // label 在第一个位置
        int i = 1;
        int limit = A.length;
        // label 在最后一个位置
        if(isEnd){
            i=0;
            limit = A.length-1;
        }
        int j = 1;
        X[0] = 1.0;// 第一维是偏置，所有x的第一维是 1
        for(int k=i;k<limit;k++){
            X[j++] = Double.parseDouble(A[k]);
        }
        return X;
    }
}
