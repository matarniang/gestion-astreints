import time
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import random
from send_mailer import *
import os

########################################################### BASE DONNE #####################################################################

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

######################################################### CLASS DEPARTEMENT ###############################################################

class Departement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_departement = db.Column(db.String(100))
    nom_direction = db.Column(db.String(100))
    services = db.relationship('Service' ,backref=db.backref('departement'))
    manageriales = db.relationship('AstreinteManageriale', backref=db.backref('departement'))

###########################################################################################################################################

############################ METHODE AJOUTER AFFICHER SUPRIMER DELETE EDITER  FOR DEPARTEMENT ########################################################


###########################################################################################################################################

######################################################### CLASS SERVICE ###################################################################

class Service(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nom_service=db.Column(db.String(100))
    perimetre=db.Column(db.String(100) )
    departement_id=db.Column(db.Integer,db.ForeignKey('departement.id'))
    sous_service=db.Column(db.String(255))
    personnes=db.relationship('Personne',backref=db.backref('service'))



############################################################################################################################################

###################################### METHODE AJOUTER SUPRIMER DELETE EDITER  FOR SERVICE #################################################


############################################################################################################################################

###################################################### CLASS PERSONNE #####################################################################

class Personne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100))
    etat = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, default=datetime.utcnow())
    telephone = db.Column(db.String(100))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    status = db.Column(db.String(100))
    code = db.Column(db.Integer, nullable=True, default=0)
    type_astreintes = db.Column(db.String(100))
    niveau_astreintes = db.Column(db.String(100))
    nombre_semaine = db.Column(db.Integer, nullable=False, default=0)
    compteursemaines = db.Column(db.Integer, nullable=False, default=0)

#################################################################################################################################

class AstreinteManageriale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100))
    etat = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, default=datetime.utcnow())
    telephone = db.Column(db.String(100))
    departement_id = db.Column(db.Integer, db.ForeignKey('departement.id'))
    status = db.Column(db.String(100))
    code = db.Column(db.Integer, nullable=True, default=0)
    niveau_astreintes = db.Column(db.String(100))
    nombre_semaine = db.Column(db.Integer, nullable=False, default=0)
    compteursemaines = db.Column(db.Integer, nullable=False, default=0)

########################################## AJOUTER UPDATE EDITER DELETE #########################################################

@app.route('/delete/<id>',methods=['DELETE'])
def delete_personne(id):
    personne=Personne.query.get(id)
    db.session.delete(personne)
    db.session.commit()
def getmanageriales():
    amn_1=AstreinteManageriale.query.filter_by(niveau_astreintes="N+1")
    amn_2=AstreinteManageriale.query.filter_by(niveau_astreintes="N+2")
    amn_3=AstreinteManageriale.query.filter_by(niveau_astreintes="N+3")

    if(compteur(amn_1)==compteurP(amn_1)):

        if(compteur(amn_1)==compteurP(amn_1)) and compteurNE(amn_1)<compteurP(amn_1):
            perso=compteurverife(amn_1)
            if perso.nombre_semaine==perso.compteursemaines:
                getNE(amn_1)
                if (compteur(amn_2)==compteurP(amn_2)):
                    perso = verife(amn_2)
                    if perso.nombre_semaine == perso.compteursemaines:
                        compteurzero(amn_2)
                        getOKandE(amn_2)
                    else:
                        perso.compteursemaines = perso.compteursemaines+1
                        perso.etat="OK"
                        Commite(perso)
                elif (compteur(amn_2)<compteurP(amn_2)):
                    perso = verife(amn_2)
                    if perso.nombre_semaine == perso.compteursemaines:
                        getmanagOK(amn_2)
                    else:
                        perso.compteursemaines = perso.compteursemaines+1
                        perso.etat="OK"
                        perso.code = 1
                        Commite(perso)
            else:
                perso.compteursemaines = perso.compteursemaines+1
                Commite(perso)
        else:
            getNE(amn_2)
            compteurzero(amn_1)
            getOKandE(amn_1)
    elif(compteur(amn_1)<compteurP(amn_1)):
        changementEtat(amn_1)
        if compteur(amn_1)==compteurP(amn_1):
            pass

        else:getmanagE(amn_1)

    if(compteur(amn_3)==compteurP(amn_3)):

        if (compteur(amn_3) == compteurP(amn_3)) and compteurNE(amn_3) < compteurP(amn_3):

            perso = compteurverife(amn_3)

            if perso.nombre_semaine == perso.compteursemaines:

                compteurzero(amn_3)

                getOKandE(amn_3)

            else:

                perso.compteursemaines = perso.compteursemaines+1

                Commite(perso)

        else:getOKandE(amn_3)

    elif(compteur(amn_3)<compteurP(amn_3)):

        changementEtat(amn_3)

        if compteur(amn_3)==compteurP(amn_3):
            pass

        else:getmanagE(amn_3)


def get_astreints(service:str,sousservice:str,int_id:int):

    services=Service.query.filter_by(nom_service=service,sous_service=sousservice,id=int_id).first()

    pers_in_service=services.personnes

    if(compteur(pers_in_service)==len(pers_in_service)):

        if (compteur(pers_in_service) == compteurP(pers_in_service)) and compteurNE(pers_in_service) < compteurP(pers_in_service):

            perso = compteurverife(pers_in_service)

            if perso.nombre_semaine == perso.compteursemaines:

                compteurzero(pers_in_service)

                getOKandE(pers_in_service)
            else:
                perso.compteursemaines = perso.compteursemaines+1

                Commite(perso)

        else:getOKandE(pers_in_service)

    elif(compteur(pers_in_service)<len(pers_in_service)):

        changementEtat(pers_in_service)

        if compteur(pers_in_service) == compteurP(pers_in_service):

            pass

        else:getmanagE(pers_in_service)

@app.route('/initiale', methods=['GET'])
def initiale():
    personnes=Personne.query.all()
    manageriales=AstreinteManageriale.query.all()
    getinitial(personnes)
    getinitial(manageriales)
    return "INITIALISATION SUCCESS"
def getinitial(personnes):
    for personne in personnes:
        personne.etat="NE"
        personne.code=1
        personne.nombre_semaine=1
        personne.compteursemaines=0
        personne.date_time=datetime.utcnow()
        Commite(personne)

@app.route('/astreintes', methods=['GET'])
def send():
    personnes=Personne.query.all()
    manageriales=AstreinteManageriale.query.all()
    services=Service.query.all()

    for service in services:
        get_astreints(service.nom_service,service.sous_service,service.id)
    getmanageriales()
    astrientes=[]
    astrientes_manag=[]
    for personne in personnes:
        if personne.etat=="OK":
            astrientes.append(personne)
    for manageriale in manageriales:
        if manageriale.etat=="OK":
            astrientes_manag.append(manageriale)
    get_gdp_data(astrientes,astrientes_manag)
    return "message envoyer"

def getmanagOK(amn):
    personneOK=random.choice(list(amn))
    for personne in amn:
        if personneOK.date_time>personne.date_time:
            personneOK=personne
    personneOK.etat="OK"
    personneOK.code=1
    personneOK.compteursemaines=personneOK.compteursemaines + 1
    personneOK.date_time = datetime.utcnow()
    Commite(personneOK)
    return personneOK

def getmanagE(amn):
    personneE=random.choice(list(amn))
    for personne in amn:
        if personneE.date_time>personne.date_time:
            personneE=personne
    personneE.etat="E"
    personneE.code=0
    Commite(personneE)
    return personneE

def changementEtat(personnes):
    for personne in personnes:
        if personne.etat=="OK" and personne.nombre_semaine==personne.compteursemaines:
            personne.etat="NE"
            Commite(personne)
        elif personne.etat=="E":
            personne.etat="OK"
            personne.code=1
            personne.compteursemaines=personne.compteursemaines + 1
            personne.date_time=datetime.utcnow()
            Commite(personne)
        elif personne.etat=="OK" and personne.nombre_semaine>personne.compteursemaines:
            personne.compteursemaines = personne.compteursemaines + 1
            personne.date_time = datetime.utcnow()
            Commite(personne)
            #updateDate(personnes)
            break

def compteurNE(personnes):
    nombre=0
    for personne in personnes:
        if personne.etat=="NE":
            nombre = nombre + 1
    return nombre

def compteur(personnes):
    nombre=0
    for personne in personnes:
        if personne.code==1:
            nombre=nombre + 1
    return nombre

def compteurP(personnes):
    nombre=0
    for personne in personnes:
        nombre = nombre + 1
    return nombre

def getOKandE(amn):
    personneOk=getmanagOK(amn)
    personneE=getmanagE(amn)
    for personne in amn:
        if personne != personneOk and personne != personneE:
            personne.etat="NA"
            personne.code=0
            Commite(personne)
def getNE(amn):
    for personne in amn:
        personne.etat="NE"
        Commite(personne)

def Commite(personne):
    db.session.add(personne)
    db.session.commit()
def compteurzero(personnes):
    for personne in personnes:
        personne.compteursemaines=0
        Commite(personne)

def compteurverife(amn):
    perso = None
    for personne in amn:
        if personne.etat == "OK":
            perso = personne
    return perso

def verife(amn):
    perso=random.choice(list(amn))
    for personne in amn:
        if perso.date_time<personne.date_time:
            perso=personne
    return perso



if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1",port=5000)



#* * * * * /usr/local/bin/python
#* * * * * cd /Users/user/Documents/python/api-astreintes && . venv/bin/python && python base.py >> cron.log

#/Users/user/Desktop/api-astreintes/venv/bin/python /Users/user/Documents/python/api-astreintes/base.py

# * * * * * cd /Users/user/Documents/python/api-astreintes && . venv/bin/activate && python base.py >> cron.log 2>&1
# */60 * * * * curl http://127.0.0.1:5000/astreintes
