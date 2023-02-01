import yaml
import smtplib
from kucoin.client import Client as KuClient
from gate_api import ApiClient, Configuration, Order, SpotApi

def load_kukoin_client(file):
    with open(file) as file:
        auth = yaml.load(file, Loader=yaml.FullLoader)
    return KuClient(auth['kucoin_api'],auth['kucoin_secret'],auth['kucoin_pass'])


def load_gateio_client(file):
    with open(file) as file:
        auth = yaml.load(file, Loader = yaml.FullLoader)
    config = Configuration(key = auth['gateio_api'], secret = auth['gateio_secret'])
    return SpotApi(ApiClient(config))

def send_email(file, message):
    with open(file) as file:
        auth = yaml.load(file, Loader = yaml.FullLoader)
    fromaddr = auth['email_address']
    toaddrs  = auth['email_address']
    msg = message
    username = auth['email_address']
    password = auth['email_password']
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
