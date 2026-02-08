# iot设备mqtt管理

## 介绍

本项目是一个基于mqtt的iot设备管理项目，包含服务器端和设备端两个部分. 当前实现包括：
- 设备上传设备id和ip、时间戳
- 服务器将数据存入redis供其他服务获取

使用前提：已经在本地或者服务器上安装好了mqtt broker，如mosquitto

## 服务器管理

依赖`requirements.txt`
```shell
pip install -r requirements.txt
```

运行：
```shell
python mqtt_serv.py
```

## 设备管理

依赖`requirements-device.txt`
```shell
pip install -r requirements-device.txt
```

运行：
```shell
python mqtt_device.py
```
## 配置文件

配置文件为`config.conf`，包含mqtt broker的地址、端口、用户名、密码等信息。

目录中有一个`config.conf.example`文件，可以复制重命名为`config.conf`并修改其中的参数。

## 服务化

可以将脚本作为linux的服务随系统启动