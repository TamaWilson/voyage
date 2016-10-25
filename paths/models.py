import os
os.environ['NEO4J_REST_URL'] = 'http://neo4j:neo4@localhost:7474/db/data/'

from django.db import models

from py2neo import Graph
from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty,Relationship,FloatProperty)

class ConectaRel(StructuredRel):
     #cada atributo da classe está relacionado com um tipo de propriedade, os relacionamento definido por essa classe usam Float, além disso definimos que as propiedades são obrigatórias 
    distancia = FloatProperty(required=True)
    vnormal = FloatProperty(required=True)
    vrush = FloatProperty(required=True)

class Localidade(StructuredNode):
     #Da mesma forma os relacionamentos são definidos no model, também definimos os nós e suas propriedades (além dos seus tipos) 
    nome = StringProperty(unique_index=True, required=True)
    
    # traverse incoming IS_FROM relation, inflate to Person objects
    conectar = Relationship('Localidade', 'CONECTA_COM', model=ConectaRel) #Um atributo para representar um relacionamento possível para esse tipo de nó é criado baseado no modelo do ConectaRel

