<<<<<<< HEAD
# 📝 Documentación Técnica: Motores de Optimización y Persistencia (Sandbox)

Este apartado detalla la arquitectura lógica y matemática desarrollada en el cuaderno de experimentación (`notebooks/sandbox_opt.ipynb`) para dar cumplimiento a los requerimientos analíticos del proyecto.

---

### 📊 Fase 1: Estructuración y Definición de Datos Crudos (Pandas & NumPy)
* **Título de la Celda:** Carga de Datos de Entrada y Disponibilidad de Inventario
* **Descripción:** Se inicializan las matrices de información técnica utilizando estructuras nativas de Python que posteriormente son convertidas a DataFrames mediante `pandas`. Aquí se definen los insumos biológicos del medio de cultivo, sus costos comerciales (valores de la función objetivo) y las capacidades límite de almacenamiento en bodega.

---

### 🧮 Fase 2: Optimización Lineal Continua (SciPy)
* **Título de la Celda:** Modelamiento de Recetas Económicas de Medio de Cultivo
* **Descripción:** Implementación del primer núcleo analítico a través de `scipy.optimize.linprog`. El algoritmo modela un problema de mezcla clásico en ingeniería. Establece una función de minimización de costos operando sobre restricciones de frontera (límites de stock) y restricciones técnicas de desigualdad, donde los requisitos mínimos nutricionales de Carbono y Nitrógeno son transformados matemáticamente multiplicando por $-1$ para cumplir con el estándar algebraico de la librería ($A_{ub} \cdot x \le b_{ub}$).

---

### ⏱️ Fase 3: Optimización Entera Mixta y Scheduling (PuLP)
* **Título de la Celda:** Programación y Secuenciación de Operaciones del Biorreactor
* **Descripción:** Aplicación de un modelo de Programación Lineal Entera Mixta (MILP) utilizando la librería `pulp`. Modela la programación temporal de una cola de producción compuesta por 3 lotes independientes en una sola unidad de proceso batch. El algoritmo minimiza la variable de tiempo final (*Makespan*) calculando los tiempos de inicio óptimos (variables continuas) y gobernando el ordenamiento temporal mediante variables binarias de precedencia acopladas a la restricción lógica **Big-M** para asegurar que no ocurran colisiones de horario en el reactor.

---

### 💾 Fase 4: Persistencia de Datos y Modelo Relacional (SQLite)
* **Título de la Celda:** Almacenamiento y Auditoría del Cronograma Óptimo en SQL
* **Descripción:** Integración de persistencia relacional al ciclo de vida del modelo de datos por medio de `sqlite3`. El código utiliza comandos estructurados de SQL para inicializar una base de datos local (`data/planta_piloto.db`), limpiar el entorno y guardar masivamente la secuencia calculada por el optimizador. Termina ejecutando una consulta de auditoría con ordenamiento secuencial (`SELECT ... ORDER BY`) para certificar la integridad y disponibilidad de los datos guardados.
=======
# biooptima-scheduling
Sistema inteligente de optimización de recetas y secuenciación de operaciones (Scheduling) para plantas de fermentación industrial utilizando Python.
>>>>>>> 9d9a2079a42000489991508d0b55f7e5a841630e
