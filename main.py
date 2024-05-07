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
        print("SUCESSO AO CONECTAR AO BANCO DE DADOS")
except Error as e:
    print(f'\nERRO AO CONECTAR AO BANCO DE DADOS: {e}\n')

#Função para inserir um produto
def inserir_produto(produto):
    try:
        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {produto[0]}')
        resultado = executor_sql.fetchone()
        if not resultado:
            executor_sql.execute(f'insert into PRODUTOS (Cod_produto, Nome_produto, Descricao_produto, PV, CP, RB, CF, CV, IV, OC, ML) values ({produto[0]}, {produto[1]}, {produto[2]}, {produto[3]}, {produto[4]}, {produto[5]}, {produto[6]}, {produto[7]}, {produto[8]}, {produto[9]}, {produto[10]})')
        else: print('\nESTE PRODUTO JÁ EXISTE!')

    except Error as e:
        print(f'\nERRO AO INSERIR PRODUTO: {e}\n')

#Função para consultar um dado especifico de um certo produto
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

#Função para atualizar um produto especifico
def atualizar_produto(dado, novo_valor, cod_produto):
    try:
        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
        resultado = executor_sql.fetchone()

        if resultado:
            antigo_valor = consultar_produto(dado, cod_produto)
            if antigo_valor == novo_valor: print('\nESSA INFORMAÇÃO JÁ ESTÁ ARMAZENADA!')
            else:
                if isinstance(novo_valor, str): #verifica se o valor é uma string
                    novo_valor = f'"{novo_valor}"'
                executor_sql.execute(f'UPDATE PRODUTOS SET {dado} = {novo_valor} WHERE Cod_produto = {cod_produto}')
                conexao_bd.commit()
                print(f'\nPRODUTO ATUALIZADO!')
                print(f'{dado} = {antigo_valor} -> {dado} = {novo_valor}')
        else: print('\nPRODUTO NÃO EXISTENTE!') 
    except Error as e:
        print(f'\nERRO AO ATUALIZAR PRODUTO: {e}')

#Função para excluir um produto especifico
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

#Função para listar todos os produtos do banco de dados
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
        else: print('\nVOCÊ NÃO POSSUI PRODUTOS!')
    except Error as e:
        print(f'\nERRO AO LISTAR PRODUTOS: {e}\n')

#Função para consultar todos os dados de um dado produto
def consultar_produto_especifico(cod_produto):
    executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')

    print(f'\nCÓDIGO DO PRODUTO: {consultar_produto('Cod_produto', cod_produto)}')
    print(f'NOME DO PRODUTO: {consultar_produto('Nome_produto', cod_produto)}')
    print(f'DESCRIÇÃO DO PRODUTO: {consultar_produto('Descricao_produto', cod_produto)}')
    print(f'CUSTO DO PRODUTO: R$ {consultar_produto('CP', cod_produto)}')
    print(f'CUSTO FIXO DO PRODUTO: {consultar_produto('CF', cod_produto)}%')
    print(f'COMISSÃO DE VENDAS: {consultar_produto('CV', cod_produto)}%')
    print(f'IMPOSTOS DO PRODUTO: {consultar_produto('IV', cod_produto)}%')
    print(f'RENTABILIDADE DO PRODUTO: {consultar_produto('ML', cod_produto)}%')

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

#Função para criar menu de opções
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
    
#Função que pega dados do produto caso o usuário escolha cadastrar um produto
def pegar_dados():
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

                PV = round((CP / (1 - ((CF + CV + IV + ML) / 100))), 2) #preço de venda

                calculo_custo_aquisicao = round((CP / PV) * 100, 2) 
                RB = PV - CP  #receita bruta
                calculo_receita_bruta = round(((PV - CP) / PV) * 100, 2)
                calculo_custo_fixo = round((PV * CF) / 100, 2)
                calculo_comissao_vendas = round((CV * PV) / 100, 2)
                calculo_impostos = round((IV * PV) / 100, 2)       
                OC = CF + CV + IV #outros custos
                calculo_outros_custos = calculo_custo_fixo + calculo_comissao_vendas + calculo_impostos
                calculo_rentabilidade = calculo_receita_bruta - calculo_outros_custos

                #Pegando dados para inserir na tabela PRODUTOS e na tabela CALCULOS
                produto = [cod_produto, nome_produto, descricao_produto, PV, CP, RB, CF, CV, IV, OC, ML]
                
                calculos = [cod_produto, calculo_custo_aquisicao, calculo_receita_bruta, calculo_custo_fixo, calculo_comissao_vendas, calculo_impostos, calculo_outros_custos, calculo_rentabilidade]

                inserir_produto(produto)
                # inserir_calculos(calculos)

                #Fora dessa função (mudar)        
                print()
                tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
                tabela_resultados = [
                ["A. Preço de Venda", PV, "100"], #consultar_produto('PV', cod_produto)
                ["B. Custo de Aquisição (Fornecedor)", consultar_produto('CP', cod_produto), calculo_custo_aquisicao],
                ["C. Receita Bruta (A-B)", RB, calculo_receita_bruta], #consultar_produto('RB', cod_produto)
                ["D. Custo Fixo/Administrativo", calculo_custo_fixo, consultar_produto('CF', cod_produto)],
                ["E. Comissão de Vendas", calculo_comissao_vendas, consultar_produto('CV', cod_produto)],
                ["F. Impostos", calculo_impostos, consultar_produto('IV', cod_produto)],
                ["G. Outros custos (D+E+F)", calculo_outros_custos, OC], #consultar_produto('OC', cod_produto)
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
                  
            except Exception:
                print(Exception)    


#Inicio do programa
print('SEJA BEM-VINDO AO INSTOCK!')
print('PARA INICIARMOS ESCOLHA UMA DAS OPÇÕES A BAIXO:\n')

menu=['CADASTRAR PRODUTO',\
      'CONSULTAR DADO',\
      'ATUALIZAR INFORMAÇÃO',\
      'LISTAR PRODUTOS',\
      'EXCLUIR PRODUTO',\
      'Sair do Programa']

opcao=666
while opcao!=6:

    opcao = int(opcaoEscolhida(menu))

    if opcao==1:
        pegar_dados()

    elif opcao==2:
        #consultar_produto()
        print()

    elif opcao==3:
        cod_produto = input("Digite o código do produto que deseja atualizar: ")
        consultar_produto_especifico(cod_produto)
        print()
        dado = input("Digite o dado que deseja atualizar:")
        novo_valor = ("Digite o novo valor para esse dado: ")
        atualizar_produto(dado, novo_valor, cod_produto)

    elif opcao==4:
        listar_produtos()

    elif opcao==5:
        cod_produto = input("Digite o código do produto que deseja excluir: ")
        excluir_produto(cod_produto)

#Opção de continuar
continuar = obter_input('\nDeseja continuar utilizando o programa? [S/N]: ').upper()
while continuar not in ['S', 'N']:
    print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
    continuar = obter_input('\nDeseja continuar utilizando o programa? [S/N]: ').upper()
    if continuar == 'N':
        executor_sql.close()
        conexao_bd.close()
        print('\nOBRIGADO POR USAR ESTE PROGRAMA!')
        break
                                
#Prepara o código para o próximo produto
print('\nINSIRA AS INFORMAÇÕES DO PRÓXIMO PRODUTO!\n')