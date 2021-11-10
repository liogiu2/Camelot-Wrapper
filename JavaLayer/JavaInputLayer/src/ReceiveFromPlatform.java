import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class ReceiveFromPlatform implements Runnable {

    private static final int PORT = 9998;
    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private static Socket socketIn;
    private BlockingQueue<String> queueIn;
    private BufferedReader stdIn;
    private Logger logger;
    private ServerSocketConnection serverSocketConnection;

    public ReceiveFromPlatform(BlockingQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
        logger = App.getLogger();
        serverSocketConnection = new ServerSocketConnection(PORT);
    }

    public void interrupt() {
        logger.info("ReceiveFromPlatform: interrupting.");
        running.set(false);
        // try {
        //     socketIn.close();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
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

    public void run() {
        running.set(true);
        stopped.set(false);
        serverSocketConnection.createServer();
        // socketCreation();
        // try {
        //     stdIn = new BufferedReader(new InputStreamReader(socketIn.getInputStream()));
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        while (running.get()) {
            soketInputReader();
        }
        stopped.set(true);
    }

    private void socketCreation() {
        // try {
        //     socketIn = new Socket("localhost", 9998);
        // } catch (UnknownHostException e1) {
        //     e1.printStackTrace();
        // } catch (IOException e1) {
        //     e1.printStackTrace();
        // }
    }

    private void soketInputReader() {

        // String in;
        // try {
        //     in = stdIn.readLine();

        //     logger.info("ReceiveFromPlatform: "+ in);
        //     if (in != null) {
        //         queueIn.put(in);
        //     }
        // } catch (IOException e) {
        //     logger.info("ReceiveFromPlatform: IOException: "+ e.getMessage());
        // } catch (InterruptedException e) {
        //     logger.info("ReceiveFromPlatform: InterruptedException: "+ e.getMessage());
        //     logger.info("ReceiveFromPlatform: Stopping everything");
        //     App.interruptEverything();
        // }

        String message = serverSocketConnection.receiveMessage();
        if (message != null) {
            //logger.info("ReceiveFromPlatform: " + message);
            queueIn.add(message);
        }
    }
}