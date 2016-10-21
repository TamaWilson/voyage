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
    context = { "localidades" : localidades, }

    return render(request, 'paths/index.html', context)

def results(request):
    origem = request.POST['origem']
    destino = request.POST['destino']

    #Verifica no lado do servidor se a origem/destino são iguais ou escolhidos corretamente
    if(origem == destino) or (origem == "NOK") or (destino == "NOK"):
        context = { 'erro': True }
    else:
        hora_local = datetime.datetime.now().time() #carrega o horário local para uma variável
        velocidade= "v_normal" #inicia a execução com a velocidade definida como normal

        #Verifica se a variavel hora_local está no intervalo dos horários de pico    
        if (datetime.time(18,0,0,0) < hora_local and datetime.time(19,0,0,0) > hora_local) or (datetime.time(11,30,0,0) < hora_local and datetime.time(14,0,0,0) > hora_local): 
            velocidade= "v_pico" #Se a condição for positiva a velocidade é definida para o horário de pico
    
        query = '''MATCH (start:Localidade {nome: '%s'}), (end:Localidade {nome: '%s'})
        MATCH p=(start)-[:CONECTA_COM*]->(end)
        WITH p,reduce(s = 0, r IN rels(p) | s + (60*r.distancia)/r.%s) AS dist
        RETURN p, dist ORDER BY dist Limit 1''' % (origem, destino,velocidade) #carrega a query com algoritmo de Dijkstra. Nesse momento o calculo de distância é realizado na proria query
        
        
        results, meta = db.cypher_query(query) #executa a query retorna um record list contendo apenas 1 resultado (o menor)
        if(len(results) <1): #caso nenhum resultado tenha retornado as flags de erro são definidas
            context = { "null_result": True, "erro": False }
        else:
            result = results[0] #Recupera o unico indice do RecordList como um objeto do tipo Record
            raw_nodes = result['p'] #Atraves do index 'p' retornamos o PathGraph com todos os nós

            pre_nodes = [Localidade.inflate(row) for row in raw_nodes.nodes] #Inicializamos os nós para acessar suas propriedades
    
            nodes = []
            for node in pre_nodes: #percorremos a lista de nós para obter o nome deles em uma outra lista
                node.refresh()
                nodes.append(node.nome)
    
            context = { 'caminho' : nodes, 'custo': round(result['dist'],2) , "erro": False, "null_result": False } #definimos o contexto com o nome dos nos, o custo total e as flags de controle da view

    return render(request, 'paths/results.html', context)


def insert(request): #funcao para inserir um no no banco de dados
    
    context = { 'insert': False, 'status':"Ocorreu um erro" }

    if request.POST.get("nome"):
        
        nome_node = request.POST['nome']   #recupera o texto inserido na pagina
        node = Localidade(nome=nome_node)  #cria a instancia de um objeto Localidade
        node.save()    #salva o no no banco de dados   
        context = { 'insert': True, 'status':"Localidade cadastrada com sucesso"}
    return render(request, 'paths/insert.html', context)


    
def conectar(request): #funcao para ligar um nó ao outro

    #recupera as localidades e cria o contexto inicial da página de relacionamentos
    localidades = [] 
    for node in Localidade.nodes:
        localidades.append(node.nome)
    context = { "localidades" : localidades, 'insert':False, 'status': "<span style='color: red;font-weight: bolder;'>ERRO<span>"  }
    
    if request.POST.get("distancia"):
        origem = request.POST['origem']
        destino = request.POST['destino']
        vn = int(request.POST['v_normal'])
        vp = int(request.POST['v_pico'])
        distancia_n = float(request.POST['distancia'])

        if(origem == destino) or (origem == "NOK") or (destino == "NOK"):
             context = { "localidades" : localidades, 'insert': True, 'status': "<span style='color: red;font-weight: bolder;'>ERRO<span>" }
        else:
            #Busca no banco pelos nós escolhidos na pagina
            node_origem = Localidade.nodes.get(nome=origem)
            node_destino = Localidade.nodes.get(nome=destino)

            #instancia um relacionamento entre os nós com os dados informados
            relation = node_origem.conectar.connect(node_destino, {'distancia':distancia_n, 'v_normal':vn, 'v_pico':vp})
            relation.save()     #salva o relacionamento no banco e apos isso configura o contexto da página de resposta.
            context = { "localidades" : localidades, 'insert': True, 'status': "<span style='color: green;font-weight: bolder;'>CONECTADO COM SUCESSO<span>" }


    return render(request, 'paths/conectar.html', context)

