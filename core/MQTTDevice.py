import paho.mqtt.client as mqtt
import json
import time
import socket

class MQTTDevice:
    def __init__(self, device_id, broker='localhost', port=1883,
                 username=None, password=None, ip_dns = '8.8.8.8'):
        self.device_id = device_id
        self.broker = broker
        self.port = port
        self.topic = f"device/{device_id}/status"
        self.connected = False
        self.ip_dns = ip_dns
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        # 如果有用户名密码
        if username and password:
            self.client.username_pw_set(username, password)


    def get_ip(self):
        """获取本机IP地址"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((self.ip_dns, 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"连接成功，状态码: {reason_code}")
        self.connected = True

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        print(f"连接断开，状态码: {reason_code}")
        self.connected = False

    def publish_once(self):
        """发布一次消息"""
        if not self.connected:
            print("未连接，跳过本次发布")
            return

        data = {
            "ip": self.get_ip(),
            "timestamp": int(time.time())
        }
        payload = json.dumps(data)
        result = self.client.publish(self.topic, payload)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"已发布到 {self.topic}: {payload}")
        else:
            print(f"发布失败，错误码: {result.rc}")

    def connect_with_retry(self):
        """带重试的连接"""
        while True:
            try:
                print(f"尝试连接到 {self.broker}:{self.port}")
                self.client.connect(self.broker, self.port, keepalive=60)
                break
            except Exception as e:
                print(f"连接失败: {e}，10秒后重试...")
                time.sleep(10)

    def start(self, interval=30):
        """持续发布，每隔interval秒发送一次"""
        self.connect_with_retry()
        self.client.loop_start()
        # 等待1s确保连接成功
        time.sleep(1)
        print(f"开始发布数据到 {self.topic}")

        try:
            while True:
                self.publish_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n停止发布")
        finally:
            self.client.loop_stop()
            self.client.disconnect()


# if __name__ == "__main__":
#     # 使用示例
#     publisher = MQTTDevice(
#         device_id="A11",
#         broker=broker_host,
#         username="mqtt_user",
#         password="kwl123456."
#     )
#     publisher.start(interval=5)
