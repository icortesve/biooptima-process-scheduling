# 🧬 BioOptima Process Scheduling: Industrial Bioreactor Optimization

Sistema inteligente de optimización de recetas de medios de cultivo y secuenciación de operaciones (*scheduling*) para plantas de fermentación industrial en Python.

---

## 📝 Documentación Técnica: Motores de Optimización y Persistencia

Este apartado detalla la arquitectura lógica y matemática desarrollada en el entorno de experimentación (`notebooks/sandbox_opt.ipynb`) para dar cumplimiento a los requerimientos analíticos del proyecto.

### 📊 Fase 1: Estructuración y Definición de Datos Crudos (Pandas & NumPy)
* **Título de la Celda:** Carga de Datos de Entrada y Disponibilidad de Inventario
* **Descripción:** Se inicializan las matrices de información técnica utilizando estructuras nativas de Python que posteriormente son convertidas a DataFrames mediante `pandas`. Se definen los insumos biológicos del medio de cultivo, sus costos comerciales (función objetivo) y las capacidades límite de almacenamiento en bodega.

### 🧮 Fase 2: Optimización Lineal Continua (SciPy)
* **Título de la Celda:** Modelamiento de Recetas Económicas de Medio de Cultivo
* **Descripción:** Implementación del primer núcleo analítico a través de `scipy.optimize.linprog`. El algoritmo modela un problema de mezcla clásico en ingeniería para la minimización de costos operando sobre restricciones de frontera (límites de stock) y restricciones nutricionales de desigualdad (Carbono y Nitrógeno) transformadas al estándar algebraico ($A_{ub} \cdot x \le b_{ub}$).

### ⏱️ Fase 3: Optimización Entera Mixta y Scheduling (PuLP)
* **Título de la Celda:** Programación y Secuenciación de Operaciones del Biorreactor
* **Descripción:** Aplicación de un modelo de Programación Lineal Entera Mixta (MILP) mediante `pulp`. Modela la programación temporal de una cola de producción de 3 lotes independientes en una sola unidad batch. Minimiza el tiempo final (*Makespan*) calculando los tiempos de inicio óptimos y gobernando el ordenamiento temporal mediante variables binarias de precedencia acopladas a la restricción lógica **Big-M** para evitar colisiones de horario.

### 💾 Fase 4: Persistencia de Datos y Modelo Relacional (SQLite)
* **Título de la Celda:** Almacenamiento y Auditoría del Cronograma Óptimo en SQL
* **Descripción:** Integración de persistencia relacional por medio de `sqlite3`. El código utiliza SQL para inicializar una base de datos local (`data/planta_piloto.db`), limpiar el entorno y almacenar la secuencia calculada por el optimizador, finalizando con una consulta de auditoría con ordenamiento secuencial (`SELECT ... ORDER BY`) para certificar la integridad del resultado.

---

## ⚙️ Instalación y Ejecución

```bash
# Activar entorno virtual e instalar dependencias
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt