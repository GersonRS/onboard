import socket
import time
import random

from .common import get_config, DEFAULT_CONFIG_PATH

if __name__ == "__main__":
    config = get_config(["-c", DEFAULT_CONFIG_PATH.as_posix()])
    mongo = config["mongo"]
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((mongo["host"], mongo["port"]))
                print("Successfully started mongo")
                break
        except socket.error:
            print("Waiting for mongo")
            time.sleep(0.5 + (random.randint(0, 100) / 1000))
