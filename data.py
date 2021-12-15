from json import dump

from base import *
# import random
#services = Service.query.filter_by(nom_service="ARS").first()
#pers_in_service = services.personnes
#
#
# personne = random.choice(list(pers_in_service))
# print("{}".format(personne.nom))
#

#pd = []
#pers_in_service = services.personnes
# for personne in pers_in_service:
#     #add=[]
#     pd.append(personne.date_time)
#     pd.append(personne.id)
#     #pd.append(add)

# services = Service.query.filter_by(nom_service="ARS", sous_service="null", id=1).first()
# compteurI = 0
# pers_in_service = services.personnes
# for personne in pers_in_service:
#     if personne.code == 1:
#         compteurI = compteurI + 1

# print("compteurI: {}  pers_in_service: {}".format(compteurI,len(pers_in_service)))

manageriale = AstreinteManageriale.query.filter_by(niveau_astreintes="N+2")

for personne in manageriale:
    print("compteurI: {}  {} {}  {}".format(personne.nom,personne.prenom,personne.niveau_astreintes,personne.departement_id))