import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Logger;

public class SendToPlatform implements Runnable {

    private static final int PORT = 12345;
    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private Socket socketOut;
    private BlockingQueue<String> queueOut;
    // private PrintWriter out;
    private DataOutputStream dos;
    private Logger logger;
    private ServerSocketConnection serverSocketConnection;

    public SendToPlatform(BlockingQueue<String> queueOut, AtomicBoolean running) {
        this.queueOut = queueOut;
        this.running = running;
        this.logger = App.getLogger();
        serverSocketConnection = new ServerSocketConnection(PORT);
    }

    public void interrupt() {
        logger.info("SendToPlatform: interrupting.");
        running.set(false);
        serverSocketConnection.sendMessage("kill");
        serverSocketConnection.closeServer();
        // out.print("kill");
        // out.flush();
        // try {
        // dos.writeUTF("kill");
        // dos.close();
        // socketOut.close();
        // } catch (IOException e) {
        // logger.severe("SendToPlatform: " + e.getMessage());
        // }
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
        serverSocketConnection.createServer();
        // socketCreation();
        // logger.info("SendToPlatform: socket created");
        // try {
        // //out = new PrintWriter(socketOut.getOutputStream(), true);
        // dos = new DataOutputStream(socketOut.getOutputStream());
        // } catch (IOException e) {
        // logger.severe(e.getMessage());
        // }
        // logger.info("SendToPlatform: starting sending");
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

        // if (!queueOut.isEmpty()) {
        // String element = null;
        // try {
        // element = queueOut.poll(1000, TimeUnit.MILLISECONDS);
        // } catch (InterruptedException e) {
        // logger.severe("SendToPlatform: InterruptedException: "+ e.getMessage());
        // App.interruptEverything();
        // }
        // logger.info("SendToPlatform: " + element);
        // if(element == null) {
        // logger.info("SendToPlatform: element is null");
        // } else {
        // try {
        // dos.writeUTF(element);
        // } catch (IOException e) {
        // logger.severe("SendToPlatform: error while sending: "+e.getMessage());
        // }
        // //out.println(element);
        // logger.info("SendToPlatform: Message sent.");
        // // if (out.checkError()) {
        // // logger.severe("SendToPlatform: error while sending to platform");
        // // }
        // }

        // }
        if (!queueOut.isEmpty()) {
            String element = null;
            try {
                element = queueOut.poll(1000, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
                logger.severe("SendToPlatform: InterruptedException: " + e.getMessage());
            }
            logger.info("SendToPlatform: trying sending: " + element);
            serverSocketConnection.sendMessage(element);
            logger.info("SendToPlatform: Message \"" + element + "\" sent.");
            String ok = serverSocketConnection.receiveMessage();
            logger.info("SendToPlatform: received: " + ok + "for message "+element);
        }
    }
}