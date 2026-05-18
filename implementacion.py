#pydicom, numpy, pandas y opencv-python.
import pydicom
import numpy as np  
import pandas as pd
import cv2
import os

class ProcesadorDICOM():
    def __init__(self):
        self.listaArchivos = []
        self.df = None
        self.archivosImagenes = []
    
    def cargarArchivos(self,ruta:str):
        for archivo in os.listdir(ruta): #Se lee cada archivo compatible en el directorio
            if archivo.endswith('.dcm'):
                ruta_completa = os.path.join(ruta,archivo)
                try:
                    elemento = pydicom.dcmread(ruta_completa, force=True)
                    self.listaArchivos.append(elemento)
                    print(f'El archivo {archivo} se ha leído con éxito')
                except:
                    print(f'El archivo {archivo} no pudo leerse')
                    continue
            else:
                print(f'El archivo {archivo} no es un archivo dicom válido')
        
    def extraerInformacion(self):
        if not self.listaArchivos:
            print("No hay archivos cargados")
            self.df = pd.DataFrame()
            return
        datos = []
        for archivo in self.listaArchivos: #Se extrae la información necesaria con los tags
            fila ={
                'ID-paciente':archivo.get((0x0010,0x0020),None),
                'Nombre Paciente':archivo.get((0x0010,0x0010),None),
                'ID Estudio':archivo.get((0x0020,0x000D), None),
                'Descripción':archivo.get((0x0008,0x1030), None),
                'Fecha':archivo.get((0x0008,0x0020),None),
                'Modalidad':archivo.get((0x0008,0x0060),None),
                'Num. filas':archivo.get((0x0028,0x0010),None),
                'Num. columnas':archivo.get((0x0028,0x0011),None)
            }
            datos.append(fila)
        self.df = pd.DataFrame(datos)

    def calcularIntensidad(self):
        if self.df is None or len(self.df) == 0:
            print("DataFrame vacío")
            return
        intensidades = []
        for index,archivo in enumerate(self.listaArchivos):
            id_archivo = f"archivo_{index}"
            try:
                imagen = archivo.pixel_array
                intensidad = np.mean(imagen)
                intensidades.append(intensidad)
            except:
                intensidades.append(None)
                print(f'No se pudo calcular la intensidad de {id_archivo}')
        self.df['Intensidad promedio'] = intensidades

    def procesarImagenes(self):
        output_path = "salida_imagenes"
        if not os.path.exists(output_path): #por si no existe la carpeta, la crea
            os.makedirs(output_path)

        for index,archivo in enumerate(self.listaArchivos):
            id_archivo = f"imagen_0{index+1}"
            try:
                if 'PixelData' not in archivo: #verifica que el archivo tenga datos de imagen
                    print(f'El archivo {id_archivo} no se pudo procesar')
                    continue
                self.archivosImagenes.append(archivo)
                imagen = archivo.pixel_array

                if imagen.dtype not in [np.uint8,np.uint16,np.int16,np.int32]:
                    imagen = imagen.astype(np.float64)

                #Si la matriz de pixeles tiene alguna forma que no podemos procesar, hay que estandarizarla
                if len(imagen.shape) == 3 and imagen.shape[2] not in [3,4]:
                    # Volumen 3D (ej: 2,512,512)
                    slice_medio = imagen.shape[0] // 2
                    imagen = imagen[slice_medio, :, :]
                elif len(imagen.shape) == 4:
                    imagen = imagen[0,:,:,0]

                imagen_normalizada = cv2.normalize(imagen, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

                # Convertir a grises si tiene múltiples canales
                if len(imagen_normalizada.shape) == 3:
                    if imagen_normalizada.shape[2] == 3:
                        imagen_normalizada = cv2.cvtColor(imagen_normalizada, cv2.COLOR_BGR2GRAY)
                        print(f"  Convertido de RGB a grises")
                    elif imagen_normalizada.shape[2] == 4:
                        imagen_normalizada = cv2.cvtColor(imagen_normalizada, cv2.COLOR_BGRA2GRAY)
                        print(f"  Convertido de RGBA a grises")
                    else:
                        # Si tiene otro número de canales, tomar el primer canal
                        imagen_normalizada = imagen_normalizada[:, :, 0]
                        print(f"  Tomado primer canal de {imagen_normalizada.shape}")
                
                # Asegurar que sea 2D
                if len(imagen_normalizada.shape) != 2:
                    print(f"  Error: Shape inesperado {imagen_normalizada.shape}")
                    continue

                im_ecualizada=cv2.equalizeHist(imagen_normalizada)
                bordes = cv2.Canny(im_ecualizada, 50, 150) #Se utiliza un umbral bajo de 50 para capturar bordes fuertes y evitar ruido. Se recomienda que el umbral alto sea de 2 a 3 veces el umbral bajo. Esto es vital en imágenes médicas para evitar falsos positivos

                cv2.imwrite(os.path.join(output_path, f"{id_archivo}_ecualizada.png"), im_ecualizada)
                cv2.imwrite(os.path.join(output_path, f"{id_archivo}_bordes.png"), bordes)
                print(f'Imagen {id_archivo} procesada correctamente')
            except pydicom.errors.InvalidDicomError:
            # Si falla, el taller dice que debemos manejar el error (lo saltamos) 
                print(f"Archivo {id_archivo} sin imagen") 
                continue




procesador = ProcesadorDICOM()
procesador.cargarArchivos('data')
procesador.extraerInformacion()
procesador.calcularIntensidad()
procesador.procesarImagenes()
print(procesador.df)
print(f'Archivos iniciales: {len(procesador.listaArchivos)}')
print(f'Imágenes procesadas: {len(procesador.archivosImagenes)}')