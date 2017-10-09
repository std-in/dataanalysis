package nyh.optimization;

/**
 * Created by NYH on 2017/5/19.
 */
public class BatchGradient {
    public void batchGradientDescent() {
        double inputDataMatrix[][] = {{1, 4, 2}, {2, 5, 2}, {5, 5, 1}, {4, 4, 2}}; // X输入
        double expectResult[] = {19, 26, 19, 20}; // 期望输出值
        double w[] = {0, 0, 0}; // 权重参数 因为这里只涉及到两个变量 ，即X为两列输入
        double learningRate = 0.01;
        double loss = 100; // 损失值
        for (int i = 0; i < 100 && loss > 0.0001; i++) {
            double err_sum = 0;
            for (int j = 0; j < 4; j++) {
                double h = 0;
                for (int k = 0; k < 3; k++) {
                    h = h + inputDataMatrix[j][k] * w[k];
                }
                err_sum = expectResult[j] - h;
                for (int k = 0; k < 2; k++) {
                    w[k] = w[k] + learningRate * err_sum * inputDataMatrix[j][k]; // 权值每次改变的幅度，这个公式是通过梯度下降得到的
                }
            }
            System.out.println("此时的w权值为：" + "w0:" + w[0] + "---" + "w1:" + w[1]);
            double loss_sum = 0;
            for (int j = 0; j < 4; j++) {
                double sum = 0;
                for (int k = 0; k < 3; k++) {
                    sum = sum + inputDataMatrix[j][k] * w[k];
                }
                loss_sum += (expectResult[j] - sum) * (expectResult[j] - sum);
            }
            System.out.println("loss:" + loss_sum);
        }
    }

    public static void main(String[] args) {
        BatchGradient bg = new BatchGradient();
        bg.batchGradientDescent();
    }
}
