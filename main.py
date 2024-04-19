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

            print("O preço de venda é de: ",PV)  
            break
        except ValueError:
            print("o valor precisa ser numérico!")
            continue