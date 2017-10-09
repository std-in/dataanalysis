package dictionary;

/**
 * Created by NYH on 2017/1/13.
 */
public class Account implements Cloneable{
    private String shareName;
    private int shareNum = 0;
    private boolean keep = false;
    private double balance = 0;

    @Override
    public Account clone() throws CloneNotSupportedException
    {
        Account account = (Account) super.clone();
        return account;
    }

    public String getShareName() {
        return shareName;
    }

    public void setShareName(String shareName) {
        this.shareName = shareName;
    }

    public int getShareNum() {
        return shareNum;
    }

    public void setShareNum(int shareNum) {
        this.shareNum = shareNum;
    }

    public boolean isKeep() {
        return keep;
    }

    public void setKeep(boolean keep) {
        this.keep = keep;
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }
}
