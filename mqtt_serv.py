from core.MQTTSubscriber import MQTTSubscriber
from core.Config import Config

if __name__ == "__main__":
    config = Config('config.conf')

    server = MQTTSubscriber(
        broker=config.get_broker_host(),
        port=config.get_broker_port(),
        username=config.get_broker_username(),
        password=config.get_broker_password()
    )
    server.start()