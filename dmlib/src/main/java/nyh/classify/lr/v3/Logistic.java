/******
 * from https://blog.csdn.net/qunxingvip/article/details/51535897
 */

package nyh.classify.lr.v3;

import java.util.List;
import java.util.Random;

public class Logistic {
    //学习率
    private double rate;
    // w 权值向量
    private double[] weights;
    // w 上一次迭代值
    private double [] upWeights;
    // deltaW
    private double[] deltaWeights;
    // errSum 训练误差
    private double errSum;
    // 输入向量的维度
    private int size;
    // 迭代最大次数
    private int limit = 500 ;
    // 停止迭代阈值
    private double epsilon = 0.0001;
    // 训练集
    List<Instance> data;
    // 随机数
    Random random = new Random(201606);

    // 不同的构造器
    public Logistic(int size){
        this.rate=0.001;
        this.size = size;
        weights = new double[size+1];
        upWeights = new double[size+1];
        deltaWeights = new double[size+1];
        errSum = 0.0;
//      upWeights = weights;
        randomWeights(weights);

    }
    public Logistic(int size,double rate){
        this(size);
        this.rate = rate;
    }
    public Logistic(int size,double rate,int limit){
        this(size,rate);
        this.limit = limit;
    }
    public Logistic(int size,double rate,int limit,double epsilon){
        this(size,rate,limit);
        this.epsilon = epsilon;
    }
    public void loadData(String fileName,boolean isEnd){
        ReadData readData = new ReadData();
        data = readData.readDataSet(fileName, isEnd);
    }

    /**
     * 随机初始化权值
     * @param mat
     */
    public void randomWeights(double[] mat){
        for(int i=0;i<mat.length;i++){
            double w = random.nextDouble();
            mat[i] = w>0.5?w:(-w);
        }
    }

    /**
     * 训练模型
     * @param fileName
     * @param isEnd
     */
    public void train(String fileName,boolean isEnd,boolean isGD){
        loadData(fileName,isEnd);
        normalization();
        if(isGD)
            gradientDescent();
        else
            stocGradientDescent();
    }

    /**
     * 归一化
     */
    public void normalization(){
        double[] min = data.get(0).x;
        double[] max = data.get(1).x;
        for(int i=1;i<data.size();i++){
            Instance instance = data.get(i);
            double[] x = instance.x;
            for(int j=0;j<x.length;j++){
                if(x[j]<min[j]){
                    min[j] = x[j];
                }else if(x[j]>max[j]){
                    max[j] = x[j];
                }
            }
        }

        for(int i=0;i<data.size();i++){
            Instance instance = data.get(i);
            double label = instance.label;
            double[] x = instance.x;
            for(int j=0;j<x.length;j++){
                if(max[j] == min[j])
                    continue;
                x[j] = (x[j] - min[j])/(max[j] - min[j]);
            }
            data.set(i, new Instance(label,x));
        }
    }

    /**
     * 预测 返回预测标签
     * @param x
     * @return
     */
    public int predict(double[] x){
        double wtx = wTx(x);
        double logit = sigmoid(wtx);
        if(logit>0.5)
            return 1;
        else
            return 0;
    }

    /**
     * 返回预测精度
     * @param testData
     * @return
     */
    public double accuracyRate(List<Instance> testData){
        int count = 0;
        for(int i=0;i<testData.size();i++){
            Instance instance = testData.get(i);
            double[] x = instance.x;
            double label = instance.label;
            int pred=predict(x);
            if(label == pred)
                count++;
        }
        return count*1.0/testData.size();
    }

    /**
     * 返回权值
     * @return
     */
    public double[] getWeights(){
        return weights;
    }

    /**
     * sigmoid 函数
     * @param z
     * @return
     */
    public double sigmoid(double z){
//      if(z>10)
//          return 1.0;
//      if(z<-10)
//          return 0.0;
        return 1.0/(1+Math.pow(Math.E,-z));
    }

    public double wTx(double[] x){
        double wtx = 0.0;
        for(int i=0;i<weights.length;i++){
            wtx += weights[i] * x[i];
        }
        return wtx;
    }

    /**
     * 批量梯度下降法 计算训练误差
     */
    public void calculateErrSum(){
        errSum = 0.0;
        for(int i=0;i<data.size();i++){
            Instance instance = data.get(i);
            double label = instance.label;
            double[] x = instance.x;
            double wtx = wTx(x);
            double logit = sigmoid(wtx);
            errSum += (label - logit);
        }

    }
    /**
     * 随机梯度下降法 计算训练误差
     */
    public void calculateErrSum(int id){
        errSum = 0.0;
        Instance instance = data.get(id);
        double real = instance.label;
        double[] x = instance.x;
        double wtx = wTx(x);
        double predict = sigmoid(wtx);
        errSum = (real - predict);
    }

    /**
     * 批量梯度下降法更新 deltaW
     */
    public void calculateDeltaWeights(){
        int m = data.size();
        for(int i=0;i<deltaWeights.length;i++){
            deltaWeights[i] = 0.0;
            for(int j=0;j<data.size();j++){
                Instance instance = data.get(j);
                double[] x = instance.x;
                deltaWeights[i] += x[i];
            }
            deltaWeights[i] = deltaWeights[i] * errSum/m;
        }
    }
    /**
     * 随机梯度下降法
     */
    public void stocCalculateDeltaWeights(){
        int m = data.size();
        for(int i=0;i<deltaWeights.length;i++){
            deltaWeights[i] = 0.0;
            for(int j=0;j<data.size();j++){
                Instance instance = data.get(j);
                double[] x = instance.x;
                deltaWeights[i] += x[i];
            }
            deltaWeights[i] = deltaWeights[i] * errSum;
        }
    }

    /**
     * 更新weights
     */
    public void updateWeights(){
        upWeights = weights;
        for(int i=0;i<weights.length;i++){
            weights[i] = weights[i] + rate*deltaWeights[i];
        }
    }

    /**
     * errSum，很小的时候停止迭代
     * @return
     */
    public boolean judge(){
        return Math.abs(errSum)<epsilon;
    }

    /**
     * 批量梯度下降法
     */
    public void gradientDescent(){
        for(int i=0;i<limit;i++){
            calculateErrSum();
            System.out.println("errSum:"+errSum);
            calculateDeltaWeights();
            updateWeights();
            if(i==limit*0.9){
                System.out.println("到达最大迭代次数的90%");
            }
            if(i==limit-1){
                System.out.println("到达最大迭代次数");
            }
//          printArray(weights);
//          printArray(upWeights);
            if(judge()){
                break;
            }
        }
    }
    /**
     * 随机梯度下降法
     *
     * @param 
     * @return
     */
    public void stocGradientDescent(){
        int nextId = random.nextInt(data.size());
        for(int i=0;i<limit;i++){
            nextId = random.nextInt(data.size());
            calculateErrSum(nextId);
            System.out.println("errSum:"+errSum);
            stocCalculateDeltaWeights();
            if(i==limit*0.9){
                System.out.println("到达最大迭代次数的90%");
            }
            if(i==limit-1){
                System.out.println("到达最大迭代次数");
            }
//          printArray(weights);
//          printArray(upWeights);
            if(judge()){
                break;
            }
        }
    }
}
