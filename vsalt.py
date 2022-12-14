#!/usr/bin/python3
#
#            _ _
#  ___  __ _| | |_ ___
# / __|/ _` | | __/ _ \
# \__ \ (_| | | || (_) |
# |___/\__,_|_|\__\___/
#
# Pequeño script para facilitar el uso de saltstack
#
#
#
#
#


import subprocess
import sys
import os
from time import sleep

comandos = ["instalar", "actualizar", "reset", "ping", "info", "list_users", "ejecutar", "tareas",
            "descargar", "update_d", "actualizar_lote"]  # comandos soportados por vsalt.py

if os.geteuid() != 0:
    print("ERROR: vsalt debe ser ejecutado como usuario root")  # no root, no fun
    sys.exit()
else:
    if len(sys.argv) == 1:
        print("vsalt --help para ayuda")  # ejecucion sin parametros
        sys.exit()
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":  # ayuda
        print("\nvsalt\nUSO: vsalt <MAQUINA> <COMANDO>")
        print("Comandos disponibles: info, ping, instalar, actualizar, update_d, reset, list_users, ejecutar, descargar y tareas")
        print("Ejecuta 'vsalt minions' para ver la lista de minions en el master")
        print("----------------------------------------------------------------------------------")
        print("* info: devuelve los valores de los grains del minion seleccionado")
        print("* ping: realiza un test ping para ver si la maquina esta levantada")
        print("* instala: instalar <PAQUETE> -> instala PAQUETE en minion seleccionado")
        print("* actualiza: actualizar windows del minion seleccionado")
        print("* update_d: update_d url hora usuario: update desatendida como usuario a la hora indicada")
        print("* reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
        print("* list_users: devuelve lista de usuarios en el minion ")
        print("* ejecutar: ejecutar '<COMANDO>' -> ejecuta comando en minion (comando entre comillas simples)")
        print("* descargar: descarga un archivo en una ruta indicada del minion")
        print("----------------------------------------------------------------------------------")
        print("* vsalt lote archivo.txt 'comando a ejecutar':")
        print("Ejecuta el comando en una lista de minions en un archivo (un minion por linea)")
        print("----------------------------------------------------------------------------------")
        print("* vsalt actualizar_lote archivo.txt :")
        print("Actualiza windows de una lista de minions en un archivo (un minion por linea)")
        print("----------------------------------------------------------------------------------")
        print("* tareas <ACCION> (OPCION)")
        print("* tareas crear: crea una tarea programada en el minion")
        print("* tareas eliminar (tarea): elimina una tarea programada del minion.")
        print("* tareas listar: lista todas las tareas programadas del minion")
        print("* tareas info (tarea): devuelve info de una tarea concreta del minion")
        print("----------------------------------------------------------------------------------")
        print("Ej.: sudo vsalt MINION actualizar")
        print("Ej.: sudo vsalt MINION instalar malwarebytes")
        print("Ej.: sudo vsalt MINION reset pepe abc123")
        print("Ej.: sudo vsalt MINION ejecutar 'dir c:\\windows\\'\n")
        sys.exit()

    # Lista de Minions activos en master

    elif sys.argv[1] == "minions":
        print("Consultando la lista de minions.....")
        subprocess.run(["salt-key", "-L"])
        sys.exit()

    # Actualizar minions en lote

    elif sys.argv[1] == "actualizar_lote":
        if len(sys.argv) == 2:
            print("ERROR: falta el archivo con la lista de minions")
            sys.exit()
        elif len(sys.argv) == 3:
            f = open(sys.argv[2], "r")
            minions = f.read()
            minions = minions.replace("\n", " ")
            f.close()
            print("Actualizando", minions)
            subprocess.run(["salt", "-L", minions, "win_wua.list", "install=True"])
            sys.exit()

    # Ejecucion de comandos en lista de minions dada por un archivo (un minion por linea)

    elif sys.argv[1] == "lote":
        if len(sys.argv) == 2:
            print("ERROR: falta el archivo con la lista de minions")
            sys.exit()
        elif len(sys.argv) == 3:
            f = open(sys.argv[2], "r")
            minions = f.read()
            minions = minions.replace("\n", " ")
            f.close()
            cmd = "'" + input("Comando a ejecutar en lote de minions: ")
            cmd = cmd + "'"
            print("Comando a ejecutar:", cmd)
            print("Minions:", minions)
            sino = ["si", "no"]
            resp = input("Proceder: si o no? ")
            while resp not in sino:  # bucle, o si o no
                print("ERROR: debes responder 'si' o 'no'")
                resp = input("Proceder: si o no? ")
            if resp.lower() == "si":  # ejecutamos
                print("Ejecutando el comando en los minions seleccionados...")
                subprocess.run(["salt", "-L", minions, "cmd.run", cmd])
                sys.exit()
            elif resp.lower() == "no":  # cancelamos
                print("Cancelando....")
                sys.exit()
        elif len(sys.argv) == 4:
            f = open(sys.argv[2], "r")
            minions = f.read()
            minions = minions.replace("\n", " ")
            f.close()
            cmd = sys.argv[3]
            print("Ejecutando el comando en los minions seleccionados...")
            subprocess.run(["salt", "-L", minions, "cmd.run", cmd])
            sys.exit()
        elif len(sys.argv) > 4:
            print("ERROR: Error de sintaxis\nLa forma correcta es \"vsalt lote lista.txt 'comando a ejecutar'\"")
            sys.exit()

    # Menu ayuda

    elif len(sys.argv) == 2:
        print("\nvsalt\nUSO: vsalt <MAQUINA> <COMANDO>")
        print("Comandos disponibles: info, ping, instalar, actualizar, update_d, reset, list_users, ejecutar y tareas")
        print("Ejecuta 'vsalt minions' para ver la lista de minions en el master")
        print("----------------------------------------------------------------------------------")
        print("* info: devuelve los valores de los grains del minion seleccionado")
        print("* ping: realiza un test ping para ver si la maquina esta levantada")
        print("* instalar: instala <PAQUETE> -> instala PAQUETE en minion seleccionado")
        print("* actualizar: actualiza windows del minion seleccionado")
        print("* update_d: update_d url hora usuario: update desatendida como usuario a la hora indicada")
        print("* reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
        print("* list_users: devuelve lista de usuarios en el minion ")
        print("* ejecutar: ejecutar '<COMANDO>' -> ejecuta comando en minion (comando entre comillas simples)")
        print("* descargar: descarga un archivo en una ruta indicada del minion")
        print("----------------------------------------------------------------------------------")
        print("* vsalt lote archivo.txt 'comando a ejecutar':")
        print("Ejecuta el comando en una lista de minions en un archivo (un minion por linea)")
        print("----------------------------------------------------------------------------------")
        print("* vsalt actualizar_lote archivo.txt :")
        print("Actualiza windows de una lista de minions en un archivo (un minion por linea)")
        print("----------------------------------------------------------------------------------")
        print("* tareas <ACCION> (OPCION)")
        print("* tareas crear: crea una tarea programada en el minion")
        print("* tareas eliminar (tarea): elimina una tarea programada del minion")
        print("* tareas listar: lista todas las tareas programadas del minion")
        print("* tareas info (tarea): devuelve info de una tarea concreta del minion")
        print("----------------------------------------------------------------------------------")
        print("Ej.: sudo vsalt MINION actualizar")
        print("Ej.: sudo vsalt MINION instalar malwarebytes")
        print("Ej.: sudo vsalt MINION reset pepe abc123")
        print("Ej.: sudo vsalt MINION ejecutar 'dir c:\\windows\\'\n")
        sys.exit()
    elif len(sys.argv) >= 3:  # comprobar q el comando
        if sys.argv[2] not in comandos:  # este en aceptados
            print("ERROR: no entiendo el comando")
            print("Los comandos disponibles son: info, ping, instala, actualiza, reset, list_users y ejecutar")
            sys.exit()
try:  # si llegamoos hasta aqui es que escribieron bien los parametros
    comando = sys.argv[2]  # probamos por si acaso

    # INFO DEL MINION

    if comando.lower() == "info":  # info de la maquina
        makina = sys.argv[1]
        print("Doxeando.........")
        sleep(1)
        subprocess.run(["salt", makina, "grains.items"])
        sys.exit()


    # WIN UPDATE DE MINION

    elif comando.lower() == "actualizar":  # update de minions
        makina = sys.argv[1]
        print("Actualizando maquina", makina, "..........")
        subprocess.run(["salt", makina, "win_wua.list", "install=True"])
        sys.exit()

    # TEST PING A MINION

    elif comando.lower() == "ping":  # ping de minions
        makina = sys.argv[1]
        print("Pingeando a", makina)
        subprocess.run(["salt", makina, "test.ping"])
        sys.exit()


    # INSTALAR PAQUETE EN MINION

    elif comando.lower() == "instalar":  # instala software en minion
        if len(sys.argv) != 4:
            print("ERROR: debes indicarme un programa para instalar")
            sys.exit()
        else:
            makina = sys.argv[1]
            print("Instalando", sys.argv[3], "en", makina, "...")
            subprocess.run(["salt", makina, "chocolatey.install", sys.argv[3]])
            sys.exit()

    # RESETEAR PASSWORD DE USUARIO DE MINION

    elif comando.lower() == "reset":  # reset user y pass minion
        if len(sys.argv) != 5:
            print("ERROR: debes indicar usuario y password")
            sys.exit()
        else:
            makina = sys.argv[1]
            user = sys.argv[3]
            passwd = sys.argv[4]
            str = "net user " + user + " " + passwd
            print("Reseteando pass para", user, " // Nueva password:", passwd)
            subprocess.run(["salt", makina, "cmd.run", str])
            sys.exit()

    # LISTAR USUARIOS DEL MINION

    elif comando.lower() == "list_users":  # lista los users del minion
        makina = sys.argv[1]
        print("Preguntando la lista de usuarios de", makina)
        subprocess.run(["salt", makina, "cmd.run", "net users"])
        sys.exit()

    # EJECUTAR

    elif comando.lower() == "ejecutar":  # ejecuta un comando en el minion
        makina = sys.argv[1]
        coman = sys.argv[3]
        print("Ejecutando", coman)
        subprocess.run(["salt", makina, "cmd.run", coman])
        sys.exit()

    # DESCARGAR

    elif comando.lower() == "descargar":
        makina = sys.argv[1]
        url = input("URL del archivo a descargar: ")
        ruta = input("Ruta en el minion donde descargar (nombre fichero incluido): ")
        cmd = "'curl " + url + " -o " + ruta + "'"
        print("Descargar", url, "en", ruta, )
        sino = ["si", "no"]
        resp = input("Proceder: si o no? ")
        while resp not in sino:  # bucle, o si o no
            print("ERROR: debes responder 'si' o 'no'")
            resp = input("Proceder: si o no? ")
        if resp.lower() == "si":  # creamos tarea
            print("Comprobando si curl esta instalado en", makina, "....")
            subprocess.run(["salt", makina, "chocolatey.install_missing", "curl"])
            print("Descargando", url, "........")
            subprocess.run(["salt", makina, "cmd.run", cmd])
            x = "'dir " + ruta + "'"
            subprocess.run(["salt", makina, "cmd.run", x])
            sys.exit()
        elif resp.lower() == "no":  # cancelamos
            print("Cancelando....")
            sys.exit()

    # UPDATE DESATENDIDA (eliminar .exe de c:\temp, descargar un exe y crear tarea para ejecutar exe)

    elif comando.lower() == "update_d":
        if len(sys.argv) < 6:
            print("ERROR: faltan argumentos.\nUso: vsalt minion update_d url hora usuario")
            sys.exit()
        elif len(sys.argv) == 6:
            makina = sys.argv[1]
            url = sys.argv[3]
            hora = sys.argv[4]
            usuario = sys.argv[5]
            borra = "'del /q /f c:\\temp\*.exe'"
            descarga = "'curl " + url + " -o " + "c:\\temp\\update.exe" + "'"
            print("Eliminando todos los .exe de c:\\temp....")
            subprocess.run(["salt", makina, "cmd.run", borra])
            print("Comprobando si curl esta instalado en", makina, "....")
            subprocess.run(["salt", makina, "chocolatey.install_missing", "curl"])
            print("Descargando", url, "en c:\\temp\\update.exe .....")
            subprocess.run(["salt", makina, "cmd.run", descarga])
            print("Creando la tarea programada para ejecutar update.exe como", usuario, "...")
            person = "user_name=" + usuario
            cmd = "cmd=\'c:\\temp\\update.exe\'"
            hora = "start_time=\'" + hora + "\'"
            subprocess.run(["salt", makina, "task.create_task", "update_d", person, "force=True",
                            "action_type=Execute", cmd, "trigger_type=Once", hora])
            sys.exit()

        # BLOQUE TAREAS

    elif comando.lower() == "tareas":
        print("Tareas.....")
        if len(sys.argv) < 4:  # lo has escrito bien?
            print("Error: debes especificar una accion para tareas\nAcciones: crear, listar, info y eliminar")
            sys.exit()

        subcom = ["crear", "eliminar", "listar", "info"]  # args disponibles
        makina = sys.argv[1]
        if sys.argv[3] not in subcom:
            print("Error: no puedo", sys.argv[3], "una tarea")
        elif sys.argv[3] == "crear":  # crear tarea
            if len(sys.argv) < 11:
                print("ERROR: Faltan argumentos")
                print("Ej.: vsalt minion tareas crear nombre_tarea usuario comando argumentos trigger hora_inicio repeticion intervalo")
                print("trigger: 0=once, 1=daily ; repeticion: 0=no, 1=si")
                print("intervalo: 5=5min, 10=10min, 15=15min, 30=30min, 1h=1hora")
            nom = sys.argv[4]
            user = "user_name=" + sys.argv[5]
            cmd = "cmd='" + sys.argv[6] + "'"
            args = "arguments='" + sys.argv[7] + "'"
            if sys.argv[8] == "0":
                trigger = "trigger_type=Once"
            elif sys.argv[8] == "1":
                trigger = "trigger_type=Daily"
            x = str(sys.argv[9])
            hora = "start_time=\'" + x + "\'"
            rep = sys.argv[10]
            if rep == "0":
                subprocess.run(["salt", makina, "task.create_task", nom, user, "force=True",
                                "action_type=Execute", cmd, args, trigger, hora])
                sys.exit()
            elif rep == "1":
                if sys.argv[11] == "5":
                    lapsus = "repeat_interval='5 minutes'"
                elif sys.argv[11] == "10":
                    lapsus = "repeat_interval='10 minutes'"
                elif sys.argv[11] == "15":
                    lapsus = "repeat_interval='15 minutes'"
                elif sys.argv[11] == "30":
                    lapsus = "repeat_interval='30 minutes'"
                elif sys.argv[11] == "1h":
                    lapsus = "repeat_interval='1 hour'"
                subprocess.run(["salt", makina, "task.create_task", nom, user, "force=True",
                                "action_type=Execute", cmd, args, trigger, hora, lapsus])
                sys.exit()
        elif sys.argv[3] == "listar":  # listar tareas
            makina = sys.argv[1]
            subprocess.run(["salt", makina, "task.list_tasks"])
            sys.exit()
        elif sys.argv[3] == "eliminar":  # eliminar treas
            makina = sys.argv[1]
            if len(sys.argv) == 5:  # si paso la tarea como arg, borrala
                print("Eliminando la tarea", sys.argv[4])
                subprocess.run(["salt", makina, "task.delete_task", sys.argv[4]])
                sys.exit()
            elif len(sys.argv) == 4:  # si no te la paso, dejame elegir
                subprocess.run(["salt", makina, "task.list_tasks"])
                print("Estas son las tareas disponibles.")
                victim = input("Que tarea debemos eliminar? (recuerda case sensitive!!): ")
                subprocess.run(["salt", makina, "task.delete_task", victim])
                sys.exit()
            elif len(sys.argv) > 5:  # demasiadas tareas para un solo script
                print("Error: Las tareas se eliminan de una en una.\nError de sintaxis.")
                sys.exit()
        elif sys.argv[3] == "info":  # info tareas
            makina = sys.argv[1]
            if len(sys.argv) == 5:  # si te paso la tarea como arg, doxeala
                print("Doxeando la tarea", sys.argv[4])
                subprocess.run(["salt", makina, "task.info", sys.argv[4]])
                sys.exit()
            elif len(sys.argv) == 4:  # si no te la paso, dejame elegir
                subprocess.run(["salt", makina, "task.list_tasks"])
                print("Estas son las tareas disponibles.")
                victim = input("Que tarea quieres ver? (recuerda case sensitive!!): ")
                subprocess.run(["salt", makina, "task.info", victim])
                sys.exit()
            elif len(sys.argv) > 5:  # demasiadas tareas a doxear
                print("Error: Las tareas se doxean de una en una.\nError de sintaxis.")
                sys.exit()
  # FIN BLOQUE DE TAREAS


except IndexError:
    print("Uno o mas argumentos son incorrectos, revisa el oneliner")
    sys.exit()