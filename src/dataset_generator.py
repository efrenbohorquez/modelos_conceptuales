"""
🎓 GENERADOR DE DATASET INTEGRADO PARA MAESTRÍA EN ANALÍTICA DE DATOS
Universidad Central - Modelos Conceptuales de Redes Neuronales
Especialización: Supermarket Sales Analytics

Este módulo genera un dataset sintético pero realista de ventas de supermercado
específicamente diseñado para demostrar los conceptos de redes neuronales
en el contexto académico de maestría.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

class SupermarketDatasetGenerator:
    """Generador de datos sintéticos de supermercado para análisis académico"""
    
    def __init__(self):
        # Configuración de productos realistas
        self.product_lines = [
            "Health and beauty", "Electronic accessories", "Home and lifestyle",
            "Sports and travel", "Food and beverages", "Fashion accessories"
        ]
        
        # Ciudades principales para el análisis
        self.cities = ["Yangon", "Naypyitaw", "Mandalay"]
        self.branches = ["A", "B", "C"]
        
        # Tipos de cliente
        self.customer_types = ["Member", "Normal"]
        self.genders = ["Male", "Female"]
        
        # Métodos de pago
        self.payment_methods = ["Cash", "Credit card", "Ewallet"]
        
        # Configuración de precios por categoría (USD)
        self.price_ranges = {
            "Health and beauty": (10, 100),
            "Electronic accessories": (15, 200),
            "Home and lifestyle": (20, 150),
            "Sports and travel": (25, 180),
            "Food and beverages": (5, 50),
            "Fashion accessories": (8, 120)
        }
    
    def generate_synthetic_dataset(self, n_records=5000, output_dir="data/datasets/raw"):
        """
        Genera un dataset sintético de ventas de supermercado
        
        Args:
            n_records (int): Número de registros a generar
            output_dir (str): Directorio de salida
            
        Returns:
            pandas.DataFrame: Dataset generado
        """
        print(f"🎓 Generando dataset sintético de {n_records} registros...")
        
        # Inicializar datos
        data = []
        start_date = datetime(2023, 1, 1)
        
        # Generar cada registro
        for i in range(n_records):
            # Seleccionar categoría y configurar precios
            product_line = random.choice(self.product_lines)
            price_min, price_max = self.price_ranges[product_line]
            
            # Variables principales
            record = {
                'Invoice ID': f"750-67-{random.randint(1000, 9999)}",
                'Branch': random.choice(self.branches),
                'City': random.choice(self.cities),
                'Customer type': random.choice(self.customer_types),
                'Gender': random.choice(self.genders),
                'Product line': product_line,
                'Unit price': round(random.uniform(price_min, price_max), 2),
                'Quantity': random.randint(1, 10),
                'Date': (start_date + timedelta(days=random.randint(0, 365))).strftime('%m/%d/%Y'),
                'Time': f"{random.randint(10, 21):02d}:{random.randint(0, 59):02d}",
                'Payment': random.choice(self.payment_methods)
            }
            
            # Calcular variables derivadas
            record['Tax 5%'] = round(record['Unit price'] * record['Quantity'] * 0.05, 4)
            record['Total'] = round(record['Unit price'] * record['Quantity'] + record['Tax 5%'], 4)
            record['cogs'] = round(record['Unit price'] * record['Quantity'], 4)
            record['gross margin percentage'] = 4.761904762  # Promedio realista
            record['gross income'] = record['Tax 5%']
            
            # Rating influenciado por factores realistas
            rating_base = 7.0
            
            # Factores que influyen en rating
            if record['Customer type'] == 'Member':
                rating_base += 0.5
            if record['Payment'] == 'Ewallet':
                rating_base += 0.3
            if record['Total'] > 200:
                rating_base += 0.4
            if record['Product line'] in ['Health and beauty', 'Electronic accessories']:
                rating_base += 0.2
                
            # Añadir ruido realista
            rating_noise = random.uniform(-1.5, 1.5)
            record['Rating'] = max(4.0, min(10.0, round(rating_base + rating_noise, 1)))
            
            data.append(record)
        
        # Crear DataFrame
        df = pd.DataFrame(data)
        
        # Asegurar orden de columnas consistente
        column_order = [
            'Invoice ID', 'Branch', 'City', 'Customer type', 'Gender', 
            'Product line', 'Unit price', 'Quantity', 'Tax 5%', 'Total', 
            'Date', 'Time', 'Payment', 'cogs', 'gross margin percentage', 
            'gross income', 'Rating'
        ]
        df = df[column_order]
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Guardar dataset
        csv_path = os.path.join(output_dir, "supermarket_sales_synthetic.csv")
        xlsx_path = os.path.join(output_dir, "supermarket_sales_synthetic.xlsx")
        
        df.to_csv(csv_path, index=False)
        df.to_excel(xlsx_path, index=False)
        
        print(f"✅ Dataset guardado en:")
        print(f"   📄 CSV: {csv_path}")
        print(f"   📊 Excel: {xlsx_path}")
        
        return df
    
    def generate_statistics_report(self, df):
        """
        Genera un reporte estadístico del dataset
        
        Args:
            df (pandas.DataFrame): Dataset a analizar
            
        Returns:
            dict: Estadísticas del dataset
        """
        stats = {
            'total_records': len(df),
            'total_revenue': df['Total'].sum(),
            'avg_transaction': df['Total'].mean(),
            'product_distribution': df['Product line'].value_counts().to_dict(),
            'customer_distribution': df['Customer type'].value_counts().to_dict(),
            'branch_distribution': df['Branch'].value_counts().to_dict(),
            'payment_distribution': df['Payment'].value_counts().to_dict(),
            'rating_stats': {
                'mean': df['Rating'].mean(),
                'std': df['Rating'].std(),
                'min': df['Rating'].min(),
                'max': df['Rating'].max()
            }
        }
        
        return stats
    
    def create_documentation(self, stats, output_dir="data/datasets/raw"):
        """
        Crea documentación del dataset generado
        
        Args:
            stats (dict): Estadísticas del dataset
            output_dir (str): Directorio de salida
        """
        doc_content = f"""# DOCUMENTACIÓN DEL DATASET SINTÉTICO
## Supermarket Sales - Proyecto de Maestría

### 📊 RESUMEN GENERAL
- **Total de registros:** {stats['total_records']:,}
- **Ingresos totales:** ${stats['total_revenue']:,.2f}
- **Transacción promedio:** ${stats['avg_transaction']:.2f}

### 🛍️ DISTRIBUCIÓN POR LÍNEA DE PRODUCTO
"""
        for product, count in stats['product_distribution'].items():
            percentage = (count / stats['total_records']) * 100
            doc_content += f"- **{product}:** {count} ({percentage:.1f}%)\n"

        doc_content += f"""
### 👥 DISTRIBUCIÓN POR TIPO DE CLIENTE
"""
        for customer_type, count in stats['customer_distribution'].items():
            percentage = (count / stats['total_records']) * 100
            doc_content += f"- **{customer_type}:** {count} ({percentage:.1f}%)\n"

        doc_content += f"""
### 🏪 DISTRIBUCIÓN POR SUCURSAL
"""
        for branch, count in stats['branch_distribution'].items():
            percentage = (count / stats['total_records']) * 100
            doc_content += f"- **Sucursal {branch}:** {count} ({percentage:.1f}%)\n"

        doc_content += f"""
### 💳 MÉTODOS DE PAGO
"""
        for payment, count in stats['payment_distribution'].items():
            percentage = (count / stats['total_records']) * 100
            doc_content += f"- **{payment}:** {count} ({percentage:.1f}%)\n"

        doc_content += f"""
### ⭐ ESTADÍSTICAS DE RATING
- **Promedio:** {stats['rating_stats']['mean']:.2f}
- **Desviación estándar:** {stats['rating_stats']['std']:.2f}
- **Rango:** {stats['rating_stats']['min']:.1f} - {stats['rating_stats']['max']:.1f}

### 🎯 USO ACADÉMICO
Este dataset ha sido diseñado específicamente para demostrar:
1. **Regresión con MLPRegressor:** Predicción de Rating
2. **Segmentación con PCA + KMeans:** Clustering de clientes
3. **Clasificación con MLPClassifier:** Predicción de Product line
4. **Detección de anomalías:** Identification de transacciones atípicas

### 📚 VARIABLES DISPONIBLES
- **Invoice ID:** Identificador único de factura
- **Branch:** Sucursal (A, B, C)
- **City:** Ciudad (Yangon, Naypyitaw, Mandalay)
- **Customer type:** Tipo de cliente (Member, Normal)
- **Gender:** Género (Male, Female)
- **Product line:** Línea de producto (6 categorías)
- **Unit price:** Precio unitario en USD
- **Quantity:** Cantidad vendida
- **Tax 5%:** Impuesto del 5%
- **Total:** Total de la transacción
- **Date:** Fecha de la transacción
- **Time:** Hora de la transacción
- **Payment:** Método de pago (Cash, Credit card, Ewallet)
- **cogs:** Costo de bienes vendidos
- **gross margin percentage:** Porcentaje de margen bruto
- **gross income:** Ingreso bruto
- **Rating:** Calificación del cliente (4.0 - 10.0)

---
**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Universidad Central - Maestría en Analítica de Datos**
"""
        
        doc_path = os.path.join(output_dir, "DATASET_DOCUMENTATION.md")
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"📚 Documentación guardada en: {doc_path}")

def main():
    """Función principal para generar el dataset completo"""
    print("🎓 GENERADOR DE DATASET INTEGRADO")
    print("   Universidad Central - Maestría en Analítica de Datos")
    print("   Modelos Conceptuales de Redes Neuronales")
    print("=" * 60)
    
    # Inicializar generador
    generator = SupermarketDatasetGenerator()
    
    # Generar dataset principal (5000 registros para análisis robusto)
    df = generator.generate_synthetic_dataset(n_records=5000)
    
    # Generar estadísticas
    stats = generator.generate_statistics_report(df)
    
    # Crear documentación
    generator.create_documentation(stats)
    
    # Crear también una versión pequeña para pruebas rápidas
    df_small = generator.generate_synthetic_dataset(
        n_records=100, 
        output_dir="data/datasets/processed"
    )
    
    print("\n🎉 GENERACIÓN COMPLETADA")
    print(f"📊 Dataset principal: 5,000 registros")
    print(f"🧪 Dataset de prueba: 100 registros")
    print(f"📚 Documentación incluida")
    print("\n🚀 El dataset está listo para los análisis de maestría!")

if __name__ == "__main__":
    main()
