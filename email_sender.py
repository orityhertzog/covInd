import smtplib
import ssl
import socket

socket.getaddrinfo('localhost', 25)
import os

assert 'SYSTEMROOT' in os.environ


def email():
    smtp_server = 'smtp@gmail.com'
    port = 587
    sender = 'orityhertzog@gmail.com'
    password = 'cxui9Tcuc'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        print('worked')



