import pandas as pd
import glob
import json
import os
import re

# 1. Buscamos  todos los archivos JSON dentro de la carpeta 'json'
archivos_json = glob.glob("./json/*.json")

todos_los_mensajes = []

print(f"🕵️‍♂️ Iniciando consolidación. Se encontraron {len(archivos_json)} archivos en total.")

# 2. Iteramos y normalizamos en la carga
for archivo in archivos_json:
    nombre_base = os.path.basename(archivo).replace(".json", "")
    
    # === REGLA 1: NORMALIZACIÓN DEL CHAT_ID ===
    # Eliminamos los sufijos de copia como " (1)", " (2)", etc.
    chat_id_limpio = re.sub(r'\s\(\d+\)', '', nombre_base)
    # Quitamos el símbolo '+' para homogeneizar todos los números
    chat_id_limpio = chat_id_limpio.replace('+', '')
    
    # Filtro de seguridad: Si el archivo es un script de Python o JS, lo asaltamos
    if not chat_id_limpio.isdigit():
        continue
     
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos_chat = json.load(f)
            
            for mensaje in datos_chat:
                # === REGLA 2: FILTRO ANTI-BASURA RESIDUAL ===
                # Si queda algún JSON viejo con líneas muertas de la interfaz, las asaltamos aquí
                if mensaje.get('emisor') == 'Desconocido' or 'información de contacto' in mensaje.get('mensaje', ''):
                    continue
                
                rol_emisor = 'Soporte' if 'Yo' in mensaje.get('emisor', '') else 'Cliente'
                
                fila = {
                    'chat_id': chat_id_limpio, # Guardamos el ID unificado (ej: 34643520400)
                    'fecha_hora_raw': mensaje.get('fecha_hora'),
                    'rol': rol_emisor,
                    'emisor': mensaje.get('emisor'),
                    'mensaje': mensaje.get('mensaje')
                }
                todos_los_mensajes.append(fila)
    except Exception as e:
        print(f"⚠️ No se pudo leer el archivo {archivo}: {e}")

# 3. Construcción y limpieza avanzada en Pandas
if todos_los_mensajes:
    df = pd.DataFrame(todos_los_mensajes)
    
    # Convertimos la fecha a formato datetime nativo
    df['fecha_hora'] = pd.to_datetime(df['fecha_hora_raw'], format='%H:%M, %d/%m/%Y', errors='coerce')
    
    # === REGLA 3: DE-DUPLICACIÓN INTELIGENTE ===
    # Como se procesaron los archivos con (1), habrá mensajes idénticos repetidos.
    # Eliminamos los duplicados asegurando conservar solo un registro único por mensaje real.
    df = df.drop_duplicates(subset=['chat_id', 'fecha_hora', 'mensaje'], keep='first')
    
    # Ordenamos cronológicamente todo el dataset unificado
    df = df.sort_values(by=['chat_id', 'fecha_hora']).reset_index(drop=True)
    
    # === REGLA 4: RE-GENERACIÓN SECUENCIAL DE IDs ===
    # Volvemos a generar el mensaje_id (1, 2, 3...) para cada chat de forma limpia y ordenada
    df['mensaje_id'] = df.groupby('chat_id').cumcount() + 1
    
    # Reorganizamos las columnas para el output final
    columnas_ordenadas = ['chat_id', 'mensaje_id', 'fecha_hora', 'rol', 'emisor', 'mensaje']
    df = df[columnas_ordenadas]
    
    # 4. Exportación del Dataset Maestro Sanearizado
    df.to_csv("dataset_soporte_padmi.csv", index=False, encoding='utf-8-sig')
    
    print("\n=== 🎉 ¡PIPELINE RESISTENTE A DUPLICADOS COMPLETADO! ===")
    print(f"静态 Total de interacciones reales consolidadas: {len(df)}")
    print(f"👥 Clientes únicos unificados: {df['chat_id'].nunique()}")
    print(f"💾 Dataset guardado con éxito como: 'dataset_soporte_padmi.csv'")
    
else:
    print("❌ No se encontraron datos válidos para procesar.")