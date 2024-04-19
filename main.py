PK = input("digite o código do produto: ")
nome_produto = input("digite o nome do produto: ")
descrição_produto = input("digite a descrição do produto: ")

while True:
        try:
            #custo do produto
            CP = float(input("digite o custo do produto: "))
            
            if CP <= 0:
                print("O custo do produto não pode ser menor ou igual a 0")
                continue
           
            #custo fixo/administrativo
            CF = float(input("digite o custo do fixo: "))
            
            if CF < 0:
                print("O custo fixo não pode ser negativo!")
                continue
            
            #comissão de vendas
            CV = float(input("digite a comissão sobre a venda: "))
            
            if CV < 0:
                print("A comissão de venda não pode ser negativa!")
                continue
            
            #impostos 
            IV = float(input("digite o valor dos impostos: "))
            
            if IV < 0:
                print("O valor dos impostos não pode ser negativo!")
                continue
            
            #rentabilidade
            ML = float(input("digtite a rentabilidade desejada: "))
            
            if ML < 0:
                print("A rentabilidade desejada não pode ser negativa!")
                continue
            
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