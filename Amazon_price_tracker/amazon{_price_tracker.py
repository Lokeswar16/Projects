import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import lxml
import time
# for refrence see https://www.digitalocean.com/community/tutorials/scrape-amazon-product-information-beautiful-soup
from cffi.backend_ctypes import long

url='https://www.amazon.in/HP-i3-1115G4-Micro-Edge-Anti-Glare-15s-fq2673TU/dp/B0B4N6JVMW/ref=sr_1_1_sspa?crid=2IHEU9TA4UB71&keywords=laptop&qid=1673609726&sprefix=%2Caps%2C5596&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'
# Many websites have certain protocols for blocking robots from accessing data.
# Therefore, in order to extract data from a script, we need to create a User-Agent.SO we have to pass header argument along wth url
headers = ({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    })
response = requests.get(url=url, headers=headers)
webpage_text = response.text
# print(webpage_text)
soup = BeautifulSoup(response.content, "lxml")

# discount_on_product = soup.find("span", class_="savingPriceOverride").getText().strip()
# emi_starts_at = soup.find("span", class_="a-hidden").getText().strip()
# emi=soup.select("span b")

def get_price(soup):

    title = soup.find("span", id='productTitle').getText().strip()
    price = soup.select_one(".a-price-whole").getText().strip()
    # price.removesuffix('.')
    price_in_thousands=int(price.split(",")[0])
    print(price_in_thousands)
    # 50 cause we want to be notified when the price of the laptop is below 50 thousand
    if (price_in_thousands < 50):
        # establish a connection and send email
        print("YEsss")
        subject = f"Price Drop alert!!!!! "# The subject line
        body = f"The product {title} is now at a price of Rs {price}.Here is the link to buy it {url}" # The body for the mail

        message = MIMEMultipart()
        message['From'] = my_email_gmail
        message['To'] = my_email_yahoo
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        msg = message.as_string()

        # using the smtp lib to send ourselves an email when the price is below a certain value
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email_gmail, password=app_password_gmail)
            connection.sendmail(from_addr=my_email_gmail,
                                to_addrs=my_email_yahoo,
                                msg=msg)
my_email_gmail = "testing.in.py@gmail.com"  # sender's address
my_email_yahoo = "mek45704@gmail.com"  # reciever's address
password_gmail = "abcd1234()" #password of the sender's gmail account
app_password_gmail="vngqqzqdxwcmkmmy" #sender's app password gmail
password_yahoo = "abcd1234()@"
#You have to generate an app passoword after turning on two -step authentication and then use this password in your app-password-gmail variable
# get_price(soup)
import schedule
# schedule.every(5).minutes.do(get_price,soup)
schedule.every(5).hours.do(get_price,soup) #running the code after every 5 hours
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)

