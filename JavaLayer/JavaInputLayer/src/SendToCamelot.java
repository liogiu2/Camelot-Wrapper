import java.util.concurrent.BlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class SendToCamelot implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private BlockingQueue<String> queueIn;
    private Logger logger;

    public SendToCamelot(BlockingQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
        this.logger = App.getLogger();
    }

    public void interrupt() {
        logger.info("SendToCamelot: interrupting.");
        running.set(false);
        worker.interrupt();
        Thread.currentThread().interrupt();
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
            String msg = null;
            try {
                msg = queueIn.take();
            } catch (InterruptedException e) {
                logger.severe("SendToCamelot: InterruptedException: "+e.getMessage());
                App.interruptEverything();
            }
            logger.info("SendToCamelot: "+ msg);
            System.out.println(msg);
        }
        stopped.set(true);
    }

}
