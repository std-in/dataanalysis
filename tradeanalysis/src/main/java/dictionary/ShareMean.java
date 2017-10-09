package dictionary;

import java.util.Date;

/**
 * Created by NYH on 2017/1/13.
 */
public class ShareMean {
    private Date date;
    private double value;

    public ShareMean(Date date, double value){
        this.date = date;
        this.value = value;
    }

    public Date getDate() {
        return date;
    }

    public double getValue() {
        return value;
    }
}
