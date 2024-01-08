from server import Server
from api import api
from app import web_app
import multiprocessing
from desktop import desktop

# Making a web app from our API
web_app(api)

if __name__ == '__main__':

    # Starting a new process
    conn_recv, conn_send = multiprocessing.Pipe()
    
    # Starting desktop window
    deskop_window = multiprocessing.Process(target=desktop, kwargs={"conn_send": conn_send, "context": "show"})
    deskop_window.start()

    instance = Server(app="main:api")
    instance.run()

    window_status = ''
    while 'closed' not in window_status:
        # get a unit of work
        window_status = conn_recv.recv()
        # report
        print(f'got {window_status}', flush=True)

    instance.stop()