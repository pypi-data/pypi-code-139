
import ftplib

if __name__=='__main__':
    ftp=ftplib.FTP(host='0.0.0.0',source_address=('0.0.0.0',2121))
    ftp.login('user', '12345')