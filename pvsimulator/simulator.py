
import csv
import logging
import pika
import random
from datetime import datetime


class Simulator(object):
    def __init__(self, broker_host, broker_port, queue_name, username, password, outfile):
        self._logger = logging.getLogger("pvsimulator.simulator")
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._queue_name = queue_name
        self._credentials = pika.PlainCredentials(username, password)
        self._outfile = outfile
        
    def start(self):

        try:

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._broker_host, 
                    port=self._broker_port,
                    credentials=self._credentials
                    )
            )
            channel = connection.channel()

            channel.basic_qos(prefetch_count=1)
            channel.queue_declare(queue=self._queue_name, durable=True)


            channel.basic_consume(
                queue=self._queue_name, 
                on_message_callback=self.__receive)
            self._logger.info(f"Reading messages from {self._queue_name}")
            try:
                channel.start_consuming()
            except KeyboardInterrupt as ex:
                channel.stop_consuming()
                connection.close()
                self._logger.info("Operation stoped by user. Connection closed")
        
        except pika.exceptions.ConnectionClosedByBroker as err:
            self._logger.error("Connection was closed unexpectedly")
        except pika.exceptions.AMQPChannelError as err:
            self._logger.error(f"Caught a channel error: {err}, stopping...")
        except pika.exceptions.AMQPConnectionError as err:
            self._logger.error("Unable to connect to broker")  
    
    def __receive(self, channel, method, properties, body):

        self._logger.info(f"Received {body}")

        meter_value = float(body)

        pv_value = random.uniform(0, 9000)

        record = {
            "timestampt": datetime.now(),
            "meter_value": meter_value,
            "pv_value": pv_value,
            "sum": meter_value + pv_value
        }
        self.__write_record(record)

        channel.basic_ack(delivery_tag = method.delivery_tag)

    def __write_record(self, record):

        self._logger.info(f"Writting record to file")
        with open(self._outfile, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            writer.writerow(record)
        self._logger.info(f"Record {record} written to file pv-simulator-output.csv")
        
        