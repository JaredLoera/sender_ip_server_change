import schedule
import time
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os





#Cnfiguracion del correo
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = 465
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
MAIL_ENCRYPTED = True
MAIL_ENCRYPTED_PROTOCOL = 'ssl'

def checkPublicIP():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip = response.json()['ip']
        last_ip = readLastIPPublicSaved()
        if ip != last_ip:
            saveIPPublic(ip)
            print(f'Public IP changed: {ip}')
            sendEmail(ip)
        else:
            print(f'Public IP: {ip}')
            recipients = read_Emails_List()
            for recipient in recipients:
                print(f'Sending email to {recipient}')

    except Exception as e:
        print(f'Error: {e}')

def readLastIPPublicSaved():
    try:
        with open('public_ip.json', 'r') as file:
            data = json.load(file)
            return data.get('ip', '')
    except FileNotFoundError:
        return ''
    except Exception as e:
        print(f'Error: {e}')
        return ''

def saveIPPublic(ip):
    try:
        with open('public_ip.json', 'w') as file:
            json.dump({'ip': ip}, file)
            print(f'Public IP saved: {ip}')
    except Exception as e:
        print(f'Error: {e}')

def sendEmail(newIp):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = 'salazarloerajared@gmail.com'
        msg['Subject'] = 'Public IP changed'
        body = f'Public IP changed: {newIp}'
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, 'salazarloerajared@gmail.com', text)
        server.quit()
        print('Email sent')
    except Exception as e:
        print(f'Error: {e}')

def read_Emails_List():
        try:
            with open('emails.json', 'r') as file:
                 data = json.load(file)
                 return [entity['email']for entity in data]
        except FileNotFoundError:
            print('File not found')
            return []
        except Exception as e:
            print(f'Error: {e}')
            return []

# Esto se ejecuta cada 10 segundos
schedule.every(10).seconds.do(checkPublicIP)

while True:
    schedule.run_pending()
    time.sleep(1)