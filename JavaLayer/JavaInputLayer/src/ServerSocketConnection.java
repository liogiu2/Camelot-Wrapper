import java.net.Socket;
import java.io.IOException;
import java.util.logging.Logger;
import java.net.ServerSocket;

public class ServerSocketConnection {

    private int port;
    private Socket socket;
    private ServerSocket serverSocket;
    private Logger logger;

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

}
