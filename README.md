# salto
script python para automatizar operaciones con saltstack y tener "one liners" mas pequeños

USO: salto MAQUINA COMANDO\n
Comandos disponibles: info, ping, instalar, actualizar, reset, list_users, ejecutar y tareas
Ejecuta 'salto minions' para ver la lista de minions en el master
----------------------------------------------------------------------------------
* info: devuelve los valores de los grains del minion seleccionado
* ping: realiza un test ping para ver si la maquina esta levantada
* instalar: instala PAQUETE -> instala PAQUETE en minion seleccionado
* actualizar: actualiza windows del minion seleccionado
* reset: reset USER PASS -> cambia el passwword a PASS del usuario USER
* list_users: devuelve lista de usuarios en el minion 
* ejecutar: ejecutar 'COMANDO' -> ejecuta comando en minion (comando entre comillas simples)
* descargar: descarga un archivo en una ruta indicada del minion
----------------------------------------------------------------------------------
* salto lote archivo.txt 'comando a ejecutar':
Ejecuta el comando en una lista de minions en un archivo (un minion por linea)
----------------------------------------------------------------------------------
* tareas ACCION (OPCION)
* tareas crear: crea una tarea programada en el minion
* tareas eliminar (tarea): elimina una tarea programada del minion
* tareas listar: lista todas las tareas programadas del minion
* tareas info (tarea): devuelve info de una tarea concreta del minion
-----------------------------------------------------------------------------------
Ej.: sudo salto MINION actualizar
Ej.: sudo salto MINION instalar malwarebytes
Ej.: sudo salto MINION reset pepe abc123
Ej.: sudo salto MINION ejecutar 'dir c:\windows\'