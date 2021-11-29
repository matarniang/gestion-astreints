import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.message import Message
from email import encoders
import os
from base import *
import json
#import pyodbc
import pandas as pd
from pretty_html_table import build_table

content = open('../api-astreintes/config/gmail.json', mode='r', encoding=None)
config = json.load(content)

# print(config['username'])
email = config['username']
password = config['password']
sender = 'balloniang415@gmail.com'


# receiver = ['balloniang415@gmail.com','disi2212@gmail.com','khadyfall777@yahoo.fr','seckkhadime2@gmail.com']
def get_gdp_data(rst_astreint):
    astreints = rst_astreint.json[0]
    astreint_prochains = rst_astreint.json[1]
    email_astreint = rst_astreint.json[0]["email"]
    email_astreint_prochains = rst_astreint.json[1]["email"]
    chef_service = 'balloniang415@gmail.com'
    receiver = [email_astreint, email_astreint_prochains]

    gdp_dict = {'Prenom' :  [rst_astreint.json[0]['prenom'],    rst_astreint.json[1]['prenom']],
                 'Nom':      [rst_astreint.json[0]['nom'],       rst_astreint.json[1]['nom']],
                 'email':    [rst_astreint.json[0]['email'],     rst_astreint.json[1]['email']],
                 'Matricule':[ rst_astreint.json[0]['password'], rst_astreint.json[1]['password']],
                 'Etat':     [ rst_astreint.json[0]['etat'],     rst_astreint.json[1]['etat']]
                }
    data = pd.DataFrame(gdp_dict)
    output = build_table(data, "blue_light")
    return send_mail(output,chef_service,email_astreint,email_astreint_prochains)


def send_mail(output,chef_service,email_astreint,email_astreint_prochains):

    body_content = output
    body_as = "Bonsoir Monsieur/Madame vous devez gerer les astreintes cette semaines Merci et Bonne Nuit"
    body_asp = "Bonsoir Monsieur/Madame vous devez gerer les astreintes la semaines prochaines pour valider : <a href='#'>validation</>"
    email_receved(body_content,chef_service)
    email_receved(body_as,email_astreint)
    email_receved(body_asp,email_astreint_prochains)



def email_receved(body,receveur):
    message = MIMEMultipart()
    message['subject'] = 'Gestions des Astreintes'
    message['From'] = 'balloniang415@gmail.com'
    message.attach(MIMEText(body, "html"))
    msg_body = message.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(sender, receveur, msg_body)
    server.close()
    return f"Message envoyer avec succss"





