import requests
import re

def get_external_ip():
    ip_dns = "http://checkip.dyndns.org"
    ip_regex_pattern = "(?:[0-9]{1,3}\.){3}[0-9]{1,3}"

    res = requests.get(ip_dns).text
    ip = re.search(ip_regex_pattern, res).group()

    return ip
