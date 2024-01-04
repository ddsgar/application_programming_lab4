import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('games.csv')
print(df.head())

df['victory_status'].value_counts().plot(kind='bar', color='blue', edgecolor='black', width=0.8)
plt.xlabel('Статус победы')
plt.ylabel('Количество игр')
plt.title('Распределение статуса победы')
plt.show()

#Гипотеза: корреляция между цветом фигур и победой практически отсутствует
df['winner'].value_counts().plot(kind='bar', color='salmon', edgecolor='black', width=0.8)
plt.xlabel('Победитель')
plt.ylabel('Количество игр')
plt.title('Распределение победителей')
plt.show()


