import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
#Site to get data http://dhime.ideam.gov.co/atencionciudadano/

class Ideam():
    def __init__(self, path, encoding='utf-8', sep='|', type='t_maxmin', serie='diário'):

        def dataframe():
            if type == 't_maxmin':
                df = pd.read_csv(path, encoding=encoding,
                                 index_col=False, sep=sep)
                df["Fecha"] = pd.to_datetime(df['Fecha'])
                return df

        import pandas as pd
        self.dataset = dataframe()
        self.type_data = type
        self.len = len(self.dataset)
        self.type = 'original'
        self.startdate = self.dataset['Fecha'][0]
        self.enddate = self.dataset['Fecha'][len(self.dataset) - 1]

    def byYear(self, year, var):
        # percorre procurando por ano
        inicio, final = 0, 0
        for linha in range(self.len):
            l = linha
            if self.date(linha).year == year:
                inicio = linha  # linha de inicio
                while self.date(l).year == year and l < self.len - 1:
                    l += 1
                final = l
                break
        return np.array(self.dataframe[f'{var}'][inicio:final])

    def byMonth(self, year, month, var):
        """
        Dado um array diário com vários anos, ele seleciona e retorna apenas uma região daquele mês pedido
        :param year:
        :param month:
        :param var:
        :return:
        """
        # percorre procurando por ano
        inicio, final = 0, 0
        for linha in range(self.len):
            l = linha
            if self.date(linha).year == year and self.date(linha).month == month:
                inicio = linha  # linha de inicio
                while self.date(l).year == year and self.date(l).month == month and l < self.len - 1:
                    l += 1
                final = l
                break
        return np.array(self.dataset[f'{var}'][inicio:final])
        #  íncides de temperatura

    def rx5day(self):
       import indice
       a = indice.Indice(self.dataset)
       a = a.rx5day(retornar="date")
       return a

    def rx5day_month(self, with_x=False):
        k = 0
        m = x = y = np.array([0])
        kano = 0
        for ano in range(self.startdate.year, self.enddate.year + 1):
            for mes in range(1, 13):
                while self.date(k).month == mes:  # while in the month
                    t = 0
                    for k2 in range(5):
                        if k == self.len - 1:
                            break
                        t += float(self.dataset["Valor"][k])
                        k += 1
                    if t > y[kano]:
                        y[kano] = t
                        m[kano] = int(mes)
                    if k == self.len - 1:
                        break
            y = np.append(y, 0)
            m = np.append(m, 0)
            kano += 1

        return np.arange(self.startdate.year, self.enddate.year + 1), y[:-1], m[:-1]

    def tx(self, with_x=False):
        """
        Encontra a temperatura máxima da máxima anual.
        Os dados necessitam ser diários
        :return:
        """
        if self.type_data != 't_maxmin':
            raise "The file has not 'type'= 'temp_maxmin' "
        if with_x == False:
            y = [0]
            date_start = self.date(0).year  # Indice que fixa o ano para analisar
            cont = 0
            for tam in range(0, self.len):  # Percorre cada índice dos elementos
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataset['max'][tam]):
                        y[cont] = float(self.dataset['max'][tam])
                else:  # Se não atualizamos os índices para cálcular o próximo ano
                    y.append(0)
                    cont += 1
                    date_start += 1
            return y[0:-2]
        elif with_x == True:
            x = np.arange(self.date(0).year, self.date(self.len-1).year)
            y = [0]
            date_start = self.date(0).year  # Indice qua fixa o ano para analisar
            cont = 0
            for tam in range(0, self.len):  # Percorre cada índice dos elementos
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataset['Valor'][tam]):
                        y[cont] = float(self.dataset['Valor'][tam])
                else:  # Se não atualizamos os índices para cálcular o próximo ano
                    y.append(0)
                    cont += 1
                    date_start += 1
            return x, y[0:-1]

    def tn(self, with_x=False):
        '''
                Encontra a temperatura máxima da mínima anual.
                Os dados necessitam ser diários
                :return:
                '''
        if self.type_data != 't_maxmin':
            raise 'O arquivo não está citado "type" como temp_maxmin'
        if with_x == False:
            y = [0]
            date_start = self.date(0).year
            cont = 0
            for tam in range(0, self.len):
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataset['Valor'][tam]):
                        y[cont] = float(self.dataset['Valor'][tam])
                else:
                    y.append(0)
                    cont += 1
                    date_start += 1
            return y[0:-2]
        elif with_x == True:
            x = np.arange(self.date(0).year, self.date(self.len-1).year)
            y = [0]
            date_start = self.date(0).year
            cont = 0
            for tam in range(0, self.len):
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataset['Valor'][tam]):
                        y[cont] = float(self.dataset['Valor'][tam])
                else:
                    y.append(0)
                    cont += 1
                    date_start += 1
            return x, y[0:-1]

    def tx90p(self, with_x=False):
        '''
        Encontra o percentil de 90% do TX para o mesmo período

        :param with_x:
        :return:
        '''
        #x, y = self.TX(with_x=True) # Calcula o TXx
        x = np.arange(self.date(0).year,self.date(self.len-1).year)
        y = []      #
        cont = i =0
        tx90p = [0]                 # O vetor começa em 0
        for ano in x:
            dias = 0
            ptx = np.nanpercentile(self.byYear(ano, var='Valor'),90)
            print(ptx)
            while self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                if self.dataset['Valor'][cont] > ptx:  # compara com o percentil 90% do TX anual
                    tx90p[i] += 1
                cont += 1
                dias += 1
            tx90p[i] = 100 * tx90p[i] / dias   #Deixa em percentual anual
            i += 1
            tx90p.append(0)

        if with_x:
            return x, tx90p[0:-1]
        return tx90p[0:-1]

    def tn90p(self, with_x=True):
        '''

        :param with_x: True or False, se deseja que venha o valor da data também
        :return:
        '''
        x = np.arange(self.date(0).year, self.date(self.len - 1).year)
        cont = i = 0
        tn90p = [0]  # O vetor começa em 0
        for ano in x:
            dias = 0
            ptx = np.nanpercentile(self.byYear(ano, var='Valor'), 90)
            print(ptx)
            while self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                if self.dataset['Valor'][cont] > ptx:  # compara com o percentil 90% do TX anual
                    tn90p[i] += 1
                cont += 1
                dias += 1
            tn90p[i] = 100 * tn90p[i] / dias  # Deixa em percentual anual
            i += 1
            tn90p.append(0)

        if with_x:
            return x, tn90p[0:-1]
        return tn90p[0:-1]

    def date(self, line_number):
        if self.type == 'format1':
            return self.dataset['time'][line_number]
        return self.dataset['Fecha'][line_number]

    def empty_data(self):
        if self.type == 'format1':
            s = np.sum(np.isnan(self.dataset[f'pr'].to_numpy("float32")))
            s = (s / self.len) * 100
            return s
        s = np.sum(np.isnan(self.dataset[f'Valor'].to_numpy("float32")))
        s = (s / self.len) * 100
        return s

    def format1(self, comma_to_dot=True, grow=True):
        import pandas as pd
        from datetime import datetime
        if self.type != 'format1':
            self.dataset['Fecha'] = pd.to_datetime(self.dataset['Fecha'])
            self.dataset['Valor'] = np.array(self.dataset['Valor']).astype(float)
            self.dataset = self.dataset.rename(columns={'Fecha': 'time', 'Valor': 'pr'})
            self.type = 'format1'


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
    def to_csv(self, path):
        self.dataset.to_csv(path)

    def to_netcdf(self,path):
        import xarray as xr
        t = self.dataset.to_xarray()
        t = xr.Dataset(t)
        t.to_netcdf(path)

a = Ideam('/media/thiagosilva/thigs/Projetos/Amazônia/selecionados/Colombia/PTPM_CON@48015050.data')
x,y = a.get_month(range(2,7),2017, with_x=True)

plt.plot(x,y)
plt.show()