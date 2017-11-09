from proxy_server import Server

if __name__ == '__main__':
    config = {
        "HOST_NAME": "0.0.0.0",
        "BIND_PORT": 1337,
        "MAX_REQUEST_LENGTH": 1024,
        "CONNECTION_TIMEOUT": 10
    }

    server = Server(config)
    server.listen()
