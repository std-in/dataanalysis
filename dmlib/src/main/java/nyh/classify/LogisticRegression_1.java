package nyh.classify;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by NYH on 2017/5/19.
 */
public class LogisticRegression_1 {
    float[] Tag;
    float[][] Var;
    float[] beta;


    public LogisticRegression_1() throws IOException {//函数作用：初始化，把文件的数据读入程序中
        BufferedReader br = new BufferedReader(new FileReader("dmlib/data/iris.index"));
        String line = "";
        List<String> Var = new ArrayList<String>();
        List<String> Tag = new ArrayList<String>();
        while ((line = br.readLine()) != null) {
            String[] content = line.split(",");
            String tmp = "";
            for (int i = 0; i < content.length - 1; i++) {
                tmp = tmp + " " + content[i];
            }
            Var.add(tmp.trim());
            Tag.add(content[content.length - 1]);
        }
        this.Tag = new float[Tag.size()];
        this.Var = new float[Var.size()][Var.get(0).split(" ").length + 1];
        for (int i = 0; i < Tag.size(); i++) {
            this.Var[i][0] = 1.0f;
            this.Var[i][1] = Float.parseFloat(Var.get(i).split(" ")[0]);
            this.Var[i][2] = Float.parseFloat(Var.get(i).split(" ")[1]);
            this.Var[i][3] = Float.parseFloat(Var.get(i).split(" ")[2]);
            this.Var[i][4] = Float.parseFloat(Var.get(i).split(" ")[3]);
            this.Tag[i] = Float.parseFloat(Tag.get(i));
        }
    }

    public float sum_exp(float x_i[], float beta[]) {//函数作用：求exp(x[0]*beta[0]+...+x[j]*beta[j])其中x[0]=1
        float tmp = 0;
        for (int j = 0; j < x_i.length; j++) {
            tmp = tmp + x_i[j] * beta[j];

        }
        return (float) Math.exp(tmp);
    }

    public float Logistic_D(float x[][], float y[], float beta[], int j) {//函数作用：求最大似然函数对数的偏导数值
        float tmp = 0;
        for (int i = 0; i < x.length; i++) {
            tmp = x[i][j] * sum_exp(x[i], beta) / (1 + sum_exp(x[i], beta)) - y[i] * x[i][j];
        }
        return tmp;
    }

    public float Logistic_D_norm(float x[][], float y[], float beta[]) {//函数作用：求偏导数值的二范数值
        float tmp = 0;
        for (int j = 0; j < beta.length; j++) {
            tmp = tmp + Logistic_D(x, y, beta, j) * Logistic_D(x, y, beta, j);
        }
        return (float) Math.sqrt(tmp);
    }

    //函数作用：梯度下降法求解最大似然函数的最小值点
    public void Logistic_main(float x[][], float y[], float beta[], float a) {
        float error_sum = Logistic_D_norm(x, y, beta);
        System.out.println("error_sum: " + error_sum);
//        if (error_sum <= 0.01) {
        if (error_sum <= 8.7) {
            this.beta = beta;
            return;
        }
        float[] beta_tmp = beta;
        for (int j = 0; j < beta.length; j++) {
            beta_tmp[j] = beta[j] - Logistic_D(x, y, beta, j) * a;
        }
        beta = beta_tmp;
        Logistic_main(x, y, beta, a);
    }

    public void Logistic_predict(float x[][], float y[], float beta[]) {//函数作用输出真实值与逻辑斯蒂回归预测值
        float[] y_predict = new float[y.length];
        for (int i = 0; i < y.length; i++) {
            y_predict[i] = sum_exp(x[i], this.beta) / (1 + sum_exp(x[i], this.beta));
            System.out.println("Actual:" + Tag[i] + "    Predict:" + y_predict[i]);
        }
        return;
    }

    public static void main(String[] args) throws IOException {
        LogisticRegression_1 a = new LogisticRegression_1();
        float[] beta = a.Var[0];
        for (int i = 0; i < beta.length; i++) {
            beta[i] = 0.0f;
        }
        a.Logistic_main(a.Var, a.Tag, beta, (float) 0.01);
        a.Logistic_predict(a.Var, a.Tag, a.beta);
    }
}
