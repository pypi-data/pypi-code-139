import itertools


def loopList(Array_Of_List):
        output = []
        for element in itertools.product(*Array_Of_List):
            output.append(list(element))

        return output

      
def loopDictionary(Dictionary):

    keys=list(Dictionary.keys()) 
    values=list(Dictionary.values())  

    valueOutput = []
    for element in itertools.product(*values):
        valueOutput.append(list(element)) 

    valueWithName=[]
    for i in valueOutput:
        obj={}
        for index,j in enumerate(i):
            obj[keys[index]]=j
        valueWithName.append(obj)    

    return valueWithName

