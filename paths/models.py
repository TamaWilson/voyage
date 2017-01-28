from django.db import models

from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty,RelationshipTo,FloatProperty, Relationship)


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



