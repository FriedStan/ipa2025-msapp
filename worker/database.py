import os
import time
from datetime import datetime, timezone

from pymongo import MongoClient


def insert_interface_status(data):
    MONGO_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_LOCATION = os.environ.get("MONGO_LOCATION")
    mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_LOCATION}:27017/"
    db_name = os.environ.get("DB_NAME")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    interface_status = db["interface_status"]

    ts = time.time()
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    data["timestamp"] = dt

    interface_status.insert_one(data)
    router_ip = data.get("router_ipaddr")

    print(f"Stored interface status for {router_ip}")
