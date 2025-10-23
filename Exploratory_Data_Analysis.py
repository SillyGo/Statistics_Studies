'''
#MODA
import pandas as pd

def locate(lista1:list, value):
    for i in range(len(lista1)):
        if (lista1[i] == value): 
            return i
    return -1

def mode(lista:list):
    words = []
    count = []

    for i in range(len(lista)):
        index = locate(words, lista[i])
        if index == -1:
            words.append(lista[i])
            count.append(0)
        else:
            count[index] += 1
    
    max_element = max(count)
    index = locate(count, max_element)
    return words[index]

def least_recurring(lista:list):
    words = []
    count = []

    for i in range(len(lista)):
        index = locate(words, lista[i])
        if index == -1:
            words.append(lista[i])
            count.append(0)
        else:
            count[index] += 1
    
    min_element = min(count)
    index = locate(count, min_element)
    return words[index]

path = "infracoestransparencia-janeiro-a-maio-2025.csv"
crimes = pd.read_csv(path, sep=';')

infracao = crimes['infracao']
list_infr = list(infracao)

print(mode(list_infr))                  #criei uma função não muito robusta que calcula a moda
print(least_recurring(list_infr))       #criei uma função não muito robusta que calcula o elemento menos recorrente

#com os dados acima, podemos concluir que a (ou uma das) infrações mais comuns é a de número 7455. Ou seja, ->
#a de trafegar em velocidade superior a até 20% da máxima da via.
#Tiramos também que a infração mais "rara" é a de número 6327, que consiste em deixar de reduzir a velocidade -> 
#ao se aproximar de pontos onde trabalhadores estão na via.

'''

'''
#MEDIDAS DE POSIÇÃO

import pandas as pd
from scipy.stats import trim_mean

path = "infracoestransparencia-janeiro-a-maio-2025.csv"
crimes = pd.read_csv(path, sep=';')

#print(crimes.columns) #verifica oque podemos estudar

horainfracao = crimes['horainfracao']

def hora_fracao(hora:str):
    inteiro, fracionario = int(hora.split(':')[0]), int(hora.split(':')[1])
    return inteiro + fracionario/60

horas_fracionarias = []
for i in range(len(horainfracao)):
    horas_fracionarias.append(hora_fracao(str(horainfracao[i])))

print("pre-processamento concluído!")

horas_fracionarias = pd.Series(horas_fracionarias)
#print(horas_fracionarias.mean())                       #media normal
#print(horas_fracionarias.median())                     #mediana normal (também poderia computar a mediana ponderada, mas não sei oque eu colocaria como os pesos)
#print(pd.DataFrame(horas_fracionarias).mode())         #moda 

print(trim_mean(horas_fracionarias, 0.1))               #trimmed mean. Aqui, não temos muita importância, mas poderiamos aplicar em cenários com outliers muito consideráveis e indesejáveis.
'''

'''
#MEDIDAS DE DISPERSÃO
import pandas as pd

path = "infracoestransparencia-janeiro-a-maio-2025.csv"
crimes = pd.read_csv(path, sep=';')

print(crimes.columns)

#aqui, acho relevante usarmos como exemplo os horários de acontecimento das irregularidades de trânsito,  ->
#isso pode nos informar, por exemplo, se essas infrações se concentram em horários de pico, ou se ocorrem ->
#na surdina da noite, quando não tem ninguem para fazer a verificação.

horainfracao = crimes['horainfracao']

def hora_fracao(hora:str):
    inteiro, fracionario = int(hora.split(':')[0]), int(hora.split(':')[1])
    return inteiro + fracionario/60

horas_fracionarias = []
for i in range(len(horainfracao)):
    horas_fracionarias.append(hora_fracao(str(horainfracao[i])))

print("pre-processamento concluído!")
horas_fracionarias = pd.Series(horas_fracionarias)

print(horas_fracionarias.var()) #variância ? 
print(horas_fracionarias.std()) #standart deviation / desvio padrão

#PS. desvio padrão é sensível a outliers. Para resolver isso, podemos usar MAD, ou median absolute deviation ->
#MAD calcula a mediana dos valores absolutos dos desvios da mediana para cada um dos valores. Criarei uma    ->
#função que computa a MAD abaixo:

def MAD(lista:pd.Series):
    #objetivos: 1. encontrar a mediana:
    mediana = lista.median()
    devs = []
    for i in range(len(lista)):
        devs.append(abs(mediana - lista[i]))
    devs = pd.Series(devs)
    return devs.median()

print(MAD(horas_fracionarias))

#MAD pode ser mais robusta que o desvio padrão que, novamente, é sensível a outliers.
#veremos agora como usar "quantiles" (nn sei a tradução para português)

#IQR = horas_fracionarias.quantile(0.75) - horas_fracionarias.quantile(0.25) #limites do boxplot :D
#print(IQR)

upper_quartile = str( int(horas_fracionarias.quantile(0.9))) + ':' + str(round(60*(horas_fracionarias.quantile(0.9) - int(horas_fracionarias.quantile(0.9)))))
lower_quartile = str( int(horas_fracionarias.quantile(0.1))) + ':' + str(round(60*(horas_fracionarias.quantile(0.1) - int(horas_fracionarias.quantile(0.1)))))

print(lower_quartile)       #experimentei com intervalo de quantis maiores, 80% dos dados estão entre 7:50 e 19:08, que coincidem com os horários "gerais" das pessoas saindo e voltando do trabalho
print(upper_quartile)       #20% dos dados estão antes das 7 horas e 50, e depois das 19:08, conforme esperado
'''

'''
#EXPLORANDO DISTRIBUIÇÃO DOS DADOS:

import pandas as pd
import matplotlib.pyplot as plt

path = "infracoestransparencia-janeiro-a-maio-2025.csv"
crimes = pd.read_csv(path, sep=';')

def hora_fracao(hora:str):
    inteiro, fracionario = int(hora.split(':')[0]), int(hora.split(':')[1])
    return inteiro + fracionario/60

horainfracao = crimes['horainfracao']

horas_fracionarias = []
for i in range(len(horainfracao)):
    horas_fracionarias.append(hora_fracao(str(horainfracao[i])))

print("pre-processamento concluído!")
horas_fracionarias = pd.Series(horas_fracionarias)

#-------#

#ax = horas_fracionarias.plot.box()  #criando um boxplot usando pandas
#ax.set_ylabel("horas do dia") 
#plt.show()                          #ainda precisamos dar plt.show() com matplotlib

#-------#

#bin_horas = pd.cut(horas_fracionarias, 24)
#bin_horas.value_counts()

#-------#

#ax = horas_fracionarias.plot.hist(figsize=(10,10), bins=24) #criação de histograma
#ax.set_xlabel("horas do dia")
#plt.show()

#vemos que os dados seguem o padrão esperado, com alguns poucos picos que eu não sei explicar o motivo, ->
#como um pico de infrações que existe às 21h; talvez as pessoas aproveitem que teria menos regulamentação
#além disso, criamos 24 bins porque existem 24 horas em um dia.

#-------#

#ax = horas_fracionarias.plot.hist(density=True, xlim=[0,24], bins=range(1,24))
#horas_fracionarias.plot.density(ax=ax)
#ax.set_xlabel('infrações')

#plt.show()

#aqui fizemos o mesmo que fizemos antes (plot de histograma) mas também plotando a densidade de dados.

#-------#

'''
'''
#EXPLORANDO DADOS BINÁRIOS E CATEGÓRICOS:

#aqui, eu queria tentar usar os crimes / rua. Para isso, terei que fazer algumas modificações à estrutura do bagui

import pandas as pd

path = "infracoestransparencia-janeiro-a-maio-2025.csv"
crimes = pd.read_csv(path, sep=';')

local = crimes['localcometimento']

#precisamos reorganizar em uma relação entre "rua" e "número"

def locate(lista1:list, value):
    for i in range(len(lista1)):
        if (lista1[i] == value): 
            return i
    return -1

def Words_And_Count(lista:list):
    words = []
    count = []

    for i in range(len(lista)):
        index = locate(words, lista[i])
        if index == -1:
            words.append(lista[i])
            count.append(0)
        else:
            count[index] += 1

        if (i % 10000) == 0:
            print(f'{int(100*(i/len(lista)))}%')
    
    return words, count

#AQUI, O PROCESSAMENTO É MUITO LENTO, ENTÃO OPTEI POR SALVAR OS DADOS PROCESSADOS EM UM .CSV E FICAR USANDO ELE

#words, count = Words_And_Count(list(local))
#print(len(words))
#print(len(count))

#data = {"rua": words, "freq": count}

#df = pd.DataFrame(data)

#df.to_csv('freq_de_rua.csv', index=False)

df = pd.read_csv('freq_de_rua.csv')
print(len(df))

#low_bound = df['freq'].quantile(0.1)
#upp_bound = df['freq'].quantile(0.9)
#upp_bound = df['freq'][len(df['freq']) - 1]

#df = df[df['freq'].between(low_bound, upp_bound)]

#print(len(df))

df = df.sort_values(by='freq')

df['freq'] = df['freq']/1500

n = 0.5
print(df['freq'].quantile(n))

df = df[(df['freq'] >= df['freq'].quantile(n))]

#print(len(df))

#print(df['rua'])

#ax = df.plot.bar(figsize=(10,10), legend=False)
#ax.set_xlabel("nome da rua")
#ax.set_ylabel("frequencia")

#import matplotlib.pyplot as plt
#plt.show()

#aqui claramente falta processamento dos dados. A rua com mais infrações era para ser alguma como a agamenon ->
#magalhães, mas acabou sendo a rua arquiteto luiz nunes. Minha hipótese é que os dados estão divididos entre ->
#trechos das ruas, de tal modo que, se eu fosse capaz de somar o total de ocorrências para quando aparece    ->
#uma rua grande, eu provavelmente seria capaz de identificar a rua que, verdadeiramente, possui mais         ->
#infrações. Mas algo interessante é que, considerando-se apenas trechos de rua, poderíamos ainda dizer que   ->
#a rua arquiteto luiz nunes possui o maior número de infrações, considerando-se entre n.315 e 379

ax = df.plot.scatter(x='rua', y='freq', figsize=(8, 8), marker='$\u25EF$')
#ax.set_xlabel('rua')
ax.set_ylabel('freq')
ax.axhline(0, color='grey', lw=1)
ax.axvline(0, color='grey', lw=1)

import matplotlib.pyplot as plt
plt.show()

#péssimo exemplo, mas por enquanto estou só querendo entender como usar scatterplots.
#para correlação, usamos dados numéricos, aqui estou usando dados categóricos (facepalm)
'''