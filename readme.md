combined a few examples together to come up with a ssl sockets wrapper python chat program

https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/

https://docs.python.org/3.7/library/ssl.html

https://www.electricmonk.nl/log/2018/06/02/ssl-tls-client-certificate-verification-with-python-v3-4-sslcontext/

openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt

openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt

