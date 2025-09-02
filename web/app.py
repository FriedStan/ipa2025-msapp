"""Flask App"""

import os

from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

APP = Flask(__name__)


MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")

CLIENT = MongoClient(MONGO_URI)
MYDB = CLIENT[DB_NAME]
MYCOL = MYDB["routers"]
INFO = MYDB["interface_status"]


@APP.route("/")
def main():
    return render_template("index.html", data=MYCOL.find())


@APP.route("/add", methods=["POST"])
def add_router():
    router_ipaddr = request.form.get("router_ipaddr")
    username = request.form.get("username")
    password = request.form.get("password")

    if router_ipaddr and username and password:
        router_info = {
            "router_ipaddr": router_ipaddr,
            "username": username,
            "password": password,
        }
        MYCOL.insert_one(router_info)
    return redirect("/")


@APP.route("/delete", methods=["POST"])
def delete_router():
    id = request.form.get("_id")
    try:
        print(f"Del: {id}")
        MYCOL.delete_one({"_id": ObjectId(id)})
    except Exception:
        pass
    return redirect(url_for("main"))


@APP.route("/router/<string:ip>")
def show_interfaces(ip):
    return render_template("show_interface.html", data=INFO.find({"router_ip": ip}), router_ip=ip)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080)
