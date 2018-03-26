package nyh.executor;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: nyh
 * \* Date: 18-3-23
 * \* Time: 下午5:07
 * \* Description:
 * \
 */
public class FinalTest {
    public static void main(String args[]) {
        int a = 0;
        testVariable(a);
        String[] b = {"a", "b"};
        testReference(b);
    }

    public static void testVariable(final int a) {
//        a = 1;
        System.out.println("a: " + a);
    }
    public static void testReference(final String[] b) {
//        b = {"a", "bb"};
        b[0] = "aa";
        System.out.println("b[0]: " + b[0]);
    }
}
