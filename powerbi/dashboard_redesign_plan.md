# Rediseño del Dashboard Clínico

## Objetivo
Reconstruir el dashboard desde cero para que deje de verse como una demo de clasificación y pase a comunicar seguimiento clínico, carga operativa y lectura de riesgo sobre pacientes evaluados.

## Idea central
La historia del dashboard debe responder tres preguntas:

1. Cuántos pacientes y evaluaciones estamos gestionando.
2. Cómo se está comportando el riesgo clínico en el tiempo.
3. Qué variables y perfiles diferencian mejor casos benignos y malignos.

## Layout recomendado

### Columna izquierda fija
Usar una franja vertical para filtros y KPI principales.

#### Filtros
- Año
- Mes
- Clasificación predicha
- Rango etario
- Paciente

#### KPI
- Pacientes únicos
- Evaluaciones totales
- Casos malignos
- Tasa de malignidad
- Score promedio de riesgo
- Pacientes con seguimiento múltiple

## Zona principal

### Bloque 1: Panorama clínico
Objetivo: entender volumen y comportamiento general.

- Línea o área:
  - `Evaluaciones por mes`
- Línea secundaria o combo:
  - `% de casos malignos por mes`
- Barras horizontales:
  - `Pacientes con más evaluaciones`

### Bloque 2: Distribución clínica
Objetivo: comparar el perfil de los casos.

- Donut:
  - `Distribución benigno vs maligno`
- Histograma:
  - `Distribución de edad por clasificación`

### Bloque 3: Lectura de variables clínicas
Objetivo: mostrar diferencias entre grupos con sentido analítico.

- Boxplot:
  - `radius_mean por clasificación`
- Boxplot:
  - `texture_mean por clasificación`
- Boxplot:
  - `area_mean por clasificación`
- Boxplot:
  - `smoothness_mean por clasificación`

Nota:
Si el dashboard queda muy cargado, usar solo dos boxplots por página y agregar un selector de variable clínica.

### Bloque 4: Seguimiento de pacientes
Objetivo: que el dashboard se vea realmente clínico y no solo analítico.

- Tabla:
  - Paciente
  - Fecha última evaluación
  - Total evaluaciones
  - Última clasificación
  - Último score
- Gráfico de líneas por paciente seleccionado:
  - `Evolución del prediction_score`
- Timeline simple:
  - `Controles del paciente en el tiempo`

## Página recomendada

### Página 1: Resumen ejecutivo
- KPI a la izquierda
- Evaluaciones por mes
- Tasa de malignidad
- Distribución benigno vs maligno
- Top pacientes con seguimiento

### Página 2: Perfil clínico
- Edad por clasificación
- Boxplots de variables clave
- Scatter opcional solo si aporta

### Página 3: Seguimiento individual
- Tabla de pacientes
- Selector de paciente
- Evolución temporal del score
- Últimos controles y clase predicha

## Visuales a eliminar o replantear

### Sacar
- Visual de influencias tipo "qué hace subir predicted_class"
Motivo:
Se siente más de explicación de modelo que de dashboard clínico operativo.

### Revisar
- Scatter `radius_mean vs texture_mean`
Motivo:
Puede verse bonito, pero aporta poco si no responde una pregunta clínica concreta.

## Medidas sugeridas en Power BI

### Conteos base
```DAX
Pacientes Unicos = DISTINCTCOUNT(clinical_measurements[patient_id])

Evaluaciones Totales = COUNTROWS(clinical_measurements)

Casos Malignos =
CALCULATE(
    COUNTROWS(clinical_measurements),
    clinical_measurements[predicted_class] = "Malignant"
)
```

### Tasas
```DAX
Tasa Malignidad =
DIVIDE([Casos Malignos], [Evaluaciones Totales], 0)
```

### Riesgo promedio
```DAX
Score Promedio =
AVERAGE(clinical_measurements[prediction_score])
```

### Seguimiento múltiple
```DAX
Pacientes con Seguimiento Multiple =
COUNTROWS(
    FILTER(
        VALUES(clinical_measurements[patient_id]),
        CALCULATE(COUNTROWS(clinical_measurements)) > 1
    )
)
```

## Columnas calculadas útiles

### Año
```DAX
Año = YEAR(clinical_measurements[evaluation_date])
```

### Mes-Año
```DAX
MesAño = FORMAT(clinical_measurements[evaluation_date], "MMM yyyy")
```

### Grupo etario
```DAX
Grupo Etario =
SWITCH(
    TRUE(),
    clinical_measurements[age] < 30, "Menor de 30",
    clinical_measurements[age] < 40, "30-39",
    clinical_measurements[age] < 50, "40-49",
    clinical_measurements[age] < 60, "50-59",
    clinical_measurements[age] < 70, "60-69",
    "70+"
)
```

## Paleta recomendada
- Rosa fuerte: KPI, títulos, elementos activos
- Rosa suave: benignos
- Rosa más oscuro / frambuesa: malignos
- Fondo claro: blanco rosado o crema muy suave
- Grises suaves: ejes, bordes, etiquetas secundarias

## Principios visuales
- Menos gráficos por página, más jerarquía.
- KPI alineados en una columna izquierda estable.
- Títulos que expliquen qué se está leyendo.
- Cada visual debe responder una pregunta concreta.
- Si un gráfico no ayuda a distinguir seguimiento, riesgo o perfil clínico, se elimina.

## Prioridad de reconstrucción

1. Rehacer layout general.
2. Mover filtros y KPI a la izquierda.
3. Reconstruir página de resumen ejecutivo.
4. Agregar página de perfil clínico.
5. Agregar página de seguimiento individual.
6. Ajustar tipografía, colores y espaciado final.

## Qué sí rescatar del dashboard actual
- KPI principales
- Distribución benigno vs maligno
- Seguimiento temporal de evaluaciones
- Histograma de edad si queda más limpio

## Qué no rescataría
- Panel de influencias
- Scatter actual si no se justifica clínicamente
- Exceso de elementos en una sola pantalla
