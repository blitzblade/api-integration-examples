import hashlib
import hmac
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import time
import os, sys
from config import Config

config = Config()


def send_email_with_attachment(message,to, includes_attachment=False,filepath="", subject="No subject"):
    sent_from = config.gmail_username
    # to = config.email_recipients

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ", ".join(to)
    part = MIMEBase('application', "octet-stream")
    try:
        attachment = open(filepath, 'rb').read()
    except:
        attachment = None
    part.set_payload(attachment)

    try:
        filename = os.path.split(filepath)[-1]
    except:
        filename = "file"

    msg.attach(MIMEText(message))
    if includes_attachment:
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
        msg.attach(part)

    message = msg.as_string()
    # all together
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(config.gmail_username, config.gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()
        print("Message sent successfully...")
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_info()[2].tb_lineno))
        print('Something went wrong...')


def print_err(err):
    print(str(err) + " on line " + str(sys.exc_info()[2].tb_lineno))

def is_opposite_trend(response):
    try:
        hourly_price_change = response['changes']['price']['hour']
        price_changes = open(os.path.join(config.current_path,'price_trend.txt')).readlines()

        current_price = response['open']['hour']
        price_changes.append(str(hourly_price_change)+"\n")
        with open(os.path.join(config.current_path,'price_trend.txt'), 'w+') as f:
            f.writelines(price_changes)

        is_opposite = not((float(price_changes[-1]) < 0 and float(price_changes[-2]) < 0) or (float(price_changes[-1]) > 0 and float(price_changes[-2]) > 0))
        return {"current_price":current_price, "price_change": hourly_price_change, "is_opposite": is_opposite}
    except Exception as ex:
        print_err(ex)

# def get_crypto_stats():
#     timestamp = int(time.time())
#     payload = '{}.{}'.format(timestamp, config.public_key)
#     hex_hash = hmac.new(config.secret_key.encode(), msg=payload.encode(), digestmod=hashlib.sha256).hexdigest()
#     signature = '{}.{}'.format(payload, hex_hash)

#     headers = {'X-Signature': signature, 'X-ba-key': config.header_key}
#     result = requests.get(url=config.url, headers=headers)
#     print(result.status_code)
#     print(result.content)
#     response = result.json()
#     return response

def get_crypto_stats(crypto="BTC"):
    timestamp = int(time.time())
    payload = '{}.{}'.format(timestamp, config.public_key)
    hex_hash = hmac.new(config.secret_key.encode(), msg=payload.encode(), digestmod=hashlib.sha256).hexdigest()
    signature = '{}.{}'.format(payload, hex_hash)

    headers = {'X-Signature': signature, 'X-ba-key': config.header_key}
    result = requests.get(url=config.url.format(crypto=crypto), headers=headers)
    response = result.json()
    return response


if __name__=="__main__":
    # response = get_crypto_stats()
    # result = is_opposite_trend(response)
    # print(result)
    # if result:
    #     if result['is_opposite']:
    #         message = "The price is going the opposite direction. Decide what to do now!"+ \
    #         "\nCurrent Price: {}".format(result['current_price']) + \
    #         "\nPrice change: {}".format(result['price_change'])
    #         # send_email_with_attachment(message)
    #         print("Email sent")
    pass
