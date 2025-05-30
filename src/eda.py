# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configurar estilo de visualización
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def analisis_descriptivo(df: pd.DataFrame):
    """
    Análisis exploratorio de datos modernizado con visualizaciones interactivas
    y análisis específicos para datos de supermercado
    """
    
    # Información general del dataset
    st.markdown("### 📊 Resumen General del Dataset")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filas", f"{df.shape[0]:,}")
    with col2:
        st.metric("Columnas", df.shape[1])
    with col3:
        st.metric("Variables Numéricas", len(df.select_dtypes(include=['number']).columns))
    with col4:
        st.metric("Variables Categóricas", len(df.select_dtypes(include=['object']).columns))
    
    # Vista previa de los datos con mejor formato
    st.markdown("### 👀 Vista Previa de los Datos")
    with st.expander("Mostrar datos de muestra", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)
      # Análisis de calidad de datos
    st.markdown("### 🔍 Calidad de los Datos")
    calidad_datos(df)
    
    # Análisis de variables numéricas mejorado
    st.markdown("### 📈 Análisis de Variables Numéricas")
    st.markdown("**🎯 Esta sección incluye Unit price, Quantity, Tax 5%, Total y más variables numéricas**")
    analisis_variables_numericas(df)
    
    # Análisis de variables categóricas mejorado
    st.markdown("### 📊 Análisis de Variables Categóricas")
    analisis_variables_categoricas(df)
    
    # Análisis de correlaciones interactivo
    st.markdown("### 🔗 Análisis de Correlaciones")
    analisis_correlaciones(df)
    
    # Análisis específico para supermercado
    st.markdown("### 🛒 Análisis Específico de Supermercado")
    analisis_supermercado(df)

def calidad_datos(df):
    """Análisis de calidad de datos con visualizaciones"""
    
    # Valores nulos
    nulos = df.isnull().sum()
    if nulos.sum() > 0:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Valores Nulos por Columna:**")
            nulos_df = nulos[nulos > 0].reset_index()
            nulos_df.columns = ['Columna', 'Valores Nulos']
            nulos_df['Porcentaje'] = (nulos_df['Valores Nulos'] / len(df) * 100).round(2)
            st.dataframe(nulos_df, use_container_width=True)
        
        with col2:
            if len(nulos_df) > 0:
                fig = px.bar(nulos_df, x='Columna', y='Porcentaje', 
                           title='Porcentaje de Valores Nulos',
                           color='Porcentaje', color_continuous_scale='Reds')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No se encontraron valores nulos en el dataset")
    
    # Duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        st.warning(f"⚠️ Se encontraron {duplicados} filas duplicadas ({duplicados/len(df)*100:.2f}%)")
    else:
        st.success("✅ No se encontraron filas duplicadas")

def analisis_variables_numericas(df):
    """Análisis modernizado de variables numéricas"""
    
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    # Mensaje destacado
    st.markdown("---")
    st.markdown("### 🔢 **SECCIÓN DE VARIABLES NUMÉRICAS**")
    st.markdown("**✨ Aquí puedes analizar Unit price, Quantity, Tax 5%, Total, etc.**")
      # Agregar información de depuración
    st.write(f"🔍 **Debug:** Detectadas {len(num_cols)} variables numéricas")
    if len(num_cols) > 0:
        st.write(f"📊 **Variables numéricas:** {', '.join(num_cols)}")
    
    if len(num_cols) == 0:
        st.info("No se encontraron variables numéricas en el dataset")
        return
    
    # Selector de variables para análisis detallado
    st.markdown("#### 🔢 Selección de Variables para Análisis Detallado")
    
    # Mensaje informativo para evitar confusión
    st.info("💡 **Instrucciones:** Selecciona las variables que deseas analizar. Los cambios se aplicarán automáticamente sin reiniciar la página.")
    
    selected_vars = st.multiselect(
        "Selecciona variables numéricas para análisis detallado:",
        num_cols,
        default=num_cols[:min(4, len(num_cols))],
        help="Estas son las variables que incluyen Unit price, Quantity, Tax 5%, Total, etc.",
        key="eda_numeric_vars_selector"
    )
    
    if selected_vars:
        # Estadísticas descriptivas
        with st.expander("📋 Estadísticas Descriptivas", expanded=False):
            st.dataframe(df[selected_vars].describe().round(3), use_container_width=True)
        
        # Distribuciones con plotly
        st.markdown("**Distribuciones de Variables:**")
        
        # Crear subplots para histogramas
        n_vars = len(selected_vars)
        n_cols = min(2, n_vars)
        n_rows = (n_vars + n_cols - 1) // n_cols
        
        for i, var in enumerate(selected_vars):
            if i % 2 == 0:
                col1, col2 = st.columns(2)
            
            with col1 if i % 2 == 0 else col2:
                # Histograma interactivo
                fig = px.histogram(df, x=var, marginal="box", 
                                 title=f'Distribución de {var}',
                                 nbins=30, opacity=0.7)
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Boxplots comparativos
        if len(selected_vars) > 1:
            st.markdown("**Comparación de Distribuciones (Boxplots):**")
            
            # Normalizar datos para comparación
            df_norm = df[selected_vars].copy()
            for col in selected_vars:
                df_norm[col] = (df_norm[col] - df_norm[col].mean()) / df_norm[col].std()
            
            fig = go.Figure()
            for var in selected_vars:
                fig.add_trace(go.Box(y=df_norm[var], name=var, boxpoints='outliers'))
            
            fig.update_layout(
                title="Comparación de Distribuciones (Datos Normalizados)",
                yaxis_title="Valores Normalizados",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

def analisis_variables_categoricas(df):
    """Análisis modernizado de variables categóricas"""
    
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(cat_cols) == 0:
        st.info("No se encontraron variables categóricas en el dataset")
        return
    
    # Selector de variables categóricas
    selected_cats = st.multiselect(
        "Selecciona variables categóricas para análisis:",
        cat_cols,
        default=cat_cols[:min(3, len(cat_cols))],
        key="eda_categorical_vars_selector"
    )
    
    if selected_cats:
        for var in selected_cats:
            with st.expander(f"📊 Análisis de {var}", expanded=False):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Tabla de frecuencias
                    freq_table = df[var].value_counts().reset_index()
                    freq_table.columns = ['Categoría', 'Frecuencia']
                    freq_table['Porcentaje'] = (freq_table['Frecuencia'] / len(df) * 100).round(2)
                    st.dataframe(freq_table, use_container_width=True)
                
                with col2:
                    # Gráfico de barras interactivo
                    if len(freq_table) <= 15:  # Para evitar gráficos muy cargados
                        fig = px.bar(freq_table, x='Categoría', y='Frecuencia',
                                   title=f'Distribución de {var}',
                                   color='Frecuencia', color_continuous_scale='viridis')
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Para variables con muchas categorías, mostrar solo las top 15
                        top_15 = freq_table.head(15)
                        fig = px.bar(top_15, x='Categoría', y='Frecuencia',
                                   title=f'Top 15 categorías de {var}',
                                   color='Frecuencia', color_continuous_scale='viridis')
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                        st.info(f"Mostrando solo las 15 categorías más frecuentes de {len(freq_table)} total")

def analisis_correlaciones(df):
    """Análisis de correlaciones interactivo"""
    
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(num_cols) < 2:
        st.info("Se necesitan al menos 2 variables numéricas para calcular correlaciones")
        return
    
    # Calcular matriz de correlación
    corr_matrix = df[num_cols].corr()
    
    # Mapa de calor interactivo
    fig = px.imshow(corr_matrix, 
                    text_auto=True, 
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    title="Matriz de Correlación",
                    labels=dict(color="Correlación"))
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlaciones más fuertes
    st.markdown("**Correlaciones más Fuertes:**")
    
    # Obtener correlaciones sin la diagonal
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            var1 = corr_matrix.columns[i]
            var2 = corr_matrix.columns[j]
            corr_val = corr_matrix.iloc[i, j]
            corr_pairs.append({'Variable 1': var1, 'Variable 2': var2, 'Correlación': corr_val})
    
    corr_df = pd.DataFrame(corr_pairs)
    corr_df['Correlación Abs'] = abs(corr_df['Correlación'])
    corr_df = corr_df.sort_values('Correlación Abs', ascending=False)
    
    # Mostrar top 10 correlaciones
    top_corr = corr_df.head(10)[['Variable 1', 'Variable 2', 'Correlación']]
    top_corr['Correlación'] = top_corr['Correlación'].round(3)
    st.dataframe(top_corr, use_container_width=True)

def analisis_supermercado(df):
    """Análisis específico para datos de supermercado"""
    
    # Verificar si tenemos las columnas típicas de supermercado
    supermarket_cols = {
        'ventas': ['Total', 'gross income', 'cogs'],
        'productos': ['Product line', 'Unit price', 'Quantity'],
        'clientes': ['Customer type', 'Gender', 'Rating'],
        'ubicacion': ['Branch', 'City'],
        'tiempo': ['Date', 'Time']
    }
    
    available_analyses = []
    
    # Análisis de ventas
    ventas_cols = [col for col in supermarket_cols['ventas'] if col in df.columns]
    if ventas_cols:
        available_analyses.append('Análisis de Ventas')
      # Análisis de productos
    if 'Product line' in df.columns:
        available_analyses.append('Análisis de Productos')
    
    # Análisis de clientes
    cliente_cols = [col for col in supermarket_cols['clientes'] if col in df.columns]
    if cliente_cols:
        available_analyses.append('Análisis de Clientes')
    
    if not available_analyses:
        st.info("No se detectaron columnas específicas de supermercado para análisis especializado")
        return
    
    selected_analysis = st.selectbox(
        "Selecciona un análisis específico:",
        available_analyses,
        key="eda_supermercado_analysis_selector"
    )
    
    if selected_analysis == 'Análisis de Ventas' and ventas_cols:
        analisis_ventas_supermercado(df, ventas_cols)
    elif selected_analysis == 'Análisis de Productos' and 'Product line' in df.columns:
        analisis_productos_supermercado(df)
    elif selected_analysis == 'Análisis de Clientes' and cliente_cols:
        analisis_clientes_supermercado(df, cliente_cols)

def analisis_ventas_supermercado(df, ventas_cols):
    """Análisis específico de ventas"""
    
    st.markdown("**📈 Métricas de Ventas:**")
    
    # Métricas principales
    if 'Total' in ventas_cols:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ventas = df['Total'].sum()
            st.metric("Ventas Totales", f"${total_ventas:,.2f}")
        
        with col2:
            venta_promedio = df['Total'].mean()
            st.metric("Venta Promedio", f"${venta_promedio:.2f}")
        
        with col3:
            ticket_max = df['Total'].max()
            st.metric("Ticket Máximo", f"${ticket_max:.2f}")
        
        with col4:
            ticket_min = df['Total'].min()
            st.metric("Ticket Mínimo", f"${ticket_min:.2f}")
    
    # Distribución de ventas
    if 'Total' in df.columns:
        fig = px.histogram(df, x='Total', nbins=50, 
                          title='Distribución de Ventas Totales',
                          marginal='box')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def analisis_productos_supermercado(df):
    """Análisis específico de productos"""
    
    st.markdown("**🛍️ Análisis de Líneas de Productos:**")
    
    # Ventas por línea de producto
    if 'Total' in df.columns:
        ventas_por_producto = df.groupby('Product line')['Total'].agg(['sum', 'mean', 'count']).reset_index()
        ventas_por_producto.columns = ['Línea de Producto', 'Ventas Totales', 'Venta Promedio', 'Cantidad Transacciones']
        
        # Gráfico de ventas por producto
        fig = px.bar(ventas_por_producto, x='Línea de Producto', y='Ventas Totales',
                    title='Ventas Totales por Línea de Producto',
                    color='Ventas Totales', color_continuous_scale='viridis')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla resumen
        st.dataframe(ventas_por_producto.round(2), use_container_width=True)

def analisis_clientes_supermercado(df, cliente_cols):
    """Análisis específico de clientes"""
    
    st.markdown("**👥 Análisis de Clientes:**")
    
    # Análisis por tipo de cliente
    if 'Customer type' in cliente_cols:
        col1, col2 = st.columns(2)
        
        with col1:
            customer_dist = df['Customer type'].value_counts()
            fig = px.pie(values=customer_dist.values, names=customer_dist.index,
                        title='Distribución por Tipo de Cliente')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Total' in df.columns:
                avg_by_customer = df.groupby('Customer type')['Total'].mean().reset_index()
                fig = px.bar(avg_by_customer, x='Customer type', y='Total',
                           title='Venta Promedio por Tipo de Cliente',
                           color='Total', color_continuous_scale='blues')
                st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de satisfacción (Rating)
    if 'Rating' in cliente_cols:
        st.markdown("**⭐ Análisis de Satisfacción (Rating):**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            rating_stats = df['Rating'].agg(['mean', 'std', 'min', 'max']).round(2)
            st.metric("Rating Promedio", f"{rating_stats['mean']:.2f} ⭐")
            st.write(f"**Desviación Estándar:** {rating_stats['std']:.2f}")
            st.write(f"**Rango:** {rating_stats['min']:.1f} - {rating_stats['max']:.1f}")
        
        with col2:
            fig = px.histogram(df, x='Rating', nbins=20,
                             title='Distribución de Ratings de Cliente',
                             marginal='box')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
