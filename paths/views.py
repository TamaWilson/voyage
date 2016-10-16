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

    if(origem == destino) or (origem == "NOK") or (destino == "NOK"):
        context = { 'erro': True }
    else:
        hora_local = datetime.datetime.now().time()
        velocidade= "v_normal"
    
        if (datetime.time(18,0,0,0) < hora_local and datetime.time(19,0,0,0) > hora_local) or (datetime.time(11,30,0,0) < hora_local and datetime.time(14,0,0,0) > hora_local): 
            velocidade= "v_pico"
    
        query = '''MATCH (start:Localidade {nome: '%s'}), (end:Localidade {nome: '%s'})
        MATCH p=(start)-[:CONECTA_COM*]->(end)
        WITH p,reduce(s = 0, r IN rels(p) | s + (60*r.distancia)/r.%s) AS dist
        RETURN p, dist ORDER BY dist Limit 1''' % (origem, destino,velocidade)
        
        
        results, meta = db.cypher_query(query) #RECORDLIST
        if(len(results) <1):
            context = { "null_result": True, "erro": False }
        else:
            result = results[0] #PEGANDO O UNICO INDEX DA RECORDLIST TEMOS O RECORD
            raw_nodes = result['p'] #RECUPERANDO O PATH GRAPH COM OS NOS EM SI

            pre_nodes = [Localidade.inflate(row) for row in raw_nodes.nodes]
    
            nodes = []
            for node in pre_nodes:
                node.refresh()
                nodes.append(node.nome)
    
            context = { 'caminho' : nodes, 'custo': round(result['dist'],2) , "erro": False, "null_result": False }

    return render(request, 'paths/results.html', context)


def cadastrar(request):

    nome = request.POST['nome']
    v_normal = request.POST['v_normal']
    v_pico = request.POST['v_pico']
    distancia = request.POST['distancia']

    
    



    
