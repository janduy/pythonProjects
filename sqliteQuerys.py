import sqlite3
from dataBaseName import dataBaseName
from terminalClear import terminalClear
import datetime

conn = sqlite3.connect(dataBaseName())
cursor = conn.cursor()
time = datetime.datetime.now()



#-------------------------------------------------------------------------------
# Cria uma data no formato Y-m-d
#-------------------------------------------------------------------------------
def myDateFormat():
    return str(time.year) + "-" + str(time.month) + "-" + str(time.day)
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Salva os registros na tabela Produção
#-------------------------------------------------------------------------------
def signalSave(lineProduction):

    hora = str(time.hour)

    cursor.execute("""
    INSERT INTO producao (quantidade, linha_producao, hora, created_at)
    VALUES (?,?,?,?)
    """, (1, lineProduction, hora, myDateFormat()))

    conn.commit()
    #conn.close()

#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Edita o campo Quantidade da tabela Produçao sempre incrementando 1
#-------------------------------------------------------------------------------
def signalUpdate():
    
    quantidade = getSignalFromHourAndDate() + 1

    hora = str(time.hour)

    cursor.execute("""
    UPDATE producao SET quantidade = ? WHERE hora = ? AND enviado IS NULL
    """, (quantidade,hora,))

    conn.commit()
    #conn.close()
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Retorna O valor do campo Quantidade buscando pelo campo Hora atual e Data atual da tabela Produção
# Return : O valor do campo Quantidade
#-------------------------------------------------------------------------------
def getSignalFromHourAndDate():
    
    hora = str(time.hour)

    cursor.execute("""SELECT quantidade FROM producao WHERE hora = ? AND created_at = ?""", (hora, myDateFormat(),))

    quantidade = 0

    for row in cursor.fetchall():
        quantidade = row[0]

    if (quantidade > 0):
        return quantidade
    else:
        return False
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Verifica se existe algum registro por Hora atual e Data atual da tabela Produção
# Return : True ou False
#-------------------------------------------------------------------------------
def existSignalFromHour():
    
    hora = str(time.hour)
    cursor.execute("""SELECT quantidade FROM producao WHERE hora = ? AND created_at = ?""", (hora, myDateFormat(),))

    quantidade = 0

    for row in cursor.fetchall():
        quantidade = row[0]

    if quantidade > 0:
        return True

    return False
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Cadastra a Linha de Produção
#-------------------------------------------------------------------------------
def saveLineProduction(lineProduction):

    cursor.execute("""
    INSERT INTO linhaProducao (linha_producao, created_at)
    VALUES (?,?)
    """, (lineProduction, myDateFormat()))

    conn.commit()
    conn.close()
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Seleciona a Linha de Produção cadastrada
# Return : O valor do campo linha_produção da tabela Produção
#-------------------------------------------------------------------------------
def selectLineProduction():

    cursor.execute("""SELECT * FROM linhaProducao LIMIT 1""")

    lineProduction = ""

    for row in cursor.fetchall():
        lineProduction = row[1]

    return lineProduction
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Seleciona todos os registros que ainda não foram exportados
# Return : Tupla com todos os registro
#-------------------------------------------------------------------------------
def selectAllSignals():

    cursor.execute("""SELECT * FROM producao WHERE enviado is null""")
    return cursor.fetchall()
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Seta os registros que já foram exportados
#-------------------------------------------------------------------------------
def setSignalsExportedBYid(id):
    
    cursor.execute("""
    UPDATE producao SET enviado = ? WHERE id = ?
    """, ("true", id,))

    conn.commit()
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Apresenta todos os Registros cadastrados na tabela Produção
#-------------------------------------------------------------------------------
def showMeTheProducaoTable():

    cursor.execute("""SELECT * FROM producao ORDER BY created_at ASC, hora DESC""")
    
    terminalClear()

    print("-------------------------------------------------------------------------------------")
    print("REGISTROS CADASTRADOS NA TABELA PRODUCAO")
    print("-------------------------------------------------------------------------------------")

    for row in cursor.fetchall():
        quantidade = "0" + str(row[1]) if row[1] < 10 else str(row[1])

        print("id: " + str(row[0]) + " | quantidade: " + quantidade + " | linha producao: " + str(row[2]) + " | hora: " + str(row[3]) + " | data: " + str(row[4]) + " | enviado: " + str(row[5]))
#-------------------------------------------------------------------------------