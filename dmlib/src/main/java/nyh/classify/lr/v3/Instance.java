package nyh.classify.lr.v3;

public class Instance {
    public int label;
    public double[] x;
    public Instance(){}
    public Instance(int label,double[] x){
        this.label = label;
        this.x = x;
    }
}
