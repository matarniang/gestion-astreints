# import time
# from flask import Flask, request,jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from datetime import datetime
# #from flask_crontab import Crontab
# import random
# from send_mailer import *
# import os
#
# ########################################################### BASE DONNE #####################################################################
#
# app = Flask(__name__)
#
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
#
# ######################################################### CLASS DEPARTEMENT ###############################################################
#
# class Departement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom_departement = db.Column(db.String(100))
#     nom_direction = db.Column(db.String(100))
#     services = db.relationship('Service' ,backref=db.backref('departement'))
#     manageriales = db.relationship('AstreinteManageriale', backref=db.backref('departement'))
#
# class DepartementSchema(ma.Schema):
#     class Meta:
#         fields=('id','nom_departement','nom_direction')
# departement_schema=DepartementSchema()
# departements_schema=DepartementSchema(many=True)
#
# ###########################################################################################################################################
#
# ############################ METHODE AJOUTER AFFICHER SUPRIMER DELETE EDITER  FOR DEPARTEMENT ########################################################
#
# @app.route('/departements', methods=['GET'])
# def get_departement():
#     all_departement  = Departement.query.all()
#     result = departements_schema.dump(all_departement)
#     return jsonify(result)
#
# ###########################################################################################################################################
#
# ######################################################### CLASS SERVICE ###################################################################
#
# class Service(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     nom_service=db.Column(db.String(100))
#     perimetre=db.Column(db.String(100) )
#     departement_id=db.Column(db.Integer,db.ForeignKey('departement.id'))
#     sous_service=db.Column(db.String(255))
#     personnes=db.relationship('Personne',backref=db.backref('service'))
#
# class ServiceSchema(ma.Schema):
#     class Meta:
#         fields=('id', 'nom_service','perimetre','departement_id')
# service_schema = ServiceSchema()
# services_schema = ServiceSchema(many=True)
#
# ############################################################################################################################################
#
# ###################################### METHODE AJOUTER SUPRIMER DELETE EDITER  FOR SERVICE #################################################
#
# @app.route('/services', methods=['GET'])
# def get_services():
#     all_services=Service.query.all()
#     result = services_schema.dump(all_services)
#     return jsonify(result)
#
# ############################################################################################################################################
#
# ###################################################### CLASS PERSONNE #####################################################################
#
# class Personne(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.String(100))
#     prenom = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     etat = db.Column(db.String(100))
#     date_time = db.Column(db.DateTime, default=datetime.utcnow())
#     telephone = db.Column(db.String(100))
#     service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
#     status = db.Column(db.String(100))
#     code = db.Column(db.Integer, nullable=True, default=0)
#     type_astreintes = db.Column(db.String(100))
#     niveau_astreintes = db.Column(db.String(100))
#
# class PersonneSchema(ma.Schema):
#     class Meta:
#         fields=('id', 'nom', 'prenom', 'email', 'etat', 'password', 'service_id', 'status','date_time')
#
# personne_schema = PersonneSchema()
# personnes_schema = PersonneSchema(many=True)
#
# #################################################################################################################################
#
# class AstreinteManageriale(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.String(100))
#     prenom = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     etat = db.Column(db.String(100))
#     date_time = db.Column(db.DateTime, default=datetime.utcnow())
#     telephone = db.Column(db.String(100))
#     departement_id = db.Column(db.Integer, db.ForeignKey('departement.id'))
#     status = db.Column(db.String(100))
#     code = db.Column(db.Integer, nullable=True, default=0)
#     niveau_astreintes = db.Column(db.String(100))
#
#
# class AstreinteMSchema(ma.Schema):
#     class Meta:
#         fields=('id','nom', 'prenom', 'email','etat','departement_id','code','status', 'date_time')
#
# AstreinteM_schema = AstreinteMSchema()
# AstreinteMs_shema = AstreinteMSchema(many=True)
#
# @app.route('/astreintesMg', methods=['GET'])
# def get_manageriale():
#     all_astreintes  = AstreinteManageriale.query.all()
#     result = AstreinteMs_shema.dump(all_astreintes)
#     return jsonify(result)
#
# ########################################## AJOUTER UPDATE EDITER DELETE #########################################################
#
# @app.route('/personne/<id>',methods=['GET'])
# def get_personne(id):
#     personne = Personne.query.get(id)
#     return personne_schema.jsonify(personne)
#
# @app.route('/personnes', methods=['GET'])
# def get_personnes():
#     all_personnes  = Personne.query.all()
#     result = personnes_schema.dump(all_personnes)
#     return jsonify(result)
#
# @app.route('/update/<id>', methods=['POST'])
# def update_personne(id):
#     personne = Personne.query.get(id)
#     nom = request.json['nom']
#     prenom = request.json['prenom']
#     email = request.json['email']
#     password = request.json['password']
#     etat = request.json['etat']
#     personne.nom = nom
#     personne.prenom = prenom
#     personne.email = email
#     personne.password = password
#     personne.etat = etat
#     db.session.commit()
#     return personne_schema.jsonify(personne)
#
# @app.route('/delete/<id>',methods=['DELETE'])
# def delete_personne(id):
#     personne = Personne.query.get(id)
#     db.session.delete(personne)
#     db.session.commit()
# def getmanageriales():
#     amn_1=AstreinteManageriale.query.filter_by(niveau_astreintes="N+1")
#     amn_2 = AstreinteManageriale.query.filter_by(niveau_astreintes="N+2")
#     amn_3 = AstreinteManageriale.query.filter_by(niveau_astreintes="N+3")
#     if(compteur(amn_1)==compteurP(amn_1)):
#         getOKandE(amn_1)
#     elif(compteur(amn_1)<compteurP(amn_1)):
#         changementEtat(amn_1)
#         if (compteur(amn_1)==compteurP(amn_1)):
#             if (compteur(amn_2)==compteurP(amn_2)):
#                 getOKandE(amn_2)
#                 getinitial(amn_1)
#             elif (compteur(amn_2)<compteurP(amn_2)):
#                 changementEtat(amn_2)
#                 getmanagE(amn_2)
#                 getinitial(amn_1)
#         elif(compteur(amn_1)<compteurP(amn_1)):
#             getmanagE(amn_1)
#     if(compteur(amn_3)==compteurP(amn_3)):
#         getOKandE(amn_3)
#     elif(compteur(amn_3)<compteurP(amn_3)):
#         changementEtat(amn_3)
#         getmanagE(amn_3)
#
# def get_astreints(service:str,sousservice:str,int_id:int):
#     services=Service.query.filter_by(nom_service=service,sous_service=sousservice,id=int_id).first()
#     pers_in_service=services.personnes
#     if(compteur(pers_in_service)==len(pers_in_service)):
#         getOKandE(pers_in_service)
#     elif(compteur(pers_in_service)<len(pers_in_service)):
#         changementEtat(pers_in_service)
#         getmanagE(pers_in_service)
#
# @app.route('/initiale', methods=['GET'])
# def initiale():
#     personnes=Personne.query.all()
#     manageriales = AstreinteManageriale.query.all()
#     getinitial(personnes)
#     getinitial(manageriales)
#     return "INITIALISATION SUCCESS"
# def getinitial(personnes):
#     for personne in personnes:
#         personne.etat = "NE"
#         personne.code = 1
#         personne.date_time = datetime.utcnow()
#         db.session.add(personne)
#         db.session.commit()
#
# @app.route('/astreintes', methods=['GET'])
# def send():
#     personnes = Personne.query.all()
#     manageriales = AstreinteManageriale.query.all()
#     services = Service.query.all()
#
#     for service in services:
#         get_astreints(service.nom_service,service.sous_service,service.id)
#     getmanageriales()
#
#     astrientes=[]
#     astrientes_manag=[]
#     for personne in personnes:
#         if personne.etat == "OK":
#             astrientes.append(personne)
#
#     for manageriale in manageriales:
#         if manageriale.etat=="OK":
#             astrientes_manag.append(manageriale)
#     get_gdp_data(astrientes,astrientes_manag)
#
#     return "message envoyer"
#
# def getmanagOK(amn):
#     personneOK = random.choice(list(amn))
#     for personne in amn:
#         if personneOK.date_time > personne.date_time:
#             personneOK = personne
#     personneOK.etat = "OK"
#     personneOK.date_time=datetime.utcnow()
#     personneOK.code = 1
#     db.session.add(personneOK)
#     db.session.commit()
#     return personneOK
#
# def getmanagE(amn):
#     personneE=random.choice(list(amn))
#     for personne in amn:
#         if personneE.date_time>personne.date_time:
#             personneE=personne
#     personneE.etat="E"
#     personneE.code=0
#     db.session.add(personneE)
#     db.session.commit()
#     return personneE
#
# def changementEtat(personnes):
#     for personne in personnes:
#         if personne.etat == "OK":
#             personne.etat = "NE"
#             db.session.add(personne)
#             db.session.commit()
#         elif personne.etat == "E":
#             personne.etat = "OK"
#             personne.code = 1
#             personne.date_time = datetime.utcnow()
#             db.session.add(personne)
#             db.session.commit()
#
#
# def compteur(personnes):
#     indice=0
#     for personne in personnes:
#         if personne.code==1:
#             indice = indice + 1
#     return indice
#
# def compteurP(personnes):
#     indice=0
#     for personne in personnes:
#         indice = indice + 1
#     return indice
#
# def getOKandE(amn):
#     personneOk = getmanagOK(amn)
#     personneE = getmanagE(amn)
#     for personne in amn:
#         if personne != personneOk and personne != personneE:
#             personne.etat = "NA"
#             personne.code = 0
#             db.session.add(personne)
#             db.session.commit()
#
# if __name__ == '__main__':
#     app.run(debug=True, host="127.0.0.1",port=5000)
#
#
#
# #* * * * * /usr/local/bin/python
# #* * * * * cd /Users/user/Documents/python/api-astreintes && . venv/bin/python && python base.py >> cron.log
#
# #/Users/user/Desktop/api-astreintes/venv/bin/python /Users/user/Documents/python/api-astreintes/base.py
#
# # * * * * * cd /Users/user/Documents/python/api-astreintes && . venv/bin/activate && python base.py >> cron.log 2>&1
# # */60 * * * * curl http://127.0.0.1:5000/astreintes

from base import *

ams = AstreinteManageriale.query.all()

for personne in ams:
    print("{} {}".format(personne.compteursemaines,personne.compteursemaines+1))