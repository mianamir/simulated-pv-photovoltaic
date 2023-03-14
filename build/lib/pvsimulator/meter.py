
import logging
import pika
import random
import time


class Meter(object):

    def __init__(self, broker_host, broker_port, queue_name, username, password):
        self._logger = logging.getLogger("pvsimulator.simulator")
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._queue_name = queue_name
        self._credentials = pika.PlainCredentials(username, password)

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

            channel.queue_declare(queue=self._queue_name, durable=True)
            channel.confirm_delivery()
            self.__publish(channel)
            connection.close()
        except pika.exceptions.ConnectionClosedByBroker:
            self._logger.error("Connection was closed unexpectedly")
        except pika.exceptions.AMQPChannelError as err:
            self._logger.error(f"Caught a channel error: {err}, stopping...")
        except pika.exceptions.AMQPConnectionError:
            self._logger.error("Unable to connect to broker")
    
    def __publish(self, channel):
        self._logger.info("Generating raw PV values")
        while True:
            value = random.uniform(0, 9000)

            try:
                channel.basic_publish(
                    exchange='', 
                    routing_key='raw', 
                    body=f"{value:.2f}",
                    mandatory=True,
                    properties=pika.BasicProperties(
                        delivery_mode = 2,
                    )
                )
                self._logger.info(f"Sent {value:.2f}")

                time.sleep(2)
            except pika.exceptions.UnroutableError:
                self._logger.warn('Message was returned')
                continue
            except KeyboardInterrupt as ex:
                self._logger.info("Operation stopped by user")
                break
