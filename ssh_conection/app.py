import pandas as pd
import paramiko
import re
import time

# Leer el archivo Excel
df = pd.read_excel("puntos.xlsx")

# Credenciales SSH
username = 'gamble'
password = 'consuerte'

# Función para obtener la MAC por SSH
def obtener_mac(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port=22, username=username, password=password)
        comando = 'ip a'
        stdin, stdout, stderr = ssh.exec_command(comando)
        salida = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            return f"Error: {error.strip()}"
        elif salida.strip() == "":
            return "Sin salida de comando"

        mac = None
        interfaz_actual = None
        bloques = salida.split("\n")
        for i in range(len(bloques)):
            linea = bloques[i].strip()
            match_interfaz = re.match(r'^\d+:\s+(enp\w+|eth\d+):', linea)
            if match_interfaz:
                interfaz_actual = match_interfaz.group(1)
                for j in range(i + 1, i + 5):
                    if j < len(bloques):
                        match_mac = re.search(r'link/ether\s+([0-9a-fA-F:]{17})', bloques[j])
                        if match_mac:
                            mac = match_mac.group(1)
                            break
                if mac:
                    break

        if mac and interfaz_actual:
            return mac
        else:
            return "MAC no encontrada"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        ssh.close()

# Crear una lista para guardar los resultados
macs_resultados = []

# Iterar sobre cada IP
for index, row in df.iterrows():
    ip = row['IP']
    print(f"🔍 Procesando IP {ip} ({index + 1} de {len(df)})...")
    resultado = obtener_mac(ip)
    print(f"➡️ Resultado: {resultado}")
    macs_resultados.append(resultado)
    time.sleep(0.5)  # Pausa para evitar bloqueos de red

# Guardar los resultados en la columna 'MAC'
df['MAC'] = macs_resultados

# Guardar en nuevo archivo
df.to_excel("puntos_con_mac.xlsx", index=False)
print("✅ Archivo guardado como 'puntos_con_mac.xlsx'")
