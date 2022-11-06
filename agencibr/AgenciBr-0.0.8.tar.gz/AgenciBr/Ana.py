import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Ana:
    def __init__(self, arquivo, sep=';', index_col=False, list=False, encoding='latin-1',
                 on_bad_lines='skip', comma_to_dot=True, lat=None, lon=None):
        def find_cod(df):
            '''
            Encontra o código da estação no dataframe
            '''
            line_codigo = 0
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Código' in temp:
                    ind = temp.index('Código')
                    temp = temp[ind + 2].split(':')
                    return int(temp[1])
                line_codigo += 1

        def linha_inicio_df(arquivo):
            '''Abre o arquivo porém pula linhas em branco que por padrão são 4
            No inicio a primeira linha é transformada em head. Portanto, somamos+4+1'''
            df = pd.read_csv(arquivo, sep=';',
                             encoding='latin-1', on_bad_lines='skip')
            return len(df) + 1 + 4

        def dataset(path):
            df = pd.read_csv(path, skiprows=linha_inicio_df(path), sep=sep, encoding=encoding,
                             index_col=index_col, on_bad_lines=on_bad_lines)
            if comma_to_dot:
                temp = []
                for k in df['Data']:
                    temp.append(datetime.datetime.strptime(k, '%d/%m/%Y'))
                df['Data'] = temp.copy()
                df = df.sort_values(by='Data')
                df = df.reset_index()
                return df.replace({',': '.'}, regex=True)
            else:
                temp = []
                for k in df['Data']:
                    temp.append(datetime.datetime.strptime(k, '%d/%m/%Y'))
                df['Data'] = temp.copy()
                df = df.sort_values(by='Data')
                df = df.reset_index()

                return df

        if not list:
            self.dataset = dataset(arquivo)
            self.code = find_cod(pd.read_csv(arquivo, nrows=50, index_col=False,
                                               on_bad_lines='skip', encoding='latin-1'))
            self.fonte = pd.read_csv(arquivo, nrows=2, index_col=False,
                                     on_bad_lines='skip', encoding='latin-1')
            self.startdate = self.dataset['Data'][0]  # data_starend(arquivo)[0]
            self.enddate = self.dataset['Data'][len(self.dataset) - 1]
            self.len = len(self.dataset)
            self.type_data = "original"
            self.lat = lat
            self.lon = lon
            self.status = None
            self.city = None
            self.state = None
            self.list = None

        else:
            self.path = arquivo
            self.list = arquivo

    # internal functions
    def only_mondata(self, list=False):
        from datetime import datetime
        """" Remove all columns that is not referent of month precipitation and day, in original data from Agenci
        """

        if list:
            list_temp = []
            for k in self.list:
                df = k
                lista_meses = ['Data', 'Chuva01', 'Chuva02', 'Chuva03', 'Chuva04', 'Chuva05',
                               'Chuva06', 'Chuva07', 'Chuva08', 'Chuva09', 'Chuva10',
                               'Chuva11', 'Chuva12', 'Chuva13', 'Chuva14', 'Chuva15',
                               'Chuva16', 'Chuva17', 'Chuva18', 'Chuva19', 'Chuva20',
                               'Chuva21', 'Chuva22', 'Chuva23', 'Chuva24', 'Chuva25',
                               'Chuva26', 'Chuva27', 'Chuva28', 'Chuva29', 'Chuva30',
                               'Chuva31']
                columns = df.columns
                for a in columns:
                    if a not in lista_meses:
                        del df[a]
                list_temp.append(df)

        elif list == False:
            df = self.dataset
            lista_meses = ['Data']
            # adicionamos as colunas dos dados
            for k in range(32):
                'The precipitation data have the name "Chuva" or "Clima", in the row data from month'
                if k < 10:
                    lista_meses.append(f'Chuva0{k}')
                    lista_meses.append(f'Clima0{k}')
                else:
                    lista_meses.append(f'Chuva{k}')
                    lista_meses.append(f'Clima{k}')
            columns = df.columns
            for a in columns:
                if a not in lista_meses:
                    del df[a]
            self.type_data = "only_mondata"
            self.dataset = df.drop_duplicates(subset=["Data"])

        else:
            return 'List is only True or False'

    def format1(self, comma_to_dot=True, grow=True):
        """

        :param comma_to_dot: If the person forgot converto comma to point, can do it now
        :param grow: if want the data with the lower in top and greater in end
        :return: Return to self.dataset the data reorganized by form:

         Data      dia1     dia2    dia3    dia4    dia5    dia6    dia7 ...
                 1993     0.1      0.3     0.7     0.8     0.6     0.4     0.1
                 1993     0.2      0.9     0.5     0.2     0.1     1.9     9.1
                 1993     0.7      0.2     0.9     0.8     0.7     0.4     0.1
                 .
                 .
                 .

                E deixamos da forma:

                time        pr
                1997-07-01  0.1
                1997-07-02  0.3
                ....
                ...
                ...
                2020-01-01  0.3
                2020-01-02  0.0

        """

        import pandas as pd
        from datetime import datetime
        if self.type_data != 'format1': # If the data is not the format1
            # Organize the file by date, the lower to greater
            df_ordenado = self.dataset
            df_ordenado['Data'] = pd.to_datetime(df_ordenado['Data'], format="%d/%m/%Y")
            df_ordenado = df_ordenado.drop_duplicates(subset='Data')

            if comma_to_dot:
                df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
                df_ordenado = df_ordenado.reset_index()
                df_ordenado = df_ordenado.drop(columns='index')
                self.dataset = df_ordenado
            if not grow:
                self.dataset = df_ordenado.sort_values(by=['Data'], ascending=True)

            Data = []
            prec = []
            self.only_mondata()

            # indução
            colum = self.dataset.columns
            for linha in range(len(self.dataset)):
                for dia in range(1, 32):
                    try:
                        temp = self.dataset[colum[0]][linha]
                        Data.append(datetime(temp.year, temp.month, dia)) # check if the date is real
                        prec.append(float(self.dataset[colum[dia]][linha]))
                    except:
                        n = 0
            df = pd.DataFrame(list(zip(Data, prec)), columns=['time', 'pr'])
            self.type_data = "format1"
            self.len = len(df)
            self.dataset = df

    def date(self, line):
        """
        This function get a especific date in a line
        :param linha:
        :return:
        """

        from datetime import datetime
        if self.type_data in ["original", "only_mondata"]:
            return self.dataset["Data"][line]
        else:
            return self.dataset['time'][line]
    def where(self, date):
        """
        Return the index where is the date
        :param date: date in datetime.datetime format
        :return:
        """
        self.format1()
        return np.where(self.dataset()['time'] == date)
    def empty_data(self):
        if self.type_data == "format1":
            #print(self.dataset['pr'].to_numpy("float32"))
            t = np.sum(np.isnan(self.dataset['pr'].to_numpy("float32")))
            return (t/self.len)*100
        else:
            self.only_mondata()
            s = 0
            for i,c in enumerate(self.dataset.columns):
                if c!="Data" and c!= "Chuva31" and c!= "Chuva30" and c!= "Chuva29":
                    s += np.sum(np.isnan(self.dataset[f'{c}'].to_numpy("float32")))
            print("You are using the original data and this is a estimative, use format1 before to be precise")
            s = (s/(self.enddate-self.startdate).days)*100
            return s

    # select data or return a data
    def get_year(self,year, with_x=False, return_x0=False):
        """
        From array muti-year, return a year specific
        :param year: can by a Int, or list of Int
        :param with_x:
        :param return_x0: Return the index init
        :return:
        """
        self.format1()
        if isinstance(year, int): # if is only a year
            try:
                a = pd.to_datetime(
                    self.dataset['time']).dt.year.to_numpy() == year  # array with true or false if the year is that we want
            except:
                raise f"The Data don't have the year {year}"

            a= np.where(a== True)[0] # Return array with index of True and correct the list format
            if with_x:
                return self.dataset['time'][a], self.dataset['pr'][a]
            elif return_x0:
                return a[0], self.dataset['time'][a]
            return self.dataset['pr'][a]
        else: # is many years
            xf = pd.Series([])
            yf = np.array([])
            for i in year:
                try:
                    a = pd.to_datetime(
                        self.dataset[
                            'time']).dt.year.to_numpy() == i # array with true or false if the year is that we want
                except:
                    raise f"The Data don't have the year {i}"

                a = np.where(a == True)[0]  # Return array with index of True and correct the list format
                xf = pd.concat([xf, self.dataset['time'][a]])
                yf = np.concatenate([yf, self.dataset['pr'][a].to_numpy()])
            if with_x:
                return xf, yf
            elif return_x0:
                raise "This function exist only to one year"
            return yf
    def get_month(self, month, year, with_x=False):
        """
        From array muti-year, return a month specific
        :param month: The month to select as Int, or list of month to get
        :param year: The year to select
        :with_x: return the data, True or Not
        :return: Array with data of month select
        """
        if self.type_data != "format'":
            self.format1()
        #x0 is the index wen start the year that we want
        x0, time = self.get_year(year, return_x0=True)
        if isinstance(month, int):
            try:
                a = time.dt.month.to_numpy() == month  # array with true or false if the year is that we want
            except:
                raise f"The data has't the month {month}"
            a = np.where(a == True)[0]  # Return array with index of True and correct the list format
            a += x0
            if with_x:
                return self.dataset['time'][a], self.dataset['pr'][a]
            return self.dataset['pr'][a]
        else:
            xf = pd.Series([])
            yf = np.array([])
            for i in month:
                try:
                    a = time.dt.month.to_numpy() == i  # array with true or false if the year is that we want
                except:
                    raise f"The data has't the month {i}"
                a = np.where(a == True)[0]  # Return array with index of True and correct the list format
                a += x0
                xf = pd.concat([xf, self.dataset['time'][a]])
                yf = np.concatenate([yf, self.dataset['pr'][a].to_numpy()])
            if with_x:
                return xf, yf
            return yf
    def get_lonlat(self, by="Código"):
        """
        The data was get by web http://telemetriaws1.ana.gov.br/EstacoesTelemetricas.aspx in oct 2022
        and is save with name "estacoes.csv"
        and save in self.lat and self.lon, that before are None
        :param by: what will be used to find latitude and longitude
        :return:
        """
        if by=="Código":
            data = pd.read_csv("estacoes.csv")
            data = data.query(f"Código=={self.code}")
            self.lat = float(data["Y"])
            self.lon = float(data["X"])
            self.city = data["Município"]
            self.state = data["Estado"]
            self.status = data["Operando"]
    def get_height(self):
        """
        The data original and the table don't have height, to use in calculus we use a API of web https://nationalmap.gov/epqs/

        :return: The height associated with a latitude and longitude
        """
        import requests

        url = "GET pqs.php?x=string&y=string&units=string&output=string HTTP/1.1"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    #Save
    def to_netcdf4(self, path):
        import xarray as xr
        self.format1()

        # pr to float
        df = self.dataset
        df["pr"] = np.array(df['pr']).astype(float)

        # Run to get lat and lon, create the array of position
        self.get_lonlat()
        lat = [self.lat] * self.len
        lon = [self.lon] * self.len
        df['lat'] = lat
        df['lon'] = lon

        # opening the df with xarray
        ds = df.set_index(['time', 'lat', 'lon']).to_xarray()

        ds = xr.Dataset(ds)
        # add variable attribute metadata
        ds.attrs['lat'] = 'Units: °'
        ds.attrs['lon'] = 'Units: °'
        ds.attrs['time'] = 'daily data of time'

        ds.to_netcdf(path)

    def save_csv(self, pasta, sep=';', index=False):
        self.dataset.to_csv(pasta, sep=sep, index=index)

    def haversine(self, lon1, lat1):
        """
        Calculate the great circle distance in kilometers between a point and the stations self
        on the earth (specified in decimal degrees)
        """
        #self.get_lonlat()
        lon2, lat2 = -22, -47
        from math import cos, sin, asin, sqrt, radians
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a3 = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a3))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r

    def identificador(self, path, only_line=50):

        '''Path é o caminho até a pasta com os aquivos das estações'''

        import pandas as pd
        import os

        codigo = []

        for k in os.listdir(path):
            df = pd.read_csv(path + '/' + k, nrows=only_line + 1, encoding='latin-1',
                             on_bad_lines='skip')
            line_codigo = 0
            # encontra a linha que contém o código da estação
            # vai pegar o código e armazenar na variavel codigo

            while True:

                temp = str(df.loc[line_codigo]).split()

                # se código aparece na linha, sabemos que é esta
                if 'Código' in temp:
                    ind = temp.index('Código')
                    temp = temp[ind + 2].split(':')
                    codigo.append(int(temp[1]))
                    break
                line_codigo += 1
        # lendo o arquivo com todas as estações
        ref = pd.read_csv('../estacoes.csv', usecols=['Código', 'Latitude',
                                                      'Longitude', 'X', 'Y']
                          , index_col=False)
        ref = ref[ref['Código'].isin(codigo)]
        ref = ref.reset_index(drop=True)
        ref = ref.reset_index()
        ref = ref.rename(columns={'index': 'Identificador_Estação'})
        return ref

    def plot(self, title='', xlabel='', ylabel=''):
        """
        This function help with fast plot, to more detalhe use the matplotlib
        :param title:
        :param xlabel:
        :param ylabel:
        :return: Retorna o gráfico dos dados salvos no self.dataset
        """

        from matplotlib import pyplot as plt
        if self.type_data == "format1":
            y = self.dataset.iloc[:,1]
            x = self.dataset.iloc[:,0]
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.tight_layout()
            plt.bar(x, y)
            plt.show()
        else:
            x= np.array([])
            y=np.array([])
            for c in range(self.len):
                for l in range(1,32):
                    try:
                        y = np.append(y, self.dataset.iloc[l,c])
                        x = np.append(x, self.dataset.iloc[0,c+l])
                    except:
                        oi=''
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.tight_layout()
            plt.bar(x, y)
            plt.show()

    def identificador_distancia(self, path, start_alt=0, stop_alt=1000, len=3,
                                limite_distancia=1000, return_distance=False, alt=True):
        '''
        Para o bom funcionamento, o primeiro termo é um Dataframe que precisa conter:
        colunas com 'Altitude', 'Latitude', 'Longitude' e 'Identificador_Estação'. Este último sendo um índice que
        você usa para distinguir estações.

        'a' é o código da estação que usaremos para encontrar o
          'Identificador_Estação' da estação que você está considando como referência
        'star_alt' é o valor mínimo de altura
        'Stop_alt' é o valor máximo de altura
        'len' é o número de estações que você quer coletar que sejam perto

        A função retorna uma lista com os índices das estações mais próximas em ordem crescente
        '''

        def find_cod(df):
            '''
            Encontra o código da estação no dataframe
            '''
            line_codigo = 0
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Código' in temp:
                    ind = temp.index('Código')
                    temp = temp[ind + 2].split(':')
                    return int(temp[1])
                line_codigo += 1

        def haversine(lon1, lat1, lon2, lat2):

            """
            Calculate the great circle distance in kilometers between two points
            on the earth (specified in decimal degrees)
            """
            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a3 = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a3))
            r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
            return c * r

        from math import sqrt, cos, sin, asin, radians, inf

        l_e_p = []
        i_e_p = []
        tm_l = 0
        identificador = Ana(path + '/' + (os.listdir(path)[0]), encoding='latin-1',
                                index_col=False).identificador(path)
        if alt == False:
            altitude = 1

            '''Ajusta tamanho das estações'''
            for k in range(len + 2):
                tm_l += 1
                l_e_p.append(inf)
                i_e_p.append('Nan')

            if self.codigo in list(identificador['Código']):
                # indica a estação de referencia como a
                a = list(identificador['Código']).index(self.codigo)

                a = identificador['Identificador_Estação'][a]

                for b in identificador['Identificador_Estação']:
                    cont = 0
                    if a != b and stop_alt >= altitude >= start_alt:  # todos os valores menos o próprio
                        '''vereremos as estações e veremos as 3 mais próximas
                        cidade1 é a cidade que trataremos os dados
                        cidade2 é a cidade que analisaremos '''

                        lat1, lon1 = identificador['Latitude'][a], identificador['Longitude'][a]
                        lat2, lon2 = identificador['Latitude'][b], identificador['Longitude'][b]
                        distancia = haversine(lon1, lat1, lon2, lat2)

                        '''Se alguma cidade for mais próxima do que a que consta na lista, esta a substitui
                        Está em ordem crescente'''
                        for z in range(tm_l - 3):  # todas as linhas menos as 2 últimas
                            if l_e_p[z] > distancia and distancia <= limite_distancia:
                                for c in range(z + 1, tm_l):
                                    if l_e_p[c] > l_e_p[z]:
                                        l_e_p[c] = l_e_p[z]
                                        i_e_p[c] = i_e_p[z]
                                        break
                                i_e_p[z] = identificador['Identificador_Estação'][b]
                                l_e_p[z] = distancia
                                break

                if return_distance is True:
                    return l_e_p[0:len]
                else:
                    return i_e_p[0:len]
        else:
            '''Ajusta tamanho das estações'''
            for k in range(len + 2):
                l_e_p.append(inf)
                i_e_p.append('Nan')

                # indica a estação de referencia como a
                a = identificador['Código'].index(self.codigo)
                a = identificador['Identificador_Estação'][a]

                for b in identificador['Identificador_Estação']:
                    cont = 0
                    if a != b and stop_alt >= (
                            identificador['Altitude'][b]) >= start_alt:  # todos os valores menos o próprio
                        '''vereremos as estações e veremos as 3 mais próximas
                        cidade1 é a cidade que trataremos os dados
                        cidade2 é a cidade que analisaremos '''

                        lat1, lon1 = identificador['Latitude'][a], identificador['Longitude'][a]
                        lat2, lon2 = identificador['Latitude'][b], identificador['Longitude'][b]
                        distancia = haversine(lon1, lat1, lon2, lat2)

                        '''Se alguma cidade for mais próxima do que a que consta na lista, esta a substitui
                        Está em ordem crescente'''

                        for z in range(len(l_e_p) - 3):  # todas as linhas menos as 2 últimas
                            if l_e_p[z] > distancia and distancia <= limite_distancia:
                                for c in range(z + 1, len(l_e_p)):
                                    if l_e_p[c] > l_e_p[z]:
                                        l_e_p[c] = l_e_p[z]
                                        i_e_p[c] = i_e_p[z]

                                        break
                                i_e_p[z] = identificador['Identificador_Estação'][b]
                                l_e_p[z] = distancia

                                break
            if return_distance is True:
                return l_e_p[0:len]
            else:
                return i_e_p[0:len]

    def dados_to_padrao(self, ano_final='máximo', crescente=True, virgula_para_ponto=False, floats=2):
        '''dataframe_organizar é o arquivo dataframe que será organizado; nos dados faltantes deve contér 'sd'
         O INDEX deve ser a data em ano e mês, cada coluna coresponder à um dia do mês conforme e
         o nome da coloca de datas deve se chamar 'Data' como modelo abaixo:

         Data      dia1     dia2    dia3    dia4    dia5    dia6    dia7 ...
         1993     0.1      0.3     0.7     0.8     0.6     0.4     0.1
         1993     0.2      0.9     0.5     0.2     0.1     1.9     9.1
         1993     0.7      0.2     0.9     0.8     0.7     0.4     0.1
         .
         .
         .


        Ano final é até que ano deve ser organizado
        '''
        import pandas as pd

        # Organizando o arquivo pela datas do menor até o maior
        dataframe_organizar = self.dataset
        if ano_final == 'máximo':
            ano_final = pd.to_datetime(max(self.dataset['Data']), format="%d/%m/%Y").year

        dataframe_organizar['Data'] = pd.to_datetime(dataframe_organizar['Data'], format="%d/%m/%Y")
        df_ordenado = dataframe_organizar
        df_ordenado = df_ordenado.drop_duplicates(subset='Data')
        if virgula_para_ponto:
            df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
        if not crescente:
            df_ordenado = df_ordenado.sort_values(by=['Data'], ascending=True)
        df_ordenado = df_ordenado.reset_index()
        df_ordenado = df_ordenado.drop(columns='index')
        # criando as listas, valores de inicio e parada
        ano_inicial = (min(dataframe_organizar['Data'])).year
        lista = []
        lista_mes30 = [4, 6, 9, 11]
        lista_mes31 = [1, 3, 5, 7, 8, 10, 12]
        lista_bissexto = []

        k = 0  # valor que armazena a posição da linha
        dataframe = {'Ano': '', 'Mês': '', 'Dia': '', 'Precipitação': ''}
        # Algoritmo para ano bissexto
        for c in range(1900, ano_final):
            ano = c
            if (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0:
                lista_bissexto.append(c)

        if 1 > 0:
            # Iniciando a organização dos dados
            while ano_inicial <= ano_final and k < len(df_ordenado) - 1:
                # Se o 'Ano inicial' ano que estamos querendo estiver no dataframe ordenado

                if ano_inicial == (
                        df_ordenado['Data'][k]).year:  # como cada linha representa um mês, K é a posição da linha

                    dataframe['Ano'] = (df_ordenado['Data'][k]).year

                    for b in range(1, 13):
                        # Verifica se o mês existe na linha

                        if k == len(df_ordenado['Data']) - 1 or k == len(df_ordenado['Data']):
                            break
                        if b == df_ordenado.iloc[k]['Data'].month:

                            # Verifica se o ano é bissexto
                            if ano_inicial in lista_bissexto:
                                # Se o mês tem 31 dias
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                # Se o mês têm 30 dias
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b
                                    for c in range(1, 31):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                # Se é fevereiro, é bissexto
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 30):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), 2)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())

                                k += 1
                            else:
                                # Se o mês têm 31 dias
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):

                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), 2)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                    k += 1
                                # Se o mês têm 30 dias
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b

                                    for c in range(1, 31):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                    k += 1
                                # Se é fevereiro, não bissexto
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 29):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                    k += 1

                        # se não existir, será colocado espaços vazios nos dados do mês
                        else:
                            # separar nos casos de meses 31 e 30 e cria valores vazios
                            if ano_inicial in lista_bissexto:
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b
                                    for c in range(1, 31):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 30):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())

                            else:
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b
                                    for c in range(1, 31):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 29):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())

                    ano_inicial += 1
                # Caso em que o ano da linha pulou para outro ano. Ano faltante
                else:
                    dataframe['Ano'] = ano_inicial
                    # criamos o que seriam os meses e dias, porém com dados em branco

                    for b in range(1, 13):
                        if ano_inicial in lista_bissexto:
                            if b in lista_mes31:
                                dataframe['Mês'] = b
                                for c in range(1, 32):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            elif b in lista_mes30:
                                dataframe['Mês'] = b
                                for c in range(1, 31):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            else:
                                dataframe['Mês'] = b
                                for c in range(1, 30):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                        else:
                            if b in lista_mes31:
                                dataframe['Mês'] = b
                                for c in range(1, 32):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            elif b in lista_mes30:
                                dataframe['Mês'] = b
                                for c in range(1, 31):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            else:
                                dataframe['Mês'] = b
                                for c in range(1, 29):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c

                    ano_inicial += 1

            datad = pd.DataFrame(lista)
            #
            self.dataset = datad

            def do_data_lost(self):
                import datetime
                # se não estiver crescente, deixa crescente
                if self.enddate < self.startdate:
                    self.dataset = self.dataset.sort_values(by=['Data'], ascending=True)
                for a in range(self.len):
                    if self.date(a) > self.date(a):
                        obh = 0

    def mean(self, with_x=False, retornar=True):
        """
        Calculate the media when the 'arquivo' is a list of many Ana file
        :param with_x:
        :param retornar:
        :return:
        """
        import os
        from AgenciBr.Ana import Ana
        li = os.listdir(self.path)
        start=datetime.date(2090,12,2)
        end=datetime.date(1902,12,2)
        size=0
        for i in li: # get the size of array
            a = Ana(self.path+'/'+i)
            if a.startdate< start:
                start = a.startdate
            if a.enddate > end:
                end = a.enddate

        x = np.arange(start, end, np.timedelta64(1, "D")) # the time array
        y = np.zeros(x.size)
        d = np.zeros(x.size)

        for i in li:  # get the size of array
            a = Ana(self.path + '/' + i)
            a.format1()
            k2= 0
            for i2, k in enumerate(x):
                if pd.to_datetime(k) == a.dataset['time'][k2]:  # se encontramos o intervalo que é idêntico
                    y[i2] += a.dataset['pr'][k2]
                    d[i2] += 1
                    k2 +=1

        # divide by d
        for k in range(size):

            y[k] = y[k]/d[k]
        if retornar:
            if with_x:
                return x, y
            return y
        print(x.size, y.size)
        self.dataset = pd.DataFrame(zip(x.tolist(),y.tolist()), columns=['time', 'pr'])
        print(self.dataset)
        self.type_data = 'format1'

    # Download data
    def download(self,codigo, format='csv', dir='', tipo_especifico=False, save_zip=False):
        """
        Download the Ana data. Code from https://github.com/joaohuf/Ferramentas_HidroWeb
        :param codigo: Code that Ana use to define each station
        :param format: The format of save .mdb, .txt, .csv
        :param dir: The directory to save the file
        :param tipo_especifico:
        :param save_zip: Save file in zip or not
        :return:
        """
        import requests
        from io import BytesIO
        from zipfile import ZipFile, BadZipFile

        # Link onde estão os dados das estações convencionaiss
        BASE_URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais'

        def unzip_station_data(station_raw_data, dir, tipo_especifico):
            try:
                main_zip_bytes = BytesIO(station_raw_data)
                main_zip = ZipFile(main_zip_bytes)

                for inner_file_name in main_zip.namelist():
                    inner_file_content = main_zip.read(inner_file_name)
                    inner_file_bytes = BytesIO(inner_file_content)
                    if not tipo_especifico:
                        with ZipFile(inner_file_bytes, 'r') as zipObject:
                            zipObject.extractall(dir)
                    elif tipo_especifico in inner_file_name:
                        with ZipFile(inner_file_bytes, 'r') as zipObject:
                            zipObject.extractall(dir)
            except BadZipFile:
                print('No .zip founded')

        # Change the format to Ana format
        if format == 'csv':
            params = {'tipo': 3, 'documentos': codigo}
            r = requests.get(BASE_URL, params=params)
        elif format == 'txt':
            params = {'tipo': 2, 'documentos': codigo}
            r = requests.get(BASE_URL, params=params)
        elif format == 'mdb':
            params = {'tipo': 1, 'documentos': codigo}
            r = requests.get(BASE_URL, params=params)
        else:
            raise "the data format is not csv , mdb or txt"

        # Check if the code exist in Ana file
        if not isinstance(r.content, bytes):
            print(f'Arquivo {codigo} inválído')
            return

        # if save_zip is true, save zip
        if save_zip:
            print(f'Salvando dados {codigo} como zip')
            with open(f'{dir}estacao_{codigo}.zip', 'wb') as f:
                f.write(r.content)
        # else, unpack each zip file
        else:
            print(f'Extraindo dados da estação {codigo} do zip')
            unzip_station_data(r.content, dir, tipo_especifico)

    # Extreme index
    def rx5day(self, with_x=False, retornar='number_of_5day_heavy_precipitation_periods_per_time_period'):
        from AgenciBr.indice import Indice
        if self.list:
            fazer=0
        if self.type_data != 'format1':
            self.format1()

        ind = Indice(self.dataset)
        ind = ind.rx5day(with_x=with_x, retornar=retornar)
        return ind
    def cdd(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.cdd(with_x=with_x)
        return ind
    def cwd(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.cwd(with_x=with_x)
        return ind
    def prcptot(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.prcptot(with_x=with_x)
        return ind
    def prcptot_monthly(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.prcptot_monthly(with_x=with_x)
        return ind
    def r99p(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.r99p(with_x=with_x)
        return ind
    def rnnmm(self, number, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.rnnmm(number=number, with_x=with_x)
        return ind
    def r10mm(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.r10mm(with_x=with_x)
        return ind
    def r20mm(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.r20mm(with_x=with_x)
        return ind
    def r99ptot(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.r99pTOT(with_x=with_x)
        return ind
    def rx1day_anual(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.rx1day_anual(with_x=with_x)
        return ind
    def rx1day_monthly(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.rx1day_monthly(with_x=with_x)
        return ind

import matplotlib.pyplot as plt
a = Ana('/media/thiagosilva/thigs/Projetos/Amazônia/selecionados/ANA/Medicoes_convencionais_Carauari_ANA/chuvas_T_00668000.txt', sep=';')
x,y = a.prcptot_monthly(with_x=True)
x = x.tolist()
plt.plot(x,y)
print(x,y)
print()
plt.show()