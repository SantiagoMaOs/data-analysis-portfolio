# Importamos las librerias necesarias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Cargamos los datos desde el archivo .csv
superstore = pd.read_csv("C:/Users/ASUS/OneDrive/Documents/Sample_Superstore.csv", encoding='latin1')

# Verificamos algunos aspectos basicos del dataset
print(superstore.shape)
print(superstore.info())
print(superstore.head())

# Revisamos si hay duplicados
superstore.drop_duplicates(inplace=True)

# Revisamos los valores nulos y los eliminamos
print("Valores nulos:")
print(superstore.isnull().sum())

superstore.dropna(subset=['Sales', 'Profit', 'Order Date'], inplace=True)

# Revisamos los ingresos y las ganancias totales
total_sales = superstore['Sales'].sum()
total_profit = superstore['Profit'].sum()
print(f"Ingresos Totales: ${total_sales:,.2f}")
print(f"Ganancia Total: ${total_profit:,.2f}")

# Ahora agrupamos las ventas y las ganancias por region, y categoria
region_sales = superstore.groupby('Region')[['Sales', 'Profit']].sum().sort_values('Sales', ascending=False)
print(region_sales)

category_sales = superstore.groupby(['Category', 'Sub-Category'])[['Sales', 'Profit']].sum().sort_values('Sales', ascending=False)
print(category_sales)

# Observamos que Order Date esta en formato Object por lo tanto lo pasamos a formato datetime
superstore['Order Date'] = pd.to_datetime(superstore['Order Date'])

monthly_sales = superstore.resample('ME', on='Order Date')['Sales'].sum()
print(monthly_sales)


# Ventas por región
sns.barplot(data=region_sales.reset_index(), x='Region', y='Sales')
plt.title('Ventas Totales por Región')
plt.ylabel('Sales ($)')
plt.show()

# Evolución mensual
monthly_sales.plot(figsize=(10, 4), title='Ventas mensuales')
plt.ylabel('Sales ($)')
plt.xlabel('Fecha')
plt.grid(True)
plt.show()

print('-------------------------------------------------------------------------------')

print('Cuales son los producto que mas y los que menos ventas producen?')
ventas_por_producto = superstore.groupby('Product Name')['Sales'].sum().reset_index()
top_3_productos = ventas_por_producto.nlargest(3, 'Sales')
print('los 3 producto que mas ventas producen son: ', top_3_productos)

bottom_3_productos = ventas_por_producto.nsmallest(3, 'Sales')
print('Los 3 productos que menos ventas producen son: ', bottom_3_productos)

print('Cuales son los producto que mas y los que menos ganancias producen?')
ventas_por_producto = superstore.groupby('Product Name')['Profit'].sum().reset_index()
top_3_productos = ventas_por_producto.nlargest(3, 'Profit')
print('los 3 producto que mas ganancias producen son: ', top_3_productos)

bottom_3_productos = ventas_por_producto.nsmallest(3, 'Profit')
print('los 3 producto que menos ganancias producen son: ', bottom_3_productos)
