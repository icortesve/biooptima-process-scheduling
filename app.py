import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import linprog
import pulp
import sqlite3
import os

# Configuración principal de la página del Dashboard
st.set_page_config(page_title="BioOptima - Control de Planta", page_icon="🧪", layout="wide")

st.title("🧪 BioOptima: Sistema Inteligente de Optimización y Scheduling")
st.markdown("---")

# Estructurar la aplicación en dos pestañas interactivas
tab1, tab2 = st.tabs(["📋 Optimización de Receta (SciPy)", "⏱️ Programación de Operaciones (PuLP)"])

# ==========================================
# PESTAÑA 1: OPTIMIZACIÓN DE RECETA (SciPy)
# ==========================================
with tab1:
    st.header("Optimización Económica de Medios de Cultivo")
    st.write("Ajusta los parámetros para calcular la mezcla de costo mínimo cumpliendo las restricciones nutricionales.")
    
    # Controles interactivos en la barra lateral o columnas
    col1, col2 = st.columns(2)
    with col1:
        peso_total = st.slider("Masa total del lote a preparar (kg)", 50, 500, 150, step=50)
        min_carbono_pct = st.slider("Requisito mínimo de Carbono (%)", 10, 50, 35)
    with col2:
        min_nitrogeno_pct = st.slider("Requisito mínimo de Nitrógeno (%)", 10, 50, 20)

    # Datos base dinámicos
    c = [1.5, 4.8, 6.2, 2.5] # Costos de: Glucosa, Extracto, Peptona, Sales
    
    # Calcular restricciones en base a los sliders
    req_carbono = peso_total * (min_carbono_pct / 100.0)
    req_nitrogeno = peso_total * (min_nitrogeno_pct / 100.0)
    
    # Matrices SciPy
    A_ub = [[-1, 0, 0, 0], [0, -1, -1, 0]]
    b_ub = [-req_carbono, -req_nitrogeno]
    A_eq = [[1, 1, 1, 1]]
    b_eq = [peso_total]
    limites = [(0, 300), (0, 80), (0, 50), (0, 150)]
    
    if st.button("Calcular Receta Óptima"):
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=limites, method='highs')
        
        if res.success:
            st.success(f"¡Optimización Exitosa! Costo mínimo del lote: ${res.fun:.2f} USD")
            
            # Mostrar resultados en una tabla limpia de Pandas
            res_df = pd.DataFrame({
                "Componente": ["Glucosa", "Extracto de Levadura", "Peptona de Carne", "Sales Fosfato"],
                "Cantidad (kg)": [round(x, 2) for x in res.x],
                "Costo Parcial (USD)": [round(x * costo, 2) for x, costo in zip(res.x, c)]
            })
            st.dataframe(res_df, use_container_width=True)
        else:
            st.error("No se encontró una solución viable con las restricciones seleccionadas. Intenta bajando los porcentajes nutricionales.")

# ==========================================
# PESTAÑA 2: SCHEDULING DE OPERACIONES (PuLP)
# ==========================================
with tab2:
    st.header("Secuenciación (Scheduling) del Biorreactor")
    st.write("Modifica los tiempos de proceso de cada lote para calcular la secuencia óptima libre de traslapes.")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        t_a = st.number_input("Horas Lote A", min_value=1, max_value=24, value=4)
    with col_b:
        t_b = st.number_input("Horas Lote B", min_value=1, max_value=24, value=6)
    with col_c:
        t_c = st.number_input("Horas Lote C", min_value=1, max_value=24, value=3)
        
    lotes = ["Lote_A", "Lote_B", "Lote_C"]
    tiempo_proceso = {"Lote_A": t_a, "Lote_B": t_b, "Lote_C": t_c}
    
    if st.button("Optimizar Cronograma Planta"):
        # Motor PuLP
        prob = pulp.LpProblem("Scheduling_Streamlit", pulp.LpMinimize)
        t_start = pulp.LpVariable.dicts("Inicio", lotes, lowBound=0, cat='Continuous')
        C_max = pulp.LpVariable("Tiempo_Total", lowBound=0, cat='Continuous')
        
        pares = [(i, j) for i in lotes for j in lotes if i != j]
        y = pulp.LpVariable.dicts("Precedencia", pares, cat='Binary')
        
        prob += C_max
        for i in lotes:
            prob += C_max >= t_start[i] + tiempo_proceso[i]
            
        M = 100
        for (i, j) in pares:
            if i < j:
                prob += t_start[j] >= t_start[i] + tiempo_proceso[i] - M * (1 - y[(i, j)])
                prob += t_start[i] >= t_start[j] + tiempo_proceso[j] - M * y[(i, j)]
                
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        # Guardar resultados en SQLite y mostrarlos
        st.info(f"Tiempo total mínimo de ocupación: {pulp.value(C_max)} horas")
        
        cronograma_list = []
        for i in lotes:
            inicio = pulp.value(t_start[i])
            fin = inicio + tiempo_proceso[i]
            cronograma_list.append((i, inicio, fin, tiempo_proceso[i]))
            
        # Ordenar por tiempo de inicio para la visualización
        cronograma_list.sort(key=lambda x: x[1])
        
        # --- BLOQUE SQLITE (Persistencia) ---
        db_path = os.path.join("data", "planta_piloto.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cronograma_biorreactor (
            id INTEGER PRIMARY KEY AUTOINCREMENT, lote_nombre TEXT, hora_inicio REAL, hora_fin REAL, duracion_horas INTEGER
        )
        """)
        cursor.execute("DELETE FROM cronograma_biorreactor")
        cursor.executemany("""
        INSERT INTO cronograma_biorreactor (lote_nombre, hora_inicio, hora_fin, duracion_horas) VALUES (?, ?, ?, ?)
        """, cronograma_list)
        conn.commit()
        conn.close()
        
        # Mostrar en interfaz
        st.success("¡Resultados guardados con éxito en la base de datos SQL (`planta_piloto.db`)!")
        
        df_cronograma = pd.DataFrame(cronograma_list, columns=["Lote", "Hora Inicio", "Hora Término", "Duración (h)"])
        st.table(df_cronograma)