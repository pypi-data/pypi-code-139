import pandas as pd
import math
import numpy as np
import heapq
from scipy.stats.mstats import gmean, hmean

class Value:
    def __init__(self) -> None:
        '''
        path:   địa chỉ lưu file
        data:   file dữ liệu dùng để test
        result, element, index, last_op,
            index_ht, index_file_kq,
            n, count, high_profit, 
            exp_high_profit, index_file :   các biến số trong quá trình xử lí
        '''
        self.path = ''
        self._name = 'Value'
        self._alpha = ''
        self.data_full = pd.DataFrame()
        self.data_test = pd.DataFrame()
        self._description = 'với công thức được chọn, mỗi năm, tính giá trị công thức với các biến số tương ứng của cty, cty nào có giá tị lớn nhất thì chọn'
        self._module = []
        self._method_create_exp = ['create_exp_all', 'sinhF']
        self._result = []
        self._element = ""
        self._index_vetcan = []
        self._index = 0
        self._index_F = 0   
        self._last_op = ""
        self._index_ht = 0
        self._index_qk = 0
        self._index_file_qk = 0
        self._n = 1
        self._count = 0
        self._high_profit = []
        self._exp_high_profit = []
        self._index_file = 0
        self._number_ct = math.inf
        self._profit_condition = 0
        self._index_T = []  
        self._index_test = []
        self._time_moment = 0
        self._Fn = None
        self._expFn = []
        self._pfFn = []
        self._maxpf = 0
        self._F0 = None
        self._type_data = 'YEAR'
        self._flag = True
        self._dtFn = pd.DataFrame()
        self._len_data_i = []
        self.high_rank_fomula = ['test']*100
        self.high_rank_val = np.zeros(100)
        self.min_rank_val = np.min(self.high_rank_val)

    def _update_last_time(self):
        try:
            self._index_qk = int(pd.read_csv(f'{self.path}/index.csv')['index'][0])
            self._index_file_qk = int(pd.read_csv(f'{self.path}/index.csv')['index_file'][0])
            self._count =  int(pd.read_csv(f'{self.path}/index.csv')['count'][0])
            self._n =  int(pd.read_csv(f'{self.path}/index.csv')['n'][0])
        except:
            pass
    def create_exp_option(self, time_moment, number_ct=5000, profit_condition=1.4, type_data = 'YEAR', method = 'vetcan', module = 'basic'):

        self._update_last_time()
        self._time_moment = time_moment
        self._number_ct = number_ct
        self._profit_condition = profit_condition
        self._type_data = type_data
        self._index_T = self._get_index_T()
        self.data_test = self.data_full.loc()[self._index_T[-self._time_moment]:self._index_T[-1]].reset_index(drop=True)
        self._index_test = self._get_index_T(for_data= 'test')

        self._len_data_i = []
        for i in range(1, len(self._index_test)):
            self._len_data_i.append(self._index_test[i]-self._index_test[i-1])
        self._run(method)
        if method == 'sinhF':
            self._save_file()
        self._save_process()

        file_fomula = pd.DataFrame({'fomula': self._exp_high_profit, 'profit': self._high_profit})

        return file_fomula
    
    def get_variable(self):
        list_variable = [[]]*26
        list_column = list(self.data_test.columns)
        for i in range(4, len(list_column)):
            list_variable[i-4] = np.array(self.data_test[list_column[i]])
        return list_variable

        
    def _run(self, method):
        global A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z, PROFIT, COMPANY

        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = [[]]*26
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = self.get_variable()
        PROFIT = np.array(self.data_test["PROFIT"])
        COMPANY = np.array(self.data_test["SYMBOL"])
        var_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        count = 0
        for var in [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]:
            if len(var) > 0:
                self._alpha = self._alpha + var_char[count]
            count += 1

        if method == 'sinhbac':
            print('chạy sinh bậc')
            while True:
                try:
                    self._index_file = self._index_file_qk          #update 9h 26/9/2022
                    self._crExp_sinh_bac()
                    self._index_ht = 0
                    self._index_file_qk = 0
                    # self._n += 1
                except:
                    break

    def _crExp_sinh_bac(self):
        print(self._n)
        list_size = self._processListSize(self._preProcessListSize(self._get_same(self._process_list_size_element(self._sizeElement([], [], self._n)))))
        list_exp_child = []
        print(len(list_size), self._index_file_qk)
        for i in range(self._index_file_qk, len(list_size)):
            print('check index_file', self._index_file_qk, self._index_file, len(list_size))
            list_power = []
            for key, value in list_size[i].items():
                key = key.split('_')
                self._crElement(self._creatElement(int(key[0]), int(key[1])), value)
                power = int(key[0])- int(key[1])
                list_power.append(power)
                list_exp_child.append(self._result.copy())
                self._result = []
                self._element = ""
                self._index = []
                self._last_op = ""
            self._result = []
            try:
                self._auto_code_power(list_exp_child, [], 0, list_power)
            except:
                raise Exception('Đã sinh đủ công thức theo yêu cầu')
            list_exp_child = []
            self._index_file += 1
            self._index_ht = 0
            self._index_qk = 0
        self._n += 1
        return "DONE"
  
    def _processListSize(self, listSizeEle):
        result = []
        for i in range(len(listSizeEle)):
            listSizeEle[i] = [(listSizeEle[i][j], listSizeEle[i][j+1])
                            for j in range(0, len(listSizeEle[i]), 2)]
            listSizeEle[i].sort(key=lambda x: x[0])
            listSizeEle[i].sort(key=lambda x: x[0]+x[1])
        dict_list = {}
        for i in range(len(listSizeEle)):
            try:
                k = dict_list[str(listSizeEle[i])]
            except:
                dict_list[str(listSizeEle[i])] = 1
                result.append(listSizeEle[i])
        for i in range(len(result)):
            dict_ele_size = {}
            for j in range(len(result[i])):
                try:
                    dict_ele_size[f"{result[i][j][0]}_{result[i][j][1]}"] += 1
                except:
                    dict_ele_size[f"{result[i][j][0]}_{result[i][j][1]}"] = 1
            result[i] = dict_ele_size
        return result

    def _get_bac(self, item_full):
        item = [item_full[i] for i in range(0, len(item_full), 2)]
        bac = np.min(item)
        list_bac = []
        list_bac_possible = [bac-2*x for x in range(round(bac/2)+1)]
        for bac in list_bac_possible:
            if bac > 0:
                list_bac.append(bac)
        return list_bac

    def _preProcessListSize(self, new_size_element):
        list_all_bac = []
        for item in new_size_element:
            list_all_bac.append(self._get_bac(item))
        list_all_size_element = []
        for id in range(len(list_all_bac)):
            size_element = new_size_element[id]
            list_bac = list_all_bac[id]
            for bac in list_bac:
                temp_size_element = size_element.copy()
                check = True
                for i in range(0, len(size_element), 2):
                    if temp_size_element[i] > bac:
                        temp_size_element[i+1] = int((temp_size_element[i] - bac)/2)
                        # if temp_size_element[i+1] % 1 != 0:
                        #     check = False
                        temp_size_element[i] = int((temp_size_element[i] + bac)/2)
                # if check == True:
                list_all_size_element.append(temp_size_element)
                temp_size_element = []
        return list_all_size_element

    def _get_same(self, list_size_element):
        new_size_element = []
        for item in list_size_element:
            mod_arr = np.mod(np.array(item), 2)
            if np.sum(mod_arr) == 0:
                new_size_element.append(item)
            elif np.sum(mod_arr) == len(mod_arr)/2:
                new_size_element.append(item)
        return new_size_element

    def _process_list_size_element(self, list_size_element):
        list_new_size_element = []
        for item in list_size_element:
            check = True
            for i in range(1, len(item), 2):
                if item[i] > 0:
                    check = False
            if check == True:
                list_new_size_element.append(item)
        return list_new_size_element
    
    def _sizeElement(self, listSizeEle, sizeEle, total_size):
        if sum(sizeEle) == total_size:
            if len(sizeEle) % 2 == 1:
                sizeEle.append(0)
                listSizeEle.append(sizeEle.copy())
                sizeEle.pop()
            else:
                listSizeEle.append(sizeEle.copy())
        else:
            if len(sizeEle) == 0:
                for i in range(1, total_size - sum(sizeEle)+1):
                    sizeEle.append(i)
                    self._sizeElement(listSizeEle, sizeEle, total_size)
                    sizeEle.pop()
            else:
                if len(sizeEle) % 2 == 1:
                    for i in range(total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._sizeElement(listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
                else:
                    for i in range(1, total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._sizeElement(listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
        return listSizeEle

    def _crElement(self, elements, times):
        if len(self._index_vetcan) == times:
            self._result.append(self._element)
        else:
            if len(self._index_vetcan) == 0:
                start = 0
            else:
                start = self._index_vetcan[-1]
            last_op_psedou = self._last_op
            for i in range(start, len(elements)):
                for op in ['+', '-']:
                    if i == start and op != self._last_op and self._last_op != "":
                        continue
                    else:
                        self._element += op + elements[i]
                        self._index_vetcan.append(i)
                        self._last_op = op
                        self._crElement(elements, times)
                        self._element = self._element[:len(self._element)-len(elements[0])-1]
                        self._index_vetcan.pop()
                        self._last_op = last_op_psedou
        
    def _creatElement(self, multi, divide):
        key = {}
        for i in range(len(self._alpha)):
            key[self._alpha[i]] = i+1
        exp_multi = [list(self._alpha)]
        n = max(multi, divide)
        while len(exp_multi) < n:
            exp_multi.append([])
            for i in range(len(exp_multi[-2])):
                for j in range(key[exp_multi[-2][i][-1]] - 1, len(self._alpha)):
                    exp_multi[-1].append(exp_multi[-2][i]+"*"+self._alpha[j])
        if divide == 0:
            return exp_multi[multi-1]
        exp_divide = list(map(lambda x: x.replace("*", "/"), exp_multi[divide-1]))
        exp_multi = exp_multi[multi-1]
        result = []
        
      
        for i in range(len(exp_multi)):
            for j in range(len(exp_divide)):
                if self._expInvalid(exp_multi[i], exp_divide[j]):
                    result.append(exp_multi[i] + "/" + exp_divide[j])
        return result

    def _auto_code_power(self, elements, exp, power, list_power):
        if len(exp) == len(elements):
            self._index_ht += 1
            if self._index_ht >= self._index_qk:
                ct = f'({"".join(exp)}){"/A" * power}'
                # p = self.get_profit(ct)
                # if p > self._profit_condition:
                #     self._high_profit.append(p)
                #     self._exp_high_profit.append(ct)
                #     if len(self._exp_high_profit) > self._number_ct:
                #         raise Exception('Target Complete')

        else:
            n = len(exp)
            for i in range(len(elements[n])):
                exp.append(elements[n][i])
                power = list_power[n]
                self._auto_code_power(elements, exp, power, list_power)
                exp.pop()

















