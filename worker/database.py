import os, time
from datetime import datetime, timezone

from pymongo import MongoClient

def insert_interface_status(data):
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    interface_status = db["interface_status"]

    ts = time.time()
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    data["timestamp"] = dt

    interface_status.insert_one(data)

    print(f"Stored interface status for {data.get("router_ip")}")
