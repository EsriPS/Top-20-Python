from admin import admin
from explorer import explorer
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

app.register_blueprint(admin.admin)
app.register_blueprint(explorer.explorer)

if __name__ == "__main__":
    app.run()
