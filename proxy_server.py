# import required modules
import socket
import threading
import signal
from time import gmtime, strftime, localtime
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

        logging.debug('%s', (None, log_level, formatted_message), extra=logger_dict)

    def shutdown(self):
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
        while True:
            (client_socket, client_address) = self.server_socket.accept()
            d = threading.Thread(name=self._get_clientname(client_address),
                                 target=self.proxy_thread,
                                 args=(client_socket, client_address))
            d.setDaemon(True)
            d.start()
        self.shutdown()

    def _get_client_name(self, client_addr):
        """
        Returns client name
        :param client_addr: address of client
        :return: client_name: string
        """
        return "Client" + str(client_addr)

