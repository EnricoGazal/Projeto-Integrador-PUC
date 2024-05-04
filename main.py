import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

#Configuração do banco de dados
try:
    conexao_bd = mysql.connector.connect(
        host="172.16.12.14", # IP do servidor da PUC
        user="BD080324137",
        password="Orinf7",
        database="BD080324137"
    )
    if conexao_bd.is_connected():
        executor_sql = conexao_bd.cursor() #executor de comandos SQL
except Error as e:
    print(f'ERRO AO CONECTAR AO BANCO DE DADOS: {e}\n')

def inserir_dados(produtos_insert, dados):
    try:
        executor_sql.execute(produtos_insert, dados)
        conexao_bd.commit()
    except Error as e:
        print(f'ERRO AO INSERIR PRODUTO: {e}\n')

def consulta_dado (dado, cod_produto):
    try:
        executor_sql.execute('SELECT column_name FROM information_schema.columns WHERE table_name = "PRODUTOS"')
        resultado = executor_sql.fetchall()  #recupera os dados gerados pela query

        #transforma o array de dados obtidos em um array de strings para consulta
        colunas_tabela = []
        for item in resultado:
            colunas_tabela.append(item[0])
        
        if dado in colunas_tabela:
            executor_sql.execute(f'SELECT {dado} FROM PRODUTOS WHERE Cod_produto like {cod_produto}')
            resultado = executor_sql.fetchall()
            return resultado[0][0] #pega o primeiro item dos dados que no caso será o dado solicitado
        else: print('ESSE TIPO DE DADO NÃO EXISTE NA TABELA!')
    except Error as e:
        print(f'\nERRO AO CONSULTAR DADO: {e}\n')

#Função para obter o valor de um input
def obter_input(texto):
    valor = input(texto)
    while not valor.strip():
        print('\nINSIRA UM VALOR VÁLIDO!')
        valor = input(texto)
    return valor

#Função para obter um valor do tipo float em um input  
def obter_num_float(numero):
    while True:
        try:
            valor = round(float(input(numero)), 2)
            while valor <= 0:
                print('\nINSIRA UM VALOR NUMÉRICO POSITIVO E ACIMA DE 0!')
                valor = round(float(input(numero)), 2)
            return valor
        except ValueError:
            print('\nINSIRA UM VALOR NUMÉRICO!')
    
print('SEJA BEM-VINDO AO INSTOCK!')
print('PARA INICIARMOS FORNEÇA AS INFORMAÇÕES ABAIXO POR FAVOR\n')

while True:
        try:
            cod_produto = obter_input("Digite o código do produto: ") #chave primária
            nome_produto = obter_input("Digite o nome do produto: ")
            descricao_produto = obter_input("Digite a descrição do produto: ")

            #custo do produto
            CP = obter_num_float("Digite o custo do produto (R$): ")
               
            #custo fixo/administrativo
            CF = obter_num_float("Digite o custo do fixo (%): ")
                
            #comissão de vendas
            CV = obter_num_float("Digite a comissão sobre a venda (%): ")
                
            #impostos 
            IV = obter_num_float("Digite o valor dos impostos (%): ")
                
            #rentabilidade
            ML = obter_num_float("Digite a rentabilidade desejada (%): ")

            #Inserindo os dados dos produtos da tabela
            produtos_insert = "insert into PRODUTOS (Cod_produto, Nome_produto, Descricao_produto, CP, CF, CV, IV , ML) values (%s, %s, %s, %s, %s, %s, %s, %s)"
            dados = (cod_produto, nome_produto, descricao_produto, CP, CF, CV, IV, ML)
            inserir = inserir_dados(produtos_insert, dados)
            
            #Fórmula Preço de Venda
            PV = round((CP / (1 - ((CF + CV + IV + ML) / 100))), 2)
            calculo_custo_aquisicao = round((CP / PV) * 100, 2)
            calculo_receita_bruta = round(((PV - CP) / PV) * 100, 2)
            calculo_custo_fixo = round((PV * CF) / 100, 2)
            calculo_comissao_vendas = round((CV * PV) / 100, 2)
            calculo_impostos = round((IV * PV) / 100, 2)
            calculo_outros_custos = calculo_custo_fixo + calculo_comissao_vendas + calculo_impostos
            calculo_rentabilidade = calculo_receita_bruta - calculo_outros_custos
            
            print()
            tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
            tabela_resultados = [
                ["A. Preço de Venda", PV, "100"],
                ["B. Custo de Aquisição (Fornecedor)", consulta_dado('CP', cod_produto), calculo_custo_aquisicao],
                ["C. Receita Bruta (A-B)", (PV - CP), calculo_receita_bruta],
                ["D. Custo Fixo/Administrativo", calculo_custo_fixo, consulta_dado('CF', cod_produto)],
                ["E. Comissão de Vendas", calculo_comissao_vendas, consulta_dado('CV', cod_produto)],
                ["F. Impostos", calculo_impostos, consulta_dado('IV', cod_produto)],
                ["G. Outros custos (D+E+F)", calculo_outros_custos, (CF + CV + IV)],
                ["H. Rentabilidade (C-G)", calculo_rentabilidade, consulta_dado('ML', cod_produto)]
            ]  
            print(tabulate(tabela_resultados, headers = tabela_cabecalho))
            
            #Faixa de lucro do produto
            if calculo_rentabilidade >= 20:
                print('\nSua classificação de rentabilidade é de nivel ALTO')
                  
            elif calculo_rentabilidade >= 10 and calculo_rentabilidade < 20:
                print('\nSua classificação de rentabilidade é de nivel MÉDIO')
                  
            elif calculo_rentabilidade > 0 and calculo_rentabilidade < 10:
                print('\nSua classificação de rentabilidade é de nivel BAIXO')
                  
            elif calculo_rentabilidade == 0:
                print('\nSua classificação de rentabilidade é de nivel EQUILIBRADO')
                  
            else:
                print('\nSua classificação de rentabilidade é de PREJUIZO')
                   
            #Opção de continuar
            continuar = input('\nDESEJA CONTINUAR UTILIZANDO O PROGRAMA? [S/N]: ').upper()
            while continuar not in ['S', 'N']:
                print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                continuar = input('\nDESEJA CONTINUAR UTILIZANDO O PROGRAMA? [S/N]: ').upper()
            if continuar == 'N':
                executor_sql.close()
                conexao_bd.close()
                print('\nOBRIGADO POR USAR ESTE PROGRAMA!')
                break
                
            print('\nINSIRA AS INFORMAÇÕES DO PRÓXIMO PRODUTO!\n')
                
        except Exception:
            print(Exception)