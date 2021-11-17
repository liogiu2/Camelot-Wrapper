import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class ReceiveFromCamelot implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private volatile LinkedBlockingQueue<String> queue;
    private BufferedReader stdIn;
    private Logger logger;

    public ReceiveFromCamelot(LinkedBlockingQueue<String> queue, AtomicBoolean running) {
        this.queue = queue;
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

    private void stdInReceiver() {
        // String line;
        // try {
        // line = stdIn.readLine();
        // logger.info("ReceiveFromCamelot: " + line);
        // queueIn.add(line);
        // logger.info("ReceiveFromCamelot: " + line + " added to queue");

        // if (line.equalsIgnoreCase("input Quit")) {
        // logger.info("ReceiveFromCamelot: Starting closing procedure");
        // App.interruptEverything();
        // }
        // } catch (IOException e) {
        // logger.severe("ReceiveFromCamelot: IOException: " + e.getMessage());
        // }
        String line;
        try {
            line = stdIn.readLine();
            logger.info("ReceiveFromCamelot: " + line);

            queue.put(line);

            logger.info("ReceiveFromCamelot: " + line + " added to queue");

            if (line.equalsIgnoreCase("input Quit")) {
                logger.info("ReceiveFromCamelot: Starting closing procedure");
                App.interruptEverything();
            }
        } catch (IOException | InterruptedException e) {
            logger.severe("ReceiveFromCamelot: Exception: " + e.getMessage());
        }
    }
}
