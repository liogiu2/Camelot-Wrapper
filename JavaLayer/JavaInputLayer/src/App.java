import java.util.concurrent.ConcurrentLinkedQueue;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class App {
    static Thread sendToSocket;
    static Thread receiveFromSocket;
    static Thread receive;
    static Socket socketIn;
    static Socket socketOut;
    static Process process;
    static boolean isRunning = true;

    static class ClosingCommands extends Thread {

        public void run() {
            isRunning = false;
            process.destroy();
        }
     }
  


    public static void main(String[] args) throws Exception {
        Runtime.getRuntime().addShutdownHook(new ClosingCommands());
        process = Runtime.getRuntime().exec("python  C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\prova.py");

        ConcurrentLinkedQueue<String> queueIn = new ConcurrentLinkedQueue<String>();
        ConcurrentLinkedQueue<String> queueOut = new ConcurrentLinkedQueue<String>();

        //Thread for the socket communication
        receiveFromSocket = new Thread(new Runnable() {
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
        });
        receiveFromSocket.start();

        //Thread for the socket communication
        sendToSocket = new Thread(new Runnable() {
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
                    while(isRunning){
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
        });
        sendToSocket.start();

        //Thread for standard input reading 
        receive = new Thread(new Runnable() {
            @Override
            public void run() {
                //Scanner scanner = new Scanner(System.in);
                BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
                while(isRunning){
                    String line;
                    try {
                        line = stdIn.readLine();
                        queueOut.add(line);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    
                }
            }
        });
        receive.start();

        while(isRunning){
            if(!queueIn.isEmpty()){
                System.out.println(queueIn.poll());
            }
        }


    }
}
