import time
import requests
from stem import Signal
from stem.control import Controller


proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

while True:
    with Controller.from_port(port = 9051) as c:
        c.authenticate()
        c.signal(Signal.NEWNYM)
        print(f"Your IP is : {requests.get('https://ident.me', proxies=proxies).text}")
        print("Changing IP Address in every 300 seconds (5min)....\n\n")
        time.sleep(300)

