import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/ASUS/OneDrive/Documents/estrategias de marketing.csv', parse_dates=['Fecha'])

df['CTR'] = df['Clics'] / df['Impresiones']             # Tasa de clics
df['CPC'] = df['Costo'] / df['Clics']                   # Costo por clic
df['Tasa_conversion'] = df['Conversiones'] / df['Clics']  # Tasa de conversión

resumen_canal = df.groupby('Canal')[['CTR', 'CPC', 'Tasa_conversion']].mean().round(4)
print(resumen_canal)

df['Semana'] = df['Fecha'].dt.isocalendar().week

semanal = df.groupby(['Semana', 'Canal'])[['Impresiones', 'Clics', 'Costo', 'Conversiones']].sum().reset_index()

# Calcular métricas semanales
semanal['CTR'] = semanal['Clics'] / semanal['Impresiones']
semanal['CPC'] = semanal['Costo'] / semanal['Clics']
semanal['Tasa_conversion'] = semanal['Conversiones'] / semanal['Clics']

# CTR semanal
plt.figure(figsize=(10, 6))
sns.lineplot(data=semanal, x='Semana', y='CTR', hue='Canal', marker='o')
plt.title('CTR semanal por canal')
plt.xlabel('Semana')
plt.ylabel('CTR (Click-through rate)')
plt.grid()
plt.show()

# CPC semanal
plt.figure(figsize=(10, 6))
sns.lineplot(data=semanal, x='Semana', y='CPC', hue='Canal', marker='o')
plt.title('CPC semanal por canal')
plt.xlabel('Semana')
plt.ylabel('CPC (Costo por clic)')
plt.grid()
plt.show()

# Tasa de conversión semanal
plt.figure(figsize=(10, 6))
sns.lineplot(data=semanal, x='Semana', y='Tasa_conversion', hue='Canal', marker='o')
plt.title('Tasa de conversión semanal por canal')
plt.xlabel('Semana')
plt.ylabel('Tasa de conversión')
plt.grid()
plt.show()

