package nyh.executor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Future;
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class CallableTest {
    public static void main(String[] args) {
        List<Request> sublist1 = new ArrayList<>(2);
        sublist1.add(new Request("a", 1.0));
        sublist1.add(new Request("b", 1.1));
        List<Request> sublist2 = new ArrayList<>(2);
        sublist2.add(new Request("c", 1.2));
        sublist2.add(new Request("d", 1.3));
        List<Response> result = new CallableTest().getResponse(sublist1, sublist2);
        for (Response re: result) {
            System.out.println(re.getId() + " " + re.getValue());
        }
    }
    public List<Response> getResponse(List<Request> sublist1, List<Request> sublist2) {
        List<Response> result = new ArrayList<>(2);
        List<Future<List<Response>>> taskList = new ArrayList<>(2);
        ThreadPoolExecutor executor = new ThreadPoolExecutor(6, 10,
                5, TimeUnit.SECONDS, new SynchronousQueue<Runnable>());
        taskList.add(executor.submit(new CallableThread(sublist1)));
        taskList.add(executor.submit(new CallableThread(sublist2)));

        for (Future<List<Response>> task: taskList) {
            try {
                List<Response> tmp = task.get();
                result.addAll(tmp);
            } catch (Exception e) {
                e.printStackTrace();
                System.exit(1);
            }
        }
        return result;
    }
}
