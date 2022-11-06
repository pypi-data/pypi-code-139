import status

def getAll(model,serializer):
    obj = model.objects.all()
    serializedData = serializer(obj, many=True)
    return {"data":{"data":serializedData.data,"message":"Data fetched Successfully"},"status":status.HTTP_200_OK}

def post(serializer,data):
    serializedData = serializer(data=data)
    if serializedData.is_valid():
        serializedData.save()
        return {"data":{"data":serializedData.data,"message":"Data Added Successfully"},"status":status.HTTP_201_CREATED}
                        
    return {"data":{"error":serializedData.errors,"message":"Error"}, "status":status.HTTP_400_BAD_REQUEST}   

def deleteAll(model):
    obj = model.objects.all()
    obj.delete()
    return {"data":{"message":"Deleted All Data Successfully"},"status":status.HTTP_204_NO_CONTENT}


def get_object(model, pk):
        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            return False    
  
def get( model,serialzer,pk):
    obj = get_object(model,pk)
    if obj:
        serializedData = serialzer(obj)
        return {"data":{"data":serializedData.data,"message":"Data fetched Successfully"},"status":status.HTTP_200_OK}
    return {"data":{"message":"This Product Doesn't Exists"},"status":status.HTTP_204_NO_CONTENT}      


def patch(model,serialzer,pk,data):
    obj = get_object(model,pk)
    if obj:
        serializedData = serialzer(obj,data=data,partial=True)
        if serializedData.is_valid():
            serializedData.save()
            return {"data":{"data":serializedData.data,"message":"Data Updated Successfully"},"status":status.HTTP_200_OK}
        return {"data":{"error":serializedData.errors,"message":"Error"}, "status":status.HTTP_400_BAD_REQUEST}
    return {"data":{"message":"This Product Doesn't Exists"},"status":status.HTTP_204_NO_CONTENT}  

def delete(model, pk):
    obj = get_object(model,pk)
    if obj:
        obj.delete()
        return {"data":{"message":"Deleted Successfully"},"status":status.HTTP_204_NO_CONTENT}
    return {"data":{"message":"This Product Doesn't Exists"},"status":status.HTTP_204_NO_CONTENT}      