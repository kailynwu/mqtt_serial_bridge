import sys
import os
import json
from serial.tools import list_ports


def get_system_type():
    """获取当前系统类型"""
    platform = sys.platform
    if platform.startswith('win'):
        return 'Windows'
    elif platform.startswith('linux'):
        return 'Linux'
    elif platform.startswith('darwin'):  # macOS 系统
        return 'macOS'
    else:
        return 'Unknown'


def get_available_ports():
    """获取所有可用串口列表"""
    try:
        ports = list(list_ports.comports())
        return [port.device for port in ports]
    except Exception as e:
        return f"获取串口失败: {str(e)}"


def save_config(config):
    """保存配置到config目录下的配置文件"""
    try:
        # 创建config目录（如果不存在）
        os.makedirs('config', exist_ok=True)
        # 保存配置到JSON文件
        with open(os.path.join('config', 'serial_config.json'), 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("配置保存成功，路径: config/serial_config.json")
    except Exception as e:
        print(f"配置保存失败: {str(e)}")


if __name__ == "__main__":
    system = get_system_type()
    ports = get_available_ports()

    print(f"当前系统: {system}")
    print(f"可用串口: {ports if isinstance(ports, list) else '无可用串口'}")

    config_list = []  # 存储多个串口配置的列表

    if isinstance(ports, list) and len(ports) > 0:
        while True:  # 循环添加多个配置
            # 用户选择指定串口（保持原有逻辑）
            while True:
                selected_port = input("请输入要使用的串口（如COM3或/dev/ttyUSB0）: ").strip()
                if selected_port in ports:
                    break
                print(f"错误：{selected_port} 不在可用串口列表中，请重新输入")

            # 用户输入波特率（保持原有逻辑）
            while True:
                baudrate = input("请输入波特率（如9600、115200）: ").strip()
                if baudrate.isdigit() and int(baudrate) > 0:
                    baudrate = int(baudrate)
                    break
                print("错误：波特率必须是正整数，请重新输入")

            # 用户输入发布主题（验证非空）
            while True:
                publish_topic = input("请输入发布主题（如 serial/send/data）: ").strip()
                if publish_topic:
                    break
                print("错误：发布主题不能为空，请重新输入")

            # 用户输入订阅主题（验证非空）
            while True:
                subscribe_topic = input("请输入订阅主题（如 serial/receive/commands）: ").strip()
                if subscribe_topic:
                    break
                print("错误：订阅主题不能为空，请重新输入")

            # 构造配置字典并添加到列表
            config_list.append({
                "system": system,
                "selected_port": selected_port,
                "baudrate": baudrate,
                "send_topic": publish_topic,
                "receive_topic": subscribe_topic
            })

            # 询问是否继续添加
            continue_add = input("是否继续添加新的串口配置？(y/n): ").strip().lower()
            if continue_add not in ['y', 'yes']:
                break

        if config_list:  # 有配置时保存
            save_config(config_list)
        else:
            print("未添加任何配置")
    else:
        print("无可用串口，无法进行配置")