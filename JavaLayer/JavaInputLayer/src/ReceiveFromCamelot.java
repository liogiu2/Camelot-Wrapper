import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class ReceiveFromCamelot implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private ConcurrentLinkedQueue<String> queueIn;
    private BufferedReader stdIn;
    private Logger logger;

    public ReceiveFromCamelot(ConcurrentLinkedQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
        logger = App.getLogger();
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
        stdIn = new BufferedReader(new InputStreamReader(System.in));
        while (running.get()) {
            try {
                stdInReceiver();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        stopped.set(true);
    }

    private void stdInReceiver() throws InterruptedException{
        String line;
        try {
            line = stdIn.readLine();
            logger.info("ReceiveFromCamelot: "+line);
            queueIn.add(line);

            if (line.equals("input Quit")) {
                App.interruptEverything();
                interrupt();
                throw new InterruptedException();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
