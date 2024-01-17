import os
import sqlite3

from arcgis.gis import GIS
from database import Database
from flask import Blueprint, redirect, render_template, request, url_for
from models import Portals
from sqlalchemy import select

admin = Blueprint("admin", __name__, url_prefix="/admin")

db_session = Database(schema="admin")


@admin.route("/")
def hello_world():
    return "Hello, World!"


@admin.route("/portals")
def portals():
    return render_template("portals.html")
    page = request.args.get("page", 1, type=int)
    rows = request.args.get("rows", 10, type=int)
    stmt = select(Portals).limit(rows).offset((page - 1) * rows)
    portal_list = [portal.to_dict() for portal in db_session.session.execute(stmt)]
    return render_template("portals.html", portals=portal_list)
