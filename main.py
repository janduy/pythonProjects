import sqlite3
from dataBaseName import dataBaseName
from sqliteQuerys import signalSave
from sqliteQuerys import selectLineProduction
from sqliteQuerys import existSignalFromHour
from sqliteQuerys import signalUpdate
from sqliteQuerys import showMeTheProducaoTable
from sqliteQuerys import existLineProduction
from sqliteQuerys import incrementContadorIntable1
from sqliteQuerys import existDataInTable1
from sqliteQuerys import countToday
from terminalClear import terminalClear
import datetime
import time

import RPi.GPIO as GPIO 

PIN =23 

# Configura o modo de definicao de pinos como BOARD
GPIO.setmode(GPIO.BCM)

# Destiva avisos
GPIO.setwarnings(False) 

# Resistencia interna no input
#GPIO.setup(PIN,GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 

#modificacao 6 nov
GPIO.setup(PIN, GPIO.IN)

# Cadastrando evento de borda de descida
#GPIO.add_event_detect(PIN, GPIO.FALLING, bouncetime = 200)



#-------------------------------------------------------------------------------
# Verifica se existe algum registro na Tabela Linha de Produção
#-------------------------------------------------------------------------------
if existLineProduction() == False:
	terminalClear()
	print("Voce esqueceu de Cadastrar uma Linha de Producao. \n Digite: python lineProduction.py para criar!")
	exit()
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Verifica se existe algum registro por hora atual e data atual
#-------------------------------------------------------------------------------
while (1):

	#if GPIO.event_detected(PIN):
	if (GPIO.input(PIN)==GPIO.HIGH):

		if (existSignalFromHour() != True):

			try:

				signalSave(selectLineProduction()[0], selectLineProduction()[1])
				print("Novo registro realizado com Sucesso.")

				showMeTheProducaoTable()

			except Exception as e:
				print("Erro ao tentar Cadastrar um novo Registro: ", e)

            		# Verifica se existe registros na tabela 1
			if existDataInTable1():

				try:
					incrementContadorIntable1(str(countToday()), selectLineProduction()[1])
				except Exception as e:
					print("Erro ao tentar Incrementar o Contador na tabela1", e)

			else:
				print("Nao existe registros na tabela 1. O campo contador nao pode ser Incrementado")

		else:

			try:

				signalUpdate()
				print("Novo incremento realizado com Sucesso.")
				
				showMeTheProducaoTable()

			except Exception as e:
				print("Erro ao tentar Incrementar um Registro: ", e)


            		# Verifica se existe registros na tabela 1
			if existDataInTable1():

				try:
					incrementContadorIntable1(str(countToday()), selectLineProduction()[1])
				except Exception as e:
					print("Erro ao tentar Incrementar o Contador na tabela1", e)

			else:
				print("Nao existe registros na tabela 1. O campo contador nao pode ser Incrementado")
	time.sleep(.2)
#-------------------------------------------------------------------------------
