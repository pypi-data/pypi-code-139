import requests

def Abaixar_um_arquivo(Site_do_arquivo, Nome_e_tipo_do_arquivo):
    Resposta = requests.get(Site_do_arquivo)
    if Resposta.status_code == requests.codes.OK:
        Novo_arquivo = open(Nome_e_tipo_do_arquivo, "wb")
        Novo_arquivo.write(Resposta.content)
    else:
        Resposta.raise_for_status()