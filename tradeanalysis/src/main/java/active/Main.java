package active;

import datasource.DataFromText;
import decision.MeanAnalysis;
import dictionary.Account;
import dictionary.Share;
import dictionary.ShareMean;

import java.io.IOException;
import java.text.ParseException;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * Created by NYH on 2017/1/13.
 */
public class Main {
    public static void main(String[] args) throws IOException, ParseException, CloneNotSupportedException{
        int myBalance = 10000;
        Share[] shareData = new DataFromText("/home/nyh/work/data/601558.txt", true).getData(",");

        int SMIn = 0, MMIn = 0, SMMIn = 0;
        int SMOut = 0, MMOut = 0, SMMOut = 0;
        int SMTotol = 0, MMTotol = 0, SMMTotol = 0;

        int totolIter = 0;
        int iter = 1000;
        for(int i = 0; i < iter; i ++){
            int firstMean = new Random().nextInt(2);
            int secondMean = new Random().nextInt(3);
            if(firstMean >= secondMean){
                continue;
            }
            Account myAccount = new Account();
            myAccount.setBalance(myBalance);
            // data period account
            MeanAnalysis mA = new MeanAnalysis(shareData, 100, myAccount);
            // choose two means as parameters to compute the income
            Map<Integer, ShareMean[]> candidateMeans = new HashMap<Integer, ShareMean[]>();
            candidateMeans.put(0, mA.getShare5Means());
            candidateMeans.put(1, mA.getShare10Means());
            candidateMeans.put(2, mA.getShare30Means());
            candidateMeans.put(3, mA.getShare60Means());

            mA.setShareMeanIncome(mA.getShare5Means());
            mA.set2MeanIncome(candidateMeans.get(firstMean), candidateMeans.get(secondMean));
            mA.setShare2MeanIncome(candidateMeans.get(firstMean), candidateMeans.get(secondMean));
            if (mA.getTrades().size() < 1 ){
                continue;
            }
            totolIter ++;
            double SMResult = mA.getShareMeanAccount().getBalance();
            double MMResult = mA.getTwoMeanAccount().getBalance();
            double SMMResult = mA.getShare2MeanAccount().getBalance();
            System.out.println(SMResult + "  " + MMResult + "  " + SMMResult);

            if(SMResult > myBalance) SMIn ++; else SMOut++;
            if(MMResult > myBalance) MMIn ++; else MMOut++;
            if(SMMResult > myBalance) SMMIn ++; else SMMOut++;
            SMTotol += SMResult;
            MMTotol += MMResult;
            SMMTotol += SMMResult;
        }
        System.out.println("The true iterators  " + totolIter);
        System.out.println("Type InTimes OutTimes Balance");
        System.out.println("SM:   " + SMIn + "      " + SMOut + "   " + (SMTotol - totolIter * myBalance));
        System.out.println("MM:   " + MMIn + "      " + MMOut + "   " + (MMTotol - totolIter * myBalance));
        System.out.println("SMM:  " + SMMIn + "      " + SMMOut + "   " + (SMMTotol - totolIter * myBalance));

/*
        int income = 0, outcome = 0;
        for(int i = 0; i < 100; i ++ ){
            Account myAccount = new Account();
            myAccount.setBalance(myBalance);
            MeanAnalysis mA = new MeanAnalysis(shareData, 100, myAccount);
            mA.setShareMeanIncome(mA.getShare5Means());
            double result = mA.getShareMeanAccount().getBalance();

            if(result > myBalance) income ++; else outcome ++;
            System.out.println("Balance    TradeTimes");
            System.out.println(result + "     " + mA.getTrades().size());
        }
        System.out.println("Income times: " + income);
        System.out.println("Outcome times: " + outcome);
        */
        /*
        DateFormat df = DateFormat.getDateTimeInstance(DateFormat.MEDIUM,DateFormat.MEDIUM);
        System.out.println("The trade details" );
        for (int i = 0; i < mA.getTrades().size(); i ++) {
            Trade trade = mA.getTrades().get(i);
            System.out.println(df.format(trade.getTradeDay()) + " " + trade.getTradeNum()
                    + " " + trade.isBuy()+ " " + trade.getTradePrice());

        }*/

    }
}
