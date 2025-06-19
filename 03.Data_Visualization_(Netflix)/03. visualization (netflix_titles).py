import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
from sklearn.linear_model import LinearRegression

# 1. Cargar datos
netflix = pd.read_csv('C:/Users/ASUS/Downloads/netflix_titles.csv/netflix_titles.csv')

# 2. Limpieza mínima
print(netflix.info())
print(netflix.isnull().sum())

# Eliminamos columnas irrelevantes para visualizaciones cuantitativas
netflix = netflix.drop(columns=['show_id', 'description'])

# Convertir 'date_added' a datetime
netflix['date_added'] = pd.to_datetime(netflix['date_added'], format='mixed', errors='coerce')

# Crear columna 'year_added'
netflix['year_added'] = netflix['date_added'].dt.year

# Filtrar solo películas
movies = netflix[netflix['type'] == 'Movie'].copy()

# 3. Visualizaciones

# Películas agregadas por año
plt.figure(figsize=(10, 5))
movies['year_added'].value_counts().sort_index().plot(kind='bar')
plt.title("Películas agregadas por año")
plt.xlabel("Año")
plt.ylabel("Cantidad de películas")
plt.tight_layout()
plt.show()

# Películas por clasificación
plt.figure(figsize=(10, 4))
sns.countplot(data=movies, x='rating', order=movies['rating'].value_counts().index)
plt.title("Películas por clasificación")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. ANOVA: Duración promedio por clasificación
movies['duration_minutes'] = movies['duration'].str.extract('(\d+)').astype(float)
rating_groups = [group['duration_minutes'].dropna() for name, group in movies.groupby('rating') if group['duration_minutes'].notnull().any()]
f_stat, p_val = f_oneway(*rating_groups)
print(f"ANOVA: F = {f_stat:.2f}, p = {p_val:.4f}")

# Boxplot
plt.figure(figsize=(10, 5))
sns.boxplot(data=movies, x='rating', y='duration_minutes')
plt.title("Duración por clasificación")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Regresión: Año vs Duración
reg_df = movies[['year_added', 'duration_minutes']].dropna()
X = reg_df[['year_added']]
y = reg_df['duration_minutes']

# Regresión lineal simple
modelo = LinearRegression()
modelo.fit(X, y)

print(f"Intercepto: {modelo.intercept_:.2f}")
print(f"Coeficiente: {modelo.coef_[0]:.2f}")

# Visualización de la regresión
plt.figure(figsize=(10, 5))
sns.scatterplot(x='year_added', y='duration_minutes', data=reg_df, alpha=0.3)
plt.plot(reg_df['year_added'], modelo.predict(X), color='red')
plt.title("Regresión: Año de adición vs Duración")
plt.tight_layout()
plt.show()

# Este dataset ya está listo para exportar a Power BI
movies.to_csv("netflix_movies_cleaned.csv", index=False)
