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

connection = pika.BlockingConnection(conn_params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='publishing') # Declare a queue
def callback(ch, method, properties, body):
  print(" [x] Received " + str(body))

channel.basic_consume('publishing',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
