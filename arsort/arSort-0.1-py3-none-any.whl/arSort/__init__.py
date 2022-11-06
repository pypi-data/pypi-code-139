import random

class Sort:
    def __init__(self, mas):
        self.mas = mas

    def bubbleSort(self, zn):
        mas = self.mas
        if zn == ">":
            for i in range(len(mas)):
                for j in range(len(mas)-1):
                    if mas[j] < mas[j+1]:
                        mas[j],mas[j+1] = mas[j+1],mas[j]
            return mas
        elif zn == "<":
            for i in range(len(mas)):
                for j in range(len(mas)-1):
                    if mas[j] > mas[j+1]:
                        mas[j],mas[j+1] = mas[j+1],mas[j]
            return mas

    def shakerSort(self, zn):
        mas = self.mas
        if zn == ">":
            left = 0
            right = len(mas)-1
            while left <= right:
                for i in range(left, right):
                    if mas[i] < mas[i+1]:
                        mas[i], mas[i+1] = mas[i+1], mas[i]
                right -= 1
                for i in range(right, left, -1):
                    if mas[i-1] < mas[i]:
                        mas[i], mas[i-1] = mas[i-1], mas[i]
                left+=1
            return mas
        elif zn == "<":
            left = 0
            right = len(mas)-1
            while left <= right:
                for i in range(left, right):
                    if mas[i] > mas[i+1]:
                        mas[i], mas[i+1] = mas[i+1], mas[i]
                right -= 1
                for i in range(right, left, -1):
                    if mas[i-1] > mas[i]:
                        mas[i], mas[i-1] = mas[i-1], mas[i]
                left+=1
            return mas

    def hairbrushSort(self, zn):
        mas = self.mas
        if zn == ">":
            step = int(len(mas)/1.247)
            swap = 1
            while step > 1 or swap > 0:
                swap = 0
                i = 0
                while i+step < len(mas):
                    if mas[i] < mas[i+step]:
                        mas[i],mas[i+step] = mas[i+step],mas[i]
                        swap += 1
                    i += 1
                if step > 1:
                    step = int(step/1.247)
            return mas
        elif zn == "<":
            step = int(len(mas)/1.247)
            swap = 1
            while step > 1 or swap > 0:
                swap = 0
                i = 0
                while i+step < len(mas):
                    if mas[i] > mas[i+step]:
                        mas[i],mas[i+step] = mas[i+step],mas[i]
                        swap += 1
                    i += 1
                if step > 1:
                    step = int(step/1.247)
            return mas

    def insertsSort(self, zn):
        mas = self.mas
        if zn == ">":
            for i in range(1, len(mas)):
                j = i - 1
                temp = mas[i]
                while mas[j] < temp and j >= 0:
                    mas[j+1] = mas[j]
                    j -= 1
                mas[j+1] = temp
            return mas
        elif zn == "<":
            for i in range(1, len(mas)):
                j = i - 1
                temp = mas[i]
                while mas[j] > temp and j >= 0:
                    mas[j+1] = mas[j]
                    j -= 1
                mas[j+1] = temp
            return mas

    def dwarvesSort(self, zn):
        mas = self.mas
        if zn == ">":
            for i in range(len(mas)):
                for j in range(1, len(mas)-1):
                    if mas[j] < mas[j+1]:
                        mas[j], mas[j+1] = mas[j+1], mas[i]
                    if mas[j-1] < mas[j]:
                        mas[j], mas[j-1] = mas[j-1], mas[j]
            return mas
        elif zn == "<":
            for i in range(len(mas)):
                for j in range(1, len(mas)-1):
                    if mas[j] > mas[j+1]:
                        mas[j], mas[j+1] = mas[j+1], mas[i]
                    if mas[j-1] > mas[j]:
                        mas[j], mas[j-1] = mas[j-1], mas[j]
            return mas
    
    def bogoSort(self, zn): #оно точно вам нужно ))
        mas = self.mas
        if zn == ">":
            while self.__is_sort(mas, ">") == False:
                self.__b_sort(mas)
            return mas
        elif zn == "<":
            while self.__is_sort(mas, "<") == False:
                self.__b_sort(mas)
            return mas

    def __is_sort(self, mas, zn):
        if zn == ">":
            for i in range(len(mas)-1):
                if mas[i] < mas[i+1]:
                    return False
            return True
        elif zn == "<":
            for i in range(len(mas)-1):
                if mas[i] > mas[i+1]:
                    return False
            return True

    def __b_sort(self, mas):
        for i in range(len(mas)):
            rand = random.randint(0, len(mas)-1)
            mas[i], mas[rand] = mas[rand], mas[i]