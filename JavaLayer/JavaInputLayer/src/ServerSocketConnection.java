import java.net.Socket;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.logging.Logger;

import java.net.ServerSocket;

public class ServerSocketConnection {

    private int port;
    private Socket socket;
    private ServerSocket serverSocket;
    private Logger logger;
    private BufferedWriter out;
    private BufferedReader in;
    private OutputStream outputStream;
    private DataOutputStream dataOutputStream;
    private Object monitor = new Object();

    public ServerSocketConnection(int port) {
        this.port = port;
        logger = App.getLogger();
    }

    // Create a server for a socket connection
    public void createServer() {
        try {
            // Create a server socket
            serverSocket = new ServerSocket(port);
            // Socket creation
            socket = serverSocket.accept();
            // Create an output stream
            //outputStream = socket.getOutputStream();
            // Create a print writer
            //out = new BufferedWriter(new OutputStreamWriter(outputStream));
            // Create a buffered reader
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        } catch (IOException e) {
            logger.severe("Error creating server socket");
        }
    }

    public void createServerNew() {
        try {
            socket = new Socket("localhost", port);
            dataOutputStream = new DataOutputStream(socket.getOutputStream());

        } catch (IOException e) {
            logger.severe("Error creating server socket");
        }
    }

    // Close the server socket
    public void closeServer() {
        try {
            serverSocket.close();
        } catch (IOException e) {
            logger.severe("Error closing server socket");
        }
    }

    // Get the socket
    public Socket getSocket() {
        return socket;
    }

    public void sendMessage(String message) {
        try {
            // Sending the byte lenght of the message
            // byte[] ptext = message.getBytes("UTF-16");
            // logger.info("The lenght of the message is " + ptext.length);
            // send(String.valueOf(ptext.length));
            // Sending the message
            // logger.info("Sending message: " + message);
            send(message);
        } catch (IOException e) {
            logger.severe("Error sending message:" + e.getMessage());
        }
    }

    private void send(String message) throws IOException {
        // message += "\r\n";
        // byte[] ptext = message.getBytes("UTF-8");
        // logger.info("The lenght of the message is " + ptext.length);
        // out.write(String.format("%2d",ptext.length));
        // logger.info("Lenght sent");
        // out.write("\r\n");
        // out.flush();

        // out.write(new String(ptext));
        // logger.info("Data sent");
        // out.flush();
        synchronized (monitor) {
            byte[] dts = message.getBytes();
            dataOutputStream.writeInt(dts.length);
            dataOutputStream.write(dts);
        }

    }

    public String receiveMessage() {
        synchronized (monitor) {
            try {
                return in.readLine();
            } catch (IOException e) {
                logger.severe("Error receiving message");
                return null;
            }
        }
    }

}
