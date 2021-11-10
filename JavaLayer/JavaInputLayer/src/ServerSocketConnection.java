import java.net.Socket;
import java.nio.ByteBuffer;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.logging.Logger;
import java.net.ServerSocket;
import static java.nio.charset.StandardCharsets.*;

public class ServerSocketConnection {

    private int port;
    private Socket socket;
    private ServerSocket serverSocket;
    private Logger logger;
    private BufferedWriter out;
    private BufferedReader in;

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
            // Create a print writer
            out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            // Create a buffered reader
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
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
            byte[] ptext = message.getBytes(ISO_8859_1);
            String value = new String(ptext, UTF_8);
            out.write(value+ "\r\n");
            out.newLine();
            out.flush();
        } catch (IOException e) {
            logger.severe("Error sending message:" + e.getMessage());
        }
    }

    public String receiveMessage() {
        try {
            return in.readLine();
        } catch (IOException e) {
            logger.severe("Error receiving message");
            return null;
        }
    }

}
