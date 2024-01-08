from multiprocessing.connection import PipeConnection
import tempfile
import webview


def desktop(
    conn_send: PipeConnection,
    protocol: str = "http",
    host: str = "127.0.0.1",
    port: int = 5000,
    context: str = "show",
):
    def on_closed():
        conn_send.send("closed")

    win = webview.create_window("Demo", url=f"{protocol}://{host}:{port}/{context}")
    win.events.closed += on_closed
    webview.start(storage_path=tempfile.mkdtemp())
