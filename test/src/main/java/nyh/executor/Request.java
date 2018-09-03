package nyh.executor;

public class Request {
    private String id;
    private double value;

    public Request(String id, double value) {
        this.id = id;
        this.value = value;
    }
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }
}
