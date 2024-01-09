from server import Server
from api.main import app
from app.app import web_app
import multiprocessing
from app.desktop import desktop

# Making a web app from our API
web_app(app)

if __name__ == '__main__':

    # Starting a new process
    conn_recv, conn_send = multiprocessing.Pipe()
    
    # Starting desktop window
    deskop_window = multiprocessing.Process(target=desktop, kwargs={"conn_send": conn_send, "context": ""})
    deskop_window.start()

    instance = Server(app="main:app")
    instance.run()

    window_status = ''
    while 'closed' not in window_status:
        # get a unit of work
        window_status = conn_recv.recv()
        # report
        print(f'got {window_status}', flush=True)

    instance.stop()