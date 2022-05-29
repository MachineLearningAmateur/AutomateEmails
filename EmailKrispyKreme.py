import csv
import smtplib
import credentials
import datetime as dt 
import time #to make python sleep til then
import os #for clearing the outputs
import re #regular expressions for python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage #for images
# from email.mime.application import MIMEApplication #for attachments

def send_email(names, urls, emails):
    print("Starting to send mail...")
    smtp = smtplib.SMTP('smtp.gmail.com', port='587') #initializes the smtp object
    smtp.ehlo() #send the extended hello to our server
    smtp.starttls() #tell server we want to communicate with TLS encryption
    smtp.login(credentials.email, credentials.password) #login to our email server

    fromAddr = credentials.email
    name = None
    link = None
    toAddr = None

    for i in range(len(names)):
        name = names[i]
        link = urls[i]
        toAddr = emails[i]
        textContent = f'''
Hello {name}!

Below is the link to your digital voucher redeemable at any Krispy Kreme location (except Connecticut or Puerto Rico). Feel free to either print it out or pull it up on your smart device when you are ready to redeem at your local Krispy Kreme Store! In case there is an issue with Krispy Kreme's website in the future, you can also just screenshot the digital voucher.

Thank you for your support and we hope you enjoy your doughnuts!

Link: {link}

You (or the Psi Chi Member you are supporting) have received two activity points for taking part in the fundraiser.

Best regards,
Psi Chi International Honor Society in Psychology, UCR Chapter

*please copy and paste the URL into a new tab if clicking on the link does not work 

        '''
        msg = MIMEMultipart() #initializes the MIME object, containing our email message
        msg.attach(MIMEText(textContent, 'plain')) #converts text content to MIMEText and adds to the MIME object
        msg['Subject'] = "Psi Chi Fundraiser - Digital Dozens Voucher"
        #img_data = open('PsiChi.jpg', 'rb').read()  #used to read an image
        #msg.attach(MIMEImage(img_data, _subtype="jpg")) #converts img to MIMEImage and adds to the MIME object
        smtp.sendmail(fromAddr, toAddr, msg.as_string()) #this will send the email fromAddr to toAddr with msg as an attachment.
    smtp.quit() #closes the connection

urls = []
with open("Krispy_Kreme_Winter2.csv", 'r') as file: 
    csvReader = csv.reader(file)
    #header = next(csvReader) #this removes the header from the csv file
    for row in csvReader:
        if(row[1] != 'X'):
            urls.append(row[0]) #takes first value in array and appends it to urls
file.close() #proper coding habit is to close the file after opening it.

emails = []
names = []
with open("names_emails_winter2.csv", 'r') as eFile:
    csvReader = csv.reader(eFile)
    header = next(csvReader)
    searchCriteria = re.compile(r'sent', re.I) #looks for the string 'sent' and accepts both capital and lower case variations
    for row in csvReader:
        #print(searchCriteria.search(row[3]))
        if (searchCriteria.search(row[3]) == None): #if there is no match for 'sent', then append the name and email to their respective lists
            if (row[0] != ''):
                names.append(row[0].strip()) #strip will remove all side whitespace from the str
            if (row[2] != ''):
                emails.append(row[2].strip()) 
            print (row[0], row[2], 'true')
eFile.close() #proper coding habit to close file after opening it. 

for i in range(len(names)): 
    print(names[i], emails[i], urls[i])

print(f'Size of url list: {len(urls)}')
print(f'Size of email list: {len(emails)}')
print(emails)
print(f'Size of name list: {len(names)}')
print(names)


# send_time = dt.datetime(2021, 10, 15, 8, 0, 0)
# print(dt.datetime.now())
# print(dt.datetime(2021, 10, 15, 8, 0, 0, tzinfo=dt.timezone.utc))
count = 0

# ticker = int(input("How many hours would you like to wait? "))
# ticker = ticker * 60 * 60
# print(ticker, 'seconds')
# for i in range(ticker):
#     time.sleep(1)
#     count += 1

send_email(names, urls, emails) #this is the function used to send the mail given the list names, urls, and emails

