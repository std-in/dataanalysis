package nyh.executor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;

public class CallableThread implements Callable<List<Response>> {

    private List<Request> requests;

    public CallableThread(List<Request> re) {
        this.requests = re;
    }

    @Override
    public List<Response> call() throws Exception {
        List<Response> result = new ArrayList<>(requests.size());
        for (Request r: requests) {
            result.add(new Response(r.getId(), r.getValue() + 1.0));
        }
        return result;
    }
}
