from fastapi import FastAPI
from nicegui import ui

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@ui.page("/show")
def show():
    ui.image("https://picsum.photos/id/377/640/360")
