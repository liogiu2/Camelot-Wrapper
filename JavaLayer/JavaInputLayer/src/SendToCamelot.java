import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class SendToCamelot implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private ConcurrentLinkedQueue<String> queueIn;
    private Logger logger;

    public SendToCamelot(ConcurrentLinkedQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
        this.logger = App.getLogger();
    }

    public void interrupt() {
        logger.info("SendToCamelot: interrupting.");
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
                String msg = queueIn.poll();
                logger.info("SendToCamelot: "+ msg);
                System.out.println(msg);
            }
        }
        stopped.set(true);
    }

}
