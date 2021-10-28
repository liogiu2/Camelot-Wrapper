import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class SendToCamelot implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private ConcurrentLinkedQueue<String> queueIn;

    public SendToCamelot(ConcurrentLinkedQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
    }

    public void interrupt() {
        running.set(false);
        worker.interrupt();
    }

    boolean isRunning() {
        return running.get();
    }

    boolean isStopped() {
        return stopped.get();
    }

    public void run() {
        stopped.set(false);
        while (running.get()) {
            if(!queueIn.isEmpty()){
                System.out.println(queueIn.poll());
            }
        }
        stopped.set(true);
    }

}
