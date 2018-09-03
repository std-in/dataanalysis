package nyh.executor;

import java.util.Random;
import java.util.concurrent.*;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: nyh
 * \* Date: 18-3-20
 * \* Time: 上午11:26
 * \* Description:
 * \
 */

/**
 * executor作为灵活且强大的异步执行框架，其支持多种不同类型的任务执行策略，提供了一种标准的方法将任务的提交过程和执行过程
 * 解耦开发，基于生产者-消费者模式，其提交任务的线程相当于生产者，执行任务的线程相当于消费者，并用Runnable来表示任务，
 * Executor的实现还提供了对生命周期的支持，以及统计信息收集，应用程序管理机制和性能监视等机制。
 *
 * Executor：一个接口，其定义了一个接收Runnable对象的方法executor，其方法签名为executor(Runnable command),
 * ExecutorService：是一个比Executor使用更广泛的子类接口，其提供了生命周期管理的方法，以及可跟踪一个或多个异步任务执行状况返回Future的方法
 * AbstractExecutorService：ExecutorService执行方法的默认实现
 * ScheduledExecutorService：一个可定时调度任务的接口
 * ScheduledThreadPoolExecutor：ScheduledExecutorService的实现，一个可定时调度任务的线程池
 * ThreadPoolExecutor：线程池，可以通过调用Executors以下静态工厂方法来创建线程池并返回一个ExecutorService对象：
 */


public class ExecutorTest {

    public static void main(String[] args) throws Exception {
        ExecutorTest executorTest = new ExecutorTest();
//        executorTest.HeartBeat();
//        executorTest.ThreadPoolTest();
//        executorTest.CallableAndFuture();
        executorTest.CompletionServiceTest();

    }

    /**
     * Executors：提供了一系列静态工厂方法用于创建各种线程池
     * newFixedThreadPool:创建可重用且固定线程数的线程池，如果线程池中的所有线程都处于活动状态，此时再提交任务就在队列中等待，
     * 直到有可用线程；如果线程池中的某个线程由于异常而结束时，线程池就会再补充一条新线程。
     * newSingleThreadExecutor:创建一个单线程的Executor，如果该线程因为异常而结束就新建一条线程来继续执行后续的任务
     * newScheduledThreadPool:创建一个可延迟执行或定期执行的线程池
     * @return 使用newScheduledThreadPool来模拟心跳机制
     */
    public void HeartBeat() {
        ScheduledExecutorService executor = Executors.newScheduledThreadPool(5);
        Runnable heartBeatTask = new Runnable() {
            public void run() {
                System.out.println("HeartBeat.........................");
            }
        };
        executor.scheduleAtFixedRate(heartBeatTask,5,3, TimeUnit.SECONDS);   //5秒后第一次执行，之后每隔3秒执行一次
    }

    /**
     * newCachedThreadPool:创建可缓存的线程池，如果线程池中的线程在60秒未被使用就将被移除，在执行新的任务时，
     * 当线程池中有之前创建的可用线程就重用可用线程，否则就新建一条线程
     * @return 为每个任务新建一条线程，共创建了3条线程
     */
    public void ThreadPoolTest() {
        ExecutorService threadPool = Executors.newCachedThreadPool();//线程池里面的线程数会动态变化，并可在线程线被移除前重用
        for (int i = 1; i <= 10; i ++) {
            final int task = i;   //10个任务
//            TimeUnit.SECONDS.sleep(1);
            threadPool.execute(new Runnable() {    //接受一个Runnable实例
                public void run() {
                    System.out.println("线程名字： " + Thread.currentThread().getName() +  "  任务名为： "+task);
                }
            });
        }
    }

    /**
     * ExecutorService提供了管理Eecutor生命周期的方法，ExecutorService的生命周期包括了：运行  关闭和终止三种状态。
     * ExecutorService在初始化创建时处于运行状态。
     * shutdown方法等待提交的任务执行完成并不再接受新任务，在完成全部提交的任务后关闭
     * shutdownNow方法将强制终止所有运行中的任务并不再允许提交新任务
     * 可以将一个Runnable（如例2）或Callable（如例3）提交给ExecutorService的submit方法执行，
     * 最终返回一上Futire用来获得任务的执行结果或取消任务
     * @return 任务执行完成后并返回执行结果
     * @throws Exception
     */
    public void CallableAndFuture() throws Exception{
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Future<String> future = executor.submit(new Callable<String>() {   //接受一上callable实例
            public String call() throws Exception {
                return "MOBIN";
            }
        });
        System.out.println("任务的执行结果："+future.get());
    }

    /**
     * ExecutorCompletionService:实现了CompletionService，将执行完成的任务放到阻塞队列中，通过take或poll方法来获得执行结果
     * @return 启动10条线程，谁先执行完成就返回谁）
     * @throws Exception
     */
    public void CompletionServiceTest() throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(10);        //创建含10.条线程的线程池
        CompletionService completionService = new ExecutorCompletionService(executor);
        for (int i =1; i <=10; i ++) {
            final  int result = i;
            completionService.submit(new Callable() {
                public Object call() throws Exception {
                    Thread.sleep(new Random().nextInt(2000));   //让当前线程随机休眠一段时间
                    return result;
                }
            });
        }
        System.out.println(completionService.take().get());   //获取执行结果
    }
}
