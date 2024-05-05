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
    print(f'\nERRO AO CONECTAR AO BANCO DE DADOS: {e}\n')

# Função para inserir um produto
def inserir_produto(produtos_insert, dados):
    try:
        executor_sql.execute(produtos_insert, dados)
        conexao_bd.commit()
    except Error as e:
        print(f'\nERRO AO INSERIR PRODUTO: {e}\n')

# Função para consultar um dado especifico de um certo produto
def consultar_produto(dado, cod_produto):
    try:
        executor_sql.execute('SELECT column_name FROM information_schema.columns WHERE table_name = "PRODUTOS"')
        colunas_tabela = [item[0] for item in executor_sql.fetchall()]
        
        if dado in colunas_tabela:
            executor_sql.execute(f'SELECT {dado} FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
            resultado = executor_sql.fetchone()
            return resultado[0] #pega o primeiro item dos dados que no caso será o dado solicitado
        else: print(f'\n"{dado}" NÃO EXISTE NA TABELA!')
    except Error as e:
        print(f'\nERRO AO CONSULTAR DADO: {e}\n')

# Função para atualizar um produto especifico
def atualizar_produto(dado, novo_valor, cod_produto):
    try:
        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
        resultado = executor_sql.fetchone()

        if resultado:
            antigo_valor = consultar_produto(dado, cod_produto)
            executor_sql.execute(f'UPDATE PRODUTOS SET {dado} = {novo_valor} WHERE Cod_produto = {cod_produto}')
            conexao_bd.commit()
            print(f'\nPRODUTO ATUALIZADO!')
            print(f'\n{dado} = {antigo_valor} -> {dado} = {novo_valor}')

        else: print('\nPRODUTO NÃO EXISTENTE!') 
    except Error as e:
        print(f'\nERRO AO ATUALIZAR PRODUTO: {e}')

# Função para excluir um produto especifico
def excluir_produto(cod_produto):
    try:
        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
        resultado = executor_sql.fetchone()

        if resultado:
            print(f'\nCÓDIGO DO PRODUTO: {consultar_produto('Cod_produto', cod_produto)}')
            print(f'NOME DO PRODUTO: {consultar_produto('Nome_produto', cod_produto)}')

            resposta = obter_input('\nGOSTARIA DE EXCLUIR O PRODUTO ACIMA? [S/N]: ').upper()
            while resposta not in ['S', 'N']:
                print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                resposta = obter_input('\nGOSTARIA DE EXCLUIR O PRODUTO ACIMA? [S/N]:').upper()
            if resposta == 'S':
                executor_sql.execute(f'DELETE FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
                conexao_bd.commit()
                print('\nPRODUTO EXCLUÍDO COM SUCESSO!')
        else: print('\nPRODUTO NÃO EXISTENTE!')
    except Error as e:
        print(f'\nERRO AO EXCLUIR PRODUTO: {e}\n')

# Função para listar todos os produtos do banco de dados
def listar_produtos():
    try:
        executor_sql.execute('SELECT * FROM PRODUTOS')
        produtos = [produto for produto in executor_sql.fetchall()]
        
        if len(produtos) > 0:
            for dados_produto in produtos:
                cod_produto = dados_produto[0]
                print(f'\nCÓDIGO DO PRODUTO: {consultar_produto('Cod_produto', cod_produto)}')
                print(f'NOME DO PRODUTO: {consultar_produto('Nome_produto', cod_produto)}')
                print(f'DESCRIÇÃO DO PRODUTO: {consultar_produto('Descricao_produto', cod_produto)}')
                print(f'CUSTO DO PRODUTO: R$ {consultar_produto('CP', cod_produto)}')
                print(f'CUSTO FIXO DO PRODUTO: {consultar_produto('CF', cod_produto)}%')
                print(f'COMISSÃO DE VENDAS: {consultar_produto('CV', cod_produto)}%')
                print(f'IMPOSTOS DO PRODUTO: {consultar_produto('IV', cod_produto)}%')
                print(f'RENTABILIDADE DO PRODUTO: {consultar_produto('ML', cod_produto)}%')
        else: print('\nVOCÊ NÃO POSSUE PRODUTOS!')
    except Error as e:
        print(f'\nERRO AO LISTAR PRODUTOS: {e}\n')

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

# Função para criar menu de opções
def opcaoEscolhida(mnu):
    print ()

    opcoesValidas=[]
    posicao=0
    while posicao<len(mnu):
        print (posicao+1,') ',mnu[posicao],sep='')
        opcoesValidas.append(str(posicao+1))
        posicao+=1

    print()
    opcao = obter_input('Qual é a sua opção? ')
    while opcao not in opcoesValidas:
        print('\nOPÇÃO INVÁLIDA!')
        opcao = obter_input('Qual é a sua opção? ')
    return opcao
    
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
            # produtos_insert = "insert into PRODUTOS (Cod_produto, Nome_produto, Descricao_produto, CP, CF, CV, IV , ML) values (%s, %s, %s, %s, %s, %s, %s, %s)"
            # dados = (cod_produto, nome_produto, descricao_produto, CP, CF, CV, IV, ML)
            # inserir = inserir_produto(produtos_insert, dados)
            
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
                ["B. Custo de Aquisição (Fornecedor)", consultar_produto('CP', cod_produto), calculo_custo_aquisicao],
                ["C. Receita Bruta (A-B)", (PV - CP), calculo_receita_bruta],
                ["D. Custo Fixo/Administrativo", calculo_custo_fixo, consultar_produto('CF', cod_produto)],
                ["E. Comissão de Vendas", calculo_comissao_vendas, consultar_produto('CV', cod_produto)],
                ["F. Impostos", calculo_impostos, consultar_produto('IV', cod_produto)],
                ["G. Outros custos (D+E+F)", calculo_outros_custos, (CF + CV + IV)],
                ["H. Rentabilidade (C-G)", calculo_rentabilidade, consultar_produto('ML', cod_produto)]
            ]  
            print(tabulate(tabela_resultados, headers = tabela_cabecalho))
            
            #Faixa de lucro do produto
            if consultar_produto('ML', cod_produto) >= 20:
                print('\nSua classificação de rentabilidade é de nivel ALTO')
                  
            elif consultar_produto('ML', cod_produto) >= 10 and consultar_produto('ML', cod_produto) < 20:
                print('\nSua classificação de rentabilidade é de nivel MÉDIO')
                  
            elif consultar_produto('ML', cod_produto) > 0 and consultar_produto('ML', cod_produto) < 10:
                print('\nSua classificação de rentabilidade é de nivel BAIXO')
                  
            elif consultar_produto('ML', cod_produto) == 0:
                print('\nSua classificação de rentabilidade é de nivel EQUILIBRADO')
                  
            else:
                print('\nSua classificação de rentabilidade é de PREJUIZO')
                   
            # Opção de continuar
            continuar = obter_input('\nDESEJA CONTINUAR UTILIZANDO O PROGRAMA? [S/N]: ').upper()
            while continuar not in ['S', 'N']:
                print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                continuar = obter_input('\nDESEJA CONTINUAR UTILIZANDO O PROGRAMA? [S/N]: ').upper()
            if continuar == 'N':
                executor_sql.close()
                conexao_bd.close()
                print('\nOBRIGADO POR USAR ESTE PROGRAMA!')
                break
                
            print('\nINSIRA AS INFORMAÇÕES DO PRÓXIMO PRODUTO!\n')
                
        except Exception:
            print(Exception)