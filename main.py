import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# URL to scrape
url = "https://www.booking.com/hotel/tr/mr-lion.de.html?aid=304142&label=gen173rf-1FCAso5AFCDWltcGVyaWFsLWxhcmFIB1gDaCyIAQGYAQe4ARnIAQzYAQHoAQH4AQKIAgGiAg1wcmVzZWFyY2guY29tqAIDuAKI4Im0BsACAdICJDAyN2VlODAzLWZmZTctNDI1NS05YzBhLWFjOGMyMDk0MGY5ZdgCBeACAQ&sid=bd19c149810870016ae83db6ec75cf5e&age=0;all_sr_blocks=979729504_391097006_2_25_0;checkin=2024-08-26;checkout=2024-09-08;dest_id=-762951;dest_type=city;dist=0;group_adults=2;group_children=1;hapos=1;highlighted_blocks=979729504_391097006_2_25_0;hpos=1;matching_block_id=979729504_391097006_2_25_0;nflt=price%3DCHF-min-300-1%3Bht_beach%3D1%3Breview_score%3D70%3Broomfacility%3D11%3Bhotelfacility%3D54%3Bmealplan%3D9%3Bpopular_activities%3D240%3Breview_score%3D80;no_rooms=1;req_adults=2;req_age=0;req_children=1;room1=A%2CA%2C0;sb_price_type=total;sr_order=popularity;sr_pri_blocks=979729504_391097006_2_25_0__346320;srepoch=1719832385;srpvid=893e4e69419d0669;type=total;ucfs=1&"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5042.108 Safari/537.36"
}

# Send GET request to fetch the webpage
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# List to store room prices
room_results = []

# Extract room prices from the webpage
for el in soup.find_all("div", {"id": "available_rooms"}):
    pricing_elem = el.find("span", {"class": "prco-valign-middle-helper"})
    if pricing_elem:
        pricing_text = pricing_elem.text.strip().replace(
            ".", "").replace('\xa0', ' ').replace("CHF", "")
        try:
            price_int = int(pricing_text)
            room_results.append({"pricing": price_int})
        except ValueError:
            print(f"Unable to convert pricing to integer: {pricing_text}")
    else:
        print("No pricing element found.")

# Email configuration
EMAIL = "info@martinpoehl.ch"
PASSWORD = "3^*ci8&C6c727&"
RECIPIENT_EMAIL = "martinpoehl@me.com"

# Check room prices and send email if price is under 4000 CHF
for result in room_results:
    limit = 4000
    if result["pricing"] < limit:
        message = MIMEMultipart()
        message['From'] = EMAIL
        message['To'] = RECIPIENT_EMAIL
        message['Subject'] = f"Price Alert: Room price is under CHF {limit}"

        body = f"The room price is CHF {result['pricing']}. It's under CHF {limit}."
        message.attach(MIMEText(body, 'plain'))

        try:
            # Connect to Gmail SMTP server
            server = smtplib.SMTP('asmtp.mail.hostpoint.ch', 587)
            server.starttls()
            server.login(EMAIL, PASSWORD)

            # Send email
            text = message.as_string()
            server.sendmail(EMAIL, RECIPIENT_EMAIL, text)
            server.quit()

            print(
                f"Email notification sent for price CHF {result['pricing']}.")

            # Break the loop after sending the first notification
            break
        except Exception as e:
            print(f"Error sending email: {e}")
    else:
        print(f"Price CHF {result['pricing']} is not under CHF {limit}.")
