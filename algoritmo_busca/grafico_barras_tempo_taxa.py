import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

objects = ['Retorna 1', 'Soma de níveis', 'Nível máximo', 'Fast Forward']
y_pos = np.arange(len(objects))

# Consumo de tempo
performance = [14744, 9512, 166223, 35740]

plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Tempo (ms)')
plt.title('Consumo médio de tempo de cada heurística para o problema Tyre World')

plt.show()

# Taxa de ramificaçao
performance = [4.51, 6.95, 5.22, 4.61]

plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('nós')
plt.title('Taxa de ramificaçao média de cada heurística para o problema Tyre World')

plt.show()