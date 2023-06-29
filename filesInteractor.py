import os


class FilesInteractor():

    def __init__(self, diretorio):

        self.diretorio = diretorio
        self.nomes_arquivos = []

    def read(self):

        for nome_arquivo in os.listdir(self.diretorio):
            caminho_arquivo = os.path.join(self.diretorio, nome_arquivo)

            # Verificar se é um arquivo
            if os.path.isfile(caminho_arquivo):
                self.nomes_arquivos.append(nome_arquivo)
        return self.nomes_arquivos

    def clenDirector(self):
        for nome_arquivo in os.listdir(self.diretorio):
            caminho_arquivo = os.path.join(self.diretorio, nome_arquivo)

            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
        return True
    
    def plan(self):
        plan = []
        for i in range(0,45,1):
            plan.append("plan"+str(i))
        return plan
