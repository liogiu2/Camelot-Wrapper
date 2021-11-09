import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class ReceiveFromCamelot implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private BlockingQueue<String> queueIn;
    private BufferedReader stdIn;
    private Logger logger;

    public ReceiveFromCamelot(BlockingQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
        logger = App.getLogger();
    }

    public void interrupt() {
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
        stdIn = new BufferedReader(new InputStreamReader(System.in));
        while (running.get()) {
            stdInReceiver();
        }
        stopped.set(true);
    }

    private void stdInReceiver(){
        String line;
        try {
            line = stdIn.readLine();
            logger.info("ReceiveFromCamelot: "+line);
            queueIn.put(line);

            if (line.equalsIgnoreCase("input Quit")) {
                logger.info("ReceiveFromCamelot: Starting closing procedure");
                App.interruptEverything();
            }
        } catch (IOException e) {
            logger.severe("ReceiveFromCamelot: IOException: " + e.getMessage());
        } catch (InterruptedException e) {
            logger.severe("ReceiveFromCamelot: InterruptedException: "+e.getMessage());
            App.interruptEverything();
        }
    }
}
