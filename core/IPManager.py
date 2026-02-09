import requests
import json
import time


class IPManager:
    def __init__(self, ip_get_host, filepath='ip.txt'):
        self.filepath = filepath
        self.ip_get_host = ip_get_host
        self.ip = None
        self.get_time = None
        self.fetch_and_save()


    def fetch_and_save(self):
        """获取公网IP并保存到文件"""
        try:
            response = requests.get(self.ip_get_host, timeout=5)
            data = json.loads(response.text)
            # 如果数据格式不正确，直接返回None
            if 'data' not in data or 'ip' not in data['data']:
                print("数据格式不正确")
                return None

            self.ip = data['data']['ip']
            self.get_time = int(time.time())

            with open(self.filepath, 'w') as f:
                f.write(f"{self.ip}\n{self.get_time}")

            print(f"IP已保存: {self.ip}")
            return self.ip, self.get_time
        except Exception as e:
            print(f"获取IP失败: {e}")
            return None

    def read(self):
        """读取IP文件，如果有缓存数据则返回缓存数据"""
        if self.ip is not None and self.get_time is not None:
            return {
                'ip': self.ip,
                'get_time': self.get_time
            }
        try:
            with open(self.filepath, 'r') as f:
                lines = f.read().strip().split('\n')
                return {
                    'ip': lines[0],
                    'get_time': lines[1] if len(lines) > 1 else None
                }
        except FileNotFoundError:
            print("IP文件不存在")
            return None
        except Exception as e:
            print(f"读取失败: {e}")
            return None

    def get_ip_time(self):
        return self.get_time
