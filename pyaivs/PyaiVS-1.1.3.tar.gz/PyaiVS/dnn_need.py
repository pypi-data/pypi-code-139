from PyaiVS import model_bulid
import os
os.environ['PYTHONHASHSEED'] = str(42)  # 为了禁止hash随机化，使得实验可复现
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
os.environ['PYTHONHASHSEED']='0'
model_bulid.running('/data/jianping/bokey/OCAICM/dataset/aurorab/aurorab.csv',out_dir='/data/jianping/bokey/OCAICM/dataset/',
                    split=['cluster'],model=['DNN'],FP=['ECFP4','pubchem','MACCS'
                                                        ], run_type='result',cpus=8)

#   model      des    split   auc_roc  f1_score       acc       mcc
# 2   DNN    ECFP4  cluster  0.974368  0.940219  0.927291  0.849580
# 6   DNN  pubchem  cluster  0.960941  0.905874  0.892131  0.786023
# A   DNN    MACCS  cluster  0.935334  0.887700  0.865313  0.729039

#   model      des    split   auc_roc  f1_score       acc       mcc
# 3   DNN    ECFP4  cluster  0.973593  0.944404  0.931188  0.857310
# 8   DNN    MACCS  cluster  0.948276  0.902744  0.879414  0.759106
# 6   DNN  pubchem  cluster  0.962231  0.909223  0.881428  0.757705

#   model    des    split   auc_roc  f1_score       acc       mcc
# A   DNN  ECFP4  cluster  0.974964  0.947168  0.934603  0.863908
# 5   DNN  MACCS  cluster  0.948440  0.911214  0.888231  0.768844

#   model      des    split   auc_roc  f1_score       acc       mcc
# 2   DNN    ECFP4  cluster  0.974964  0.947168  0.934603  0.863908
# 4   DNN  pubchem  cluster  0.962506  0.897499  0.879935  0.768618

#   model      des    split   auc_roc  f1_score       acc       mcc
# 1   DNN  pubchem  cluster  0.965331  0.922219  0.906313  0.807420
# A   DNN    MACCS  cluster  0.935334  0.887700  0.865313  0.729039

#   model    des    split   auc_roc  f1_score       acc       mcc
# A   DNN  ECFP4  cluster  0.974964  0.947168  0.934603  0.863908
