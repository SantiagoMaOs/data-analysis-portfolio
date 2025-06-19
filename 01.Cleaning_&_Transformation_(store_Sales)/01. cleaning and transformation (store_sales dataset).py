import pandas as pd
import numpy as np

# Cargar los datos
store_sales = pd.read_csv('C:/Users/ASUS/OneDrive/Documents/retail_store_sales.csv')

# Información general
print(store_sales.shape)
print(store_sales.info())
print(store_sales.head())

# Eliminar duplicados
store_sales.drop_duplicates(inplace=True)

# Ver valores nulos
print('VALORES NULOS POR COLUMNA')
print(store_sales.isnull().sum())

# Rellenar valores nulos en columnas numéricas
store_sales.fillna({'Quantity': 0, 'Total Spent': 0}, inplace=True)

# Eliminar filas sin nombre de producto
store_sales = store_sales[store_sales['Item'].notna()]

# Imputar precio por unidad con la mediana por producto
store_sales['Price Per Unit'] = store_sales.groupby('Item')['Price Per Unit'].transform(
    lambda x: x.fillna(x.median())
)

# Función para verificar si se aplicó descuento
def check_discount(row):
    if pd.isnull(row['Quantity']) or pd.isnull(row['Price Per Unit']) or pd.isnull(row['Total Spent']):
        return 'Unknown'
    
    expected_total = row['Quantity'] * row['Price Per Unit']
    
    if np.isclose(expected_total, row['Total Spent']):
        return 'FALSE'  # No hubo descuento
    else:
        return 'TRUE'  # Sí hubo descuento

# Aplicar la función
store_sales['Discount Applied'] = store_sales.apply(check_discount, axis=1)

# Detección de outliers en Total Spent
Q1 = store_sales['Total Spent'].quantile(0.25)
Q3 = store_sales['Total Spent'].quantile(0.75)
IQR = Q3 - Q1

outliers = store_sales[
    (store_sales['Total Spent'] < Q1 - 1.5 * IQR) |
    (store_sales['Total Spent'] > Q3 + 1.5 * IQR)
]

print(f"Número de outliers: {len(outliers)}")

# Guardar dataset limpio
store_sales.to_csv("customer_transactions_cleaned.csv", index=False)


