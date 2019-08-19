import logging
import pika
import ssl

logging.basicConfig(level=logging.INFO)
context = ssl.create_default_context(
    cafile="./ca_certificate.pem")
context.load_cert_chain("./client_certificate.pem",
                        "./client_key.pem")
context.check_hostname = False
ssl_options = pika.SSLOptions(context, "localhost")
credentials = pika.PlainCredentials('admin', 'E9YMkr4s2qc')
conn_params = pika.ConnectionParameters(port=31894,
                                        host="localhost",
                                        credentials=credentials,
                                        ssl_options=ssl_options)

with pika.BlockingConnection(conn_params) as conn:
    ch = conn.channel()
    ch.queue_declare("publishing")
    ch.basic_publish("", "publishing", "Hello, world!")
    print(ch.basic_get("publishing"))
    conn.close()
