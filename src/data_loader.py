"""Módulo para la carga de datos.

Este módulo proporciona funciones para cargar datos de diversas fuentes,
principalmente archivos Excel, para ser utilizados en la aplicación.
"""
# Este módulo está alineado y documentado según la arquitectura conceptual.

import pandas as pd
import streamlit as st
from typing import Optional

def cargar_datos(ruta: Optional[str] = None) -> Optional[pd.DataFrame]:
    """Carga datos desde un archivo Excel.

    Si se proporciona una ruta válida, lee el archivo Excel y devuelve un DataFrame.
    Si la ruta es None o el archivo no se puede cargar, devuelve None.

    Args:
        ruta (Optional[str]): La ruta al archivo Excel. Por defecto es None.

    Returns:
        Optional[pd.DataFrame]: Un DataFrame de Pandas con los datos cargados,
                                 o None si la carga falla o la ruta es None.
    """
    if ruta:
        try:
            return pd.read_excel(ruta)
        except FileNotFoundError:
            # Consider logging this error if a logging system is in place
            # st.error(f"Error: Archivo no encontrado en la ruta: {ruta}") # Avoid streamlit in non-UI modules
            return None
        except Exception as e:
            # Consider logging this error
            # st.error(f"Error al cargar el archivo: {e}")
            return None
    return None
