import pika, os


rabbitmq_username=os.environ.get("RABBITMQ_DEFAULT_USER")
rabbitmq_password=os.environ.get("RABBITMQ_DEFAULT_PASS")

credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)

def produce(host, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key="check_interfaces")

    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body)

    connection.close()

if __name__ == "__main__":
    produce("localhost", "192.168.255.15")
