import mysql.connector
from mysql.connector import Error
from mysql.connector import ProgrammingError
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
  
#Função para verificar se o produto existe no banco de dados
def retorna_produto(cod_produto):
    try:
        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
        resultado = executor_sql.fetchone()
        if resultado: return resultado
        else: return False
    except Error as e:
        print(f'\nERRO AO VERIFICAR PRODUTO: {e}\n')

#Função que retorna os cálculos de um certo produto
def retorna_calculos(cod_produto):
    try:
        executor_sql.execute(f'SELECT * FROM CALCULOS JOIN PRODUTOS ON CALCULOS.cod = PRODUTOS.Cod_produto WHERE PRODUTOS.Cod_produto = {cod_produto}')
        resultado = executor_sql.fetchone()
        if resultado: return resultado
        else: return False
    except Error as e:
        print(f'\nERRO AO CONSULTAR CÁLCULOS: {e}\n')

#Função para inserir um produto
def inserir_produto(produto):
    try:
        executor_sql.execute(f'insert into PRODUTOS (Cod_produto, Nome_produto, Descricao_produto, CP, CF, CV, IV, ML) values ({produto[0]}, "{produto[1]}", "{produto[2]}", {produto[3]}, {produto[4]}, {produto[5]}, {produto[6]}, {produto[7]})')
        conexao_bd.commit()
        print()
        print("PRODUTO CADASTRADO COM SUCESSO!")
    except Error as e:
        print(f'\nERRO AO INSERIR PRODUTO: {e}\n')

#Função para inserir os cálculos de um produto     
def inserir_calculos(calculos):
    try:
        executor_sql.execute(f'insert into CALCULOS (cod, PV, RB, OC, calculo_custo_aquisicao, calculo_receita_bruta, calculo_custo_fixo, calculo_comissao_vendas, calculo_impostos, calculo_outros_custos, calculo_rentabilidade) values ({calculos[0]}, {calculos[1]}, {calculos[2]}, {calculos[3]}, {calculos[4]}, {calculos[5]}, {calculos[6]}, {calculos[7]}, {calculos[8]}, {calculos[9]}, {calculos[10]})')
        conexao_bd.commit()
    except Error as e:
        print(f'\nERRO AO INSERIR CÁLCULOS: {e}\n')
        
#Função para atualizar os cálculos de um produto
def atualizar_calculo(cod_calculo, calculo, novo_valor):
    try:
        executor_sql.execute(f'UPDATE CALCULOS SET {calculo} = {novo_valor} WHERE cod = {cod_calculo}')
        conexao_bd.commit()
    except Error as e:
        print(f'\nERRO AO ATUALIZAR CÁLCULO {calculo}: {e}\n')
        
#Função para consultar um dado especifico de um certo produto
def consultar_dado(dado, cod_produto):
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

#Função para exibir os cálculos de um produto
def calcular(produto):
    cod_produto = produto[0]
    CP = produto[3]
    CF = produto[4]
    CV = produto[5]
    IV = produto[6]
    ML = produto[7]
    
    PV = round((CP / (1 - ((CF + CV + IV + ML) / 100))), 2) #preço de venda
    RB =  PV - CP #receita bruta
    OC = CF + CV + IV #outros custos
    
    calculo_custo_aquisicao = round((CP / PV) * 100, 2) 
    calculo_receita_bruta = round((RB / PV) * 100, 2)
    calculo_custo_fixo = round((PV * CF) / 100, 2)
    calculo_comissao_vendas = round((CV * PV) / 100, 2)
    calculo_impostos = round((IV * PV) / 100, 2)       
    calculo_outros_custos = calculo_custo_fixo + calculo_comissao_vendas + calculo_impostos
    calculo_rentabilidade = calculo_receita_bruta - calculo_outros_custos
    
    calculos = retorna_calculos(produto[0])
    
    if calculos:
        cod_calculo = calculos[0]
        PV_bd = calculos[1]
        RB_bd = calculos[2]
        OC_bd = calculos[3]
        calculo_custo_aquisicao_bd = calculos[4]
        calculo_receita_bruta_bd = calculos[5]
        calculo_custo_fixo_bd = calculos[6]
        calculo_comissao_vendas_bd = calculos[7]
        calculo_impostos_bd = calculos[8]
        calculo_outros_custos_bd = calculos[9]
        calculo_rentabilidade_bd = calculos[10]
        
        if PV_bd != PV: atualizar_calculo(cod_calculo, 'PV', PV)
        elif RB_bd != RB: atualizar_calculo(cod_calculo, 'RB', RB)
        elif OC_bd != OC: atualizar_calculo(cod_calculo, 'OC', OC)
        elif calculo_custo_aquisicao_bd != calculo_custo_aquisicao: 
            atualizar_calculo(cod_calculo, 'calculo_custo_aquisicao', calculo_custo_aquisicao)
        elif calculo_receita_bruta_bd != calculo_receita_bruta: 
            atualizar_calculo(cod_calculo, 'calculo_receita_bruta', calculo_receita_bruta)
        elif calculo_custo_fixo_bd != calculo_custo_fixo: 
            atualizar_calculo(cod_calculo, 'calculo_custo_fixo', calculo_custo_fixo)
        elif calculo_comissao_vendas_bd != calculo_comissao_vendas: 
            atualizar_calculo(cod_calculo, 'calculo_comissao_vendas', calculo_comissao_vendas)
        elif calculo_impostos_bd != calculo_impostos: 
            atualizar_calculo(cod_calculo, 'calculo_impostos', calculo_impostos)
        elif calculo_outros_custos_bd != calculo_outros_custos: 
            atualizar_calculo(cod_calculo, 'calculo_outros_custos', calculo_outros_custos)
        elif calculo_rentabilidade_bd != calculo_rentabilidade: 
            atualizar_calculo(cod_calculo, 'calculo_rentabilidade', calculo_rentabilidade)
    else:    
        calculos = [cod_produto, PV, RB, OC, calculo_custo_aquisicao, calculo_receita_bruta, calculo_custo_fixo, calculo_comissao_vendas, calculo_impostos, calculo_outros_custos, calculo_rentabilidade]
        inserir_calculos(calculos)
        
    print()
    tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
    tabela_resultados = [
        ["A. Preço de Venda", PV, "100"],
        ["B. Custo de Aquisição (Fornecedor)", CP, calculo_custo_aquisicao],
        ["C. Receita Bruta (A-B)", RB, calculo_receita_bruta],
        ["D. Custo Fixo/Administrativo", calculo_custo_fixo, CF],
        ["E. Comissão de Vendas", calculo_comissao_vendas, CV],
        ["F. Impostos", calculo_impostos, IV],
        ["G. Outros custos (D+E+F)", calculo_outros_custos, OC],
        ["H. Rentabilidade (C-G)", calculo_rentabilidade, ML]
    ]  
    print(tabulate(tabela_resultados, headers = tabela_cabecalho))
                                            
    #Faixa de lucro do produto
    if ML >= 20:
        print('\nSua classificação de rentabilidade é de nivel ALTO')
    elif ML >= 10 and ML < 20:
        print('\nSua classificação de rentabilidade é de nivel MÉDIO')
    elif ML > 0 and ML < 10:
        print('\nSua classificação de rentabilidade é de nivel BAIXO')
    elif ML == 0:
        print('\nSua classificação de rentabilidade é de nivel EQUILIBRADO')
    else:
        print('\nSua classificação de rentabilidade é de PREJUIZO')
    
#Função que pega dados do produto caso o usuário escolha cadastrar um produto
def cadastrar(cod_produto):
    dados_inseridos = False
    while not dados_inseridos:
        try:
            produto = retorna_produto(cod_produto)
        
            if produto:
                print("ESSE CÓDIGO JÁ FOI REGISTRADO!")
                continue
    
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
    
            #Pegando dados para inserir na tabela PRODUTOS
            produto = [cod_produto, nome_produto, descricao_produto, CP, CF, CV, IV, ML]
            inserir_produto(produto)
    
            calcular(produto)
    
            dados_inseridos = True
        except ProgrammingError:
            print("DIGITE UM CÓDIGO VÁLIDO!")
            continue

#Função para consultar todas as informações de um certo produto
def consultar(cod_produto):
    try:
        produto = retorna_produto(cod_produto)

        if produto:
            nome_produto = produto[1]
            descricao_produto = produto[2]
            CP = produto[3]
            CF = produto[4]
            CV = produto[5]
            IV = produto[6]
            ML = produto[7]
            
            calculos = retorna_calculos(cod_produto)
            PV = calculos[1]
            RB = calculos[2]
            OC = calculos[3]
            calculo_custo_aquisicao = calculos[4]
            calculo_receita_bruta = calculos[5]
            calculo_custo_fixo = calculos[6]
            calculo_comissao_vendas = calculos[7]
            calculo_impostos = calculos[8]
            calculo_outros_custos = calculos[9]
            calculo_rentabilidade = calculos[10]

            print(f'\nCÓDIGO DO PRODUTO: {cod_produto}')
            print(f'NOME DO PRODUTO: {nome_produto}')
            print(f'DESCRIÇÃO DO PRODUTO: {descricao_produto}')
            
            print('\nCÁLCULOS:')
            tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
            tabela_resultados = [
                ["A. Preço de Venda", PV, "100"],
                ["B. Custo de Aquisição (Fornecedor)", CP, calculo_custo_aquisicao],
                ["C. Receita Bruta (A-B)", RB, calculo_receita_bruta],
                ["D. Custo Fixo/Administrativo", calculo_custo_fixo, CF],
                ["E. Comissão de Vendas", calculo_comissao_vendas, CV],
                ["F. Impostos", calculo_impostos, IV],
                ["G. Outros custos (D+E+F)", calculo_outros_custos, OC],
                ["H. Rentabilidade (C-G)", calculo_rentabilidade, ML]
            ]  
            print(tabulate(tabela_resultados, headers = tabela_cabecalho))
                                                    
            if ML >= 20:
                print('\nSua classificação de rentabilidade é de nivel ALTO')
            elif ML >= 10 and ML < 20:
                print('\nSua classificação de rentabilidade é de nivel MÉDIO')
            elif ML > 0 and ML < 10:
                print('\nSua classificação de rentabilidade é de nivel BAIXO')
            elif ML == 0:
                print('\nSua classificação de rentabilidade é de nivel EQUILIBRADO')
            else:
                print('\nSua classificação de rentabilidade é de PREJUIZO')
        else: print('\nPRODUTO NÃO CADASTRADO')

    except Error as e:
        print(f'ERRO AO CONSULTAR PRODUTO: {e}')

#Função para atualizar um produto especifico
def atualizar(cod_produto):
    try:
        produto = retorna_produto(cod_produto)

        if produto:
            dado = None

            print('Qual dado você gostaria de atualizar?')
            menu=['Nome do produto',\
                'Descrição do produto',\
                'Custo de produto',\
                'Custo fixo',\
                'Comissão de vendas',\
                'Impostos',\
                'Rentabilidade',\
                'Sair']
            
            while dado == None:
                opcao = int(opcaoEscolhida(menu))

                if opcao == 1:
                    dado = 'Nome_produto'
                elif opcao == 2:
                    dado = 'Descricao_produto'
                elif opcao == 3:
                    dado = 'CP'
                elif opcao == 4:
                    dado = 'CF'
                elif opcao == 5:
                    dado = 'CV'
                elif opcao == 6:
                    dado = 'IV'
                elif opcao == 7:
                    dado = 'ML'
                else: break

            if dado != None:
                antigo_valor = produto[opcao]
                if dado in ['CP', 'CF', 'CV', 'IV', 'ML']:
                    dado_numerico = True
                    novo_valor = obter_num_float("Digite o novo valor para esse dado: ")
                else: novo_valor = obter_input("Digite o novo valor para esse dado: ")
                
                if antigo_valor == novo_valor:
                    print('\nESSA INFORMAÇÃO JÁ ESTÁ ARMAZENADA!')
                else:
                    if isinstance(novo_valor, str): #verifica se o valor é uma string
                        novo_valor = f'"{novo_valor}"'
                    executor_sql.execute(f'UPDATE PRODUTOS SET {dado} = {novo_valor} WHERE Cod_produto = {cod_produto}')
                    conexao_bd.commit()
                    print(f'\nPRODUTO ATUALIZADO!')
                    print(f'{dado} = {antigo_valor} -> {dado} = {novo_valor}')
                    
                    if dado_numerico:
                        produto = retorna_produto(cod_produto)
                        calcular(produto)
        else: print('\nPRODUTO NÃO EXISTENTE!') 
    except Error as e:
        print(f'\nERRO AO ATUALIZAR PRODUTO: {e}')

#Função para listar todos os produtos do banco de dados
def listar():
    try:
        executor_sql.execute('SELECT * FROM PRODUTOS')
        produtos = [produto for produto in executor_sql.fetchall()]
        
        if len(produtos) > 0:
            for dados_produto in produtos:
                print(f'\nCÓDIGO DO PRODUTO: {dados_produto[0]}')
                print(f'NOME DO PRODUTO: {dados_produto[1]}')
                print(f'DESCRIÇÃO DO PRODUTO: {dados_produto[2]}')
                print(f'CUSTO DO PRODUTO: R$ {dados_produto[3]}')
                print(f'CUSTO FIXO DO PRODUTO: {dados_produto[4]}%')
                print(f'COMISSÃO DE VENDAS: {dados_produto[5]}%')
                print(f'IMPOSTOS DO PRODUTO: {dados_produto[6]}%')
                print(f'RENTABILIDADE DO PRODUTO: {dados_produto[7]}%')
        else: print('\nVOCÊ NÃO POSSUE PRODUTOS!')
    except Error as e:
        print(f'\nERRO AO LISTAR PRODUTOS: {e}\n')

#Função para excluir um produto especifico
def excluir(cod_produto):
    try:
        produto = retorna_produto(cod_produto)

        if produto:
            print(f'\nCÓDIGO DO PRODUTO: {produto[0]}')
            print(f'NOME DO PRODUTO: {produto[1]}')

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

#Função para cadastrar o usuário ou verificar se o mesmo já está cadastrado
def acessar(nome_digitado, senha_digitada):
    acesso_liberado = False
    while not acesso_liberado:
        try:
            nome_digitado = nome_digitado.lower()
            senha_digitada = senha_digitada.lower()
            
            executor_sql.execute(f'SELECT * FROM USUARIOS WHERE nome_usuario = "{nome_digitado}"')
            usuario = executor_sql.fetchone()

            if usuario:
                nome_usuario = usuario[0]
                senha_usuario = usuario[1]

                while senha_usuario != senha_digitada:
                    print('\nSENHA INCORRETADA\n')
                    senha_digitada = obter_input('Senha: ').lower()

                print(f'\nSEJA BEM-VINDO AO INSTOCK {nome_usuario}')
                acesso_liberado = True
            else: 
                print('\nUSUÁRIO NÃO CADASTRADO!\n')

                resposta = obter_input('GOSTARIA DE REALIZAR O CADASTRO? [S/N]: ').upper()
                while resposta not in ['S', 'N']:
                    print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                    resposta = obter_input('\nGOSTARIA DE REALIZAR O CADASTRO? [S/N]: ').upper()

                if resposta == 'S':
                    executor_sql.execute(f'insert into USUARIOS (nome_usuario, senha_usuario) values ("{nome_digitado}", "{senha_digitada}")')
                    conexao_bd.commit()
                    print('\nUSUÁRIO CADASTRADO!\n')
                    print(f'SEJA BEM-VINDO AO INSTOCK {nome_digitado}')
                    acesso_liberado = True
        except Error as e:
            print(f'\nERRO AO REALIZAR LOGIN: {e}\n') 



#Inicio do programa
try:
    nome_digitado = obter_input('Nome de usuário: ')
    senha_digitada = obter_input('Senha: ')
    acessar(nome_digitado, senha_digitada)
except KeyboardInterrupt:
    print("\nPROGRAMA INTERROMPIDO!\n")
    
print('PARA INICIARMOS ESCOLHA UMA DAS OPÇÕES ABAIXO:')

menu=['CADASTRAR PRODUTO',\
      'CONSULTAR PRODUTO',\
      'ATUALIZAR PRODUTO',\
      'LISTAR PRODUTOS',\
      'EXCLUIR PRODUTO',\
      'SAIR']

opcao=666
while opcao!=6:
    try: 
        opcao = int(opcaoEscolhida(menu))
    
        if opcao==1:
            cod_produto = obter_input("\nDigite o código do produto: ")
            cadastrar(cod_produto)
    
        elif opcao==2:
            cod_produto = obter_input("\nDigite o código do produto que deseja consultar: ")
            consultar(cod_produto)
    
        elif opcao==3:
            cod_produto = obter_input("\nDigite o código do produto que deseja atualizar: ")   
            atualizar(cod_produto)
    
        elif opcao==4:
            listar()
    
        elif opcao==5:
            cod_produto = obter_input("\nDigite o código do produto que deseja excluir: ")
            excluir(cod_produto)
    except KeyboardInterrupt:
        print("\nPROGRAMA INTERROMPIDO!\n")
        
executor_sql.close()
conexao_bd.close()
print('\nOBRIGADO POR UTILIZAR O PROGRAMA!\n')
