import pandas as pd
import glob
import json
import os

# 1. Ajustamos la ruta: tus archivos están dentro de la subcarpeta 'json'
archivos_json = glob.glob("./json/+*.json")

todos_los_mensajes = []

print(f"🕵️‍♂️ Buscando archivos... Se han detectado {len(archivos_json)} chats de clientes para consolidar.")

# 2. Iteramos sobre cada chat y estructuramos la información
for archivo in archivos_json:
    # El nombre del archivo se convierte en el identificador único del cliente en el dataset
    chat_id = os.path.basename(archivo).replace(".json", "")
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos_chat = json.load(f)
            
            for mensaje in datos_chat:
                # CREACIÓN DE METADATOS CLAVE (Feature Engineering):
                # Añadimos la columna 'rol' para que la IA separe al instante los inputs de los outputs
                rol_emisor = 'Soporte' if 'Yo' in mensaje.get('emisor', '') else 'Cliente'
                
                fila = {
                    'chat_id': chat_id,
                    'mensaje_id': mensaje.get('id'),
                    'fecha_hora_raw': mensaje.get('fecha_hora'),
                    'rol': rol_emisor,
                    'emisor': mensaje.get('emisor'),
                    'mensaje': mensaje.get('mensaje')
                }
                todos_los_mensajes.append(fila)
    except Exception as e:
        print(f"⚠️ Error al procesar el archivo {archivo}: {e}")

# 3. Construcción y optimización del DataFrame
if todos_los_mensajes:
    df = pd.DataFrame(todos_los_mensajes)
    
    # 4. Formateo de tiempos (Crucial para análisis cronológico)
    try:
        # Convertimos la fecha de texto a un objeto Datetime real de Pandas
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora_raw'], format='%H:%M, %d/%m/%Y', errors='coerce')
        # Ordenamos el dataset de forma lógica: primero por cliente, y dentro de cada cliente, cronológicamente
        df = df.sort_values(by=['chat_id', 'fecha_hora']).reset_index(drop=True)
    except Exception as e:
        print(f"ℹ️ Nota sobre las fechas: {e}. Se mantendrán en formato original.")
    
    # Reorganizamos las columnas para que la estructura sea impecable
    columnas_ordenadas = ['chat_id', 'mensaje_id', 'fecha_hora', 'rol', 'emisor', 'mensaje']
    df = df[columnas_ordenadas]
    
    # 5. Exportación del Dataset Maestro
    # Usamos 'utf-8-sig' para asegurar que Excel reconozca los acentos y emojis sin romper caracteres
    df.to_csv("dataset_soporte_padmi.csv", index=False, encoding='utf-8-sig')
    
    print("\n=== 🎉 ¡PIPELINE DE DATOS COMPLETADO! ===")
    print(f"📊 Total de interacciones (filas) consolidadas: {len(df)}")
    print(f"👥 Clientes únicos identificados: {df['chat_id'].nunique()}")
    print(f"💾 Archivo maestro guardado con éxito como: 'dataset_soporte_padmi.csv'")
    
    # Mostramos los primeros 3 registros en la consola para validar el resultado
    print("\n👀 Vista previa de las primeras filas:")
    print(df.head(3).to_string())
else:
    print("❌ No se encontraron archivos válidos que empiecen por '+' en el directorio './json/'.")