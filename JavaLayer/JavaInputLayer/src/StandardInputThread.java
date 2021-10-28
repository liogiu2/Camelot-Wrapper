import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class StandardInputThread implements Runnable {

    private Thread worker;
    private AtomicBoolean running;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private ConcurrentLinkedQueue<String> queueIn;
    private BufferedReader stdIn;

    public StandardInputThread(ConcurrentLinkedQueue<String> queueIn, AtomicBoolean running) {
        this.queueIn = queueIn;
        this.running = running;
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
            stdInReceiver();
        }
        stopped.set(true);
    }

    private void stdInReceiver() {
        String line;
        try {
            line = stdIn.readLine();
            queueIn.add(line);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
