import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class SendToPlatform implements Runnable {

    private static final int PORT = 9999;
    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private volatile LinkedBlockingQueue<String> queue;
    private Logger logger;
    private ServerSocketConnection serverSocketConnection;
    private BufferedReader stdIn;

    public SendToPlatform(LinkedBlockingQueue<String> queue, AtomicBoolean running) {
        this.queue = queue;
        this.running = running;
        this.logger = App.getLogger();
        serverSocketConnection = new ServerSocketConnection(PORT);
    }

    public void interrupt() {
        logger.info("SendToPlatform: interrupting.");
        running.set(false);
        serverSocketConnection.sendMessage("kill");
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
        stopped.set(false);
        serverSocketConnection.createServerNew();
        stdIn = new BufferedReader(new InputStreamReader(System.in));
        while (running.get()) {
            socketSender();
        }
        stopped.set(true);
    }

    private void socketSender() {

        //logger.info("SendToPlatform: Getting message from the queue.");
        // String message = null;
        // try {
        //     message = queue.take();
        // } catch (InterruptedException e) {
        //     logger.info("SendToPlatform: Exception: " + e.getMessage());
        // }
        String message = null;
        try {
            logger.info("SendToPlatform: Getting message from the queue.");
            message = queue.take();
            logger.info("SendToPlatform: Got message from the queue: " + message);
        } catch (InterruptedException e) {
            logger.info("SendToPlatform: Exception: " + e.getMessage());
        }
        if (message != null) {
            logger.info("SendToPlatform: Starting sending message");
            serverSocketConnection.sendMessage(message);
            logger.info("SendToPlatform: Message \"" + message + "\" sent.");
        }

        // if (!queue.isEmpty()) {
        // String element = null;
        // logger.info("SendToPlatform: Getting message from the queue.");
        // element = queue.poll();
        // logger.info("SendToPlatform: Got message from queue: " + element);
        // serverSocketConnection.sendMessage(element);
        // logger.info("SendToPlatform: Message \"" + element + "\" sent.");
        // }
    }
}