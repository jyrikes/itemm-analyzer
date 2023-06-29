import filesInteractor as fl
import sqlite3 as sql
import pandas as pd
import os
diretorio_atual = os.getcwd()
caminho_dataBases = os.path.join(diretorio_atual, "dataBases")


class DataCreator():

    def __init__(self, diretorio, dataBase,plan0,plan1):

        self.diretorio = diretorio
        self.files = fl.FilesInteractor(self.diretorio)
        self.nomesTabelas = self.files.read()
        self.caminho_banco_dados = os.path.join(caminho_dataBases, dataBase)
        self.dataBase = sql.connect(self.caminho_banco_dados)
        self.insertTables(plan0,plan1)
        self.close()

    def insertTables(self,plan0,plan1):

        for i, planilha_nome in enumerate(self.nomesTabelas):
            # ler a planilha em um objeto DataFrame
            planilha = pd.read_excel(self.diretorio+'/'+planilha_nome)

            # converter o índice da planilha em uma string para uso posterior
            planilha_idx = str(i)

            # criar uma string que representa o nome da tabela no banco de dados
            table_name = "plan" + planilha_idx

            # obter os tipos de dados das colunas no DataFrame
            dtypes = {col: str(planilha[col].dtype)
                      for col in planilha.columns}

            # carregar a tabela no banco de dados usando o nome da tabela e os tipos de dados das colunas
            planilha.to_sql(table_name, self.dataBase,
                            if_exists='replace', index=False, dtype=dtypes)
        self.renameTables(plan0, "Time Stamp", "Stamp")
        self.renameTables(plan0, "Step Time", "Steptime")
        self.renameTables(plan1, "Step Time", "Steptime")
   

        return True

    def renameTables(self, tabela, coluna_antiga, coluna_nova):

        cursor = self.dataBase.cursor()

        consulta_renomear_coluna = f"ALTER TABLE \"{tabela}\" RENAME COLUMN \"{coluna_antiga}\" TO \"{coluna_nova}\""

        cursor.execute(consulta_renomear_coluna)

        self.dataBase.commit()

    def close(self):
        self.dataBase.close()

    