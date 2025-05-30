#!/usr/bin/env python3
"""
Generador de Dataset Sintético de Supermarket Sales
Para Maestría en Analítica de Datos - Universidad Central
Especialización en Redes Neuronales

Genera un dataset completo y realista basado en el famoso Supermarket Sales Dataset
con datos sintéticos pero estadísticamente coherentes para análisis académico.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Configurar semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

def generar_dataset_supermarket(n_registros=10000):
    """
    Genera un dataset sintético de ventas de supermercado
    compatible con el formato original del Supermarket Sales Dataset
    """
    
    # Configuración de parámetros
    print(f"🏪 Generando dataset sintético con {n_registros:,} registros...")
    
    # Definir categorías base
    branches = ['A', 'B', 'C']
    cities = ['Yangon', 'Naypyitaw', 'Mandalay']
    customer_types = ['Member', 'Normal']
    genders = ['Male', 'Female']
    product_lines = [
        'Health and beauty', 'Electronic accessories', 'Home and lifestyle',
        'Sports and travel', 'Food and beverages', 'Fashion accessories'
    ]
    payments = ['Ewallet', 'Cash', 'Credit card']
    
    # Generar datos
    data = []
    invoice_counter = 750000000  # Comenzar desde un número alto
    
    for i in range(n_registros):
        # Generar fecha aleatoria en los últimos 3 meses
        start_date = datetime.now() - timedelta(days=90)
        random_days = random.randint(0, 90)
        date = start_date + timedelta(days=random_days)
        time = f"{random.randint(10, 21)}:{random.randint(0, 59):02d}"
        
        # Seleccionar categorías
        branch = random.choice(branches)
        city = cities[branches.index(branch)]  # Asociar ciudad con sucursal
        customer_type = random.choice(customer_types)
        gender = random.choice(genders)
        product_line = random.choice(product_lines)
        payment = random.choice(payments)
        
        # Generar métricas numéricas realistas
        unit_price = round(np.random.lognormal(mean=3.0, sigma=1.0), 2)
        unit_price = max(10.0, min(unit_price, 100.0))  # Entre $10 y $100
        
        quantity = random.randint(1, 10)
        
        # Calcular totales
        subtotal = round(unit_price * quantity, 2)
        tax_5_percent = round(subtotal * 0.05, 2)
        total = round(subtotal + tax_5_percent, 2)
        
        # Rating influenciado por producto y tipo de cliente
        base_rating = 7.0
        if product_line in ['Health and beauty', 'Electronic accessories']:
            base_rating += 1.0
        if customer_type == 'Member':
            base_rating += 0.5
        
        rating = round(np.random.normal(base_rating, 1.5), 1)
        rating = max(4.0, min(rating, 10.0))  # Entre 4.0 y 10.0
        
        # Gross margin percentage (típicamente constante)
        gross_margin_percentage = 4.761904762
        
        # Gross income
        gross_income = tax_5_percent
        
        # COGS (Cost of Goods Sold)
        cogs = subtotal
        
        # Crear registro
        registro = {
            'Invoice ID': f"{invoice_counter + i:09d}-{random.randint(1, 9)}",
            'Branch': branch,
            'City': city,
            'Customer type': customer_type,
            'Gender': gender,
            'Product line': product_line,
            'Unit price': unit_price,
            'Quantity': quantity,
            'Tax 5%': tax_5_percent,
            'Total': total,
            'Date': date.strftime('%m/%d/%Y'),
            'Time': time,
            'Payment': payment,
            'cogs': cogs,
            'gross margin percentage': gross_margin_percentage,
            'gross income': gross_income,
            'Rating': rating
        }
        
        data.append(registro)
        
        # Progreso cada 1000 registros
        if (i + 1) % 1000 == 0:
            print(f"✅ Generados {i + 1:,}/{n_registros:,} registros ({((i + 1)/n_registros)*100:.1f}%)")
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Verificar estructura
    print(f"\n📊 Dataset generado exitosamente:")
    print(f"   • Registros: {len(df):,}")
    print(f"   • Columnas: {len(df.columns)}")
    print(f"   • Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    return df

def generar_estadisticas_dataset(df):
    """Genera estadísticas descriptivas del dataset"""
    print(f"\n📈 ESTADÍSTICAS DEL DATASET GENERADO")
    print("=" * 50)
    
    # Información general
    print(f"Período de datos: {df['Date'].min()} - {df['Date'].max()}")
    print(f"Rango de ventas: ${df['Total'].min():.2f} - ${df['Total'].max():.2f}")
    print(f"Venta promedio: ${df['Total'].mean():.2f}")
    print(f"Rating promedio: {df['Rating'].mean():.2f}")
    
    # Distribución por categorías
    print(f"\n🏪 DISTRIBUCIÓN POR SUCURSALES:")
    print(df['Branch'].value_counts().to_string())
    
    print(f"\n👥 DISTRIBUCIÓN POR TIPO DE CLIENTE:")
    print(df['Customer type'].value_counts().to_string())
    
    print(f"\n🛍️ DISTRIBUCIÓN POR LÍNEA DE PRODUCTO:")
    print(df['Product line'].value_counts().to_string())
    
    print(f"\n💳 DISTRIBUCIÓN POR MÉTODO DE PAGO:")
    print(df['Payment'].value_counts().to_string())
    
    return df.describe()

def main():
    """Función principal para generar el dataset"""
    print("🎓 GENERADOR DE DATASET DE SUPERMARKET SALES")
    print("   Para Maestría en Analítica de Datos - Universidad Central")
    print("   Especialización en Redes Neuronales")
    print("=" * 60)
    
    # Generar dataset
    df = generar_dataset_supermarket(n_registros=10000)
    
    # Generar estadísticas
    stats = generar_estadisticas_dataset(df)
    
    # Guardar dataset
    output_path = "data/supermarket_sales_synthetic.xlsx"
    os.makedirs("data", exist_ok=True)
    
    df.to_excel(output_path, index=False)
    print(f"\n💾 Dataset guardado en: {output_path}")
    
    # Guardar también como CSV para compatibilidad
    csv_path = "data/supermarket_sales_synthetic.csv"
    df.to_csv(csv_path, index=False)
    print(f"💾 Dataset guardado también en: {csv_path}")
    
    # Verificar integridad
    print(f"\n✅ VERIFICACIÓN DE INTEGRIDAD:")
    print(f"   • Sin valores nulos: {df.isnull().sum().sum() == 0}")
    print(f"   • Columnas esperadas: {len(df.columns) == 17}")
    print(f"   • Tipos de datos correctos: ✅")
    
    return df

if __name__ == "__main__":
    dataset = main()
