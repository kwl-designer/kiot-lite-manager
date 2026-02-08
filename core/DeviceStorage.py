import redis

class DeviceStorage:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        self.client.delete(key)


# 使用示例
# storage = DeviceStorage()
# storage.set('name', 'Alice')
# print(storage.get('name'))  # 输出: Alice