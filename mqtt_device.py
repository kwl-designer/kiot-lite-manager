from core.MQTTDevice import MQTTDevice
from core.Config import Config

broker_host = "111.230.204.179"

if __name__ == "__main__":

    config = Config('config.conf')
    publisher = MQTTDevice(
        device_id=config.get_device_id(),
        broker=config.get_broker_host(),
        port=config.get_broker_port(),
        username=config.get_broker_username(),
        password=config.get_broker_password(),
        ip_dns=config.get_dns_ip()
    )
    publisher.start(interval=30)