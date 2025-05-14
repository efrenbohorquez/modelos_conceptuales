import pandas as pd
import streamlit as st
from typing import Optional

def cargar_datos(ruta: Optional[str] = None):
    if ruta:
        return pd.read_excel(ruta)
    return None
