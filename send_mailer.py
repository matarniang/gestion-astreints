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
import pandas as pd
from pretty_html_table import build_table

content = open("config/gmail.json", mode="r", encoding=None)
config = json.load(content)
email = config["username"]
password = config["password"]
sender = "balloniang415@gmail.com"

# receiver = ['balloniang415@gmail.com','disi2212@gmail.com','khadyfall777@yahoo.fr','seckkhadime2@gmail.com']
# recuperation perosonnes etat OK

def get_gdp_data(astreints:list):
    prenom_ast=[]
    nom_ast=[]
    telephone_ast=[]
    etat_ast=[]
    perimetre_ast=[]
    for astreint in astreints:
        prenom_ast.append(astreint.prenom)
        nom_ast.append(astreint.nom)
        telephone_ast.append(astreint.telephone)
        etat_ast.append(astreint.etat)
        if astreint.perimetre_id == None:
            perimetre_ast.append("")
        elif astreint.perimetre_id != None:
            perimetre_ast.append(Perimetre.query.get(astreint.perimetre_id).nom_perimetre)

    dict = {'PRENOM': prenom_ast, 'NOM': nom_ast, 'TELEPHONE': telephone_ast, 'PERIMETRE': perimetre_ast}
    data = pd.DataFrame(dict)
    output = build_table(data, "blue_light")
    return send_mail(output)

def send_mail(output):
    body_content = output
    email_receved(body_content,sender)
def email_receved(body,receveur):
    message = MIMEMultipart()
    message['subject'] = 'Gestions des Astreintes'
    message['From'] = 'balloniang415@gmail.com'
    message.attach(MIMEText(body, "html"))
    msg_body = message.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email, password)
    server.sendmail(sender, receveur, msg_body)
    server.close()
    return f"Message envoyer avec success"
