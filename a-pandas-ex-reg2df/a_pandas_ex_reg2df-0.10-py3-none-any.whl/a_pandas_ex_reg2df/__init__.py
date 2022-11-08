import os
import subprocess
import tempfile
from functools import partial
import pandas as pd
from bs4 import BeautifulSoup


def read_txtfile_with_bs4(file):
    text = open_file_in_binary_mode(file)
    try:
        dateiohnehtml = (
            b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        print(Fehler)
        return None


def open_file_utf16le(path):
    with open(path, encoding="utf-16-le") as f:
        data = f.read()
    return data


def get_regedit_roots(rootkey):
    regt, regtd = get_tmpfile(suffix=".reg")
    regtd()
    subprocess.run(["reg", "export", rootkey, regt])
    data = open_file_utf16le(path=regt)
    regtd()
    return data


def regedit_to_dataframe(rootkey):
    data = get_regedit_roots(rootkey)
    data2 = data.split("\n\n")
    df = pd.DataFrame(data2)
    df = df.loc[~(df[0] == "")]
    df[0] = df[0].str.strip()
    df = df.loc[df[0].str.startswith("[HKEY")]
    df2 = df[0].str.split("]\n", n=0, expand=False, regex=False)
    df = pd.concat(
        [df2.str[0].str.join(""), df2.str[1:].str.join(" ")], axis=1, ignore_index=True
    )
    df = df.loc[~(df[1] == "")].reset_index(drop=True)
    df[0] = df[0].astype("category")
    df[1] = df[1].astype("category")
    df[0] = df[0].str.slice(1)
    return df


def get_HKCU_df():
    return regedit_to_dataframe(rootkey="HKCU")


def get_HKLM_df():
    return regedit_to_dataframe(rootkey="HKLM")


def get_HKCR_df():
    return regedit_to_dataframe(rootkey="HKCR")


def get_HKU_df():
    return regedit_to_dataframe(rootkey="HKU")


def get_HKCC_df():
    return regedit_to_dataframe(rootkey="HKCC")


def get_tmpfile(suffix=".txt"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = filename.replace("/", os.sep).replace("\\", os.sep)
    tfp.close()
    return filename, partial(os.remove, tfp.name)


def get_all_installed_windows_apps():
    filename, filenamed = get_tmpfile(suffix=".tsv")
    filename2, filename2d = get_tmpfile(suffix=".vbs")

    content = rf"""Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objTextFile = objFSO.CreateTextFile("{filename}", True)
    strComputer = "."
    Set objWMIService = GetObject("winmgmts:" _
     & "{{impersonationLevel=impersonate}}!\\" & strComputer & "\root\cimv2")
    Set colSoftware = objWMIService.ExecQuery _
     ("SELECT * FROM Win32_Product")
    objTextFile.WriteLine "Caption" & vbtab & _
    "Description" & vbtab & "Identifying Number" & vbtab & _
    "Install Date" & vbtab & "Install Location" & vbtab & _
    "Install State" & vbtab & "Name" & vbtab & _
    "Package Cache" & vbtab & "SKU Number" & vbtab & "Vendor" & vbtab _
     & "Version"
    For Each objSoftware in colSoftware
     objTextFile.WriteLine objSoftware.Caption & vbtab & _
     objSoftware.Description & vbtab & _
     objSoftware.IdentifyingNumber & vbtab & _
     objSoftware.InstallLocation & vbtab & _
     objSoftware.InstallState & vbtab & _
     objSoftware.Name & vbtab & _
     objSoftware.PackageCache & vbtab & _
     objSoftware.SKUNumber & vbtab & _
     objSoftware.Vendor & vbtab & _
     objSoftware.Version
    Next
    objTextFile.Close"""
    with open(filename2, mode="w", encoding="utf-8") as f:
        f.write(content)
    subprocess.call(["cscript.exe", filename2])
    xxa = read_txtfile_with_bs4(filename)
    allinfos = [x.split("\t") for x in xxa.splitlines()]
    df = pd.DataFrame.from_records(allinfos[1:])

    columnswithoutdate = [
        "Caption",
        "Description",
        "Identifying Number",
        "Install Location",
        "Install State",
        "Name",
        "Package Cache",
        "SKU Number",
        "Vendor",
        "Version",
    ]
    try:
        df.columns = columnswithoutdate
    except Exception:
        df.columns = df.iloc[0].to_list()
    df = df.drop(0).reset_index(drop=True)
    filename2d()
    filenamed()
    return df


def open_file_in_binary_mode(file):
    with open(file, mode="rb") as f:
        data = f.read()
    return data


def pd_add_reg2df():
    pd.Q_get_HKCU_df = get_HKCU_df
    pd.Q_get_HKLM_df = get_HKLM_df

    pd.Q_get_HKCR_df = get_HKCR_df
    pd.Q_get_HKU_df = get_HKU_df

    pd.Q_get_HKCC_df = get_HKCC_df
    pd.Q_get_installed_apps = get_all_installed_windows_apps
