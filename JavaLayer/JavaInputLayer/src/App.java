import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.time.format.DateTimeFormatter;
import java.time.LocalDateTime;

public class App {
    static Thread sendToPlatformThread;
    static Thread receiveFromPlatformThread;
    static Thread receiveFromCamelotThread;
    static Thread sendToCamelotThread;
    static Process process;
    private static AtomicBoolean isRunning = new AtomicBoolean(true);
    private static Logger logger;
    private static SendToCamelot sendToCamelot;
    private static ReceiveFromCamelot receiveFromCamelot;
    private static SendToPlatform sendToPlatform;
    private static ReceiveFromPlatform receiveFromPlatform;
    private static BufferedReader reader;

    public static void main(String[] args) throws Exception {
        // process = Runtime.getRuntime().exec("python
        // C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\prova.py");

        logger = Logger.getLogger(App.class.getName());

        // Create an instance of FileHandler that write log to a file called
        // app.log. Each new message will be appended at the at of the log file.
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyyMMddHHmmss");
        LocalDateTime now = LocalDateTime.now();
        String logName = "appJava" + dtf.format(now) + ".log";
        String basePath = new File("").getAbsolutePath()+"/logs/Java/";
        File directory = new File(basePath);
        if (! directory.exists()){
            directory.mkdirs();
        }
        FileHandler fileHandler = new FileHandler(basePath+logName, false);
        logger.addHandler(fileHandler);

        startPythonProcess();
        // Queue that receives a message from the platform and sends it to Camelot
        ConcurrentLinkedQueue<String> queueIn = new ConcurrentLinkedQueue<String>();
        // Queue that receives a message from Camelot and sends it to the Platform
        ConcurrentLinkedQueue<String> queueOut = new ConcurrentLinkedQueue<String>();

        // Thread for the socket communication
        receiveFromPlatform = new ReceiveFromPlatform(queueIn, isRunning);
        receiveFromPlatformThread = new Thread(receiveFromPlatform);
        /*
         * = new Thread(new Runnable() {
         * 
         * @Override public void run() { try { socketIn = new Socket("localhost",9998);
         * } catch (UnknownHostException e1) { e1.printStackTrace(); } catch
         * (IOException e1) { e1.printStackTrace(); } try { BufferedReader stdIn =new
         * BufferedReader(new InputStreamReader(socketIn.getInputStream()));
         * while(isRunning){ String in = stdIn.readLine(); if(in != null) {
         * queueIn.add(in); } }
         * 
         * } catch (IOException e) { e.printStackTrace(); } } });
         */
        receiveFromPlatformThread.start();

        // Thread for the socket communication
        sendToPlatform = new SendToPlatform(queueOut, isRunning);
        sendToPlatformThread = new Thread(sendToPlatform);
        /*
         * = new Thread(new Runnable() {
         * 
         * @Override public void run() { try { socketOut = new Socket("localhost",9999);
         * } catch (UnknownHostException e1) { e1.printStackTrace(); } catch
         * (IOException e1) { e1.printStackTrace(); } try { PrintWriter out = new
         * PrintWriter(socketOut.getOutputStream(), true); while(isRunning.get()){
         * if(!queueOut.isEmpty()) { String element = queueOut.poll();
         * out.print(element); out.flush(); } }
         * 
         * } catch (IOException e) { e.printStackTrace(); } } });
         */
        sendToPlatformThread.start();

        // Thread for standard input reading
        receiveFromCamelot = new ReceiveFromCamelot(queueOut, isRunning);
        receiveFromCamelotThread = new Thread(receiveFromCamelot);
        /*
         * = new Thread(new Runnable() {
         * 
         * @Override public void run() { //Scanner scanner = new Scanner(System.in);
         * BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
         * while(isRunning.get()){ String line; try { line = stdIn.readLine();
         * queueOut.add(line); } catch (IOException e) { e.printStackTrace(); }
         * 
         * } } });
         */
        receiveFromCamelotThread.start();

        sendToCamelot = new SendToCamelot(queueIn, isRunning);
        sendToCamelotThread = new Thread(sendToCamelot);
        sendToCamelotThread.start();

        /*
         * String line; while ((line = reader.readLine()) != null) { logger.info(line);
         * }
         */

    }

    private static void startPythonProcess() {
        ProcessBuilder processBuilder = new ProcessBuilder();

        if (System.getProperty("os.name").toLowerCase().contains("windows")) {
            // -- Windows --

            // Run a command
            processBuilder.command("cmd.exe", "/c",
                    "python C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\prova.py");

            // Run a bat file
            // processBuilder.command("C:\\Users\\mkyong\\hello.bat");
        } else {
            // -- Linux --

            // Run a shell command
            processBuilder.command("bash", "-c",
                    "python /Users/giuliomori/Documents/GitHub/camelot_communicator/camelot_communicator/prova.py");

            // Run a shell script
            // processBuilder.command("/Users/giuliomori/Documents/GitHub/camelot_communicator/camelot_communicator/prova.py");
        }

        try {

            process = processBuilder.start();

            // reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void interruptEverything() {
        logger.info("Main: InterruptEverything called, closing all.");
        sendToCamelot.interrupt();
        // receiveFromCamelot.interrupt();
        sendToPlatform.interrupt();
        receiveFromPlatform.interrupt();
    }

    public static Logger getLogger() {
        return logger;
    }
}
