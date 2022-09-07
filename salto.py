#!/usr/bin/python3
"""COSAS POR HACER:

+ listar minions
+ ejecutar comando en lista de minions (archivo)

"""




import subprocess
import sys
import os
from time import sleep

comandos = ["instalar","actualizar","reset","ping","info","list_users", "ejecutar", "tareas",
			"descargar",]	# comandos soportados por salto.py

if os.geteuid() != 0:
	print("ERROR: salto debe ser ejecutado como usuario root")	# no root, no fun
	sys.exit()
else:
	if len(sys.argv) == 1:
		print("salto --help para ayuda")		# ejecucion sin parametros
		sys.exit()
	elif sys.argv[1] == "-h" or sys.argv[1] == "--help":	# ayuda
		print("\nsalto\nUSO: salto <MAQUINA> <COMANDO>")
		print("Comandos disponibles: info, ping, instalar, actualizar, reset, list_users, ejecutar, descargar y tareas")
		print("Ejecuta 'salto minions' para ver la lista de minions en el master")
		print("----------------------------------------------------------------------------------")
		print("* info: devuelve los valores de los grains del minion seleccionado")
		print("* ping: realiza un test ping para ver si la maquina esta levantada")
		print("* instala: instalar <PAQUETE> -> instala PAQUETE en minion seleccionado")
		print("* actualiza: actualizar windows del minion seleccionado")
		print("* reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
		print("* list_users: devuelve lista de usuarios en el minion ")
		print("* ejecutar: ejecutar '<COMANDO>' -> ejecuta comando en minion (comando entre comillas simples)")
		print("* descargar: descarga un archivo en una ruta indicada del minion")
		print("----------------------------------------------------------------------------------")
		print("* salto lote archivo.txt 'comando a ejecutar':")
		print("Ejecuta el comando en una lista de minions en un archivo (un minion por linea)")
		print("----------------------------------------------------------------------------------")
		print("* tareas <ACCION> (OPCION)")
		print("* tareas crear: crea una tarea programada en el minion")
		print("* tareas eliminar (tarea): elimina una tarea programada del minion.")
		print("* tareas listar: lista todas las tareas programadas del minion")
		print("* tareas info (tarea): devuelve info de una tarea concreta del minion")
		print("----------------------------------------------------------------------------------")
		print("Ej.: sudo salto MINION actualizar")
		print("Ej.: sudo salto MINION instalar malwarebytes")
		print("Ej.: sudo salto MINION reset pepe abc123")
		print("Ej.: sudo salto MINION ejecutar 'dir c:\\windows\\'\n")
		sys.exit()

# Lista de Minions activos en master

	elif sys.argv[1] == "minions":
		print("Consultando la lista de minions.....")
		subprocess.run(["salt-key","-L"])
		sys.exit()

# Ejecucion de comandos en lista de minions dada por un archivo CSV

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
			print("ERROR: Error de sintaxis\nLa forma correcta es \"salto lote lista.txt 'comando a ejecutar'\"")
			sys.exit()

# Menu ayuda

	elif len(sys.argv) == 2:
		print("\nsalto\nUSO: salto <MAQUINA> <COMANDO>")
		print("Comandos disponibles: info, ping, instalar, actualizar, reset, list_users, ejecutar y tareas")
		print("Ejecuta 'salto minions' para ver la lista de minions en el master")
		print("----------------------------------------------------------------------------------")
		print("* info: devuelve los valores de los grains del minion seleccionado")
		print("* ping: realiza un test ping para ver si la maquina esta levantada")
		print("* instalar: instala <PAQUETE> -> instala PAQUETE en minion seleccionado")
		print("* actualizar: actualiza windows del minion seleccionado")
		print("* reset: reset <USER> <PASS> -> cambia el passwword a PASS del usuario USER")
		print("* list_users: devuelve lista de usuarios en el minion ")
		print("* ejecutar: ejecutar '<COMANDO>' -> ejecuta comando en minion (comando entre comillas simples)")
		print("* descargar: descarga un archivo en una ruta indicada del minion")
		print("----------------------------------------------------------------------------------")
		print("* salto lote archivo.txt 'comando a ejecutar':")
		print("Ejecuta el comando en una lista de minions en un archivo (un minion por linea)")
		print("----------------------------------------------------------------------------------")
		print("* tareas <ACCION> (OPCION)")
		print("* tareas crear: crea una tarea programada en el minion")
		print("* tareas eliminar (tarea): elimina una tarea programada del minion")
		print("* tareas listar: lista todas las tareas programadas del minion")
		print("* tareas info (tarea): devuelve info de una tarea concreta del minion")
		print("----------------------------------------------------------------------------------")
		print("Ej.: sudo salto MINION actualizar")
		print("Ej.: sudo salto MINION instalar malwarebytes")
		print("Ej.: sudo salto MINION reset pepe abc123")
		print("Ej.: sudo salto MINION ejecutar 'dir c:\\windows\\'\n")
		sys.exit()
	elif len(sys.argv) >= 3:				# comprobar q el comando
		if sys.argv[2] not in comandos:			# este en aceptados
			print("ERROR: no entiendo el comando")
			print("Los comandos disponibles son: info, ping, instala, actualiza, reset, list_users y ejecutar")
			sys.exit()
try:				# si llegamoos hasta aqui es que escribieron bien los parametros
	comando = sys.argv[2]	# probamos por si acaso

	if comando.lower() == "info":	# info de la maquina
		makina = sys.argv[1]
		print("Doxeando.........")
		sleep(1)
		subprocess.run(["salt", makina, "grains.items"])

	if comando.lower() == "actualizar":		# update de minions
		makina = sys.argv[1]
		print("Actualizando maquina",makina,"..........")
		subprocess.run(["salt", makina, "win_wua.list" , "install=True"])

	elif comando.lower() == "ping":			# ping de minions
		makina = sys.argv[1]
		print("Pingeando a",makina)
		subprocess.run(["salt",makina,"test.ping"])

	elif comando.lower() == "instalar":		# instala software en minion
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
			print("Ejecutando", coman)
			subprocess.run(["salt",makina,"cmd.run",coman])
	elif comando.lower() =="descargar":
		makina = sys.argv[1]
		url = input("URL del archivo a descargar: ")
		ruta = input("Ruta en el minion donde descargar (nombre fichero incluido): ")
		cmd = "'curl " + url + " -o " + ruta + "'"
		print("Descargar", url, "en", ruta,)
		sino = ["si", "no"]
		resp = input("Proceder: si o no? ")
		while resp not in sino:  # bucle, o si o no
			print("ERROR: debes responder 'si' o 'no'")
			resp = input("Proceder: si o no? ")
		if resp.lower() == "si":  # creamos tarea
			print("Comprobando si curl esta instalado en", makina, "....")
			subprocess.run(["salt", makina, "chocolatey.install_missing", "curl" ])
			print("Descargando", url, "........")
			subprocess.run(["salt", makina, "cmd.run", cmd])
			x = "'dir " + ruta + "'"
			subprocess.run(["salt", makina, "cmd.run", x])
			sys.exit()
		elif resp.lower() == "no":  # cancelamos
			print("Cancelando....")
			sys.exit()



#BLOQUE TAREAS

	elif comando.lower() == "tareas":
		print("Tareas.....")
		if len(sys.argv) < 4:	# lo has escrito bien?
			print("Error: debes especificar una accion para tareas\nAcciones: crear, listar, info y eliminar")
		else:
			subcom = ["crear", "eliminar", "listar","info"]	# args disponibles
			makina = sys.argv[1]
			if sys.argv[3] not in subcom:
				print("Error: no puedo", sys.argv[3],"una tarea")
			elif sys.argv[3] == "crear":		# crear tarea
				if len(sys.argv) > 4:
					print("ERROR: no se pueden pasar argumentos al comando 'crear")
					sys.exit()
				nom = input("Nombre de la tarea: ")
				cmd = "cmd='"
				cmd = cmd + input("Comando a ejecutar: ")
				cmd = cmd + "'"
				trigger = ""
				args = "arguments='"
				args = args + input("Argumentos del comando: ")
				args = args + "'"
				trigger = input("Trigger: [1] Una vez [2] Diariamente\nSelecciona 1 o 2: ")
				trigs = ["1","2"]
				while trigger not in trigs:	# bucle, o 1 o 2
					print("Error: selecciona 1 o 2")
					trigger = input("Trigger: [1] Una vez [2] Diariamente\nSelecciona 1 o 2: ")
				if trigger == "1":
					trigger = "trigger_type=Once"
				elif trigger == "2":
					trigger = "trigger_type=Daily"
				print("Seleccionaste", trigger)
				x = input("Hora de inicio de tarea: ")
				x = str(x)
				hora = "start_time=\'"+x+"\'"
				rep = input("Quieres que la tarea se repita? si/no: ")
				reps = ["si","no"]
				while rep not in reps:
					print("Error: escribe 'si' o 'no'.")
					rep = input("Quieres que la tarea se repita? si/no: ")
				if rep == "si":
					lapsus = "repeat_interval='"
					print("Opciones validas: [1]: 5minutos, [2]: 10minutos, [3]: 15minutos, [4]: 30minutos, [5]: 1hora")
					selec = input("Elige una de las opciones validas: ")
					opts =["1","2","3","4","5"]
					while selec not in opts:
						print("Error: Selecciona una de las opciones correctas")
						print("Opciones validas: [1]: 5minutos, [2]: 10minutos, [3]: 15minutos, [4]: 30minutos, [5]: 1hora")
						selec = input("Elige una de las opciones validas: ")
					if selec == "1":
						lapsus = lapsus + "5 minutes'"
					elif selec == "2":
						lapsus == lapsus + "10 minutes'"
					elif selec == "3":
						lapsus = lapsus + "15 minutes'"
					elif selec == "4":
						lapsus = lapsus + "30 minutes'"
					elif selec == "5":
						lapsus = lapsus + "1 hour'"
					print("vamos a", sys.argv[3], "la tarea", nom, "con el comando", cmd, "y argumentos", args, )
					print("Hora de inicio:", hora, "- Repeticion:",lapsus)
					sino = ["si", "no"]
					resp = input("Proceder: si o no? ")
					while resp not in sino:  # bucle, o si o no
						print("ERROR: debes responder 'si' o 'no'")
						resp = input("Proceder: si o no? ")
					if resp.lower() == "si":  # creamos tarea
						print("Ejecutando win.task_create en", makina, "....")
						subprocess.run(["salt", makina, "task.create_task", nom, "user_name=System", "force=True",
										"action_type=Execute", cmd, args, trigger, hora, lapsus])
						sys.exit()
					elif resp.lower() == "no":  # cancelamos
						print("Cancelando....")
						sys.exit()

				elif rep == "no":
					print("Creando tarea sin intervalo de repeticion")
				print("vamos a",sys.argv[3],"la tarea",nom,"con el comando",cmd, "y argumentos", args,)
				print("Hora de inicio:",hora,)
				sino = ["si","no"]
				resp = input("Proceder: si o no? ")
				while resp not in sino:	# bucle, o si o no
					print("ERROR: debes responder 'si' o 'no'")
					resp = input("Proceder: si o no? ")
				if resp.lower() == "si":		# creamos tarea
					print("Ejecutando win.task_create en",makina,"....")
					subprocess.run(["salt", makina, "task.create_task", nom,"user_name=System", "force=True",
									"action_type=Execute", cmd, args, trigger, hora])
					sys.exit()
				elif resp.lower() == "no":		# cancelamos
					print("Cancelando....")
					sys.exit()
			elif sys.argv[3] == "listar":		# listar tareas
				makina = sys.argv[1]
				subprocess.run(["salt", makina, "task.list_tasks"])
				sys.exit()

			elif sys.argv[3] == "eliminar": # eliminar treas
				makina = sys.argv[1]
				if len(sys.argv) == 5: # si paso la tarea como arg, borrala
					print("Eliminando la tarea",sys.argv[4])
					subprocess.run(["salt", makina, "task.delete_task", sys.argv[4]])
					sys.exit()
				elif len(sys.argv) == 4: # si no te la paso, dejame elegir
					subprocess.run(["salt", makina, "task.list_tasks"])
					print("Estas son las tareas disponibles.")
					victim = input("Que tarea debemos eliminar? (recuerda case sensitive!!): ")
					subprocess.run(["salt", makina, "task.delete_task", victim])
					sys.exit()
				elif len(sys.argv) > 5:		# demasiadas tareas para un solo script
					print("Error: Las tareas se eliminan de una en una.\nError de sintaxis.")
					sys.exit()
			elif sys.argv[3] == "info":		# info tareas
				makina = sys.argv[1]
				if len(sys.argv) == 5:		# si te paso la tarea como arg, doxeala
					print("Doxeando la tarea", sys.argv[4])
					subprocess.run(["salt", makina, "task.info", sys.argv[4]])
					sys.exit()
				elif len(sys.argv) == 4:		# si no te la paso, dejame elegir
					subprocess.run(["salt", makina, "task.list_tasks"])
					print("Estas son las tareas disponibles.")
					victim = input("Que tarea quieres ver? (recuerda case sensitive!!): ")
					subprocess.run(["salt", makina, "task.info", victim])
					sys.exit()
				elif len(sys.argv) > 5:		# demasiadas tareas a doxear
					print("Error: Las tareas se doxean de una en una.\nError de sintaxis.")
					sys.exit()



#FIN BLOQUE DE TAREAS



except IndexError:
		print("Uno o mas argumentos son incorrectos, revisa el oneliner")

