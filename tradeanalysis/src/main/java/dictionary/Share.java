package dictionary;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by NYH on 2017/1/12.
 */
public class Share {
    private Date date;
    private double open;
    private double high;
    private double low;
    private double close;
    private int volume;
    private double account;

    public Share(Date date, double open, double high,
                 double low, double close, int volume, int account){
        this.date = date;
        this.open = open;
        this.high = high;
        this.low = low;
        this.close = close;
        this.volume = volume;
        this.account = account;
    }

    public Share(String date, String open, String high, String low, String close,
                 String volume, String account) throws ParseException {

    }

    public Share(String[] shareFutures){
        if (shareFutures.length != 7){
            System.out.println("Format share error, there is no enough parameters!");
        }
        else {
            try {
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd");
                this.date = sdf.parse(shareFutures[0]);
                this.open = Double.parseDouble(shareFutures[1]);
                this.high = Double.parseDouble(shareFutures[2]);
                this.low = Double.parseDouble(shareFutures[3]);
                this.close = Double.parseDouble(shareFutures[4]);
                this.volume = Integer.parseInt(shareFutures[5]);
                this.account = Double.parseDouble(shareFutures[6]);
            } catch (ParseException e){
                System.out.println("Cannot cast string to share future");
            }
        }
    }

    public Date getDate() {
        return date;
    }

    public double getOpen() {
        return open;
    }

    public double getHigh() {
        return high;
    }

    public double getLow() {
        return low;
    }

    public double getClose() {
        return close;
    }

    public int getVolume() {
        return volume;
    }

    public double getAccount() {
        return account;
    }
}
