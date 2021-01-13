import time
import playsound #pip || pip3 install playsound

M = 60 #Hay 60 segundos en un minuto
POMODORO_WORKING_TIME = M*25 #25 minutos
POMODORO_RESTING_TIME_LIGHT = M*4 #4 minutos
POMODORO_RESTING_TIME_HARD = M*30 #30 minutos
BELL = "bell.mp3" #si no existe el archivo bell.mp3 en la raíz, no sonará nada cuando termine cada temporizador
"""
sonido original:
https://www.youtube.com/watch?v=FuPvbVgEH_c&ab_channel=premier1supplies

Sonido descaragado y convertido con:
https://ytmp3.cc/en13/
"""
MAX_POMODOROS = 4

def menu(pomodoros):
	option = 0

	while True:
		print("\n---Menú principal---")
		print("Pomodoros actuales %d"%(pomodoros))
		print("Máximos pomodoros permitidos %d"%(MAX_POMODOROS))
		print("¿Qué quieres hacer?")
		print("( 1 ) Iniciar pomodoro")
		print("( 2 ) Cambiar cantidad de pomodoros")
		print("( 3 ) Cambiar tiempos \n\tTrabajando = %s\n\tDescanso corto = %s \n\tDescanso Largo = %s"%(secondsToMinutes(POMODORO_WORKING_TIME), secondsToMinutes(POMODORO_RESTING_TIME_LIGHT), secondsToMinutes(POMODORO_RESTING_TIME_HARD)))
		print("( 0 ) Salir")
		option = input()

		if option.isdigit():
			return int(option)
		else:
			print("Opción incorrecta, intente de nuevo")

def startPomodoro(timer):
	#bucle impresor de tiempo
	while timer >= 0:
		print(secondsToMinutes(timer))
		time.sleep(1)
		timer -=1
	#No son segundo exactos (de hecho sn más grandes) debido a la concurrencia del sistema operativo, serán más grandes dependiendo la ocupación del procesador

	#Reproduce un sonido para avisar el cambio entre fases
	try:
		playsound.playsound(BELL)
	except:
		print("Archivo --%s-- no encontrado"%BELL)

def secondsToMinutes(minutes):
	#euristica para saber los segundos restantes(segundos_totales - segundos_en_minutos)
	return "%d:%d"%(minutes//M, minutes-((minutes//M)*M)) 

def changePomodoros():
	while True:
		new_pomodoros = input("¿Cuántos pomodoros llevas?:\n")
		#Verificar que es un número valido de pomodoros <4 & >0
		if (new_pomodoros.isdigit() and int(new_pomodoros) < MAX_POMODOROS) or (new_pomodoros.isdigit() and int(new_pomodoros) < 0):
			return int(new_pomodoros)
		print("Cantidad no valida, el número de pomodoros debe de ser menor a %d y mayor a %d"%(MAX_POMODOROS, 0))

def changeTime():
	#conseguir un número valido para el tiempo
	while True:
		try:	#Veriicar que sea flotante
			new_time = float(input("¿Cuantos minutos quieres asignar?\n"))
			if new_time > 0:
				return new_time*M
		except:
			pass
		#si no lo es, no retornes nada y vuelve a intentarlo
		print("Ingrese un valor numerico valido mayor a 0")

def getLocalConfig():
	global POMODORO_WORKING_TIME, POMODORO_RESTING_TIME_LIGHT, POMODORO_RESTING_TIME_HARD, BELL
	local_config = {}
	#Si existe el archivo leelo
	try:
		with open("pomodoro.config", 'r') as file:
			#Obten la información del archivo
			local_config = getInfoFromFile(file)
			#Asigna la información a cada variable permitida
			POMODORO_WORKING_TIME = int(local_config["POMODORO_WORKING_TIME"])*M
			POMODORO_RESTING_TIME_LIGHT = int(local_config["POMODORO_RESTING_TIME_LIGHT"])*M
			POMODORO_RESTING_TIME_HARD = int(local_config["POMODORO_RESTING_TIME_HARD"])*M
			BELL = local_config["BELL"]
			return int(local_config["pomodoros"])
	#Si no existe crealo
	except:
		with open("pomodoro.config", 'w') as file:
			setInfoIntoFile(file, 0)
			return 0
	#Retorna el número de pomodoros para inicializar el programa (mala práctica)

def getInfoFromFile(file):
	#Guarda la información del archivo
	data_set = {}
	#Lee cada linea del archivo
	for line in file:
		start_reading = 0
		#Lee cada caracter de la linea
		for index, char in enumerate(line):
			#Consiguiendo la posición del punto clave =
			if char == '=':
				start_reading = index
		#El nuevo elemento es (Todo lo que hay antes de = sin espacios) = (Todo lo que hay después de = sin espacios ni \n)
		data_set[line[:start_reading].replace(" ", "")] = line[start_reading+1:].replace(" ", "").replace("\n", "")
	return data_set

def setInfoIntoFile(file, pomodoros):
	file.write("pomodoros = %d\n"%(pomodoros))
	file.write("POMODORO_WORKING_TIME = %d\n"%(POMODORO_WORKING_TIME//60))
	file.write("POMODORO_RESTING_TIME_LIGHT = %d\n"%(POMODORO_RESTING_TIME_LIGHT//60))
	file.write("POMODORO_RESTING_TIME_HARD = %d\n"%(POMODORO_RESTING_TIME_HARD//60))
	file.write("BELL = %s"%(BELL))

def setLocalConfig(pomodoros):
	#podría cambiarse ya que está haciendo algo muy parecido a getLocalConfig pero sin retornar y recibiendo un parametro
	with open("pomodoro.config", 'w') as file:
		setInfoIntoFile(file, pomodoros)

def main():
	global POMODORO_WORKING_TIME, POMODORO_RESTING_TIME_LIGHT, POMODORO_RESTING_TIME_HARD
	#lleva la cuenta de cuantos pomodores se han realizado
	pomodoros = getLocalConfig()
	#si existe un archivo de configuración le pone los pomodrores que este tiene, si no le asigna cero

	while True:
		#obtiene un entero del menú
		option = menu(pomodoros)

		#Menú de opciones
		if option == 0:		#Salir
			print("Adiós :)")
			break

		elif option == 1:	#Inicia Ciclo pomodoro -> descanso
			#Iniciar pomodoro
			print("\n---Iniciando Pomodoro---")
			startPomodoro(POMODORO_WORKING_TIME)
			pomodoros +=1
			setLocalConfig(pomodoros)


			#Iniciar descanso
			print("\n---DESCANSO ", end="")
			if pomodoros == MAX_POMODOROS: #Descanso largo
				pomodoros = 0 	#Tiene que ir al inicio para evitar el bug de tener más pomodoros de los permitidos después de un descanso largo
				setLocalConfig(pomodoros)# Se guarda inmediatamente después
				print("LARGO---")
				startPomodoro(POMODORO_RESTING_TIME_HARD)
				
			else:						#Descanso corto
				print("CORTO---")
				startPomodoro(POMODORO_RESTING_TIME_LIGHT)

		elif option == 2:	#Cambiar cantidad de pomodoros
			print("\n---Cambiar número de pomodores actuales---")
			pomodoros = changePomodoros()
			setLocalConfig(pomodoros)

		elif option == 3: 	#Cambiar tiempos del pomodoro
			"""
			ToDo
			Refactorizar código para sacar el menu de los tiempos a otra función
			"""
			while True: 
				#Menú de los tiempos que se pueden cambiar
				print("\n---Cambiar Tiempos---")
				print("¿Qué tiempo quieres cambiar?")
				print("( 1 ) Trabajando = %s"%secondsToMinutes(POMODORO_WORKING_TIME))
				print("( 2 ) Descanso corto = %s"%secondsToMinutes(POMODORO_RESTING_TIME_LIGHT))
				print("( 3 ) Descanso largo = %s"%secondsToMinutes(POMODORO_RESTING_TIME_HARD))
				print("( 0 ) Regresar")
				option_change_time = input()

				#Validando respuesta
				if option_change_time.isdigit():
					option_change_time = int(option_change_time)

					#Decidiendo ue hacer con la respuesta
					if option_change_time == 0:		#Regresar
						break
					elif option_change_time == 1:	#Cambiar Tiempo Trabajo
						POMODORO_WORKING_TIME = changeTime()
						setLocalConfig(pomodoros)
					elif option_change_time == 2: 	#Cambiar Tiempo Descanso Corto
						POMODORO_RESTING_TIME_LIGHT = changeTime()
						setLocalConfig(pomodoros)
					elif option_change_time == 3:	#Cambiar Tiempo Descanso Largo
						POMODORO_RESTING_TIME_HARD = changeTime()
						setLocalConfig(pomodoros)
					else:
						print("Opción aún no disponible, intente otra")
				else:
					print("Opción no valida, vuelva a intentarlo")
				
		else: print("Esa opción no está listada, intente seleccionando otra")

if __name__ == "__main__":
	main() 