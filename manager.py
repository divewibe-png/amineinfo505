
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import time

PORT = 5000
PASSWORD = os.environ.get("TROJAN_PASSWORD", "/amineinfo")
WS_PATH = os.environ.get("XRAY_WS_PATH", "/@amine_dz505")

XRAY_BIN = "/usr/local/bin/xray"
CONFIG_PATH = "/usr/local/etc/xray/config.json"


def log(message):
    print(f"[TROJAN] {message}", flush=True)


def build_and_save_config():
    config = {
        "log": {
            "loglevel": "warning"
        },
        "inbounds": [
            {
                "port": PORT,
                "listen": "127.0.0.1",
                "protocol": "trojan",
                "settings": {
                    "clients": [
                        {
                            "password": PASSWORD
                        }
                    ]
                },
                "streamSettings": {
                    "network": "ws",
                    "security": "none",
                    "wsSettings": {
                        "path": WS_PATH
                    }
                }
            }
        ],
        "outbounds": [
            {
                "protocol": "freedom",
                "tag": "direct"
            },
            {
                "protocol": "blackhole",
                "tag": "block"
            }
        ]
    }

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)

    log(f"Trojan configuration generated on port {PORT}")


def main():
    build_and_save_config()

    command = [
        XRAY_BIN,
        "run",
        "-config",
        CONFIG_PATH
    ]

    while True:
        process = subprocess.Popen(command)
        exit_code = process.wait()

        log(f"Xray exited with code {exit_code}; restarting in 2 seconds.")
        time.sleep(2)


if __name__ == "__main__":
    main()
