import multiprocessing
from uvicorn import Config, Server


class UvicornServer(multiprocessing.Process):
    def __init__(
        self,
        app: str,
        host: str = "127.0.0.1",
        port: int = 8080,
        log_level: str = "debug",
    ):
        super().__init__()
        self.app = app
        self.host = host
        self.port = port
        self.log_level = log_level

    def stop(self):
        self.terminate()

    def run(self, *args, **kwargs):
        Server(Config(
            app=self.app, host=self.host, port=self.port, log_level=self.log_level
        )).run()
