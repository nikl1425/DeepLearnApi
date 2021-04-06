import mysql.connector
import sshtunnel

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ('niklasHjort.mysql.pythonanywhere-services.com'),
    ssh_username='niklasHjort', ssh_password='Drageild07',
    remote_bind_address=('niklasHjort.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    connection = mysql.connector.connect(
        user='niklasHjort.mysql.pythonanywhere-services.com', password='Drageild07',
        host='127.0.0.1', port=tunnel.local_bind_port,
        database='niklasHjort$mydatabase',
    )
    print("hej")
    connection.close()