# voyage
Estudo para construção de um sistema de sugestão de rotas.

#Requisitos:

- Python 3.5
- Django 1.10
- Neomodels
- Py2neo
- Neo4j 3.0.X 
- Plugin APOC para o Neo4j

#Inicialização

- É necessário popular a database com bairros antes de utilizar o sistema, o arquivo DB_case.txt possui uma query do neo4j para tal.

#Mudanças
- Devido a incompatibilidade do Neomodel com o Neo4j 3.0 os métodos foram modificados para utilizar querys em cypher em vez dos métodos fornecidos pelo Neomodel. 

#TO-DO:

- Incluir a inicialização no código python
- Atualizar o código quando houver nova atualização do Neomodel
