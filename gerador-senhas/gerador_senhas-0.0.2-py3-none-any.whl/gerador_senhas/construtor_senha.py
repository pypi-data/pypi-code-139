import random

def VerificaLetras( lista_letras_total, senha):
# -- VERIFICA SE A SENHA CONTEM AO MENOS UM ITEM DO TIPO LETRAS

    for i in range(len(lista_letras_total)):
        if lista_letras_total[i] in list(senha):
           letras_verificado = True
           break 
        else:
                letras_verificado = False
    return letras_verificado

def VerificaNumeros( lista_numeros, senha):
# -- VERIFICA SE A SENHA CONTEM AO MENOS UM ITEM DO TIPO NUMEROS

    for i in range(len(lista_numeros)):
        if lista_numeros[i] in list(senha):
            numeros_verificado = True
            break 
        else:
            numeros_verificado = False
    return numeros_verificado        

def VerificaEspeciais( lista_especiais, senha):
# -- VERIFICA SE A SENHA CONTEM AO MENOS UM ITEM DO TIPO CARACTERES ESPECIAIS

    for i in range(len(lista_especiais)):
        if lista_especiais[i] in list(senha):
            especiais_verificado = True
            break 
        else:
            especiais_verificado = False
    return especiais_verificado

def GeradorAleatorio(lista):
# -- SELECIONA UM ITEM ALEATÓRIO DE UMA LISTA

    aleatorio = random.choice(lista)
    return aleatorio  

def Construcao( tamanho, letras = None, numeros = None, caracteres = None):
    
    lista_letras_total =['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z']
    lista_numeros = ['0','1','2','3','4','5','6','7','8','9']
    lista_especiais = ['!','?','@','#','$','%','&']
    senha = ''

    if letras and not numeros and not caracteres:
        for i in range(int(tamanho)):
            senha = senha + GeradorAleatorio(lista_letras_total)
 
    elif numeros and not letras and not caracteres:
        for i in range(int(tamanho)):
            senha = senha +GeradorAleatorio(lista_numeros)               
   
    elif caracteres and not numeros and not letras:
        for i in range(int(tamanho)):
                senha = senha + GeradorAleatorio(lista_especiais)
      
    elif letras and numeros and not caracteres:
        lista_total = lista_letras_total + lista_numeros
        while not VerificaLetras(lista_letras_total,senha) or not VerificaNumeros(lista_numeros, senha):
            senha = ''
            for i in range(int(tamanho)):
                senha = senha + GeradorAleatorio(lista_total) 
     
    elif letras and caracteres and not numeros:
        lista_total = lista_letras_total + lista_especiais 
        while not VerificaLetras(lista_letras_total,senha) or not VerificaEspeciais(lista_especiais, senha):
            senha = ''
            for i in range(int(tamanho)):
                senha = senha + GeradorAleatorio(lista_total)             
      
    elif caracteres and numeros and not letras:
        lista_total = lista_numeros + lista_especiais 
        while not VerificaNumeros(lista_numeros, senha) or not VerificaEspeciais(lista_especiais, senha):
            senha = ''
            for i in range(int(tamanho)):
                senha = senha + GeradorAleatorio(lista_total) 
      
    elif letras and numeros and caracteres:
        lista_total = lista_letras_total + lista_numeros + lista_especiais 
        while not VerificaLetras(lista_letras_total,senha) or not VerificaNumeros(lista_numeros, senha) or not VerificaEspeciais(lista_especiais, senha):
            senha = ''
            for i in range(int(tamanho)):
                senha = senha + GeradorAleatorio(lista_total)                    
      
    return senha
         
