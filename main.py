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

            #Descrição
            #A. Preço de Venda(PV)
            print('O Preço de venda foi de ', round(PV), 'que é igual a 100% do valor final')
            
            #B. Custo de Aquisição (Fornecedor)
            porcent = CP * 100 / PV
            print("o preço do produto pelo fornecedor foi igual a", round(CP),' que é igual a', round(porcent), '% do valor final')
           
            #C. Receita Bruta (A-B)
            bruto = PV - CP
            porcent1 = (bruto * 100) / PV
            print('a receita bruta foi de ', round(bruto), 'que é igual a', round(porcent1),'% do valor final')
            
            #D. Custo Fixo/Administrativo
            valorCF = PV * CF / 100
            print('o custo fixo foi de ', round(valorCF), 'que é igual a', round(CF),'% do valor final')
            
            #E. Comissão de Vendas
            valorCV = PV * CV / 100
            print('a comissao foi de ', round(valorCV), 'que é igual a', round(CV),'% do valor final')
            
            #F. Impostos
            valorIV = PV * IV / 100
            print('o valor do imposto foi de ', round(valorIV), 'que é igual a', round(IV),'% do valor final')
            
            #G. Outros custos (D+E+F)
            resto = valorCF + valorCV + valorIV
            porcent2 = CF + CV + IV
            print('outros custos ', round(resto), 'que é igual a', round(porcent2),'% do valor final')
            
            #H. Rentabilidade (C-G)
            rentabilidade = bruto - resto
            print('a rentabilidade foi de', round(rentabilidade), 'que é igual a', round(ML), '% do valor final')

            #Faixa de lucro do produto
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