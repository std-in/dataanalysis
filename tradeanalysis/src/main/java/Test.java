import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Random;

/**
 * Created by NYH on 2017/1/14.
 */
public class Test {
    public static void main(String[] args) throws ParseException{
        SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");
        Date date = sdf.parse("19990210");
        System.out.println(Integer.parseInt(date.getYear() + "" + (date.getMonth() + 1)));
        System.out.println(new Random().nextInt(100));
        System.out.println(Math.ceil(8.0 / 3) + "   " + 7 % 3);
    }
}
