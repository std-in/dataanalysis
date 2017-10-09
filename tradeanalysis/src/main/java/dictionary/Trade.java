package dictionary;

import java.util.Date;

/**
 * Created by NYH on 2017/1/14.
 */
public class Trade {
    private String accountName;
    private Date tradeDay;
    private int tradeNum;
    private boolean buy;
    private double tradePrice;

    public Trade(String accountName){
        this.accountName = accountName;
    }

    public void setBuyTrade(int shareNum, Date buyDay, double price){
        this.tradeNum = shareNum;
        this.tradePrice = price;
        this.tradeDay = buyDay;
        this.buy = true;
    }

    public void setSaleTrade(int shareNum, Date saleDay, double price){
        this.tradeDay = saleDay;
        this.tradePrice = price;
        this.tradeNum = shareNum;
        this.buy = false;
    }

    public Date getTradeDay() {
        return tradeDay;
    }

    public int getTradeNum() {
        return tradeNum;
    }

    public boolean isBuy() {
        return buy;
    }

    public double getTradePrice() {
        return tradePrice;
    }
}
