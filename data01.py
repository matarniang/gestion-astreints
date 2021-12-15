# import time
# from flask import Flask, request,jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from datetime import datetime
# #from flask_crontab import Crontab
# from send_mailer import *
# import os
# #from flask_apscheduler import APScheduler
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
#
# class Departement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom_departement = db.Column(db.String(100))
#     nom_direction = db.Column(db.String(100))
#     services = db.relationship('Service' ,backref=db.backref('departement'))
#     # def __init__(self, nom_deparement, nom_direction):
#     #      self.nom_departement = nom_deparement
#     #      self.nom_direction = nom_direction
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
# # @app.route('/departement', methods=['POST'])
# # def add_departement():
# #     nom_departement = request.json['nom_departement']
# #     nom_direction = request.json['nom_direction']
# #     new_departement = Departement(nom_departement, nom_direction)
# #     db.session.add(new_departement)
# #     db.session.commit()
# #     return departement_schema.jsonify(new_departement)
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
#     id=db.Column(db.Integer, primary_key=True)
#     nom_service=db.Column(db.String(100))
#     perimetre=db.Column(db.String(100) )
#     departement_id=db.Column(db.Integer, db.ForeignKey('departement.id'))
#     sous_service = db.Column(db.String(255))
#     personnes= db.relationship('Personne',backref=db.backref('service'))
#     # souservices = db.relationship('Souservice', backref=db.backref('service'))
#     # def __init__(self, nom_service,perimetre,departement_id):
#     #     self.nom_service = nom_service
#     #     self.perimetre = perimetre
#     #     self.departement_id = departement_id
# class ServiceSchema(ma.Schema):
#     class Meta:
#         fields=('id', 'nom_service', 'perimetre','departement_id')
# service_schema = ServiceSchema()
# services_schema = ServiceSchema(many=True)
# #
# # class Souservice(db.Model):
# #     id=db.Column(db.Integer, primary_key=True)
# #     nom_souservice=db.Column(db.String(100))
# #     perimetre_souservice=db.Column(db.String(100))
# #     service_id=db.Column(db.Integer,db.ForeignKey('service.id'))
# #
# # class SouserviceSchema(ma.Schema):
# #     class Meta:
# #         fields=('id', 'nom_souservice', 'perimetre_souservice','service_id')
# # sous_service_schema = SouserviceSchema()
# # sous_services_schema = SouserviceSchema(many=True)
#
# ############################################################################################################################################
#
# ###################################### METHODE AJOUTER SUPRIMER DELETE EDITER  FOR SERVICE #################################################
#
# # @app.route('/service', methods=['POST'])
# # def add_servie():
# #     nom_service = request.json['nom_service']
# #     perimetre = request.json['perimetre']
# #     departement_id = request.json['departement_id']
# #     new_service = Service(nom_service, perimetre,departement_id)
# #     db.session.add(new_service)
# #     db.session.commit()
# #     return service_schema.jsonify(new_service)
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
#     #confirme = db.Column(db.Integer, nullable=True, default=0)
#     # def __init__(self, nom, prenom, email, etat, password,service_id,status):
#     #     self.nom = nom
#     #     self.prenom = prenom
#     #     self.email = email
#     #     self.password = password
#     #     self.etat = etat
#     #     self.service_id = service_id
#     #     self.status = status
#     # #     #self.code = code
#     #     #self.confirme = confirme
# class PersonneSchema(ma.Schema):
#     class Meta:
#         fields=('id','nom', 'prenom', 'email','etat','password','service_id','status', 'date_time')
#
# personne_schema = PersonneSchema()
# personnes_schema = PersonneSchema(many=True)
#
# #################################################################################################################################
# # CREATE TABLE AstreinteManageriale (
# # id INTEGER NOT NULL,
# # nom VARCHAR(100),
# # prenom VARCHAR(100),
# # email VARCHAR(100),
# # etat VARCHAR(100),
# # date_time DATETIME,
# # telephone VARCHAR(100),
# # departement_id INTEGER,
# # status VARCHAR(100),
# # niveau_astreintes VARCHAR(100),
# # PRIMARY KEY (id), FOREIGN KEY(departement_id) REFERENCES departement (id) )
# ########################################## AJOUTER UPDATE EDITER DELETE #########################################################
#
# # @app.route('/personne', methods=['POST'])
# # def add_personne():
# #     nom = request.json['nom']
# #     prenom = request.json['prenom']
# #     email = request.json['email']
# #     password = request.json['password']
# #     etat = request.json['etat']
# #     status = request.json['status']
# #     service_id = request.json['service_id']
# #     #code = request.json['code']
# #     #verif = request.json['verif']
# #     new_personne = Personne(nom, prenom, email, password, etat, status,service_id)
# #     db.session.add(new_personne)
# #     db.session.commit()
# #     return personne_schema.jsonify(new_personne)
#
# @app.route('/personne/<id>', methods=['GET'])
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
# @app.route('/delete/<id>', methods=['DELETE'])
# def delete_personne(id):
#     personne = Personne.query.get(id)
#     db.session.delete(personne)
#     db.session.commit()
#
# @app.route('/initialisation', methods=['PUT'])
# def etat_initiale(service,sous_service,int_id):
#     services=Service.query.filter_by(nom_service=service,sous_service=sous_service,id=int_id).first()
#     pers_in_service=services.personnes
#     for personne in pers_in_service:
#         if personne.etat=="OK":
#             indice=personne.id + 1
#             perso=Personne.query.get(indice)
#             #if (perso.service.nom_service != service and perso.service.sous_service != sous_service):
#             for personne in pers_in_service:
#                 personne.etat="E"
#                 db.session.add(personne)
#                 db.session.commit()
#                 break
#         else:
#             personne.etat = "NA"
#             personne.date_time = datetime.utcnow()
#             db.session.add(personne)
#             db.session.commit()
# @app.route('/astreint-semaines', methods=['GET'])
# def get_astreints(service:str,sousservice:str,int_id:int):
#     services = Service.query.filter_by(nom_service=service,sous_service=sousservice,id=int_id).first()
#     pers_in_service = services.personnes
#     all_personnes = Personne.query.all()
#     for personne in pers_in_service:
#         if personne.etat == "OK":
#             personne.etat = "NE"
#             db.session.add(personne)
#             db.session.commit()
#     for personne in pers_in_service:
#         if personne.etat == "E":
#             personne.etat = "OK"
#             personne.date_time = datetime.utcnow()
#             db.session.add(personne)
#             db.session.commit()
#             ias = personne.id + 1
#             perso = Personne.query.get(ias)
#             if (ias < len(all_personnes)):
#                 if (perso.service.nom_service == service and perso.service.sous_service == sousservice):
#                     perso.etat = "E"
#                     db.session.add(perso)
#                     db.session.commit()
#                 else:
#                     etat_initiale(service, sousservice, int_id)
#                 break
#             else:
#                 etat_initiale(service, sousservice, int_id)
#
# @app.route('/astreintes', methods=['GET'])
# def send():
#     personnes = Personne.query.all()
#     services = Service.query.all()
#     for service in services:
#         get_astreints(service.nom_service,service.sous_service,service.id)
#
#     astrientes =[]
#
#     for personne in personnes:
#         if personne.etat == "OK":
#             astrientes.append(personne)
#     get_gdp_data(astrientes)
#     return "message envoyer"
#
# @app.route('/etat-zero', methods=['GET'])
# def etat_NA():
#     all_personnes  = Personne.query.all()
#     for personne in all_personnes:
#         personne.etat = "NA"
#         personne.date_time = datetime.utcnow()
#         db.session.add(personne)
#         db.session.commit()
#     return "BD UPDATE SUCCESS"
#
# @app.route('/service-zero', methods=['GET'])
# def etat_service():
#     services  = Service.query.all()
#     for service in services:
#         if service.sous_service == None:
#             service.sous_service = "null"
#             db.session.add(service)
#             db.session.commit()
#     return "BD UPDATE SUCCESS"
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host="127.0.0.1", port=5000)
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
