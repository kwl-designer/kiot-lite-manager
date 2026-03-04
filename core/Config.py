import configparser


class Config:
    def __init__(self, config_file='config.conf'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        self.net = self.get_device_net()
        self.device_id = self.get_mac_address(self.net)
    
    def get_mac_address(self, interface="eth0"):
        try:
            with open(f"/sys/class/net/{interface}/address") as f:
                return f.read().strip().replace(":", "")
        except:
            return "unknown"
    
    def get_broker_host(self):
        return self.config.get('broker', 'host')

    def get_broker_port(self):
        return self.config.getint('broker', 'port')

    def get_broker_username(self):
        return self.config.get('broker', 'username')

    def get_broker_password(self):
        return self.config.get('broker', 'password')

    def get_device_net(self):
        return self.config.get('device', 'net')

    def get_device_id(self):
        return self.device_id

    def get_dns_ip(self):
        return self.config.get('network', 'dns_ip')

    def get_ip_get_host(self):
        return self.config.get('network', 'ip_get_host')