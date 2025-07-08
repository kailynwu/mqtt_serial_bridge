import os
import json
import logging
import serial
import paho.mqtt.client as mqtt
from serial.tools import list_ports


def setup_logging():
    """设置日志记录，将日志保存到 log 目录下的文件中"""
    log_dir = 'log'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'mqtt_serial_bridge.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def get_mqtt_config():
    """获取 MQTT 配置，如果配置文件不存在则让用户输入"""
    config_dir = 'config'
    mqtt_config_file = os.path.join(config_dir, 'mqtt_config.json')
    if os.path.exists(mqtt_config_file):
        try:
            with open(mqtt_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"读取 MQTT 配置文件失败: {e}")
    os.makedirs(config_dir, exist_ok=True)
    broker = input("请输入 MQTT 代理服务器地址: ").strip()
    port = int(input("请输入 MQTT 代理服务器端口号: ").strip())
    username = input("请输入 MQTT 用户名 (留空则不使用认证): ").strip()
    password = input("请输入 MQTT 密码 (留空则不使用认证): ").strip()
    mqtt_config = {
        "broker": broker,
        "port": port,
        "username": username if username else None,
        "password": password if password else None
    }
    try:
        with open(mqtt_config_file, 'w', encoding='utf-8') as f:
            json.dump(mqtt_config, f, indent=2)
        logging.info("MQTT 配置保存成功")
    except Exception as e:
        logging.error(f"保存 MQTT 配置文件失败: {e}")
    return mqtt_config


def get_serial_config():
    """获取串口配置"""
    config_dir = 'config'
    serial_config_file = os.path.join(config_dir, 'serial_config.json')
    if os.path.exists(serial_config_file):
        try:
            with open(serial_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"读取串口配置文件失败: {e}")
    return []


def on_connect(client, userdata, flags, rc):
    """MQTT 连接成功回调函数"""
    if rc == 0:
        logging.info("MQTT 连接成功")
        serial_configs = userdata
        for config in serial_configs:
            receive_topic = config["receive_topic"]
            client.subscribe(receive_topic)
            logging.info(f"订阅接收主题: {receive_topic}")
    else:
        logging.error(f"MQTT 连接失败，错误码: {rc}")


def on_message(client, userdata, msg):
    """MQTT 消息接收回调函数"""
    try:
        serial_configs = userdata
        for config in serial_configs:
            if msg.topic == config["receive_topic"]:
                port = config["selected_port"]
                baudrate = config["baudrate"]
                try:
                    ser = serial.Serial(port, baudrate, timeout=1)
                    ser.write(msg.payload)
                    logging.info(f"从 MQTT 接收主题 {msg.topic} 接收到消息，已发送到串口 {port}: {msg.payload}")
                    ser.close()
                except Exception as e:
                    logging.error(f"向串口 {port} 发送消息失败: {e}")
    except Exception as e:
        logging.error(f"处理 MQTT 消息时出错: {e}")


def serial_to_mqtt(client, serial_config):
    """将串口数据发送到 MQTT 主题"""
    port = serial_config["selected_port"]
    baudrate = serial_config["baudrate"]
    send_topic = serial_config["send_topic"]
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        logging.info(f"已打开串口 {port}")
        while True:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                client.publish(send_topic, data)
                logging.info(f"从串口 {port} 读取到数据，已发送到 MQTT 发送主题 {send_topic}: {data}")
    except Exception as e:
        logging.error(f"读取串口 {port} 数据时出错: {e}")
    finally:
        if ser.is_open:
            ser.close()


if __name__ == "__main__":
    setup_logging()
    mqtt_config = get_mqtt_config()
    serial_configs = get_serial_config()

    client = mqtt.Client()
    if mqtt_config["username"] and mqtt_config["password"]:
        client.username_pw_set(mqtt_config["username"], mqtt_config["password"])

    client.on_connect = on_connect
    client.on_message = on_message
    client.user_data_set(serial_configs)

    try:
        client.connect(mqtt_config["broker"], mqtt_config["port"], 60)
        client.loop_start()

        for config in serial_configs:
            import threading
            serial_thread = threading.Thread(target=serial_to_mqtt, args=(client, config))
            serial_thread.daemon = True
            serial_thread.start()

        while True:
            pass
    except KeyboardInterrupt:
        logging.info("程序手动终止")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
        client.loop_stop()
        client.disconnect()
