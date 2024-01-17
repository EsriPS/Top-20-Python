import contextlib
import time
import threading
import uvicorn

class Server:
    def __init__(
        self,
        app: str = None,
        host: str = "127.0.0.1",
        port: int = 5000,
        log_level: str = "info",
        reload: bool = False,
        uvicorn_config: uvicorn.Config = None,
    ):
        self.keep_running = True
        self.app = app
        self.host = host
        self.port = port
        self.log_level = log_level
        self.reload = reload
        self.uvicorn_config = uvicorn_config

    @property
    def server(self):
        if not self.uvicorn_config:
            uvicorn_config = uvicorn.Config(
                app=self.app, host=self.host, port=self.port, log_level=self.log_level, reload=self.reload
            )

        return uvicorn.Server(config=uvicorn_config)

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.server.run)
        thread.start()
        try:
            while not self.server.started:
                time.sleep(1e-3)
            yield
            while self.keep_running:
                time.sleep(1e-3)
        finally:
            self.server.should_exit = True
            thread.join()

    def run(self):
        with self.run_in_thread():
            while self.keep_running:
                pass


if __name__ == "__main__":
    Server(app="api:api", host="127.0.0.1", port=5000, log_level="info").run()
