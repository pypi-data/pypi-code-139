import pickle
import time
import json
import os
import traceback
import glob
import datetime
import shutil


def dbremove(file  , bpath = None , backupDuration = None , keep = 0):
    fname = os.path.basename(file)
    fn = fname.split("_")[0]
    dirname = os.path.dirname(file)
    backupPath = "/".join([dirname , bpath] )
    try:
        if (os.path.basename(file).split(".")[-1] == "pkl"):
            if bpath != None:
                files = sorted(glob.glob("/".join([backupPath , "%s_*.pkl"%fn])))
                for fli , fl in enumerate(files):
                    if (keep > 0) and (fli < (len(files) - keep +1 )):
                        try:
                            bname = os.path.basename(fl)
                            fn  = fname.split(".")[0].split("_")[0]
                            bdate = bname.split("%s_"%fn)[1].replace(".pkl" , "")
                            if len(bdate)  == 8:
                                dt1 = datetime.datetime.strptime(bdate , "%Y%m%d")
                            else:
                                dt1 = datetime.datetime.strptime(bdate , "%Y%m%d%H%M%S")
                            if backupDuration:
                                if (datetime.datetime.now() - dt1) > backupDuration:
                                    try:
                                        os.remove(fl)
                                    except:
                                        pass
                            else:
                                os.remove(fl)
                        except:
                            print(traceback.format_exc())

                try:
                    os.mkdir(backupPath)
                except:
                    pass

                try:
                    fname = os.path.basename(file)
                    dirname = os.path.dirname(file)
                    newname = "/".join([dirname , bpath , fname] )
                    shutil.move(os.path.abspath(file) ,  os.path.abspath(newname ))
                except:
                    print(traceback.format_exc())
            
   
        try:
            os.remove(file)
        except:
            pass

        try:
            dirname = os.path.dirname(file)
            fn = os.path.basename(file).replace(".pkl" , ".json")
            dfile = "/".join([dirname , fn])
            os.remove(dfile)
        except:
            pass#print(traceback.format_exc())
    except:
        print(traceback.format_exc())

        
    



def pkdump(path , fname , obj , length = None , interval = None , timedelta = None , backup = None ,
                backupDuration = None , keep = 0 , json = False , dayly = False):


    if json == False:
        jfiles = list(sorted(glob.glob(path + "/%s_*.json"%fname)))
        for jf in jfiles:
            try:
                os.remove(jf)
            except:
                pass

    if length:
        files = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))
        if files:
            if len(files) >= length:
                for cnt in range(len(files) - length):
                    try:
                        dbremove(files[cnt] , bpath = backup,backupDuration = backupDuration, keep = keep)
                    except:
                        print(traceback.format_exc())
    
    deltaCheck  = True
    if timedelta:
        files = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))
        checkCnt = 0
        for fdi , file in enumerate(files):
            bname = os.path.basename(file)
            bdate = bname.split("%s_"%fname)[1].replace(".pkl" , "")
            if len(bdate)  == 8:
                dt1 = datetime.datetime.strptime(bdate , "%Y%m%d")
            else:
                dt1 = datetime.datetime.strptime(bdate , "%Y%m%d%H%M%S")
            if (datetime.datetime.now() - dt1) > timedelta:
                if fdi < (len(files)-2):
                    try:
                        dbremove(file, bpath = backup,backupDuration = backupDuration, keep = keep)
                    except:
                        print(traceback.format_exc())


    intvCheck = True
    if interval:
        file = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))[-1]
        bname = os.path.basename(file)
        bdate = bname.split("%s_"%fname)[1].replace(".pkl" , "")
        if len(bdate)  == 8:
            dt1 = datetime.datetime.strptime(bdate , "%Y%m%d")
        else:
            dt1 = datetime.datetime.strptime(bdate , "%Y%m%d%H%M%S")
        if (datetime.datetime.now() - dt1) > interval:
            intvCheck = True
        else:
            intvCheck = False
    

    
    if not(length or timedelta):
        files = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))
        for file in files[:-1]:
            try:
                dbremove(file, bpath = backup ,backupDuration = backupDuration, keep = keep)
            except:
                pass

        files = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))
        files2 = list(sorted(glob.glob(path + "/%s_*.json"%fname)))
        for file in files2:
            tmpf = file.replace(".json" , ".pkl")
            if tmpf not in files:
                try:
                    dbremove(file, bpath = backup,backupDuration = backupDuration, keep = keep)
                except:
                    pass
    
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if dayly:
        now = datetime.datetime.now().strftime("%Y%m%d")
    
    fpath  = path + "/" + fname  + "_" + now

    if intvCheck and deltaCheck:
        files = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))

        for i in range(10):
            try:
                with open(fpath + ".pkl" , "wb") as f:
                    pickle.dump(obj , f)
                    break
            except:
                pass
            time.sleep(0.1)

        if json:
            for i in range(10):
                try:
                    with open(fpath +".json" , "w") as f:
                        f.write(json.dumps(obj))
                        break
                except:
                    pass
                time.sleep(0.1)


    files = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))
    files2 = list(sorted(glob.glob(path + "/%s_*.json"%fname)))
    #print("files2"  ,files2)
    for file in files2:
        #print("file" , file)
        tmpf = file.replace(".json" , ".pkl")
        if tmpf not in files:
            try:
                os.remove(file)
            except:
                print(traceback.format_exc())
        

def pkload(path=None , fname=None , obj=None , init = None , fullName  = None ):
    
    if fullName:
        with open(fullName , "rb") as f:
            return pickle.load(f)

    files = list(sorted(glob.glob(path + "/%s_*.pkl"%fname)))
    for flr in reversed(files):
        fpath  = flr.replace(".pkl" , "")
        if os.path.isfile(fpath + ".pkl"):
            try:
                with open(fpath + ".pkl" , "rb") as f:
                    obj = pickle.load(f)

                    try:
                        with open(fpath +".json" , "r") as f:
                                test = json.loads(f.read())
                        if test != obj:
                            with open(fpath +".json" , "w") as f:
                                f.write(json.dumps(obj))
                                
                    except:
                        pass
                    if os.path.isfile(fpath +".json" ) == False:
                        with open(fpath +".json" , "w") as f:
                            f.write(json.dumps(obj))
                    
                    return obj
            except:
                if init == None:
                    if os.path.isfile(fpath +".json" ):
                        try:
                            with open(fpath +".json" , "r") as f:
                                obj = json.loads(f.read())
                                return obj
                        except:
                            pass
                    
    return init