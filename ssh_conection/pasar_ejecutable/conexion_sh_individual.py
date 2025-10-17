import paramiko



def conexion_sh(ip):
    # host = "10.2.13.200"
    # host = "10.8.0.231"    
    # host = "10.2.10.118" "10.2.60.131"

    host = ip
    port = 22
    username = 'gamble'
    password = 'consuerte'
    # comando = f"""
    # cd {ruta_remota} && \
    # unzip -o ejemplo_scripts.zip && \
    # chmod +x script1.sh script2.sh && \
    # ./script1.sh && \
    # ./script2.sh
    # """
    comando_descomprimir = ""
    try:
        print("Iniciando Conexion SH")
        # Crea un cliente SSH
        client = paramiko.SSHClient()
        # Configura el cliente para que no solicite confirmación de clave pública
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conecta al servidor
        client.connect(host, port, username, password)
        print(f"Se conecto al servidor: {host}")
    except paramiko.AuthenticationException:
        print("Error de autenticación: usuario o contraseña incorrectos")
    except paramiko.SSHException as e:
        print(f"Error en la conexion SSH: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

conexion_sh('10.2.12.146')