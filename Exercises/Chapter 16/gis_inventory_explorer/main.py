#!/usr/bin/env python3
# thanks
import multiprocessing


from nicegui import ui
from server import UvicornServer
from app_webview import start_window

from frontend import app

# Running NiceGUI
ui.run_with(app)

if __name__ == "__main__":
    conn_recv, conn_send = multiprocessing.Pipe()

    windowsp = multiprocessing.Process(target=start_window, kwargs={"conn_send": conn_send})
    windowsp.start()

    instance = UvicornServer(app="main:app")
    instance.start()

    window_status = ""
    while "closed" not in window_status:
        # get a unit of work
        window_status = conn_recv.recv()
        # report
        print(f"Window {window_status}", flush=True)

    instance.stop()