import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class App {
    static Thread sendToSocket;
    static Thread receiveFromSocket;
    static Thread receiveStandardInput;
    static Thread sendStandardOutput;
    static Process process;
    private static AtomicBoolean isRunning = new AtomicBoolean(true);
  


    public static void main(String[] args) throws Exception {
        process = Runtime.getRuntime().exec("python  C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\prova.py");

        ConcurrentLinkedQueue<String> queueIn = new ConcurrentLinkedQueue<String>();
        ConcurrentLinkedQueue<String> queueOut = new ConcurrentLinkedQueue<String>();

        //Thread for the socket communication
        SocketInputThread sit = new SocketInputThread(queueOut, isRunning);
        receiveFromSocket = new Thread(sit);
        /* = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    socketIn = new Socket("localhost",9998);
                } catch (UnknownHostException e1) {
                    e1.printStackTrace();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
                try {
                    BufferedReader stdIn =new BufferedReader(new InputStreamReader(socketIn.getInputStream()));
                    while(isRunning){
                            String in = stdIn.readLine();
                            if(in != null)
                            {
                                queueIn.add(in);
                            }                          
                        }

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }); */
        receiveFromSocket.start();

        //Thread for the socket communication
        SocketOutputThread sot = new SocketOutputThread(queueOut, isRunning);
        sendToSocket = new Thread(sot);
        /* = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    socketOut = new Socket("localhost",9999);
                } catch (UnknownHostException e1) {
                    e1.printStackTrace();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
                try {
                    PrintWriter out = new PrintWriter(socketOut.getOutputStream(), true);
                    while(isRunning.get()){
                            if(!queueOut.isEmpty())
                            {
                                String element = queueOut.poll();
                                out.print(element);
                                out.flush();
                            }                           
                        }

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }); */
        sendToSocket.start();

        //Thread for standard input reading 
        StandardInputThread stit = new StandardInputThread(queueOut, isRunning);
        receiveStandardInput = new Thread(stit);
        /* = new Thread(new Runnable() {
            @Override
            public void run() {
                //Scanner scanner = new Scanner(System.in);
                BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
                while(isRunning.get()){
                    String line;
                    try {
                        line = stdIn.readLine();
                        queueOut.add(line);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    
                }
            }
        }); */
        receiveStandardInput.start();

        StandardOutputThread stdot = new StandardOutputThread(queueIn, isRunning);
        sendStandardOutput = new Thread(stdot);
        sendStandardOutput.start();

    }
}
