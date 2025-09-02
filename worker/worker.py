import pika
import os
import time
import json
from workload import show_interface

# from database import insert_interface_status

RABBITMQ_USERNAME = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_DEFAULT_PASS")

CREDENTIALS = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    router_ip = data.get("router_ipaddr")
    interfaces_data = show_interface(
        router_ip, data.get("username"), data.get("password")
    )

    print(f"Received job for router {router_ip}")
    print(json.dumps(interfaces_data, indent=2))

    # insert_interface_status(
    #     {"router_ip": router_ip, "timestamp": "", "interfaces": interfaces_data}
    # )

    time.sleep(body.count(b"."))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume(host):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, credentials=CREDENTIALS)
    )
    channel = connection.channel()

    channel.queue_declare(queue="router_jobs")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="router_jobs", on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    for attempt in range(10):
        try:
            print(f"Connecting to RabbitMQ (try {attempt})...")
            consume("rabbitmq")
            break
        except Exception as e:
            print(f"Failed: {e}")
            time.sleep(5)
    else:
        print("Could not connect after 10 attempts")
        exit(1)
