import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()


content = '' #email content placeholder

#extracting Hacker News Stories

def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories: </b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text != 'More' else '')
        #print(tag.prettify) #find all ('span', attrs={'class':'sitestr'}))
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')

#sending the email now

print('Composing Email now...')

SERVER = 'smtp.gmail.com' # smtp server
PORT = 587 # port number
FROM = input('Please input your email address: ')
TO = 'letsgoroy9@gmail.com' #your email address, can be a list of emails as well
PASS = input('Please input your password: ')

#fp = open(file_name, 'rb')
#Create text/plain message
#msg = MIMEText('')
msg = MIMEMultipart()

#msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top HN Stories [Automated Email]' + ' ' + str(now.month) + '-' + str(now.day) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
#fp.close

print('Initializing Server')

server = smtplib.SMTP(SERVER,PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()

#remember to allow less secure app access on https://myaccount.google.com/security