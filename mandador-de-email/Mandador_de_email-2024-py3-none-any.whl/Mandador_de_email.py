import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Fuçãos
def Mandar_email(Email_que_vai_enviar, Senha_do_email_que_vai_enviar, Email_que_vai_receber, Assunto, Messagem):
	Servidor = smtplib.SMTP("smtp.gmail.com: 587")

	Servidor.starttls()

	Mandar = MIMEMultipart()
	Mandar['From'] = Email_que_vai_enviar
	Mandar['To'] = Email_que_vai_receber
	Mandar['Subject'] = Assunto
	Mandar.attach(MIMEText(Messagem, 'plain'))

	Servidor.login(Email_que_vai_enviar, Senha_do_email_que_vai_enviar)
	Servidor.sendmail(Mandar['From'], Mandar['To'], Mandar.as_string())
	time.sleep(1)
	Servidor.quit()

#Comandos
#
# Mandar_email("Email que vai enviar", "Senha do email que vai enviar", "Email que vai receber", "Assunto", "Messagem")
#
