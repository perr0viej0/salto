#!/usr/bin/python3

import subprocess
import sys
import os
from time import sleep

comandos = ["instala","actualiza","reset","ping","info","list_users"]	# comandos soportados por salto.py

if os.geteuid() != 0:
	print("ERROR: salto.py debe ser ejecutado como usuario root")	# no root, no fun
	sys.exit()
else:
	if len(sys.argv) == 1:
		print("salto.py --help para ayuda")		# ejecucion sin parametros
		sys.exit()
	elif sys.argv[1] == "-h" or sys.argv[1] == "--help":	# ayuda
		print("salto.py\nUSO: salto.py <MAQUINA> <COMANDO>")
		print("Comandos disponibles: info, ping, instala, actualiza y reset")
		print("info: devuelve los valores de los grains del minion seleccionado")
		print("ping: realiza un test ping para ver si la maquina esta levantada")
		print("instala: instala <PAQUETE> -> instala PAQUETE en minion seleccionado")
		print("actualiza: actualiza windows del minion seleccionado")
		print("reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
		print("list_users: devuelve lista de usuarios en el minion ")
		print("Ej.: sudo salto.py MINION actualiza")
		print("Ej.: sudo salto.py MINION instala malwarebytes")
		print("Ej.: sudo salto.py MINION reset pepe abc123")
		sys.exit()
	elif len(sys.argv) == 2:
		print("salto.py\nUSO: salto.py <MAQUINA> <COMANDO>")
		print("Comandos disponibles: info, ping, instala, actualiza y reset")
		print("info: devuelve los valores de los grains del minion seleccionado")
		print("ping: realiza un test ping para ver si la maquina esta levantada")
		print("instala: instala <PAQUETE> -> instala PAQUETE en minion seleccionado")
		print("actualiza: actualiza windows del minion seleccionado")
		print("reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
		print("list_users: devuelve lista de usuarios en el minion ")
		print("Ej.: sudo salto.py MINION actualiza")
		print("Ej.: sudo salto.py MINION instala malwarebytes")
		print("Ej.: sudo salto.py MINION reset pepe abc123")
	elif len(sys.argv) == 3:				# comprobar q el comando
		if sys.argv[2] not in comandos:			# este en aceptados
			print("ERROR: no entiendo el comando")
			print("Los comandos disponibles son: info, ping, instala, actualiza y reset")
			sys.exit()
try:				# si llegamoos hasta aqui es que escribieron bien los parametros
	comando = sys.argv[2]	# probamos por si acaso

	if comando.lower() == "info":
		makina = sys.argv[1]
		print("Doxeando.........")
		sleep(1)
		subprocess.run(["salt", makina, "grains.items"])

	if comando.lower() == "actualiza":		# update de minions
		makina = sys.argv[1]
		print("Actualizando maquina",makina,"..........")
		subprocess.run(["salt", makina, "win_wua.list" , "install=True"])

	elif comando.lower() == "ping":			# ping de minions
		makina = sys.argv[1]
		print("Pingeando a",makina)
		subprocess.run(["salt",makina,"test.ping"])

	elif comando.lower() == "instala":		# instala software en minion
		if len(sys.argv) != 4:
	        	print("ERROR: debes indicarme un programa para instalar")
		else:
				makina = sys.argv[1]
				print("Instalando",sys.argv[3],"en",makina,"...")
				subprocess.run(["salt",makina,"pkg.install",sys.argv[3]])

	elif comando.lower() == "reset":		# reset user y pass minion
		if len(sys.argv) != 5:
			print("ERROR: debes indicar usuario y password")
		else:
			makina = sys.argv[1]
			user = sys.argv[3]
			passwd = sys.argv[4]
			str = "net user "+user+" "+passwd
			print("Reseteando pass para",user," // Nueva password:",passwd)
			subprocess.run(["salt", makina, "cmd.run",str])
	elif comando.lower() == "list_users":	# lista los users del minion
			makina = sys.argv[1]
			print("Preguntando la lista de usuarios de", makina)
			subprocess.run(["salt", makina, "cmd.run", "net users"])
except IndexError:
		print("Uno o mas argumentos son incorrectos, revisa el oneliner")

