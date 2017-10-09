package decision;

import dictionary.Account;
import dictionary.Share;
import dictionary.ShareMean;
import dictionary.Trade;

import java.text.ParseException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Random;

/**
 * Created by NYH on 2017/1/13.
 * use close avg as future
 */
public class MeanAnalysis {
    // compute mean by num days
    private Date beginDay;
    private Date endDay;
    // analys period days
    private int period;
    private Share[] shares ;
    private ShareMean[] share5Means;
    private ShareMean[] share10Means;
    private ShareMean[] share30Means;
    private ShareMean[] share60Means;
    private Account shareMeanAccount;
    private Account twoMeanAccount;
    private Account share2MeanAccount;
    private List<Trade> trades = new ArrayList<Trade>();

    public MeanAnalysis(Share[] data,int period, Account account)
    throws ParseException, CloneNotSupportedException{
        this.period = period;
        this.shareMeanAccount = account.clone();
        this.twoMeanAccount = account.clone();
        this.share2MeanAccount = account.clone();
        int beginIndex = new Random().nextInt(data.length);
        System.out.println("The begin index = " + beginIndex);
        int endIndex = (beginIndex + period) >= data.length? (data.length -1) : (beginIndex + period);
        this.period = endIndex - beginIndex;
        this.beginDay = data[beginIndex].getDate();
        this.endDay = data[endIndex].getDate();
        this.shares = new Share[this.period];
        for (int i = beginIndex; i< endIndex; i ++){
            this.shares[i - beginIndex ] = data[i];
        }
        this.share5Means = setMean(5);
        this.share10Means = setMean(10);
        this.share30Means = setMean(5);
        this.share60Means = setMean(5);
    }

    public ShareMean[] setMean(int days){
        ShareMean[] shareMeans = new ShareMean[this.period];
        for(int i = 0; i <shares.length;i ++){
            double sumClose = 0.0;
            Share iShare = shares[i];
            if (i < days){
                for (int j = 0; j <= i; j ++){
                    sumClose += shares[j].getClose();
                }
            }
            else {
                for(int j = 0; j < days; j ++){
                    sumClose += shares[i - j].getClose();
                }
            }
            double meanClose = sumClose / days;
            shareMeans[i] = new ShareMean(shares[i].getDate(), meanClose);
        }
        return shareMeans;
    }
    // use share close and share 5mean compute the income
    public void setShareMeanIncome(ShareMean[] shareMeans){
        if (shares.length != shareMeans.length){
            System.out.println("meanShare length is not equals to shares");
            System.exit(0);
        }

        for(int i = 0; i < (this.period - 1); i ++){
            // if share price is below mean, sale
            if((shareMeanAccount.isKeep() && (shares[i].getClose() < shareMeans[i].getValue())) ||
                    (!shareMeanAccount.isKeep() && (shares[i].getClose() >= shareMeans[i].getValue()))){
                Trade trade = new Trade("SM");
                trades.add(trade);
                // sale
                if(shareMeanAccount.isKeep() && (shares[i].getClose() < shareMeans[i].getValue())){
                    trade.setSaleTrade(shareMeanAccount.getShareNum(), shares[i + 1].getDate(), shares[i + 1].getClose());
                    shareMeanAccount.setBalance(shareMeanAccount.getBalance() + shares[i + 1].getClose() * shareMeanAccount.getShareNum());
                    shareMeanAccount.setShareNum(0);
                    shareMeanAccount.setKeep(false);
                }
                // buy
                if(!shareMeanAccount.isKeep() && (shares[i].getClose() >= shareMeans[i].getValue())){
                    shareMeanAccount.setShareNum((int)Math.floor(shareMeanAccount.getBalance() / shares[i + 1].getClose()));
                    trade.setBuyTrade(shareMeanAccount.getShareNum(), shares[i + 1].getDate(), shares[i + 1].getClose());
                    shareMeanAccount.setBalance(shareMeanAccount.getBalance() - shares[i + 1].getClose() * shareMeanAccount.getShareNum());
                    shareMeanAccount.setKeep(true);
                }
            }
        }
        // if the account was keep at the last, the sals it as last day's high
        if (shareMeanAccount.isKeep()){
            Trade trade = new Trade("SM");
            trades.add(trade);
            trade.setSaleTrade(shareMeanAccount.getShareNum(),
                    shares[this.period - 1].getDate(), shares[this.period - 1].getClose());
            shareMeanAccount.setBalance(shareMeanAccount.getBalance() + shares[this.period - 1].getClose() * shareMeanAccount.getShareNum());
            shareMeanAccount.setShareNum(0);
            shareMeanAccount.setKeep(false);
        }
    }

    // use share close and share 5mean compute the income
    public void set2MeanIncome(ShareMean[] shareMeans1, ShareMean[] shareMeans2){
        if (shareMeans1.length != shareMeans2.length){
            System.out.println("The two meanShares length must have same length");
            System.exit(0);
        }

        for(int i = 0; i < (this.period - 1); i ++){
            // if share price is below mean, sale
            if((twoMeanAccount.isKeep() && (shareMeans1[i].getValue() < shareMeans2[i].getValue())) ||
                    (!twoMeanAccount.isKeep() && (shareMeans1[i].getValue() >= shareMeans2[i].getValue()))){
                Trade trade = new Trade("MM");
                trades.add(trade);
                // sale
                if(twoMeanAccount.isKeep() && (shareMeans1[i].getValue() < shareMeans2[i].getValue())){
                    trade.setSaleTrade(twoMeanAccount.getShareNum(), shares[i + 1].getDate(), shares[i + 1].getClose());
                    twoMeanAccount.setBalance(twoMeanAccount.getBalance() + shares[i + 1].getClose() * twoMeanAccount.getShareNum());
                    twoMeanAccount.setShareNum(0);
                    twoMeanAccount.setKeep(false);
                }
                // buy
                if(!twoMeanAccount.isKeep() && (shareMeans1[i].getValue() >= shareMeans2[i].getValue())){
                    twoMeanAccount.setShareNum((int)Math.floor(twoMeanAccount.getBalance() / shares[i + 1].getClose()));
                    trade.setBuyTrade(twoMeanAccount.getShareNum(), shares[i + 1].getDate(), shares[i + 1].getClose());
                    twoMeanAccount.setBalance(twoMeanAccount.getBalance() - shares[i + 1].getClose() * twoMeanAccount.getShareNum());
                    twoMeanAccount.setKeep(true);
                }
            }
        }
        // if the account was keep at the last, the sals it as last day's high
        if (twoMeanAccount.isKeep()){
            Trade trade = new Trade("MM");
            trades.add(trade);
            trade.setSaleTrade(twoMeanAccount.getShareNum(),
                    shares[this.period - 1].getDate(), shares[this.period - 1].getClose());
            twoMeanAccount.setBalance(twoMeanAccount.getBalance() + shares[this.period - 1].getClose() * twoMeanAccount.getShareNum());
            twoMeanAccount.setShareNum(0);
            twoMeanAccount.setKeep(false);
        }
    }

    public void setShare2MeanIncome(ShareMean[] shareMeans1, ShareMean[] shareMeans2){
        if (shareMeans1.length != shareMeans2.length){
            System.out.println("The two meanShares length must have same length");
            System.exit(0);
        }

        for(int i = 0; i < (this.period - 1); i ++){
            // if share price is below mean, sale
            if((share2MeanAccount.isKeep() && ((shareMeans1[i].getValue() < shareMeans2[i].getValue())
                    || (shares[i].getClose() < shareMeans1[i].getValue())
                    || (shares[i].getClose() < shareMeans2[i].getValue())))
                ||
                    (!share2MeanAccount.isKeep() && (shareMeans1[i].getValue() >= shareMeans2[i].getValue())
                            && (shares[i].getClose() >= shareMeans1[i].getValue())) ){
                Trade trade = new Trade("SMM");
                trades.add(trade);
                // sale
                if(share2MeanAccount.isKeep() && ((shareMeans1[i].getValue() < shareMeans2[i].getValue())
                        || (shares[i].getClose() < shareMeans1[i].getValue())
                        || (shares[i].getClose() < shareMeans2[i].getValue()))){
                    trade.setSaleTrade(share2MeanAccount.getShareNum(), shares[i + 1].getDate(), shares[i + 1].getClose());
                    share2MeanAccount.setBalance(share2MeanAccount.getBalance() + shares[i + 1].getClose() * share2MeanAccount.getShareNum());
                    share2MeanAccount.setShareNum(0);
                    share2MeanAccount.setKeep(false);
                }
                // buy
                if(!share2MeanAccount.isKeep() && (shareMeans1[i].getValue() >= shareMeans2[i].getValue())
                        && (shares[i].getClose() >= shareMeans1[i].getValue())){
                    share2MeanAccount.setShareNum((int)Math.floor(share2MeanAccount.getBalance() / shares[i + 1].getClose()));
                    trade.setBuyTrade(share2MeanAccount.getShareNum(), shares[i + 1].getDate(), shares[i + 1].getClose());
                    share2MeanAccount.setBalance(share2MeanAccount.getBalance() - shares[i + 1].getClose() * share2MeanAccount.getShareNum());
                    share2MeanAccount.setKeep(true);
                }
            }
        }
        // if the account was keep at the last, the sals it as last day's high
        if (share2MeanAccount.isKeep()){
            Trade trade = new Trade("SMM");
            trades.add(trade);
            trade.setSaleTrade(share2MeanAccount.getShareNum(),
                    shares[this.period - 1].getDate(), shares[this.period - 1].getClose());
            share2MeanAccount.setBalance(share2MeanAccount.getBalance() + shares[this.period - 1].getClose() * share2MeanAccount.getShareNum());
            share2MeanAccount.setShareNum(0);
            share2MeanAccount.setKeep(false);
        }
    }

    public Account getShareMeanAccount() {
        return shareMeanAccount;
    }

    public Account getTwoMeanAccount() {
        return twoMeanAccount;
    }

    public Account getShare2MeanAccount() {
        return share2MeanAccount;
    }

    public List<Trade> getTrades() {
        return trades;
    }

    public ShareMean[] getShare5Means() {
        return share5Means;
    }

    public ShareMean[] getShare10Means() {
        return share10Means;
    }

    public ShareMean[] getShare30Means() {
        return share30Means;
    }

    public ShareMean[] getShare60Means() {
        return share60Means;
    }
}
