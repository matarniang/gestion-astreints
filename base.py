import time
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import random
import time
from send_mailer import *
import os

########################################################### BASE DONNE #####################################################################

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:root@localhost:8889/GestionAstreintes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

######################################################### CLASS DEPARTEMENT ###############################################################

class Departement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_departement = db.Column(db.String(100))
    nom_direction = db.Column(db.String(100))
    services = db.relationship('Service' ,backref=db.backref('departement'))
    astreintes = db.relationship('Astreinte', backref=db.backref('departement'))

###########################################################################################################################################

######################################################### CLASS SERVICE ###################################################################

class Service(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nom_service=db.Column(db.String(100))
    departement_id=db.Column(db.Integer,db.ForeignKey('departement.id'))
    perimetres=db.relationship('Perimetre',backref=db.backref('service'))

#############################################################################################################################################

###################################### CLASS PERIMETRE  ################################################################

class Perimetre(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nom_perimetre=db.Column(db.String(100))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    astreintes = db.relationship('Astreinte', backref=db.backref('Perimetre'))
############################################################################################################################################

###################################################### CLASS ASTREINTE #####################################################################

class Astreinte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100))
    etat = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, default=datetime.utcnow())
    telephone = db.Column(db.String(100))
    perimetre_id = db.Column(db.Integer, db.ForeignKey('perimetre.id'),nullable=True)
    departement_id = db.Column(db.Integer, db.ForeignKey('departement.id'),nullable=True)
    status = db.Column(db.String(100))
    code = db.Column(db.Integer, nullable=True, default=0)
    type_astreintes = db.Column(db.String(100))
    niveau_astreintes = db.Column(db.String(100))
    nombre_semaine = db.Column(db.Integer, nullable=False, default=0)
    compteursemaines = db.Column(db.Integer, nullable=False, default=0)
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime,nullable=False )
    historiques = db.relationship('Historique', backref=db.backref('Astreinte'))

class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    astreinte_id = db.Column(db.Integer, db.ForeignKey('astreinte.id'))
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime,nullable=False )
#################################################################################################################################

########################################## FONCTION GETMENAGER #########################################################

#Cette fonction permer de choisir une personne dans amn_1 ou amn_2 && amn_3
#Pour le cas de (amn_1 ,amn_2)
##====> chaque semqines ont choisi un personne dans amn_1 update( OK====>>>NE && code===>1 )
##====> Si tous les personne trouvant dans amn_1 sont l'etat NE
##====> On choisi une personne dans amn_2 puis ont parcour encore amn_1
##====> le choix d'une personne depend de son datetime(datetime minimale)

def getMg():

    amn_1 = Astreinte.query.filter_by(type_astreintes="AM",niveau_astreintes="N+1")

    amn_2 = Astreinte.query.filter_by(type_astreintes="AM",niveau_astreintes="N+2")

    amn_3 = Astreinte.query.filter_by(type_astreintes="AM",niveau_astreintes="N+3")

    if (compteur(amn_2) == compteurP(amn_2)):

        if (compteur(amn_2) == compteurP(amn_2)) and compteurNE(amn_2) < compteurP(amn_2):

            perso = compteurverife(amn_2)

            if perso.nombre_semaine == perso.compteursemaines:

                getNE(amn_2)

                if (compteur(amn_1) == compteurP(amn_1)):

                    perso = verife(amn_1)

                    if perso.nombre_semaine == perso.compteursemaines:

                        compteurzero(amn_1)

                        setDatetimeZero(amn_1)

                        getOKandE(amn_1)

                    else:

                        perso.compteursemaines = perso.compteursemaines + 1

                        perso.etat = "OK"

                        Commite(perso)

                elif (compteur(amn_1) < compteurP(amn_1)):

                    perso = verife(amn_1)

                    if perso.nombre_semaine == perso.compteursemaines:

                        getAtreintesOK(amn_1)
                    else:
                        perso.compteursemaines = perso.compteursemaines + 1

                        perso.etat = "OK"

                        perso.code = 1

                        Commite(perso)
            else:
                perso.compteursemaines = perso.compteursemaines + 1

                Commite(perso)
        else:

            getNE(amn_1)

            compteurzero(amn_2)

            setDatetimeZero(amn_2)

            getOKandE(amn_2)

    elif (compteur(amn_2) < compteurP(amn_2)):

        changementEtat(amn_2)

        if compteur(amn_2) == compteurP(amn_2):

            pass

        else:
            getAstreinteE(amn_2)

    if (compteur(amn_3) == compteurP(amn_3)):

        if (compteur(amn_3) == compteurP(amn_3)) and compteurNE(amn_3) < compteurP(amn_3):

            perso = compteurverife(amn_3)

            if perso.nombre_semaine == perso.compteursemaines:

                compteurzero(amn_3)

                setDatetimeZero(amn_3)

                getOKandE(amn_3)

            else:

                perso.compteursemaines = perso.compteursemaines + 1

                Commite(perso)

        else:

            getOKandE(amn_3)

    elif (compteur(amn_3) < compteurP(amn_3)):

        changementEtat(amn_3)

        if compteur(amn_3) == compteurP(amn_3):

            pass

        else:

            getAstreinteE(amn_3)

######################################### Astreinte OPERATIONNELLE ###################################################

#Cette fonction permer de choisir une personne pour chqaue perimetres donnees
##====> chaque semqines ont choisi un personne dans AO update( OK====>>>NE && code===>1  datetime==>update)
##====> le choix d'une personne depend de son datetime(datetime minimale)

def getOp(perimetre:str):

    perimetres=Perimetre.query.filter_by(nom_perimetre=perimetre).first()

    pers_in_as=perimetres.astreintes

    if(compteur(pers_in_as)==len(pers_in_as)):

        if (compteur(pers_in_as) == compteurP(pers_in_as)) and compteurNE(pers_in_as) < compteurP(pers_in_as):

            perso = compteurverife(pers_in_as)

            if perso.nombre_semaine == perso.compteursemaines:

                compteurzero(pers_in_as)

                setDatetimeZero(pers_in_as)

                getOKandE(pers_in_as)
            else:
                perso.compteursemaines = perso.compteursemaines+1

                Commite(perso)

        else:
            getOKandE(pers_in_as)

    elif(compteur(pers_in_as)<len(pers_in_as)):

        changementEtat(pers_in_as)

        if compteur(pers_in_as) == compteurP(pers_in_as):

            pass

        else:getAstreinteE(pers_in_as)



#cette methode permet dinilialiser la base de donnees

@app.route('/initiale', methods=['GET'])
def initiale():
    astreintes=Astreinte.query.all()
    for astreinte in astreintes:
        astreinte.etat="NE"
        astreinte.code=1
        astreinte.nombre_semaine=1
        astreinte.compteursemaines=0
        astreinte.date_time=datetime.utcnow()
        astreinte.date_debut=None
        astreinte.date_fin=None
        Commite(astreinte)
    return "INITIALISATION SUCCESS"

#cette fonction permet de recuperer toutes les personne qui sont a l'etat ok et de l'ajouter dans un liste

@app.route('/astreintes', methods=['GET'])
def send():
    astreintes=Astreinte.query.all()
    perimetres = Perimetre.query.all()
    for astreinte in astreintes:
        if astreinte.etat == "OK":
            astreinte.date_fin = datetime.utcnow()
            Commite(astreinte)
            #historique = Historique(astreinte_id=astreinte.id,date_debut=astreinte.date_debut,date_fin=astreinte.date_fin)
            #Commite(historique)

    # for perimetre in perimetres:
    #     getOp(perimetre.nom_perimetre)
    getOp("Support Sécurité & Réseau (ARS)")

   # getMg()

    astrientes=[]

    for personne in astreintes:
        if personne.etat=="OK":
            astrientes.append(personne)

    get_gdp_data(astrientes)
    return "message envoyer"

# cette fonction permet de recuperer la personne qui a le datetime plus petit et changer son etat NE==>OK

def getAtreintesOK(amn):
    personneOK=random.choice(list(amn))
    for personne in amn:
        if personneOK.date_time>personne.date_time:
            personneOK=personne
    personneOK.etat="OK"
    personneOK.code=1
    personneOK.compteursemaines=personneOK.compteursemaines + 1
    personneOK.date_time = datetime.utcnow()
    personneOK.date_debut = personneOK.date_time
    Commite(personneOK)
    return personneOK

# cette fonction permet de recuperer la personne qui a le datetime plus petit apres getOK et changer son etat NE==>E

def getAstreinteE(amn):
    personneE=random.choice(list(amn))
    for personne in amn:
        if personneE.date_time>personne.date_time:
            personneE=personne
    personneE.etat="E"
    personneE.code=0
    Commite(personneE)
    return personneE

#cette fonction permet d 'effectuer un changement d'etat
#==========>pour une perimtre donnes la personne etat ok ======> etat NE et etat E ======> etat OK
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
            personne.date_debut = personne.date_time
            Commite(personne)
        elif personne.etat=="OK" and personne.nombre_semaine>personne.compteursemaines:
            personne.compteursemaines = personne.compteursemaines + 1
            personne.date_time = datetime.utcnow()
            Commite(personne)
            break

#permet de compter le nombre de personne etat NE
def compteurNE(personnes):
    nombre=0
    for personne in personnes:
        if personne.etat=="NE":
            nombre = nombre + 1
    return nombre

#permet de compter le nombre de personne dont le code est egale a 1
def compteur(personnes):
    nombre=0
    for personne in personnes:
        if personne.code==1:
            nombre=nombre + 1
    return nombre

#permet de compter le nombre de personne dans un perimetre
def compteurP(personnes):
    nombre=0
    for personne in personnes:
        nombre = nombre + 1
    return nombre
# cette fonction  fait un appelle de getok and getE
def getOKandE(amn):
    personneOk=getAtreintesOK(amn)
    personneE=getAstreinteE(amn)
    for personne in amn:
        if personne != personneOk and personne != personneE:
            personne.etat="NA"
            personne.code=0
            Commite(personne)

def getNE(amn):
    for personne in amn:
        personne.etat="NE"
        Commite(personne)

# cette fonction permet de commiter une personne dans la base

def Commite(personne):
    db.session.add(personne)
    db.session.commit()

#cette fonction permet de metro le compterur a zero (initialisation compteur)

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

def setDatetimeZero(amn):
    for astreinte in amn:
        astreinte.date_debut=None
        astreinte.date_fin=None
        Commite(astreinte)
    return "Update time success"

# @app.route('/historiques', methods=['GET'])
# def get_Astreinte_historique():
#     date_debut_str="2022-01-02 21:50:10"
#     date_fin_str="2022-01-02 21:53:34"
#     perso_in_histo=Historique.query.filter_by(date_debut=datetime.strptime(date_debut_str,"%Y-%m-%d %H:%M:%S"),date_fin=datetime.strptime(date_fin_str,"%Y-%m-%d %H:%M:%S"))
#     for personne in perso_in_histo:
#         print(" {} ".format(personne.date_debut))
#     return "Success"
if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1",port=5000)



# * * * * * cd /Users/user/Documents/python/api-astreintes && . venv/bin/activate && python base.py >> cron.log 2>&1
# */60 * * * * curl http://127.0.0.1:5000/astreintes
