# Este módulo está alineado y documentado según la arquitectura conceptual ubicada en:
# C:\Users\efren\Downloads\supermarket_nn_models_entrega\home\ubuntu\supermarket_nn_models\docs\modelos_conceptuales.md

import pandas as pd
import streamlit as st
from typing import Optional

def cargar_datos(ruta: Optional[str] = None):
    if ruta:
        return pd.read_excel(ruta)
    return None
