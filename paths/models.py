import os
os.environ['NEO4J_REST_URL'] = 'http://neo4j:neo4@localhost:7474/db/data/'

from django.db import models

from py2neo import Graph
from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty,Relationship,FloatProperty)

class ConectaRel(StructuredRel):
    distancia = FloatProperty(required=True)
    vnormal = FloatProperty(required=True)
    vrush = FloatProperty(required=True)

class Localidade(StructuredNode):
    nome = StringProperty(unique_index=True, required=True)
    
    # traverse incoming IS_FROM relation, inflate to Person objects
    conectar = Relationship('Localidade', 'CONECTA_COM', model=ConectaRel)

