import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_btc_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=ad723eca-82b7-49f8-a5f5-2ff83836edc6"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for crypto in data['data']:
            if crypto['symbol'] == 'BTC':
                return crypto['quote']['USD']['price']
    return None

def send_email(email, btc_price):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = email
    subject = "BTC Price Alert"
    body = f"The price of BTC has crossed your target of $80,000. The current price is ${btc_price}."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Setup the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_price_and_alert(target_price, email):
    alerted = False
    while not alerted:
        btc_price = get_btc_price()
        if btc_price:
            print(f"Current BTC price: ${btc_price}")
            if btc_price > target_price:
                send_email(email, btc_price)
                print('sent mail')
                alerted = True
        time.sleep(60) 

if __name__ == '__main__':
    target_price = 10000 
    email = "mamlesh.va06@gmail.com" 
    check_price_and_alert(target_price, email)
