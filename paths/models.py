from django.db import models

from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty,RelationshipTo,FloatProperty, Relationship)

'''
class ConectaRel(StructuredRel):
    #cada atributo da classe está relacionado com um tipo de propriedade, os relacionamento definido por essa classe usam Float, além disso definimos que as propiedades são obrigatórias 
    distancia = FloatProperty(required=True)
    vnormal = FloatProperty(required=True)
    vrush = FloatProperty(required=True)
    danger = FloatProperty(required = True)
    
class Localidade(StructuredNode):
     #Da mesma forma os relacionamentos são definidos no model, também definimos os nós e suas propriedades (além dos seus tipos) 
    nome = StringProperty(unique_index=True, required=True)
    
    conectar = RelationshipTo('Localidade', 'CONECTA_COM', model=ConectaRel) #Um atributo para representar um relacionamento possível para esse tipo de nó é criado baseado no modelo do ConectaRel
'''

class WayRel(StructuredRel):
    osmID = IntegerProperty(required=True)
    name = StringProperty()
    vnormal = FloatProperty(default=1.0)
    vrush =  FloatProperty(default=1.0)
    risk = FloatProperty(default=50.0)
    distance = FloatProperty(default=100)

class Point(StructuredNode):
    osmID = IntegerProperty(required=True)
    lat = FloatProperty(required=True)
    lon = FloatProperty(required=True)

    way = RelationshipTo('Point', 'Way', model=WayRel)


    clear = Relationship('Point', 'Way', model=WayRel)

