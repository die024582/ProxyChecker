import json
import logging
import requests
import colorama

colorama.init()

def init():
	LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
	logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt="%H:%M:%S")
	log = logging.getLogger(__name__)

	return log

def check_proxy(proxy):
	url = "https://api.ipify.org/?format=json"
	proxy_data = {
		'http': proxy,
		'https': proxy
	}

	try:
		resp_with = requests.get(url, proxies=proxy_data, timeout=5)
		resp_none = requests.get(url)
	except KeyboardInterrupt:
		quit()
	except:
		log.error(f"{proxy} | {colorama.Fore.RED} Proxy is down. {colorama.Style.RESET_ALL}")
		return

	json_none = json.loads(resp_none.text)
	json_with = json.loads(resp_with.text)

	if json_none['ip'] == json_with['ip']:
		log.error(f"{proxy} | {colorama.Fore.RED} Bad proxy; IPs match. {colorama.Style.RESET_ALL}")
		return
	else:
		log.info(f"{proxy} | {colorama.Fore.GREEN} Proxy works. Time: {resp_with.elapsed.total_seconds()}s {colorama.Style.RESET_ALL}")
		return proxy

if __name__ == "__main__":
	log = init()

	for i in open('proxies.txt', 'r').read().split("\n"):
		proxy = check_proxy(i)
		if proxy:
			file = open('output.txt', 'a')
			file.write(proxy + "\n")
			file.close()
