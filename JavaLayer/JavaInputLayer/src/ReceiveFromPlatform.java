import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class ReceiveFromPlatform implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private static Socket socketIn;
    private ConcurrentLinkedQueue<String> queueIn;
    private BufferedReader stdIn;

    public ReceiveFromPlatform(ConcurrentLinkedQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
    }

    public void interrupt() {
        running.set(false);
        try {
            socketIn.close();
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
        running.set(true);
        stopped.set(false);
        socketCreation();
        try {
            stdIn = new BufferedReader(new InputStreamReader(socketIn.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }
        while (running.get()) {
            soketInputReader();
        }
        stopped.set(true);
    }

    private void socketCreation() {
        try {
            socketIn = new Socket("localhost", 9998);
        } catch (UnknownHostException e1) {
            e1.printStackTrace();
        } catch (IOException e1) {
            e1.printStackTrace();
        }
    }

    private void soketInputReader() {

        String in;
        try {
            in = stdIn.readLine();

            if (in != null) {
                queueIn.add(in);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}