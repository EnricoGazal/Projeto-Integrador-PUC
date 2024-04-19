from tabulate import tabulate

def obter_input(mensagem):
    valor = input(mensagem)
    while not valor.strip():
        print('\nINSIRA UM VALOR VÁLIDO!')
        valor = input(mensagem)
    return valor
    
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
              print('sua classificação é de nivel alto')
              
            elif rentabilidade >= 0.10 * PV < 0.20 * PV:
              print('sua classificação é de nivel médio')
              
            elif rentabilidade > 0 * 100 < 0.10 * 100:
              print('sua classificação é de nivel baixo')
              
            elif rentabilidade == 0:
              print('sua classificação é de nivel equilibrado')
              
            else:
              rentabilidade < 0 * 100
              print('sua classificação é de prejuizo')
              
            #Opção de continuar
            try:  
                opcao = int(input('deseja continuar? ' ' 1 = sim ' ' 2 = nao'))
                if opcao > 2 or opcao < 1:
                    print('opção deve ser 1 ou 2')
                
                elif opcao == 1:
                    print('ok')
                
                else:
                    print("Obrigado por usar o programa!")
                    break
            
            except ValueError:
                print('opção deve ser 1 ou 2')
        except ValueError:
            print("o valor precisa ser numérico!")
            continue