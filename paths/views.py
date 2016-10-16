from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from neomodel import db
from paths.models import Localidade, ConectaRel
import datetime
# Create your views here.

def index(request):

    localidades = []
    for node in Localidade.nodes:
        localidades.append(node.nome)
    context = { "localidades" : localidades, "teste" : 1 }

    return render(request, 'paths/index.html', context)

def results(request):
    origem = request.POST['origem']
    destino = request.POST['destino']

    velocidade= "v_pico"
    
    query = '''MATCH (start:Localidade {nome: '%s'}), (end:Localidade {nome: '%s'})
    MATCH p=(start)-[:CONECTA_COM*]->(end)
    WITH p,reduce(s = 0, r IN rels(p) | s + (60*r.distancia)/r.%s) AS dist
    RETURN p, dist ORDER BY dist Limit 1''' % (origem, destino,velocidade)

    results, meta = db.cypher_query(query) #RECORDLIST
    result = results[0] #PEGANDO O UNICO INDEX DA RECORDLIST TEMOS O RECORD
    raw_nodes = result['p'] #RECUPERANDO O PATH GRAPH COM OS NOS EM SI

    pre_nodes = [Localidade.inflate(row) for row in raw_nodes.nodes]
    
    nodes = []
    for node in pre_nodes:
        node.refresh()
        nodes.append(node.nome)
    
    context = { 'caminho' : nodes, 'custo':result['dist']}

    return render(request, 'paths/results.html', context)
