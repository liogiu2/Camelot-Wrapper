import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class ReceiveFromPlatform implements Runnable {

    private static final int PORT = 9998;
    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private volatile LinkedBlockingQueue<String> queue;
    private Logger logger;
    private ServerSocketConnection serverSocketConnection;

    public ReceiveFromPlatform(LinkedBlockingQueue<String> queue, AtomicBoolean running) {
        this.queue = queue;
        this.running = running;
        logger = App.getLogger();
        serverSocketConnection = new ServerSocketConnection(PORT);
    }

    public void interrupt() {
        logger.info("ReceiveFromPlatform: interrupting.");
        running.set(false);
        serverSocketConnection.closeServer();
        worker.interrupt();
        Thread.currentThread().interrupt();
    }

    boolean isRunning() {
        return running.get();
    }

    boolean isStopped() {
        return stopped.get();
    }

    @Override
    public void run() {
        try {
            running.set(true);
            stopped.set(false);
            serverSocketConnection.createServer();
            while (running.get()) {
                soketInputReader();
            }
            stopped.set(true);
        } catch (Throwable e) {
            logger.severe("ReceiveFromPlatform: " + e.getMessage());
        }
    }

    private void soketInputReader() {
        String message = serverSocketConnection.receiveMessage();
        logger.info("ReceiveFromPlatform: received message: " + message);
        if (message != null) {
            try {
                logger.info("ReceiveFromPlatform: adding message to queue.");
                queue.put(message);
                logger.info("ReceiveFromPlatform: message added to queue.");
            } catch (InterruptedException e) {
                logger.severe("ReceiveFromPlatform: " + e.getMessage());
            }

        }
    }
}