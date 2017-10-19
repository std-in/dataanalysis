package com.my.blog.website.model.Po;

public class StockElements {
    private String Date;
    private double Open;
    private double High;
    private double Low;
    private double Close;
    private double AdjClose;
    private int Volume;

    public String getDate() {
        return Date;
    }

    public void setDate(String date) {
        Date = date;
    }

    public double getOpen() {
        return Open;
    }

    public void setOpen(double open) {
        Open = open;
    }

    public double getHigh() {
        return High;
    }

    public void setHigh(double high) {
        High = high;
    }

    public double getLow() {
        return Low;
    }

    public void setLow(double low) {
        Low = low;
    }

    public double getClose() {
        return Close;
    }

    public void setClose(double close) {
        Close = close;
    }

    public double getAdjClose() {
        return AdjClose;
    }

    public void setAdjClose(double adjClose) {
        AdjClose = adjClose;
    }

    public int getVolume() {
        return Volume;
    }

    public void setVolume(int volume) {
        Volume = volume;
    }
}
