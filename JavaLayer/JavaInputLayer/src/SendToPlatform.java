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
        try {
            out = new PrintWriter(socketOut.getOutputStream(), true);
        } catch (IOException e) {
            e.printStackTrace();
        }
        while (running.get()) {
            socketReceiver();
        }
        stopped.set(true);
    }

    private void socketCreation() {
        try {
            socketOut = new Socket("localhost", 9998);
        } catch (UnknownHostException e1) {
            e1.printStackTrace();
        } catch (IOException e1) {
            e1.printStackTrace();
        }
    }

    private void socketReceiver() {

        if (!queueOut.isEmpty()) {
            String element = queueOut.poll();
            logger.info("SendToPlatform: " + element);
            out.print(element);
            out.flush();
        }
    }
}