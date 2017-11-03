# import required modules
import socket
import threading
import signal
from time import gmtime, strftime, localtime
import utils
import sys
import logging


class Server:
    """
    Main Proxy Server Class
    """

    def __init__(self, config):
        """
        Initializes a server object
        """
        self.__clients = {}  # dictionary to store all the active connections
        signal.signal(signal.SIGINT, self.shutdown)  # execute shutdown method on Ctrl + C
        # create and setup TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config = config
        self.setup_socket(config)

    def setup_socket(self, config):
        """
        Sets up the reuse of socket and binds to public host and a port
        :param config: Server configuration
        :return: None
        """
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((config['HOST_NAME'], config['BIND_PORT']))
        self.server_socket.listen(10)

    def log(self, log_level, client, msg):
        """
        Logs messages to appropriate stream
        :param log_level: level of priority of message(WARNING, INFO, ERROR)
        :param client: client corresponding to the message
        :param msg: message to be logged
        :return: None
        """
        logger_dict = {
            'CurrentTime': strftime("%a, $d %b %Y %X", localtime()),
            'ThreadName': threading.current_thread().getName()
        }
        if client == -1:
            formatted_message = msg
        else:
            formatted_message = '{0}: {1} {2}'.format(client[0], client[1], msg)

        logging.debug('%s', utils.colorize_log(log_level, formatted_message), extra=logger_dict)

    def shutdown(self, signum, frame):
        """
        Handles closing of the server
        :return: None
        """
        self.log('WARNING', -1, 'Shutting down normally ...')
        main_thread = threading.current_thread()

        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        self.server_socket.close()
        sys.exit(0)

    def listen(self):
        """
        Listens for connections to the server
        :return: None
        """
        print('Proxy Server started on {}:{}'.format(self.config['HOST_NAME'],
                                                     self.config['BIND_PORT']))
        while True:
            (client_socket, client_address) = self.server_socket.accept()
            d = threading.Thread(name=self._get_client_name(client_address),
                                 target=self.proxy_thread,
                                 args=(client_socket, client_address))
            d.setDaemon(True)
            d.start()
        self.shutdown(0,  0)

    def _get_client_name(self, client_addr):
        """
        Returns client name
        :param client_addr: address of client
        :return: client_name: string
        """
        return "Client" + str(client_addr)

    def proxy_thread(self, conn, client_addr):
        """
        Handles connections from browsers
        :param conn:
        :param client_addr:
        :return:
        """
        req = conn.recv(self.config['MAX_REQUEST_LENGTH'])
        # print(req)
        line1 = req.split(b'\n')[0]
        url = line1.split(b' ')[1]

        self.log("INFO", client_addr, "Request: " + str(line1))

        http_pos = url.find(b'://')
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]
        port_pos = temp.find(b':')
        webserver_pos = temp.find(b'/')
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[port_pos + 1:])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.config['CONNECTION_TIMEOUT'])
            s.connect((webserver, port))
            s.sendall(req)

            while True:
                data = s.recv(self.config['MAX_REQUEST_LENGTH'])
                if len(data) > 0:
                    conn.send(data)
                else:
                    break
            s.close()
            conn.close()
        except socket.error as error_msg:
            self.log('ERROR', client_addr, error_msg)
            if s:
                s.close()
            if conn:
                conn.close()
            self.log("WARNING", client_addr, "Peer Reset " + str(line1))


if __name__ == '__main__':
    config = {
        "HOST_NAME": "0.0.0.0",
        "BIND_PORT": 12345,
        "MAX_REQUEST_LENGTH": 1024,
        "CONNECTION_TIMEOUT": 5
    }

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(CurrentTime)-10s] (%(ThreadName)-10s) %(message)s')

    server = Server(config)
    server.listen()
