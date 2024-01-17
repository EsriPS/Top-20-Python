import os
import sqlite3

from arcgis.gis import GIS
from flask import Blueprint, redirect, render_template, request, url_for

explorer = Blueprint("explorer", __name__, url_prefix="/")


@explorer.route("/")
def hello_world():
    return "Hello, World!"
