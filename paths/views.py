<<<<<<< HEAD
from django.shortcuts import render
from neomodel import db
from paths.models import Localidade, ConectaRel
import pygraphviz as gv
from django.conf import settings as djangoSettings

# Create your views here.

def index(request):

    localidades = [] #inicializa uma lista para receber os nós
    for node in Localidade.nodes: #utilizando a classe Localidade com o método atributo .nodes para recuperar todos os nós do banco
        localidades.append(node.nome) #o loop adiciona a propriedade "nome" de cada nós na lista
    localidades.sort()
    context = { "localidades" : localidades, } #inclui no contexto que será renderizado o array criado

    return render(request, 'paths/index.html', context)

def results(request):
    #atribui os valores inseridos na página em suas variaveis
    origem = request.POST['origem']
    destino = request.POST['destino']
     #Verifica no lado do servidor se a origem/destino são iguais ou escolhidos corretamente
    if(origem == destino):
        context = { 'erro': True }
    else:
        #verifica se o horário de pico foi ativado 
        if request.POST.get("rush"):
            velocidade= "vrush" #Se a condição for positiva a velocidade é definida para o horário de pico
        else:
            velocidade= "vnormal" #Caso não seja definido o rush, o peso da veolicidade será normal

        query = '''MATCH (start:Localidade {nome: '%s'}), (end:Localidade {nome: '%s'})
                   CALL apoc.algo.dijkstra(start, end, 'CONECTA_COM', '%s') YIELD path, weight
                   RETURN path, weight''' % (origem, destino,velocidade) #carrega a query com algoritmo de Dijkstra utilizando o plugin APOC do neo4j. 
        
        
        results, meta = db.cypher_query(query) #executa a query retorna um record list contendo apenas 1 resultado (o menor)

        if(len(results) <1): #caso nenhum resultado tenha retornado as flags de erro são definidas
            context = { "null_result": True, "erro": False }
        else:
            result = results[0] #Recupera o unico indice do RecordList como um objeto do tipo Record
            raw_nodes = result['path'] #Atraves do index 'path' retornamos o PathGraph com todos os nós
            
            drawGraph(raw_nodes)    

            context = { 'custo': round(result['weight'],2) , "erro": False, "null_result": False } #definimos o contexto com o nome dos nos, o custo total e as flags de controle da view

    return render(request, 'paths/results.html', context)


def insert(request): #funcao para inserir um no no banco de dados
    
    context = { 'insert': False, 'status':"Ocorreu um erro" }

    if request.POST.get("nome"): #caso algum valor tenha retornado da interface
        
        nome_node = request.POST['nome']   #recupera o texto inserido na pagina
        query = "CREATE (:Localidade {nome:'%s'})" % (nome_node) #executa a query para criar um novo node
        db.cypher_query(query)
        context = { 'insert': True, 'status':"Localidade cadastrada com sucesso"}
    return render(request, 'paths/insert.html', context)


    
def conectar(request): #funcao para ligar um nó ao outro

    #recupera as localidades e cria o contexto inicial da página de relacionamentos
    localidades = [] 
    for node in Localidade.nodes:
        localidades.append(node.nome)
    localidades.sort()
    context = { "localidades" : localidades, 'insert':False, 'status': "<span style='color: red;font-weight: bolder;'>ERRO<span>"  }
    
    if request.POST.get("distancia"): #verifica se algum valor foi inserido na interface
        origem = request.POST['origem']
        destino = request.POST['destino']
        vn = int(request.POST['v_normal'])
        vp = int(request.POST['v_pico'])
        danger = int(request.POST['danger'])
        distancia_n = float(request.POST['distancia'])
        

        #O calculo do peso é realizado nesse momento para inclusão no relacionamento
        pesoN = round((60*distancia_n)/vn,2)
        pesoR  = round((60*distancia_n)/vp,2)

        if(origem == destino): #checa se origem e destino são válidos ou não são iguais
             context = { "localidades" : localidades, 'insert': True, 'status': "<span style='color: red;font-weight: bolder;'>ERRO<span>" }
        else:
            #A query abaixo cria um novo relacionamento entre 2 nós informados pelo usuário
            query = "MATCH (origem:Localidade {nome:'%s'}), (destino:Localidade {nome:'%s'}) CREATE (origem)-[:CONECTA_COM {distancia: %02f, vnormal: %02f, vrush: %02f, danger: %d}]->(destino)" % (origem,destino,distancia_n,pesoN,pesoR, danger)
            db.cypher_query(query)

            context = { "localidades" : localidades, 'insert': True, 'status': "<span style='color: green;font-weight: bolder;'>CONECTADO COM SUCESSO<span>" }
            

    return render(request, 'paths/conectar.html', context)


def drawGraph(raw_nodes):
    
    nodes = [Localidade.inflate(row).nome for row in raw_nodes.nodes]
    relationships = [rel['danger'] for rel in raw_nodes.relationships]
    
    graph = gv.AGraph(directed=True)
    graph.add_nodes_from(nodes)

    for i in range(len(nodes)-1):
        hue = 0.32*(100-relationships[i])/100
        hsv = "%f 1.0 1.0" % hue
        graph.add_edge(nodes[i],nodes[i+1],color=hsv)
    graph.layout(prog="dot")
    graph.draw(djangoSettings.STATICFILES_DIRS[0] + "/paths/img/result_graph.png")

=======
from django.shortcuts import render
from neomodel import db
from paths.models import Localidade, ConectaRel
import pygraphviz as gv
from django.conf import settings as djangoSettings

# Create your views here.

def index(request):

    localidades = [] #inicializa uma lista para receber os nós
    for node in Localidade.nodes: #utilizando a classe Localidade com o método atributo .nodes para recuperar todos os nós do banco
        localidades.append(node.nome) #o loop adiciona a propriedade "nome" de cada nós na lista
    localidades.sort()
    context = { "localidades" : localidades, } #inclui no contexto que será renderizado o array criado

    return render(request, 'paths/index.html', context)

def results(request):
    #atribui os valores inseridos na página em suas variaveis
    origem = request.POST['origem']
    destino = request.POST['destino']
     #Verifica no lado do servidor se a origem/destino são iguais ou escolhidos corretamente
    if(origem == destino):
        context = { 'erro': True }
    else:
        #verifica se o horário de pico foi ativado 
        if request.POST.get("rush"):
            velocidade= "vrush" #Se a condição for positiva a velocidade é definida para o horário de pico
        else:
            velocidade= "vnormal" #Caso não seja definido o rush, o peso da veolicidade será normal

        query = '''MATCH (start:Localidade {nome: '%s'}), (end:Localidade {nome: '%s'})
                   CALL apoc.algo.dijkstra(start, end, 'CONECTA_COM', '%s') YIELD path, weight
                   RETURN path, weight''' % (origem, destino,velocidade) #carrega a query com algoritmo de Dijkstra utilizando o plugin APOC do neo4j. 
        
        
        results, meta = db.cypher_query(query) #executa a query retorna um record list contendo apenas 1 resultado (o menor)

        if(len(results) <1): #caso nenhum resultado tenha retornado as flags de erro são definidas
            context = { "null_result": True, "erro": False }
        else:
            result = results[0] #Recupera o unico indice do RecordList como um objeto do tipo Record
            raw_nodes = result['path'] #Atraves do index 'path' retornamos o PathGraph com todos os nós
            
            drawGraph(raw_nodes)    

            context = { 'custo': round(result['weight'],2) , "erro": False, "null_result": False } #definimos o contexto com o nome dos nos, o custo total e as flags de controle da view

    return render(request, 'paths/results.html', context)


def insert(request): #funcao para inserir um no no banco de dados
    
    context = { 'insert': False, 'status':"Ocorreu um erro" }

    if request.POST.get("nome"): #caso algum valor tenha retornado da interface
        
        nome_node = request.POST['nome']   #recupera o texto inserido na pagina
        query = "CREATE (:Localidade {nome:'%s'})" % (nome_node) #executa a query para criar um novo node
        db.cypher_query(query)
        context = { 'insert': True, 'status':"Localidade cadastrada com sucesso"}
    return render(request, 'paths/insert.html', context)


    
def conectar(request): #funcao para ligar um nó ao outro

    #recupera as localidades e cria o contexto inicial da página de relacionamentos
    localidades = [] 
    for node in Localidade.nodes:
        localidades.append(node.nome)
    localidades.sort()
    context = { "localidades" : localidades, 'insert':False, 'status': "<span style='color: red;font-weight: bolder;'>ERRO<span>"  }
    
    if request.POST.get("distancia"): #verifica se algum valor foi inserido na interface
        origem = request.POST['origem']
        destino = request.POST['destino']
        vn = int(request.POST['v_normal'])
        vp = int(request.POST['v_pico'])
        danger = int(request.POST['danger'])
        distancia_n = float(request.POST['distancia'])
        

        #O calculo do peso é realizado nesse momento para inclusão no relacionamento
        pesoN = round((60*distancia_n)/vn,2)
        pesoR  = round((60*distancia_n)/vp,2)

        if(origem == destino): #checa se origem e destino são válidos ou não são iguais
             context = { "localidades" : localidades, 'insert': True, 'status': "<span style='color: red;font-weight: bolder;'>ERRO<span>" }
        else:
            #A query abaixo cria um novo relacionamento entre 2 nós informados pelo usuário
            query = "MATCH (origem:Localidade {nome:'%s'}), (destino:Localidade {nome:'%s'}) CREATE (origem)-[:CONECTA_COM {distancia: %02f, vnormal: %02f, vrush: %02f, danger: %d}]->(destino)" % (origem,destino,distancia_n,pesoN,pesoR, danger)
            db.cypher_query(query)

            context = { "localidades" : localidades, 'insert': True, 'status': "<span style='color: green;font-weight: bolder;'>CONECTADO COM SUCESSO<span>" }
            

    return render(request, 'paths/conectar.html', context)


def drawGraph(raw_nodes):
    
    nodes = [Localidade.inflate(row).nome for row in raw_nodes.nodes]
    relationships = [rel['danger'] for rel in raw_nodes.relationships]
    
    graph = gv.AGraph(directed=True)
    graph.add_nodes_from(nodes)

    for i in range(len(nodes)-1):
        hue = 0.32*(100-relationships[i])/100
        hsv = "%f 1.0 1.0" % hue
        graph.add_edge(nodes[i],nodes[i+1],color=hsv)
    graph.layout(prog="dot")
    graph.draw(djangoSettings.STATICFILES_DIRS[0] + "/paths/img/result_graph.png")

>>>>>>> origin/voyage_pygraphviz
