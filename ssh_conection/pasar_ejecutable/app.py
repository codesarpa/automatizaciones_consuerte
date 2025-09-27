import logging
import paramiko
from datetime import datetime
import os
import re
import pandas as pd

nombre_log = ''

# archivo = 'ejemplo_scripts'
# extension = '.zip'
# nombre_archivo = f'{archivo}{extension}'
# ruta_archivo_local = f'C:/automatizaciones_consuerte/ssh_conection/pasar_ejecutable/{nombre_archivo}'
# ruta_remota = f'/copia/varios'
# archivo_remoto = f'{ruta_remota}/{nombre_archivo}'
# ruta_carpeta_descomprimida = f"{ruta_remota}/{archivo}"
# ejecutables = [
#     "script1.sh",
#     "script2.sh"
# ]
# comandos = {
#     "DESCOMPRIMIR ARCHIVO" : f"cd {ruta_remota} && unzip -o {nombre_archivo}",
#     "INGRESAR A CARPETA Y DAR PERMISOS A LOS EJECUTABLES" : f"cd {ruta_carpeta_descomprimida} && chmod +x script1.sh script2.sh",
#     "EJECUTAR SCRIPTS" : f"cd {ruta_carpeta_descomprimida}{comando_ejecutar_sh} "
#     }

i = 0
archivo = 'crearcarpeta'
extension = '.tar'
nombre_archivo = f'{archivo}{extension}'
ruta_archivo_local = f'C:/automatizaciones_consuerte/ssh_conection/pasar_ejecutable/{nombre_archivo}'
ruta_remota = f'/copia/varios'
archivo_remoto = f'{ruta_remota}/{nombre_archivo}'
ruta_carpeta_descomprimida = f"{ruta_remota}/{archivo}"
ejecutables = [
    "arregloprintersuperlfex.sh",
    "crearcapeta.sh"
]
comando_ejecutar_sh = f" && ./{ejecutables[0]} && ./{ejecutables[1]}"
comando_ingrsar_a_carpeta_descomprimida = f"cd {ruta_carpeta_descomprimida}"
comando_ejecutar_arregloprinter = f"{comando_ingrsar_a_carpeta_descomprimida} && ./{ejecutables[0]}"
comando_ejecutar_crearcarpeta = f"{comando_ingrsar_a_carpeta_descomprimida} && ./{ejecutables[1]}"
comandos = {
    "DESCOMPRIMIR ARCHIVO" : f"cd {ruta_remota} && tar -xvf {nombre_archivo}",
    "INGRESAR A CARPETA Y DAR PERMISOS A LOS EJECUTABLES" : f"cd {ruta_carpeta_descomprimida} && chmod +x {ejecutables[0]} {ejecutables[1]}",
    F"EJECUTAR SCRIPT: {ejecutables[0]}": f"{comando_ejecutar_arregloprinter}",
    F"EJECUTAR SCRIPT: {ejecutables[1]}": f"{comando_ejecutar_crearcarpeta}",
    "VERIFICAR CARPETAS": "test -d /home/gamble/superflex && echo 'OK: superflex existe' || echo 'ERROR: superflex no existe'\ntest -d /home/gamble/superflex/Actualizaciones && echo 'OK: Actualizaciones existe' || echo 'ERROR: Actualizaciones no existe'\ntest -d /home/gamble/Documentos/Try_icon && echo 'OK: Try_icon existe' || echo 'ERROR: Try_icon no existe'"
    }

def logs_diarios():
    ruta_base = os.path.dirname(__file__)
    fecha = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
    nombre_log = f"{fecha}.log"
    log_file = os.path.join(ruta_base, "logs", nombre_log)

    logging.basicConfig(
        filename=f'{log_file}',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    # print(log_file)
    logs = [
        logging.getLogger(__name__),
        log_file
    ]
    return logs

def eliminar_log(ruta_log):
    if os.path.exists(ruta_log):
        os.remove(ruta_log)
    else:
        print(f'No se encontro el log: {ruta_log}')

def leer_excel(log):
    ruta_base = os.path.dirname(__file__)
    nombre_excel = "puntos5.xlsx"
    ruta_excel = os.path.join(ruta_base, nombre_excel)
    
    log.info("se ingresa a leer el excel")
    df = pd.read_excel(ruta_excel)
    
    for index, row in df.iterrows():
        print("hola")
        pdv = row['CODIGO PDV']
        ip = row['IP']
        estado = row['ESTADO']
        print(repr(estado))
        if str(estado).strip() == "True":
            print("sE VALIDA TRUE, SE PASA A SIGUIENTE REGISTRO")
            print(repr(estado))
            continue
        client = conexion_sh(log,ip)
        

        if client:
            df.at[index, "SSH"] = "True"
            if enviar_archivo(log,client,ruta_archivo_local,archivo_remoto):
                df.at[index, "SFTP"] = "True"
                print("Se envia el archivo")
                log.info("Se envia el archivo")
                ejecutar_comandos(log,client,comandos, df, index)
                # print(f"{pdv} - {ip}"
        else:
            print(f"error al realizar la conexion sh: {ip}")
            continue
        
    # Forzar columna ESTADO como texto
    df["ESTADO"] = df["ESTADO"].astype(str)
    # Sobrescribe el Excel con los nuevos datos pero conservando todas las columnas
    with pd.ExcelWriter(ruta_excel, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False)

def conexion_sh(log, ip):
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
        log.info(f"Iniciando Conexion SH: {ip}")
        # Crea un cliente SSH
        client = paramiko.SSHClient()
        # Configura el cliente para que no solicite confirmación de clave pública
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conecta al servidor
        client.connect(host, port, username, password)
        log.info(f"Se conecto al servidor: {host}")
        return client
    except paramiko.AuthenticationException:
        log.error("Error de autenticación: usuario o contraseña incorrectos")
    except paramiko.SSHException as e:
        log.error(f"Error en la conexion SSH: {e}")
    except Exception as e:
        log.error(f"Error inesperado: {e}")

def enviar_archivo(log, client, ruta_archivo_local,archivo_remoto):
    try:
        sftp = client.open_sftp()
        sftp.put(ruta_archivo_local, archivo_remoto)
        sftp.close()
        log.info(f"Archivo {ruta_archivo_local} enviado a {archivo_remoto}")
        return True
    except Exception as e:
        log.error(f"Error al enviar archivo: {e}")
        return False

def ejecutar_comandos(log, client, comandos, df, index):
    # ejemplo:
    #     acceder a valores: comandos(cmd)
    #     acceder a claves: cmd
    try:
        for cmd in comandos:
            log.info(f"Ejecutando comando: {cmd}: {comandos[cmd]}")
            stdin, stdout, stderr = client.exec_command(comandos[cmd])
            salida = stdout.read().decode()
            errores = stderr.read().decode()
            
            if "EJECUTAR SCRIPT" in cmd:
                if salida:
                    log.info(f"Salida: {salida}")
                    log.info(f"Comando: {cmd}")
                    log.info(f"Exitoso")
                    df.at[index, f"SALIDA {cmd}"] = f"True: {salida}"
                if errores:
                    log.error(f"Fallo en el comando: {cmd}")
                    log.error(f"Errores: {errores}")
                    df.at[index, f"ERRORES {cmd}"] = f"False: {errores}"
            else:
                if salida:
                    log.info(f"Salida: {salida}")
                    log.info(f"Comando: {cmd}")
                    log.info(f"Exitoso")
                    df.at[index, f"{cmd}"] = f"True: {salida}"
                if errores:
                    log.error(f"Fallo en el comando: {cmd}")
                    log.error(f"Errores: {errores}")
                    df.at[index, f"{cmd}"] = f"False: {errores}"

            if "VERIFICAR CARPETAS" in cmd:
                if salida == "OK: superflex existe\nOK: Actualizaciones existe\nOK: Try_icon existe\n":
                    df.at[index, f"ESTADO"] = "True"
                else: 
                    df.at[index, f"ESTADO"] = f"False: {errores}"
            
            
            # salida = stdout.read().decode().strip()
            # errores = stderr.read().decode().strip()

            # Guardar salida normal en una columna propia
            # if salida:
            #     log.info(f"Salida: {salida}")
            #     df.at[index, f"SALIDA {cmd}"] = salida

            # # Guardar errores en otra columna
            # if errores:
            #     log.error(f"Errores: {errores}")
            #     df.at[index, f"ERROR {cmd}"] = errores

            # # Estado general de ejecución
            # if salida and not errores:
            #     df.at[index, cmd] = "True"
            # else:
            #     df.at[index, cmd] = "False"

            # if stdin:
            #     log.info(f"stdin: {stdin}")

    except Exception as e:
        log.error(f"Error ejecutando comandos: {e}")
    
logs = logs_diarios()
log = logs[0]
log.info("Hola")
leer_excel(log)

ruta_log = logs[1]
#credenciales consuerte




# # 2. Subir el archivo comprimido
# sftp = client.open_sftp()
# sftp.put(ruta_archivo_local, archivo_remoto)
# # sftp.close()

# # Ejecuta un comando en el servidor
# # stdin, stdout, stderr = client.exec_command(f"cd {ruta_remota} && unzip -o {nombre_archivo} && cd {ruta_remota}/{archivo} && chmod +x script1.sh script2.sh && ./script1.sh && ./script2.sh")
# # # Imprime la salida del comando
# # print(stdout.readlines())

# # Cierra la conexión
# client.close()
# eliminar_log(ruta_log)