#!/usr/bin/python3
"""COSAS POR HACER:
-
- usar el modulo win_task para crear y modificar tareas programadas en los minions
usuario system, dayly rep 1 hora start time
crear eliminar y modificar listar

- Ordenar el Help"""




import subprocess
import sys
import os
from time import sleep

comandos = ["instala","actualiza","reset","ping","info","list_users", "ejecutar", "tareas"]	# comandos soportados por salto.py

if os.geteuid() != 0:
	print("ERROR: salto.py debe ser ejecutado como usuario root")	# no root, no fun
	sys.exit()
else:
	if len(sys.argv) == 1:
		print("salto.py --help para ayuda")		# ejecucion sin parametros
		sys.exit()
	elif sys.argv[1] == "-h" or sys.argv[1] == "--help":	# ayuda
		print("salto.py\nUSO: salto.py <MAQUINA> <COMANDO>")
		print("Comandos disponibles: info, ping, instala, actualiza, reset, list_users y ejecutar")
		print("----------------------------------------------------------------------------------")
		print("* info: devuelve los valores de los grains del minion seleccionado")
		print("* ping: realiza un test ping para ver si la maquina esta levantada")
		print("* instala: instala <PAQUETE> -> instala PAQUETE en minion seleccionado")
		print("* actualiza: actualiza windows del minion seleccionado")
		print("* reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
		print("* list_users: devuelve lista de usuarios en el minion ")
		print("* ejecutar: ejecutar \"<COMANDO>\" -> ejecuta comando en minion (comando entre comillas)")
		print("----------------------------------------------------------------------------------")
		print("Ej.: sudo salto.py MINION actualiza")
		print("Ej.: sudo salto.py MINION instala malwarebytes")
		print("Ej.: sudo salto.py MINION reset pepe abc123")
		sys.exit()
	elif len(sys.argv) == 2:
		print("salto.py\nUSO: salto.py <MAQUINA> <COMANDO>")
		print("Comandos disponibles: info, ping, instala, actualiza, reset, list_users y ejecutar")
		print("----------------------------------------------------------------------------------")
		print("* info: devuelve los valores de los grains del minion seleccionado")
		print("* ping: realiza un test ping para ver si la maquina esta levantada")
		print("* instala: instala <PAQUETE> -> instala PAQUETE en minion seleccionado")
		print("* actualiza: actualiza windows del minion seleccionado")
		print("* reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
		print("* list_users: devuelve lista de usuarios en el minion ")
		print("* ejecutar: ejecutar \"<COMANDO>\" -> ejecuta comando en minion (comando entre comillas)")
		print("----------------------------------------------------------------------------------")
		print("Ej.: sudo salto.py MINION actualiza")
		print("Ej.: sudo salto.py MINION instala malwarebytes")
		print("Ej.: sudo salto.py MINION reset pepe abc123")
		sys.exit()
	elif len(sys.argv) >= 3:				# comprobar q el comando
		if sys.argv[2] not in comandos:			# este en aceptados
			print("ERROR: no entiendo el comando")
			print("Los comandos disponibles son: info, ping, instala, actualiza, reset, list_users y ejecutar")
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
				subprocess.run(["salt",makina,"chocolatey.install",sys.argv[3]])

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
	elif comando.lower() == "ejecutar":		# ejecuta un comando en el minion
			makina = sys.argv[1]
			coman = sys.argv[3]
			coman = str(coman)
			print("Ejecutando", coman)
			subprocess.run(["salt",makina,"cmd.run",coman])

#BLOQUE TAREAS EN DESARROLLO

	elif comando.lower() == "tareas":
		print("Tareas.....")
		if len(sys.argv) != 4:
			print("Error: debes especificar una accion para tareas\nAcciones: crear, listar y eliminar")
		else:
			subcom = ["crear", "eliminar", "listar"]
			makina = sys.argv[1]
			if sys.argv[3] not in subcom:
				print("Error: no puedo", sys.argv[3],"una tarea")
			elif sys.argv[3] == "crear":
				nom = input("Nombre de la tarea: ")
				cmd = "cmd='"
				cmd = cmd + input("Comando a ejecutar: ")
				cmd = cmd + "'"
				trigger = ""
				trigger = input("Trigger: [1] Una vez [2] Diariamente\nSelecciona 1 o 2: ")
				trigs = ["1","2"]
				while trigger not in trigs:
					print("Error: selecciona 1 o 2")
					trigger = input("Trigger: [1] Una vez [2] Diariamente\nSelecciona 1 o 2: ")
				if trigger == "1":
					trigger = "trigger_type=Once"
				elif trigger == "2":
					trigger = "trigger_type=Daily"
				print("Seleccionaste", trigger)
				x = input("Hora de inicio de tarea: ")
				hora = "start_time="+x
				print("vamos a",sys.argv[3],"la tarea",nom,"con el comando",cmd)
				sino = ["si","no"]
				resp = input("Proceder: si o no? ")
				while resp not in sino:
					print("ERROR: debes responder 'si' o 'no'")
					resp = input("Proceder: si o no? ")
				if resp.lower() == "si":
					print("Ejecutar win.task_create")
					subprocess.run(["salt", makina, "task.create_task", nom,"user_name=System", "force=True", "action_type=Execute",cmd, trigger,hora])
					print(makina)
				elif resp.lower() == "no":
					print("Cancelando....")
					sys.exit()
			elif sys.argv[3] == "listar":
				makina = sys.argv[1]
				subprocess.run(["salt", makina, "task.list_tasks"])
				sys.exit()

			elif sys.argv[3] == "eliminar":
				makina = sys.argv[1]
				subprocess.run(["salt", makina, "task.list_tasks"])
				print("Estas son las tareas disponibles.")
				victim = input("Que tarea debemos eliminar? (recuerda case sensitive!!): ")
				subprocess.run(["salt", makina, "task.delete_task", victim])
				sys.exit()
			elif sys.argv[3] == "info":
				makina = sys.argv[1]
				subprocess.run(["salt", makina, "task.list_tasks"])
				print("Estas son las tareas disponibles.")
				victim = input("Que tarea quieres ver? (recuerda case sensitive!!): ")
				subprocess.run(["salt", makina, "task.info", victim])
				sys.exit()



#FIN BLOQUE DE TAREAS



except IndexError:
		print("Uno o mas argumentos son incorrectos, revisa el oneliner")

