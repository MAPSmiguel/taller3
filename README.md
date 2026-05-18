<h1> Taller 3 - Informática Médica</h1>

<h1>Procesamiento de Imágenes DICOM con Python</h1>

---

<h3> Integrantes del equipo</h3>

- Miguel Ángel Piedrahita
- Danna Julieta Matallana

---

<h3>Descripción del proyecto</h3>

Este proyecto implementa una aplicación en Python para la automatización de lectura, extracción y 
almacenamiento de metadatos de archivos DICOM, así como el procesamiento básico de imágenes médicas utilizando OpenCV.

<h3>Funcionalidades principales:</h3>

1. **Carga de archivos DICOM**- Escanea un directorio y carga todos los archivos con extensión `.dcm`
2. **Extracción de metadatos** - Extrae metadatos con información importante, incluyendo información del paciente,
   estudio y dimensiones de la imagen
3. **Estructuración de datos** - Almacena los metadatos en un DataFrame de Pandas
4. **Análisis de imágenes** - Calcula la intensidad promedio de píxeles usando NumPy
5. **Procesamiento de imágenes** - Aplica normalización, ecualización de histograma y detección de bordes con Canny
6. **Almacenamiento de resultados** - Guarda las imágenes procesadas en formato PNG

---
<h3>DICOM vs HL7</h3> 

<h3>¿Por qué son cruciales para la interoperabilidad en salud?</h3>

**DICOM (Digital Imaging and Communications in Medicine)** y **HL7 (Health Level Seven)** son los
dos estándares más importantes que permiten que diferentes sistemas de información en salud se 
comuniquen entre sí de manera efectiva.

**DICOM** es crucial porque:
- Define cómo se almacenan, transmiten y visualizan las imágenes médicas (radiografías, TACs, resonancias, etc.)
- Garantiza que una imagen tomada en un equipo (ej. MRI de Siemens) pueda ser visualizada en el
software de otro fabricante
- Incluye no solo la imagen sino todos los metadatos necesarios para su interpretación clínica

**HL7** es crucial porque:
- Permite el intercambio de información clínica no-imagen (historias clínicas, resultados de laboratorio,
- órdenes médicas, facturación)
- Facilita la continuidad asistencial entre diferentes proveedores de salud


---

<h3>Ecualización de histograma y detección de bordes con Canny en imágenes médicas</h3>

<h2>Ventajas de su aplicación:</h2>

**Ecualización de histograma:**
- **Mejora el contraste** en regiones subexpuestas o sobreexpuestas de la imagen
- **Realza detalles anatómicos** que de otra forma serían imperceptibles
- **Preprocesamiento útil** para segmentación automática o detección de anomalías

**Detección de bordes con Canny:**
- **Resalta estructuras anatómicas** como bordes de órganos, vasos sanguíneos o fracturas óseas
- **Reduce datos** conservando la información estructural más relevante

<h2>Limitaciones:</h2>

**Ecualización de histograma:**
- **Puede amplificar ruido** en regiones uniformes (ej. fondo pulmonar en radiografías)
- **Causa pérdida de información** en regiones que ya tenían buen contraste
- **Resultados no siempre interpretables** para radiólogos acostumbrados a escalas de grises estándar

**Detección de bordes con Canny:**
- **Sensible al ruido** - las texturas anatómicas pueden generar bordes espurios
- **Dependencia crítica de umbrales** - valores incorrectos pierden bordes relevantes o incluyen demasiado ruido

---

<h3>Dificultades encontradas y herramientas Python</h3>

#### Dificultades principales:

1. **Manejo de diferentes tipos de pixeles** - Las imágenes DICOM pueden tener 8, 12, 16 bits o más. La normalización a uint8 [0,255] fue necesaria para OpenCV.

2. **Archivos DICOM sin datos de imagen** - Algunos archivos (modalidades SR, PR) no contienen pixel_array. Implementamos manejo de excepciones

3. **Formatos de imagen no estándar** - Encontramos imágenes 3D (volúmenes) y 4D (cine). Implementamos lógica para extraer cortes representativos.

4. **Tags DICOM faltantes** - Todos estos archivos están anonimizados, por lo que faltan muchos metadatos


#### Importancia de las herramientas Python:


1. **pydicom** - Esencial para trabajar con DICOM. Permite leer tags, extraer metadatos y acceder a pixel_array sin necesidad de entender la especificación completa
2. **NumPy** - Fundamental para manejar los arrays de pixeles. Ofrece operaciones útiles para realizar cálculos como intensidad promedio de miles de imágenes
3. **Pandas** - Ideal para estructurar metadatos como DataFrame. Permite filtrar, agrupar y analizar estudios por paciente, modalidad o fecha fácilmente
4. **OpenCV** - Biblioteca madura de visión por computadora. Ofrece algoritmos optimizados (Canny, ecualización) que funcionan directamente con arrays NumPy


