import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class SendToPlatform implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private static Socket socketOut;
    private ConcurrentLinkedQueue<String> queueOut;
    private PrintWriter out;
    private Logger logger;

    public SendToPlatform(ConcurrentLinkedQueue<String> queueOut, AtomicBoolean running) {
        this.queueOut = queueOut;
        this.running = running;
        this.logger = App.getLogger();
    }

    public void interrupt() {
        running.set(false);
        out.print("kill");
        out.flush();
        try {
            socketOut.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
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
        socketCreation();
        logger.info("SendToPlatform: socket created");
        try {
            out = new PrintWriter(socketOut.getOutputStream(), true);
        } catch (IOException e) {
            logger.severe(e.getMessage());
        }
        logger.info("SendToPlatform: starting sending");
        while (running.get()) {
            socketSender();
        }
        stopped.set(true);
    }

    private void socketCreation() {
        try {
            socketOut = new Socket("localhost", 9999);
        } catch (UnknownHostException e1) {
            logger.severe(e1.getMessage());
        } catch (IOException e1) {
            logger.severe(e1.getMessage());
        }
    }

    private void socketSender() {

        if (!queueOut.isEmpty()) {
            String element = queueOut.poll();
            logger.info("SendToPlatform: " + element);
            out.print(element);
            out.flush();
        }
    }
}