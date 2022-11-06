class Response:
    def __init__(self, data, status ):
        self.statusValue = status
        self.dataValue = data

    def data(self):
        return self.dataValue  

    def status(self):
        return self.statusValue 


class Helpers:
    def __init__(self,Foreing_Key_Name,Image_Name):
        self.Foreing_Key_Name = Foreing_Key_Name
        self.Image_Name = Image_Name   

    def multiple_files_helper(self,property_id, image):
        dict = {}
        dict[self.Foreing_Key_Name] = property_id
        dict[self.Image_Name] = image
        return dict    


def get_object(model, pk):
        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            return False  

def get( model,serializer,request,status):
    pk=request.query_params.get('pk',None)
    if pk:
        obj = get_object(model,pk)
        if obj:
            serializedData = serializer(obj)
            return Response({"data":serializedData.data,"message":"Data fetched Successfully"},status.HTTP_200_OK)
        return Response({"message":"Requested Data Doesn't Exists"},status.HTTP_204_NO_CONTENT)
    else:
        obj = model.objects.all()
        serializedData = serializer(obj, many=True)
        return Response({"data":serializedData.data,"message":"Data fetched Successfully"},status.HTTP_200_OK)
             

def post(serializer,request,status):
    serializedData = serializer(data=request.data)
    if serializedData.is_valid():
        serializedData.save()
        return Response({"data":serializedData.data,"message":"Data Added Successfully"},status.HTTP_201_CREATED)                      
    return Response({"error":serializedData.errors,"message":"Error"},status.HTTP_400_BAD_REQUEST)  


def delete( model,request,status):
    pk=request.query_params.get('pk',None)
    if pk:
        obj = get_object(model,pk)
        if obj:
            obj.delete()
            return Response({"message":"Deleted Successfully"},status.HTTP_204_NO_CONTENT)
        return Response({"message":"Requested Data Doesn't Exists"},status.HTTP_204_NO_CONTENT)
    else:
        obj = model.objects.all()
        obj.delete()
        return Response({"message":"Deleted All Data Successfully"},status.HTTP_204_NO_CONTENT)

        
        
def patch(model,serialzer,request,status):
    pk=request.query_params.get('pk',None)
    if pk:
        obj = get_object(model,pk)
        if obj:
            serializedData = serialzer(obj,data=request.data,partial=True)
            if serializedData.is_valid():
                serializedData.save()
                return Response({"data":serializedData.data,"message":"Data Updated Successfully"},status.HTTP_200_OK)
            return Response({"error":serializedData.errors,"message":"Error"},status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Requested Data Doesn't Exists"},status.HTTP_204_NO_CONTENT) 
    else:
        return Response({"message":"Params are Empty"},status.HTTP_204_NO_CONTENT)


def postImages(serializer,request,status,Foreing_Key_Name,Image_Name):
    key = request.data[Foreing_Key_Name]
    images = dict((request.data).lists())[Image_Name]
    flag = 1
    arr = []
    helper = Helpers(Foreing_Key_Name,Image_Name)
    for img_name in images:
        modified_data = helper.multiple_files_helper(key,img_name)
        file_serializer = serializer(data=modified_data)
        if file_serializer.is_valid():
            file_serializer.save()
            arr.append(file_serializer.data)
        else:
            flag = 0

    if flag == 1:
        return Response(arr, status.HTTP_201_CREATED)
    else:
        return Response(arr, status.HTTP_400_BAD_REQUEST) 