import os

from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)


mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]


@app.route("/")
def main():
    return render_template("index.html", data=mycol.find())

@app.route("/add", methods=["POST"])
def add_router():
    router_ipaddr = request.form.get("router_ipaddr")
    username = request.form.get("username")
    password = request.form.get("password")

    if router_ipaddr and username and password:
        router_info = {"router_ipaddr": router_ipaddr, "username": username, "password": password}
        mycol.insert_one(router_info)
    return redirect("/")

@app.route("/delete", methods=['POST'])
def delete_router():
    id = request.form.get("_id")
    try:
        print(f"Del: {id}")
        mycol.delete_one({"_id": ObjectId(id)})
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
