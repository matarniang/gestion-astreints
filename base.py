import response as response
from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from send_mailer import *
import os

# initialisation app
app = Flask(__name__)
# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialisation base donne
db = SQLAlchemy(app)
# initialisation mashmallow
ma = Marshmallow(app)

# Personne class/Model
class Personne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    etat = db.Column(db.String(100),nullable=True)
    date_time = db.Column(db.DateTime,default = datetime.utcnow())
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, nom, prenom, email, password,etat):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = password
        self.etat = etat

# Personne  Schema
class PersonneSchema(ma.Schema):
    class Meta:
        fields = ('id','nom','prenom','email','password','etat','date_time')
# Initialisation Schema
personne_schema=PersonneSchema()
personnes_schema=PersonneSchema(many=True)
@app.route('/',methods=['GET'])
def get():
    return jsonify({'msg': 'Hello world'})

@app.route('/personne', methods=['POST'])
def add_personne():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    password = request.json['password']
    etat = request.json['etat']
    new_personne = Personne(nom, prenom, email, password,etat)
    db.session.add(new_personne)
    db.session.commit()
    return personne_schema.jsonify(new_personne)

@app.route('/personne/<id>', methods=['GET'])
def get_personne(id):
    personne = Personne.query.get(id)
    return personne_schema.jsonify(personne)

@app.route('/personnes', methods=['GET'])
def get_personnes():
    all_personnes  = Personne.query.all()
    result = personnes_schema.dump(all_personnes)
    return jsonify(result)

@app.route('/update/<id>', methods=['POST'])
def update_personne(id):
    personne = Personne.query.get(id)
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    password = request.json['password']
    etat = request.json['etat']
    personne.nom = nom
    personne.prenom = prenom
    personne.email = email
    personne.password = password
    personne.etat = etat
    db.session.commit()
    return personne_schema.jsonify(personne)

@app.route('/delete/<id>', methods=['DELETE'])
def delete_personne(id):
    personne = Personne.query.get(id)
    db.session.delete(personne)
    db.session.commit()

@app.route('/initialisation', methods=['PUT'])
def etat_initiale():
    astreint_initial = Personne('nom', 'prenom', 'email', 'password', 'etat')
    all_personnes = Personne.query.all()
    for personne in all_personnes:
        if personne.etat == "OK":
            indice = personne.id + 1
            if indice <= len(all_personnes):
                for personne in all_personnes:
                    if personne.id == indice:
                        personne.etat = "E"
                        db.session.add(personne)
                        db.session.commit()
                        astreint_initial = personne_schema.dump(personne)
            elif indice > len(all_personnes):
                for personne in all_personnes:
                    if personne.id == 1:
                        personne.etat = "E"
                        db.session.add(personne)
                        db.session.commit()
                        astreint_initial = personne_schema.dump(personne)
        else:
            personne.etat = "NA"
            personne.date_time = datetime.utcnow()
            db.session.add(personne)
            db.session.commit()
    return astreint_initial

@app.route('/astreint-semaines', methods=['GET'])
def get_astreints():
    astreint_prochains=Personne('nom', 'prenom', 'email', 'password', 'etat')
    astreint=Personne('nom', 'prenom', 'email', 'password', 'etat')

    all_personnes = Personne.query.all()
    for personne in all_personnes:
        if personne.etat == "OK":
            personne.etat = "NE"
            db.session.add(personne)
            db.session.commit()
        elif personne.etat == "E":
            personne.etat = "OK"
            personne.date_time = datetime.utcnow()
            db.session.add(personne)
            db.session.commit()
            astreint = personne_schema.dump(personne)
            ias = personne.id + 1
            if ias <= len(all_personnes):
                for personne in all_personnes:
                    if personne.id == ias:
                        personne.etat = "E"
                        db.session.add(personne)
                        db.session.commit()
                        astreint_prochains = personne_schema.dump(personne)

            else:
                astreint_prochains = etat_initiale()
            break
    rst = jsonify(astreint,astreint_prochains)
    return get_gdp_data(rst)
    # return f"successfull"


if __name__ == '__main__':
    app.run(debug=True)
