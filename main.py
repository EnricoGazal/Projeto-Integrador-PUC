import mysql.connector
from tabulate import tabulate

#Configuração do banco de dados
try:
    conexao_bd = mysql.connector.connect(
        host="172.16.12.14", #IP servidor da PUC
        user="nome_de_usuario",
        password="senha_do_usuario",
        database="nome_do_banco_de_dados"
    )
    print('CONECTADO COM SUCESSO!')
except Exception:
    print(Exception)

def executar_query(query):
    executor_sql = conexao_bd.cursor()
    try:
        executor_sql.execute(query)
        conexao_bd.commit()
        print("'",query,"'", "- REALIZADO COM SUCESSO")
    except Exception:
        print(Exception)

#Função para obter o valor de um input
def obter_input(mensagem):
    valor = input(mensagem)
    while not valor.strip():
        print('\nINSIRA UM VALOR VÁLIDO!')
        valor = input(mensagem)
    return valor

#Função para obter um valor do tipo float em um input  
def obter_num_float(mensagem):
    valor = float(input(mensagem))
    while valor <= 0:
        print('\nINSIRA UM VALOR NUMÉRICO POSITIVO E ACIMA DE 0!')
        valor = float(input(mensagem))
    return valor
    
print('SEJA BEM-VINDO AO INSTOCK!')
print('PARA INICIARMOS FORNEÇA AS INFORMAÇÕES ABAIXO POR FAVOR\n')

cod_produto = obter_input("Digite o código do produto: ") #chave primária
nome_produto = obter_input("Digite o nome do produto: ")
descricao_produto = obter_input("Digite a descrição do produto: ")

while True:
        try:
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
            
            #Fórmula Preço de Venda
            PV = CP / (1 - ((CF + CV + IV + ML) / 100))
            
            print()
            tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
            tabela_resultados = [
                ["A. Preço de Venda", PV, "100"],
                ["B. Custo de Aquisição (Fornecedor)", CP, (CP / PV) * 100],
                ["C. Receita Bruta (A-B)", (PV - CP), ((PV - CP) / PV) * 100],
                ["D. Custo Fixo/Administrativo", (PV * CF) / 100, CF],
                ["E. Comissão de Vendas", (CV * PV) / 100, CV],
                ["F. Impostos", (IV * PV) / 100, IV],
                ["G. Outros custos (D+E+F)", ((PV * CF) / 100)+((CV * PV) / 100)+((IV * PV) / 100), CF + CV + IV],
                ["H. Rentabilidade (C-G)", ((PV - CP) - (((PV * CF) / 100) + ((CV * PV) / 100) + ((IV * PV) / 100))), ML]
            ]  
            print(tabulate(tabela_resultados, headers = tabela_cabecalho))
            
            
            #Faixa de lucro do produto
            rentabilidade = ((PV - CP) - (CF + CV + IV))
            if rentabilidade >= 0.20 * PV:
                print('\nSua classificação de rentabilidade é de nivel alto')
                  
            elif rentabilidade >= 0.10 * PV < 0.20 * PV:
                print('\nSua classificação de rentabilidade é de nivel médio')
                  
            elif rentabilidade > 0 * 100 < 0.10 * 100:
                print('\nSua classificação de rentabilidade é de nivel baixo')
                  
            elif rentabilidade == 0:
                print('\nSua classificação de rentabilidade é de nivel equilibrado')
                  
            else:
                rentabilidade < 0 * 100
                print('\nSua classificação de rentabilidade é de prejuizo')
                  
                  
            #Opção de continuar
            continuar = input('\nDESEJA CONTINUAR UTILIZANDO O PROGRAMA? [S/N]: ').upper()
            if continuar == 'N':
                print('\nOBRIGADO POR USAR ESTE PROGRAMA!')
                break
            elif continuar != 'S' and continuar != 'N':
                print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                
            print('\nINSIRA AS INFORMAÇÕES DO PRÓXIMO PRODUTO')
            cod_produto = obter_input("Digite o código do produto: ") #chave primária
            nome_produto = obter_input("Digite o nome do produto: ")
            descricao_produto = obter_input("Digite a descrição do produto: ")
                
        except ValueError:
            print('\nINSIRA UM VALOR NUMÉRICO!')