package nyh.classify.lr.v3;

public class Instance {
    public double label;
    public double[] x;
    public Instance(){}
    public Instance(double label,double[] x){
        this.label = label;
        this.x = x;
    }
}
