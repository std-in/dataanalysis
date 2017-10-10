package datasource;

import dictionary.Share;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by NYH on 2017/1/13.
 */
public class DataFromText {
    private File file;
    private  boolean header = true;
    public DataFromText(String path, boolean header) {
        this.header = header;
        this.file = new File(path);
    }
    public Share[] getData(String sep) throws IOException{
        List<Share> shareDays = new ArrayList<Share>();
        BufferedReader br = null;
        int lineNum = 0;
        try {
            String newLine = "";
            br = new BufferedReader(new FileReader(file));
            if (header){
                br.readLine();
            }
            while ((newLine = br.readLine()) != null){
                lineNum ++;
                String[] shareFutrues = newLine.split(sep);
                shareDays.add(new Share(shareFutrues));
            }
        } catch (IOException e){
            e.printStackTrace();
            System.out.println("The " + lineNum + "rd cannot be casted to Share data");
        } finally {
            if (br != null){
                br.close();
            }
        }
        Share[] shareDaysArray = new Share[shareDays.size()];
        for(int i = 0; i < shareDays.size(); i ++){
            shareDaysArray[i] = shareDays.get(i);
        }
        return shareDaysArray;
    }
}
