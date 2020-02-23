import BaseHTTPServer
#import socketserver
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
import time
from datetime import datetime
from cachecontrol import CacheControl
import json
import webbrowser
from colorama import *
import bs4
from bs4 import BeautifulSoup
import socket
import sys
import time

s = requests.session()

USERNAME = 'Ratz' #USERNAME HERE

print(datetime.now().strftime(Fore.YELLOW + '[%H:%M:%S:%f]-[Welcome back {}]'.format(USERNAME)))
print('  ')
print(datetime.now().strftime(Fore.YELLOW + '[%H:%M:%S:%f]-[Charging data..]'))
print(' ')

profile = '' #paste email here
password = '' #paste password here
variants = ['113771'] #paste variant_id here, NOTE THAT YOU CAN ONLY ADD 1 VARIANT X TIME TO CART, YOU CAN`T CART MULTIPLE VARIANTS

print(datetime.now().strftime(Fore.GREEN + '[%H:%M:%S:%f]-[You chosen {}]'.format(profile)))
print(' ')
time.sleep(4)

while True:
    print('http://127.0.0.1:'+sys.argv[1])
    r_server= s.get('http://127.0.0.1:'+sys.argv[1])
    print('http://127.0.0.1:'+sys.argv[1])
    #print(r_server.text)

    jsonData = r_server.text
    jsonToPython = json.loads(jsonData)
    #print(jsonToPython)
    #print(jsonToPython['cookies'])

    for x in jsonToPython['cookies']:
        cook = requests.cookies.create_cookie(x['name'],x['value'])
        print(cook)
        s.cookies.set_cookie(cook)

    print(s.cookies)

#POPULATE CHECK

print(datetime.now().strftime(Fore.YELLOW + '[%H:%M:%S:%f]-[Checking variants..]'))
print(' ')

for variant_id in variants:

    atc = "https://www.off---white.com/en/IT/orders/populate.json"

    headers_atc = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'origin': "https://www.off---white.com",
    'x-requested-with': "XMLHttpRequest",
    'x-dtpc': "5$282640112_722h3vLHPOETHIGJPIIILDFIPPLNLKALMHENII",
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    'content-type': "application/json; charset=UTF-8",
    'cache-control': "no-cache"}

    while True:
        r = s.post(atc, headers=headers_atc, json={"variant_id": variant_id, 'quantity': 1}, allow_redirects=False)
        print(r.text)
        time.sleep(3) #SET DELAY HERE, I SUGGEST FROM 6 TO 7 WITHOUT PROXIES
        print(datetime.now().strftime(Fore.YELLOW + '[%H:%M:%S:%f]-[Trying to cart variant_id {}]'.format(variant_id)))
        print('')
        try:
            if r.status_code == 200:
                break
            else:
                print(datetime.now().strftime(Fore.RED + '[%H:%M:%S:%f]-[Product unsuccessfully added to cart with status_code {}]'.format(r.status_code)))
                print('')
        except AttributeError:
            print(e)
    cart_items = r.json()['cart']['line_items']
        #print(cart_items)
    for i in cart_items:
            # print(i["name"])
            # print(i["url"])
            # print(i["image_url"])
            # print(i["full_price"])
            # print(i["variant_id"])
        url = 'https://www.off---white.com{}'.format(i["url"])

    PayloadNotify2 = {
            "attachments": [{
                "fallback": "Off---White Bot",
                "color": "#000000",
                "author_name": '',
                "title": i['name'],
                "title_link": url,
                "thumb_url": i['image_url'],
                "actions": [{
                "text": "Cart",
                "type": "button",
                "url": "https://www.off---white.com/en/IT/cart"}],
                "fields":
                [{"title": "Carted Variant",
                "value": i['variant_id'],
                "short": True},
                {"title": "Price",
                "value": i['full_price'],
                "short": True}],
                "footer": "Ratzcave",
                "footer_icon": 'https://i.imgur.com/GdrQ28e.png',
                "ts": time.time()}]}

    print(datetime.now().strftime(Fore.GREEN + '[%H:%M:%S:%f]-[Product succesfully added to cart with status_code {}]'.format(r.status_code)))
    print('')
    requests.post('https://hooks.slack.com/services/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', json=PayloadNotify2, headers={'Content-Type': 'application/json'}) #WEBHOOK HERE
    print(Fore.YELLOW + '[Payload sent]')
    print(' ')
    print(s.cookies)
    print()


    #GET REQUEST TO CART

    print(datetime.now().strftime(Fore.GREEN + '[%H:%M:%S:%f]-[Trying to get cart values]'))
    print('')

    cart = 'https://www.off---white.com/en/IT/cart'

    headers_cart = {
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'cache-control': "no-cache"}

    r = s.get(cart, headers=headers_cart, allow_redirects=False)
    print(r.status_code)

    text = r.text

    #SCRIVO IL FILE.HTML
    # jsToDecrypt = open('jsToDecrypt.html', 'w')
    # jsToDecrypt.write(text)
    # jsToDecrypt.close()

    ##soup = BeautifulSoup(text,'html.parser')
    ##jsRaw = soup.find("script").get_text()
    ##jsRes = open("jsResolver.js","w+")
    ##jsRes.write(jsRaw.encode("utf-8"))
    #devo scrivere il jsDecrypt now, forse devo aggiungere anche html, spero di no
'''
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = r.text
        print(message)
        self.wfile.write(message.encode('utf-8'))
        return
def run():
  print('Avvio del server...')
  server_address = ('127.0.0.1', 6050)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('Server in esecuzione...')
  httpd.serve_forever()
run()

#http://127.0.0.1:8081 vai qui per vedere il contenuto
'''

#creo il file
print("")
soup = BeautifulSoup(text,'html.parser')
jsRaw = soup.find("script").get_text()
#inject di codice per risolvere il js
index = jsRaw.find('location.href="https://www.off---white.com/en/IT/cart?";')
jsRawInject = jsRaw[:index] + 'ipp_sign = e+salt+md5(e+salt);alert(ipp_sign);' + jsRaw[index:]
f = open("/home/tob/Documents/OWBot/jsToDecrypt.html","w")
f.write("<!doctype html><html><head></head><body><title>JavaScript RSA Encryption</title><script src=\"http://code.jquery.com/jquery-1.8.3.min.js\"></script><script src=\"bin/jsencrypt.min.js\"></script><script type=\"text/javascript\">")
f.write(jsRawInject.encode('utf-8'))
print (jsRawInject.encode('utf-8'))
f.write("</script></body></html>")
print("file creato")
f.close()
time.sleep(5)
comandoFileCreato = requests.get('http://127.0.0.1:'+sys.argv[1])
print(comandoFileCreato.status_code)
if comandoFileCreato.status_code == 200:
    print("seconda richiesta")
#richiesta di ipp
time.sleep(20)
r_server= s.get('http://127.0.0.1:'+sys.argv[2])
print(r_server.text)
IPP_SIGN = r_server.text

#iniettiamo ipp_sign
Req_ipp_sign=requests.cookies.create_cookie('ipp_sign','{}'.format(IPP_SIGN))
s.cookies.set_cookie(Req_ipp_sign)

print('ipp_sign injected')

headers_cart = {
                'referer': "https://www.off---white.com",
                'accept-encoding': "gzip,deflate,br",
                'accept-language': "en-US,en,q=0.9",
                'connection': "keep-alive",
                'host': "www.off---white.com",
                'upgrade-insecure-requests': "1",
                'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                }

cart = 'https://www.off---white.com/en/IT/cart'

headers_cartjson = {
                'referer': "https://www.off---white.com/en/IT/cart",
                'accept-encoding': "gzip,deflate,br",
                'accept-language': "en-US,en,q=0.9",
                'connection': "keep-alive",
                'host': "www.off---white.com",
                'upgrade-insecure-requests': "1",
                'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
                'accept': "application/json, text/javascript, */*; q=0.01",
                'content-type':"application/json; charset=utf-8",
                'x-requested-with':"XMLHttpRequest",
                }

cartJson = 'https://www.off---white.com/en/IT/cart.json?'

#mandiamo richiesta di get al carrello
r_cart = s.get(cart, headers=headers_cart, allow_redirects=False)
r_cartjson = s.get(cartJson, headers=headers_cartjson, allow_redirects=False)

if r_cart.status_code == 200:
    print(r_cart.text)


if r_cartjson.status_code == 200:
    print(r_cartjson.text)