import os
import io
import pandas as pd
import requests
from Ipfs_apis import ipfs_apis
import json

MetaDataSets = 'meta_data/data_sets.json'
MetaModels = 'meta_data/models.json'


def get_datasets():
    try:
        with open(MetaDataSets,'r') as f:
            json_data = json.loads(f.read())
        out = {}
        for k,v in json_data.items():
            out[k] = f'https://nftstorage.link/ipfs/{v}'
        return out
    except Exception as e:
        print(f'Got Exception while get all datasets :{str(e)}')


def upload_dataset(name, file_path):
    try:
        if not os.path.exists(file_path):
            print(f'file_path:{file_path} doesnt exists!')
            return 1
        i = ipfs_apis.IPFS()
        key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDE0RkY4NTU4MzVGMDYwZDBCRTk0ZWQyOTBjNTdiODE1YTE5MjQxNUQiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1NzU2OTU4ODQxOSwibmFtZSI6Ik1BTklESUxMUyJ9.idaK-qJVyOb8WKP1cD0yddE8UJX4zRpBKtX-QqN49fU'
        upload_file_nft = i.upload_nft_storage(key, file_path)
        cid = upload_file_nft['value']['cid']
        new_data_set = {f'{str(name)}': f'{cid}'}
        if not os.path.exists(MetaDataSets):
            with open(MetaDataSets, 'w') as fb:
                json.dump(dict(),fb)
        with open(MetaDataSets, 'r') as fb:
            json_data = fb.read()
            meta_data_sets = json.loads(json_data)
            meta_data_sets.update(new_data_set)

        with open(MetaDataSets,'w+') as fb:
            json.dump(meta_data_sets,fb)

        return cid
    except Exception as e:
        print(f'Got Exception while upload dataset {name} :{str(e)}')


def get_dataset(name):
    try:
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        if not os.path.exists(MetaDataSets):
            print(f'File Missing {MetaDataSets}')
            return 1
        with open(MetaDataSets,'r') as fb:
            # d = fb.read()
            data = json.loads(fb.read())
            if not data.get(name):
                print(f'{name} not in data_sets, please check the name')
                return 1
            url = f'https://nftstorage.link/ipfs/{data.get(name)}'
            res = requests.get(url=url)
            print(type(res.content.decode()))
            dataframe = pd.read_csv(io.StringIO(res.content.decode()),sep=';')
            print(dataframe)
            return dataframe

    except Exception as e:
        print(f'Got Exception while getting dataset {name} :{str(e)}')


def upload_model(name, file_path):
    try:
        if not os.path.exists(file_path):
            print(f'file_path:{file_path} doesnt exists!')
            return 1
        i = ipfs_apis.IPFS()
        key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDE0RkY4NTU4MzVGMDYwZDBCRTk0ZWQyOTBjNTdiODE1YTE5MjQxNUQiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1NzU2OTU4ODQxOSwibmFtZSI6Ik1BTklESUxMUyJ9.idaK-qJVyOb8WKP1cD0yddE8UJX4zRpBKtX-QqN49fU'
        upload_file_nft = i.upload_nft_storage(key, file_path)
        cid = upload_file_nft['value']['cid']
        new_data_set = {f'{str(name)}': f'{cid}'}
        if not os.path.exists(MetaModels):
            with open(MetaModels, 'w') as fb:
                json.dump(dict(),fb)
        with open(MetaModels, 'r') as fb:
            json_data = fb.read()
            meta_data_sets = json.loads(json_data)
            meta_data_sets.update(new_data_set)

        with open(MetaModels,'w+') as fb:
            json.dump(meta_data_sets,fb)

        return cid
    except Exception as e:
        print(f'Got Exception while upload dataset {name} :{str(e)}')


def get_model(name):
    try:
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        if not os.path.exists(MetaModels):
            print(f'File Missing {MetaModels}')
            return 1
        with open(MetaModels,'r') as fb:
            # d = fb.read()
            data = json.loads(fb.read())
            if not data.get(name):
                print(f'{name} not in data_sets, please check the name')
                return 1
            url = f'https://nftstorage.link/ipfs/{data.get(name)}'
            res = requests.get(url=url)
            print(type(res.content))
            file_name = f'{name}_model.h5'
            with open(file_name,'w') as f:
                f.write(str(res.content))
            return file_name

    except Exception as e:
        print(f'Got Exception while getting dataset {name} :{str(e)}')

