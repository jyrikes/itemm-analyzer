import sqlite3 as sql
import pandas as pd
import json


class DataInterface():
    def __init__(self, bancoDeDados):
        self.bancoDeDados = bancoDeDados

    def query(self, sql_query):
        with sql.connect(self.bancoDeDados) as conn:
            dadosSql = pd.read_sql(sql_query, conn)
            return dadosSql

    def validarFiltro(self, filtro, filtrado, indice_ultimo_nao_nulo):

        if indice_ultimo_nao_nulo is not None:
            ultimo_valor_nao_nulo = filtrado.loc[indice_ultimo_nao_nulo, filtro]
        else:
            ultimo_valor_nao_nulo = None
        return ultimo_valor_nao_nulo

    def filtraCiclo(self, filtro1, filtro2, filtro3, dadosSql,  indice):
        filtrado = dadosSql[(dadosSql.Cycle == indice) &
                            ((dadosSql.Status == filtro2))]
        indice_ultimo_nao_nulo_AhCha = filtrado[filtro1].last_valid_index()
        ultimo_valor_nao_nulo_AhCha = self.validarFiltro(
            filtro1, filtrado, indice_ultimo_nao_nulo_AhCha)
        ultimo_valor_nao_nulo_Time_Stamp = self.validarFiltro(
            filtro3, filtrado, indice_ultimo_nao_nulo_AhCha)
        return [ultimo_valor_nao_nulo_AhCha, ultimo_valor_nao_nulo_Time_Stamp]

    def dataCapacites(self,plan):

        dadosSql = self.query(
            "SELECT Stamp, Status, Steptime, Cycle, AhCha, AhDch FROM "+plan)
        ciclos = dadosSql["Cycle"].unique()
        c20 = []
        for indice in ciclos:
            ultimo_valor_nao_nulo_AhCha = self.filtraCiclo(
                "AhCha", "CHA", "Stamp", dadosSql, indice)
            ultimo_valor_nao_nulo_AhDch = self.filtraCiclo(
                "AhDch", "DCH", "Steptime", dadosSql, indice)

            result = [ultimo_valor_nao_nulo_AhCha, ultimo_valor_nao_nulo_AhDch]
            c20.append(result)
        c20 = [elemento for sublista1 in c20 for sublista2 in sublista1 for elemento in sublista2 if elemento is not None]

        return c20

    def tableCapacities(self,plan):

        dt = self.dataCapacites(plan)

        #      c20    t     caga
        c1 = [dt[4], dt[5], dt[2]]
        c2 = [dt[8], dt[9], dt[6]]
        c3 = [dt[12], dt[13], dt[10]]
        c4 = [dt[16], dt[17], dt[14]]

        listaCapacidades = []
        listaCapacidades.append(c1)
        listaCapacidades.append(c2)
        listaCapacidades.append(c3)
        listaCapacidades.append(c4)

        linhas = ["C20 >= 4,75", "Tempo de descarga", "Ah carga"]
        colunas = ["Capacidade Nominal"]
        capacidades = []
        for c in listaCapacidades:
            capacidades.append(pd.DataFrame(c, columns=colunas, index=linhas))
        return capacidades

    def dataDca(self,plan2):
        dadosSql5 = self.query(
            "SELECT Step, AhStep, Steptime, Cycle FROM ",plan2)
        ciclos = dadosSql5["Cycle"].unique()
        print(ciclos)
        resultado = []
        durations = []
        for indice in ciclos:
            # selecionando os valores filtrados
            filtradoIc = dadosSql5[(dadosSql5.Step == 17) & (
                dadosSql5.Cycle == indice)].head(7)
            filtradoId = dadosSql5[(dadosSql5.Step == 30) & (
                dadosSql5.Cycle == indice)].head(14)
            filtrados = [filtradoIc, filtradoId]
            for filtro in filtrados:
                # obtendo o índice do último valor não nulo
                indice_ultimo_nao_nulo = filtro['AhStep'].last_valid_index()

                # obtendo o último valor não nulo
                if indice_ultimo_nao_nulo is not None:
                    ultimo_valor_nao_nulo = filtro.loc[indice_ultimo_nao_nulo, "AhStep"]
                    stepTime = filtro.loc[indice_ultimo_nao_nulo, "Steptime"]
                    resultado.append(ultimo_valor_nao_nulo)
                    durations.append(stepTime)
                else:
                    ultimo_valor_nao_nulo = None

        df = pd.DataFrame(resultado)
        df_durations = pd.DataFrame(durations)
        timedelta = pd.to_timedelta(df_durations[0])
        seconds = (timedelta.dt.total_seconds().astype(int))/3600

        df_Ah_h = df / pd.DataFrame(seconds)

        df_Ah_IC = df.loc[df.index % 2 == 0]
        df_Ah_h_IC = df_Ah_h.loc[df_Ah_h.index % 2 == 0]

        df_h_Ah_IC = df_Ah_h_IC/4.88902

        df_Ah_ID = df.loc[df.index % 2 != 0]
        df_Ah_h_ID = df_Ah_h.loc[df_Ah_h.index % 2 != 0]
        df_h_Ah_ID = df_Ah_h_ID/4.88902
        df_IC = pd.concat([df_Ah_IC, df_Ah_h_IC, df_h_Ah_IC], axis=1)
        df_IC = df_IC.rename(columns={0: 'Ah_IC', 1: 'Ah/h_IC', 2: 'h/Ah_IC'})

        df_ID = pd.concat([df_Ah_ID, df_Ah_h_ID, df_h_Ah_ID], axis=1)
        df_ID = df_ID.rename(columns={0: 'Ah_ID', 1: 'Ah/h_ID', 2: 'h/Ah_ID'})

        df_IC = df_IC.reset_index(drop=True)
        df_ID = df_ID.reset_index(drop=True)

        df_DCA = pd.concat([df_IC, df_ID], axis=1)

        df_DCA = df_DCA.reset_index(drop=True)

        return df_DCA

    def filtraCiclo2(self, filtro1, filtro2, filtro3, dadosSql, indice):
        filtrado = dadosSql[(dadosSql.Cycle == indice) &
                            ((dadosSql.Status == filtro2))]
        return filtrado

    def graficosCapacidade(self,plan):
        dadosSql = self.query(
            "SELECT Stamp, Status, Steptime,Cycle,AhCha, AhDch FROM "+plan)

        c20 = pd.DataFrame()  # DataFrame inicial com todos os ciclos
        ciclos = dadosSql["Cycle"].unique()
        # Loop para separar o DataFrame por ciclo
        ciclo_a = {}  # Dicionário para armazenar os valores do ciclo "AhCha" e "Steptime"
        ciclo_b = {}  # Dicionário para armazenar os valores do ciclo "AhDch" e "Steptime"

        # Loop para separar os valores dos ciclos
        for indice in ciclos:
            a = self.filtraCiclo2("AhCha", "CHA", "Stamp", dadosSql, indice)
            b = self.filtraCiclo2("AhDch", "DCH", "Steptime", dadosSql, indice)

            # Adiciona os valores do ciclo "AhCha" e "Steptime" ao dicionário ciclo_a_dict
            ciclo_a[indice] = {"AhCha": a["AhCha"].values.tolist(
            ), "Steptime": a["Steptime"].values.tolist()}

            # Adiciona os valores do ciclo "AhDch" e "Steptime" ao dicionário ciclo_b_dict
            ciclo_b[indice] = {"AhDch": b["AhDch"].values.tolist(
            ), "Steptime": b["Steptime"].values.tolist()}
        cicloCarga0 = pd.DataFrame(ciclo_a[0])
        cicloCarga1 = pd.DataFrame(ciclo_a[1])
        cicloCarga2 = pd.DataFrame(ciclo_a[2])
        cicloCarga3 = pd.DataFrame(ciclo_a[3])
        cicloCarga4 = pd.DataFrame(ciclo_a[4])
        ciclosCarga = []
        ciclosCarga.append(cicloCarga0)
        ciclosCarga.append(cicloCarga1)
        ciclosCarga.append(cicloCarga2)
        ciclosCarga.append(cicloCarga3)
        ciclosCarga.append(cicloCarga4)
        cicloCarga0 = pd.DataFrame(ciclo_b[0])
        cicloCarga1 = pd.DataFrame(ciclo_b[1])
        cicloCarga2 = pd.DataFrame(ciclo_b[2])
        cicloCarga3 = pd.DataFrame(ciclo_b[3])
        cicloCarga4 = pd.DataFrame(ciclo_b[4])
        ciclosDescarga = []
        ciclosDescarga.append(cicloCarga0)
        ciclosDescarga.append(cicloCarga1)
        ciclosDescarga.append(cicloCarga3)
        ciclosDescarga.append(cicloCarga4)

        return [ciclosCarga, ciclosDescarga]

    def gerarGrafico(self, dataFrame, xlabel, ylabel):

        graph_data = []
        i = 0
        # Itera sobre os array de dataframes
        for df in dataFrame:
            i += 1
            df.dropna(inplace=True)

            graph_data.append({
                "x": df[xlabel].tolist(),
                "y": df[ylabel].tolist(),
                "mode": "lines",
                "name": "C "+str(i)
            })
          # Cria o objeto de layout
        layout = {
            "title": "Gráfico " + ylabel,
            "xaxis": {"title": xlabel},  # Renomeia o título do eixo X
            "yaxis": {"title": ylabel}   # Renomeia o título do eixo Y
        }

        # Cria o objeto JSON com os dados e o layout
        graph_json = {
            "dados": graph_data,
            "layout": layout,
        }

        # Retorna o JSON resultante
        return json.dumps(graph_json)

    def plotar(self, indice,plan):
        dadosGraficos = self.graficosCapacidade(plan)
        cha = dadosGraficos[indice]
        xlabel = ['Steptime', 'Steptime']
        ylabel = ['AhCha', 'AhDch']
        return self.gerarGrafico(cha, xlabel[0], ylabel[indice])
    