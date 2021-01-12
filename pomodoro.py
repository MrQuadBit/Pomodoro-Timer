import time
import playsound #pip || pip3 install playsound

M = 60 #Hay 60 segundos en un minuto
POMODORO_WORKING_TIME = M*.1 #25 minutos
POMODORO_RESTING_TIME_LIGHT = M*.1 #3 minutos
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
	#auristica para saber los segundos restantes(segundos_totales - segundos_en_minutos)
	return "%d:%d"%(minutes//M, minutes-((minutes//M)*M)) 

def changePomodoros():
	while True:
		new_pomodoros = input("¿Cuántos pomodoros llevas?:\n")
		#Verificar que es un número valido de pomodoros <4 & >0
		if (new_pomodoros.isdigit() and int(new_pomodoros) < MAX_POMODOROS) or (new_pomodoros.isdigit() and int(new_pomodoros) < 0):
			return int(new_pomodoros)
		print("Cantidad no valida, el número de pomodoros debe de ser menor a %d y mayor a %d"%(MAX_POMODOROS, 0))

def changeTime():
	while True:
		try:
			new_time = float(input("¿Cuantos minutos quieres asignar?\n"))
			if new_time > 0:
				return new_time*M
		except:
			pass
		print("Ingrese un valor numerico valido mayor a 0")

def main():
	global POMODORO_WORKING_TIME, POMODORO_RESTING_TIME_LIGHT, POMODORO_RESTING_TIME_HARD
	#lleva la cuenta de cuantos pomodores se han realizado
	pomodoros = 0

	while True:
		#otiene un entero del menú
		option = menu(pomodoros)

		if option == 0:		#Salir
			print("Adiós :)")
			break

		elif option == 1:	#Inicia Ciclo pomodoro -> descanso
			#Iniciar pomodoro
			print("\n---Iniciando Pomodoro---")
			startPomodoro(POMODORO_WORKING_TIME)
			pomodoros +=1

			#Iniciar descanso
			print("\n---DESCANSO ", end="")
			if pomodoros == MAX_POMODOROS: #Descanso largo
				print("LARGO---")
				startPomodoro(POMODORO_RESTING_TIME_HARD)
				pomodoros = 0
			else:						#Descanso corto
				print("CORTO---")
				startPomodoro(POMODORO_RESTING_TIME_LIGHT)

		elif option == 2:	#Cambiar cantidad de pomodoros
			print("\n---Cambiar número de pomodores actuales---")
			pomodoros = changePomodoros()

		elif option == 3: 	#Cambiar tiempos del pomodoro
			"""
			ToDo
			Refactorizar código para sacar el menu de tiempos a otra función
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
					if option_change_time == 0:		#Regresar
						break
					elif option_change_time == 1:	#Tiempo Trabajo
						POMODORO_WORKING_TIME = changeTime()
					elif option_change_time == 2: 	#Tiempo Descanso Corto
						POMODORO_RESTING_TIME_LIGHT = changeTime()
					elif option_change_time == 3:	#Tiempo Descanso Largo
						POMODORO_RESTING_TIME_HARD = changeTime()
					else:
						print("Opción aún no disponible, intente otra")
				else:
					print("Opción no valida, vuelva a intentarlo")
				
		else: print("Esa opción no está listada, intente seleccionando otra")

if __name__ == "__main__":
	main() 