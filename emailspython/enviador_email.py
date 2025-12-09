import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_remetente = "sergioamaraldesouza@gmail.com"         # Substitua pelo seu e-mail do Gmail
senha_remetente = "Se91616461"      # Substitua pela sua senha de app do Gmail
email_destinatario = "a2023952390@teiacoltec.org"

servidor_smtp = "smtp.gmail.com"
porta_smtp = 587

mensagem = MIMEMultipart()
mensagem["From"] = email_remetente
mensagem["To"] = email_destinatario
mensagem["Subject"] = "Teste de Leitura e Recebimento de E-mail - Gmail"

mensagem.add_header("Disposition-Notification-To", email_remetente)
mensagem.add_header("Return-Receipt-To", email_remetente)
mensagem.add_header("X-Confirm-Reading-To", email_remetente)
mensagem.add_header("X-Mailer", "Python/3.9 smtplib")

corpo_email = """\
Olá, este é um e-mail de teste enviado automaticamente para verificar:

- Confirmação de **leitura**
- Confirmação de **recebimento**

Por favor, apenas abra este e-mail para simular a leitura.

Atenciosamente,
Sistema de Teste
"""
mensagem.attach(MIMEText(corpo_email, "plain"))

try:
    with smtplib.SMTP(servidor_smtp, porta_smtp) as servidor:
        servidor.starttls()
        servidor.login(email_remetente, senha_remetente)
        servidor.sendmail(email_remetente, email_destinatario, mensagem.as_string())
        print("✅ E-mail enviado com sucesso para:", email_destinatario)
except Exception as erro:
    print("❌ Erro ao enviar e-mail:", str(erro))