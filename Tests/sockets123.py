import requests


ipv4API1 =  'https://icanhazip.com/'

r = requests.get(ipv4API1)
r_new = r.text.split('\n')
print(r)
print(r_new)