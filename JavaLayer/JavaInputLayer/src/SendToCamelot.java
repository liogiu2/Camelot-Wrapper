import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class SendToCamelot implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private volatile LinkedBlockingQueue<String> queue;
    private Logger logger;

    public SendToCamelot(LinkedBlockingQueue<String> queue, AtomicBoolean running) {
        this.queue = queue;
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

                msg = queue.take();
            } catch (InterruptedException e) {
                logger.info("SendToCamelot: Exception : " + e.getMessage());
            }
            logger.info("SendToCamelot: sending message: " + msg);
            if(msg != null){
                System.out.println(msg);
                logger.info("SendToCamelot: message sent.");
            }
            
            // if (!queueIn.isEmpty()) {
            // String msg = null;
            // msg = queueIn.poll();
            // logger.info("SendToCamelot: removed from queue"+ msg);
            // System.out.println(msg);
            // }
        }
        stopped.set(true);
    }

}
