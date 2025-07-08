# MQTT串口服务器
## 项目概述
本项目旨在实现一个 MQTT 串口服务器，通过 MQTT 协议将串口数据与 MQTT 代理服务器进行双向通信。该项目包含两个主要脚本：serial_detector.py 用于检测可用串口并配置串口信息，mqtt_serial_bridge.py 用于建立 MQTT 连接并实现串口与 MQTT 之间的数据桥接。
## 功能特性
自动检测可用串口：根据不同操作系统自动检测可用的串口设备。
配置管理：允许用户配置串口和 MQTT 代理服务器的相关参数，并将配置保存到 JSON 文件中。
双向数据传输：实现串口数据与 MQTT 主题之间的双向传输，支持多个串口设备同时工作。
日志记录：将程序运行过程中的重要信息和错误信息记录到日志文件中。
## 目录结构
```plaintext
MQTT串口服务器/
├── .idea/                   # IDE配置文件
│   ├── modules.xml
│   ├── workspace.xml
│   ├── misc.xml
│   ├── MarsCodeWorkspaceAppSettings.xml
│   └── .gitignore
├── config/                  # 配置文件目录
│   ├── mqtt_config.json     # MQTT配置文件
│   └── serial_config.json   # 串口配置文件
├── log/                     # 日志文件目录
│   └── mqtt_serial_bridge.log
├── serial_detector.py       # 串口检测和配置脚本
├── mqtt_serial_bridge.py    # MQTT串口桥接脚本
└── README.md                # 项目说明文档
```
## 安装依赖
在运行项目之前，需要安装所需的 Python 库。可以使用以下命令进行安装：

```bash
pip install paho-mqtt pyserial
```
## 配置说明
MQTT 配置
MQTT 配置信息存储在 config/mqtt_config.json 文件中，示例内容如下：
```json
{
  "broker": "192.168.1.105",
  "port": 1883,
  "username": null,
  "password": null
}
```
broker：MQTT 代理服务器的地址。
port：MQTT 代理服务器的端口号。
username：MQTT 认证的用户名，留空则不使用认证。
password：MQTT 认证的密码，留空则不使用认证。
## 串口配置
串口配置信息存储在 config/serial_config.json 文件中，示例内容如下：

```json
[
  {
    "system": "Linux",
    "selected_port": "/dev/ttyACM0",
    "baudrate": 115200,
    "send_topic": "com1send",
    "receive_topic": "com1receive"
  }
]
```
system：当前操作系统类型。
selected_port：选择使用的串口设备。
baudrate：串口通信的波特率。
send_topic：将串口数据发送到 MQTT 的主题。
receive_topic：从 MQTT 接收数据并发送到串口的主题。
## 使用方法
1. 检测可用串口并配置
运行 serial_detector.py 脚本，按照提示输入所需信息：

```bash
python serial_detector.py
```
脚本会自动检测可用串口，并让用户选择要使用的串口、波特率、发布主题和订阅主题。用户可以根据需要添加多个串口配置，配置完成后会保存到 config/serial_config.json 文件中。
2. 启动 MQTT 串口桥接
运行 mqtt_serial_bridge.py 脚本，建立 MQTT 连接并实现串口与 MQTT 之间的数据桥接：

```bash
python mqtt_serial_bridge.py
```
脚本会读取 config/mqtt_config.json 和 config/serial_config.json 文件中的配置信息，连接到 MQTT 代理服务器，并启动多个线程处理不同串口的数据传输。
## 日志记录
程序运行过程中的重要信息和错误信息会记录到 log/mqtt_serial_bridge.log 文件中，方便后续排查问题。
## 注意事项
请确保 MQTT 代理服务器正常运行，并且网络连接稳定。
如果需要使用 MQTT 认证，请在 config/mqtt_config.json 文件中填写正确的用户名和密码。
在配置串口信息时，请确保所选的串口设备和波特率与实际情况一致。
## 贡献
如果你对本项目有任何建议或改进意见，欢迎提交 issue 或 pull request。
## 许可证
本项目采用 `BSD - 2 - Clause` 许可证。以下是许可证的详细内容：

```plaintext
BSD 2-Clause License

Copyright (c) 2025, kailynwu
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```