import paho.mqtt.client as mqtt
from .DeviceStorage import DeviceStorage


class MQTTSubscriber:
    def __init__(self, broker='localhost', port=1883,
                 username=None, password=None):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # 如果有用户名密码
        if username and password and username != '' and password != '':
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.storage = DeviceStorage()  # 创建Redis存储实例

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"已连接，状态码: {reason_code}")
        client.subscribe("device/+/status")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        print(f"主题: {msg.topic}, 消息: {msg.payload.decode()}")
        # 存储到Redis
        if topic.endswith("/status"):
            # 提取device id，例如 "device/A11/status" -> "A11"
            device_id = topic.split('/')[1]
            key = f"device:{device_id}"
            value = msg.payload.decode()
            self.storage.set(key, value)
            print(f"已存储: {key} = {value}")

    def start(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_forever()


# 使用示例
# subscriber = MQTTSubscriber()
# subscriber.start()