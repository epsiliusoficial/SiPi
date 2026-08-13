#!/usr/bin/env python3
"""
SiPi - Lenguaje/herramienta para crear apps, juegos, programas y automatizaciones.
Interprete principal. 100% funcional, sin simulaciones.

Uso:
    python sipi.py archivo.sipi
"""
import sys
import os
import io
import functools
import ast
import re
import subprocess
import shutil
import json
import csv
import time
import random
import math
import datetime
import hashlib
import hmac
import secrets
import statistics
import queue
import wave
import struct
import tempfile
import copy
import difflib
import urllib.request
import urllib.error
import urllib.parse
import zipfile
import webbrowser
import http.server
import socketserver
import threading
import sqlite3

VERSION = "41.24.0"

COMANDOS_CONOCIDOS = [
    "programa", "version", "importar", "modo_debug", "const", "variable", "var",
    "sumar", "restar", "decir", "imprimir", "preguntar", "si", "sino", "fin",
    "repetir", "veces", "mientras", "funcion", "llamar", "llamar_valor",
    "hilo_crear", "hilo_esperar", "hilo_resultado", "hilo_esta_vivo",
    "hilo_esperar_todos", "bloqueo_crear", "con_bloqueo",
    "devolver", "lista_crear", "lista_agregar", "lista_obtener", "lista_longitud",
    "lista_eliminar", "para_cada", "intentar", "capturar", "diccionario_crear",
    "diccionario_asignar", "diccionario_obtener", "diccionario_tiene",
    "diccionario_eliminar", "diccionario_claves", "texto_dividir",
    "texto_reemplazar", "texto_contiene", "lista_ordenar", "lista_invertir",
    "lista_contiene", "suma_lista", "promedio_lista", "minimo", "maximo",
    "redondear", "registrar_evento", "matriz_crear", "matriz_asignar",
    "matriz_obtener", "matriz_filas", "matriz_columnas",
    "vector_sumar", "vector_restar", "vector_escalar", "vector_producto_punto",
    "vector_magnitud", "vector_normalizar", "crear_archivo",
    "leer_archivo", "borrar_archivo", "crear_carpeta", "copiar_archivo",
    "ejecutar", "esperar", "reproducir_tono", "instalar_paquete",
    "guardar_dato", "obtener_dato", "borrar_dato", "obtener_url", "longitud",
    "json_crear", "json_leer", "json_guardar", "json_texto",
    "csv_leer", "csv_guardar", "cada", "segundos", "veces", "detener_temporizador",
    "enum", "estructura", "instanciar", "pagina_web", "titulo", "subtitulo",
    "texto", "enlace", "lista_web", "separador", "tarjeta",
    "tema", "color", "formulario", "campo",
    "mayusculas", "minusculas", "azar_entre", "raiz", "potencia",
    "generar_pagina_web", "iniciar_servidor_web", "listar_archivos",
    "comprimir_carpeta", "descomprimir_zip", "fecha_hora_actual",
    "hash_texto", "hash_seguro_contrasena", "verificar_contrasena", "elegir_al_azar", "ventana", "boton", "etiqueta", "entrada",
    "imagen", "cuadro", "casilla", "lista", "barra_progreso",
    "actualizar_barra", "menu_desplegable", "pestanias", "pestana",
    "crear_juego", "sprite", "sonido", "tono", "chocar", "velocidad",
    "puntaje_inicial", "mostrar_puntaje", "mover_aleatorio",
    "gravedad", "rebote", "friccion", "tamano_mundo", "camara_seguir",
    "ia", "seguir", "escapar", "patrullar", "particulas", "explosion", "humo", "fuego",
    "captura_pantalla", "copiar_portapapeles", "pegar_portapapeles",
    "generar_app_android", "generar_app_windows", "compilar_a_js", "publicar_nube", "compilar_a_python",
    "instalar_modulo",
    "sqlite_conectar", "sqlite_ejecutar", "sqlite_consultar", "sqlite_cerrar",
    "postgres_conectar", "postgres_ejecutar", "postgres_consultar", "postgres_cerrar",
    "mysql_conectar", "mysql_ejecutar", "mysql_consultar", "mysql_cerrar",
    "migracion_crear", "migracion_aplicar", "migracion_revertir", "migracion_estado",
    "escuchar_ruta", "iniciar_api_web", "responder_json", "detener_api_web",
    "romper", "continuar",
    "texto_recortar", "texto_empieza_con", "texto_termina_con", "texto_repetir",
    "lista_filtrar", "lista_mapear", "lista_reducir", "lista_unir", "lista_aplanar",
    "tipo_de",
    "lanzar_error",
    "listar_modulos", "desinstalar_modulo", "instalar_dependencias",
    "instalar_repositorio", "listar_repositorios", "buscar_paquete", "editor_visual",
    "variable_entorno", "existe_variable_entorno", "registrar_log", "log_info",
    "log_advertencia", "log_error", "afirmar", "iniciar_pruebas", "resumen_pruebas",
    "generar_dockerfile",
    "estadistica_media", "estadistica_mediana", "estadistica_moda", "estadistica_desviacion",
    "estadistica_varianza", "estadistica_rango", "regresion_lineal", "distancia_gps",
    "generar_contrasena_segura", "generar_token_seguro", "evaluar_fortaleza_contrasena",
    "hash_archivo", "firmar_hmac", "verificar_hmac", "requerir_autenticacion", "limitar_peticiones",
    "ayuda", "modo_principiante", "nivel",
    "clase", "metodo", "hereda_de", "nuevo", "llamar_metodo", "este", "es_instancia_de",
    "fecha_sumar_dias", "fecha_diferencia_dias", "fecha_es_mayor", "fecha_formatear", "fecha_dia_semana",
    "imagen_info", "imagen_redimensionar", "imagen_convertir",
    "audio_duracion", "audio_generar_tono",
    "interfaz",
    "escena_3d", "figura", "rotacion_velocidad",
    "seleccionar", "caso", "otro",
]

COMANDOS_CONOCIDOS_SET = frozenset(COMANDOS_CONOCIDOS)


# Documentacion interactiva: resumen + ejemplo de los comandos mas usados,
# consultable en runtime con 'ayuda "comando"' o desde la CLI con
# 'sipi ayuda mostrar comando'. No cubre los 170 comandos (muchos de GUI/
# juegos tienen decenas de parametros propios), pero si los que un
# principiante va a usar primero; para el resto, DOCUMENTACION.md.
AYUDA_COMANDOS = {
    "nivel": ("Sistema de niveles de dificultad (principiante/facil/medio/dificil/extremo). "
              "Escribi '#nivel principiante' en la primera linea de tu programa (o 'nivel \"facil\"' en cualquier "
              "punto) para que SiPi solo te deje usar los comandos de ese nivel o mas bajo, con un aviso claro "
              "de que nivel desbloquea lo que intentaste usar. Sin esta directiva, SiPi funciona sin restricciones, "
              "como siempre.", '#nivel principiante\nprograma "Mi primer programa"'),
    "programa": ("Primera linea obligatoria de todo archivo .sipi.", 'programa "MiPrograma"'),
    "const": ("Declara una constante: no se puede reasignar despues.", "const PI2 = 3.14"),
    "sumar": ("Suma un valor a una variable numerica existente.", "sumar contador 1"),
    "restar": ("Resta un valor a una variable numerica existente.", "restar vidas 1"),
    "decir": ("Imprime texto en pantalla. Soporta {variable} para interpolar.", 'decir "Hola {nombre}"'),
    "imprimir": ("Igual que 'decir': imprime un valor o expresion.", "imprimir resultado"),
    "si": ("Condicional. Se cierra con 'fin', opcionalmente con 'sino' en el medio.", "si edad >= 18\n    decir \"Mayor\"\nfin"),
    "mientras": ("Bucle que repite mientras se cumpla una condicion.", "mientras i < 10\n    sumar i 1\nfin"),
    "repetir": ("Bucle de N iteraciones fijas.", "repetir 5 veces\n    decir \"Hola\"\nfin"),
    "para_cada": ("Recorre cada elemento de una lista.", "para_cada item en lista\n    imprimir item\nfin"),
    "romper": ("Corta el bucle actual (break).", "si condicion\n    romper\nfin"),
    "continuar": ("Salta a la siguiente iteracion del bucle (continue).", "si condicion\n    continuar\nfin"),
    "devolver": ("Devuelve un valor desde una funcion.", "devolver x * 2"),
    "llamar_valor": ("Llama a una funcion y guarda su resultado en una variable.", 'llamar_valor doble(21) -> r'),
    "hilo_crear": ("Corre una funcion en un hilo real de sistema operativo (en paralelo), sin bloquear el resto del programa. El hilo trabaja con su PROPIA copia de las variables globales (no las comparte en vivo con el resto del programa, para evitar condiciones de carrera) -- comunicale el resultado con 'devolver' y leelo con 'hilo_resultado'.", 'hilo_crear descargar_archivo("datos.zip") -> h1'),
    "hilo_esperar": ("Bloquea hasta que el hilo indicado termine, sin leer su resultado.", "hilo_esperar h1"),
    "hilo_resultado": ("Espera a que el hilo termine (si hace falta) y guarda en una variable lo que devolvio.", "hilo_resultado h1 -> resultado"),
    "hilo_esta_vivo": ("Revisa si un hilo sigue corriendo, sin bloquear.", "hilo_esta_vivo h1 -> sigue_corriendo"),
    "hilo_esperar_todos": ("Bloquea hasta que TODOS los hilos creados hasta ahora terminen.", "hilo_esperar_todos"),
    "bloqueo_crear": ("Crea un candado (lock) real para sincronizar el acceso a un recurso compartido entre hilos (ej. un archivo, una conexion).", "bloqueo_crear candado_archivo"),
    "con_bloqueo": ("Ejecuta un bloque de codigo con el candado indicado tomado -- si otro hilo ya lo tiene, espera a que se libere antes de entrar. Se libera solo al salir del bloque, incluso si hay un error adentro.", "con_bloqueo candado_archivo\n    escribir_archivo \"log.txt\" \"linea nueva\"\nfin"),
    "lanzar_error": ("Lanza un error propio, capturable con intentar/capturar.", 'lanzar_error "Edad invalida"'),
    "intentar": ("Bloque que captura errores sin cortar el programa.", "intentar\n    ...\ncapturar\n    decir \"Error: {error}\"\nfin"),
    "lista_agregar": ("Agrega un elemento al final de una lista.", "lista_agregar numeros 5"),
    "lista_mapear": ("Aplica una funcion a cada elemento de una lista.", "lista_mapear numeros con doble -> dobles"),
    "lista_filtrar": ("Filtra una lista segun una funcion booleana.", "lista_filtrar numeros con es_par -> pares"),
    "vector_sumar": ("Suma dos listas de numeros elemento a elemento (items #71-73 del feedback: preparar arrays/matematicas antes de pensar en IA/ML). Ambas listas deben tener la misma longitud.", "vector_sumar [1, 2, 3] [4, 5, 6] -> resultado"),
    "vector_restar": ("Resta dos listas de numeros elemento a elemento.", "vector_restar [5, 5, 5] [1, 2, 3] -> resultado"),
    "vector_escalar": ("Multiplica cada elemento de una lista por un numero (escalar).", "vector_escalar [1, 2, 3] 2 -> doble"),
    "vector_producto_punto": ("Producto punto de dos vectores (suma de los productos elemento a elemento). Base de casi cualquier operacion de IA/ML (redes neuronales, similitud coseno, etc.).", "vector_producto_punto [1, 2, 3] [4, 5, 6] -> resultado"),
    "vector_magnitud": ("Magnitud (longitud euclidiana) de un vector: raiz cuadrada de la suma de los cuadrados de sus componentes.", "vector_magnitud [3, 4] -> longitud"),
    "vector_normalizar": ("Devuelve el vector unitario (misma direccion, magnitud 1) -- util antes de comparar vectores por direccion en vez de tamaño.", "vector_normalizar [3, 4] -> unitario"),
    "diccionario_asignar": ("Asigna un valor a una clave del diccionario.", 'diccionario_asignar persona "nombre" "Mateo"'),
    "diccionario_obtener": ("Lee el valor de una clave. Sin '?' da texto vacio si falta; con '?' da 'nulo' (distinguible) si falta.", 'diccionario_obtener usuario "email"? -> correo\nsi correo != nulo\n    decir "{correo}"\nfin'),
    "sqlite_conectar": ("Abre o crea una base de datos SQLite real.", 'sqlite_conectar "datos.db" como db'),
    "postgres_conectar": ("Conecta a una base de datos PostgreSQL real (para sistemas de empresa con muchos usuarios simultaneos). Se instala el driver solo la primera vez. Agrega 'con pool N' para reutilizar N conexiones entre peticiones concurrentes.", 'postgres_conectar "localhost" 5432 "midb" "usuario" "clave" como db con pool 10'),
    "mysql_conectar": ("Conecta a una base de datos MySQL/MariaDB real. Se instala el driver solo la primera vez. Agrega 'con pool N' para reutilizar N conexiones entre peticiones concurrentes.", 'mysql_conectar "localhost" 3306 "midb" "usuario" "clave" como db con pool 10'),
    "migracion_crear": ("Crea un archivo de migracion de base de datos nuevo y numerado, con secciones para el SQL que aplica el cambio y el que lo revierte.", 'migracion_crear "migraciones" "crear tabla usuarios"'),
    "migracion_aplicar": ("Aplica todas las migraciones pendientes de una carpeta a una conexion de base de datos, en orden, salteando las que ya se aplicaron antes. Funciona igual sobre SQLite, Postgres o MySQL.", 'migracion_aplicar "migraciones" en db'),
    "migracion_revertir": ("Deshace la ultima migracion aplicada.", 'migracion_revertir "migraciones" en db'),
    "migracion_estado": ("Muestra que migraciones estan aplicadas y cuales pendientes.", 'migracion_estado "migraciones" en db'),
    "sqlite_consultar": ("Ejecuta un SELECT y guarda el resultado como lista de diccionarios.", 'sqlite_consultar db "SELECT * FROM t" en filas'),
    "escuchar_ruta": ("Registra una ruta de una API web real.", 'escuchar_ruta "/api/saludo" con manejar_saludo'),
    "iniciar_api_web": ("Levanta un servidor HTTP real que atiende las rutas registradas.", "iniciar_api_web 8000"),
    "instalar_modulo": ("Descarga e instala un modulo .sipi (administrador de paquetes).", 'instalar_modulo "https://.../modulo.sipi"'),
    "instalar_repositorio": ("Descarga un repositorio COMPLETO de GitHub (varios archivos .sipi) y lo deja en paquetes/<repo>/. Es el 'repositorio de paquetes' de SiPi: cualquier repo publico de GitHub con archivos .sipi es instalable, sin sitio propio.", 'instalar_repositorio "usuario/repo"'),
    "listar_repositorios": ("Muestra los paquetes de GitHub instalados con instalar_repositorio.", "listar_repositorios"),
    "buscar_paquete": ("Busca repositorios reales en GitHub relacionados con un tema (usando la API publica de GitHub, sin ningun catalogo inventado). Muestra resultados reales para instalar con instalar_repositorio.", 'buscar_paquete "juegos"'),
    "editor_visual": ("Abre un editor visual (WYSIWYG) en el navegador para tu ventana de escritorio: arrastra botones/etiquetas/imagenes con el mouse, edita el texto con un click, y los cambios se escriben solos de vuelta en tu archivo .sipi.", "editor_visual"),
    "variable_entorno": ("Lee una variable de entorno del sistema operativo (para configuracion y secretos, sin escribirlos en el codigo).", 'variable_entorno "PUERTO" o "8000" -> puerto'),
    "registrar_log": ("Escribe un log estructurado (JSON, compatible con sistemas de monitoreo reales) en sipi.log y en pantalla.", 'registrar_log info "Servidor iniciado"'),
    "afirmar": ("Verifica que una condicion se cumpla; si no, para el programa con un error claro (o reporta el fallo en modo pruebas). Base de las pruebas automatizadas.", 'afirmar resultado == 10, "el calculo deberia dar 10"'),
    "generar_dockerfile": ("Genera un Dockerfile + docker-compose.yml reales para desplegar tu programa en cualquier infraestructura que entienda Docker.", 'generar_dockerfile "mi_sistema"'),
    "estadistica_media": ("Promedio de una lista de numeros. Tambien existen estadistica_mediana, estadistica_moda, estadistica_desviacion, estadistica_varianza y estadistica_rango.", "estadistica_media temperaturas -> promedio"),
    "regresion_lineal": ("Calcula la recta que mejor ajusta dos listas de datos (pendiente y ordenada al origen), para predecir tendencias.", "regresion_lineal horas_estudio notas -> pendiente base"),
    "distancia_gps": ("Distancia real en kilometros entre dos coordenadas GPS (formula de Haversine, considera la curvatura de la Tierra). Util para despacho de emergencias, logistica, trabajo de campo.", "distancia_gps lat1 lon1 lat2 lon2 -> km"),
    "generar_contrasena_segura": ("Genera una contrasena aleatoria criptograficamente segura.", "generar_contrasena_segura 16 -> clave"),
    "generar_token_seguro": ("Genera un token aleatorio seguro en hexadecimal (para claves de API, sesiones, etc.).", "generar_token_seguro 32 -> token"),
    "evaluar_fortaleza_contrasena": ("Puntua que tan fuerte es una contrasena (0-100), detectando patrones debiles comunes. Herramienta defensiva.", "evaluar_fortaleza_contrasena clave -> puntaje"),
    "hash_archivo": ("Calcula el hash SHA-256 de un archivo, para verificar integridad (ej. cadena de custodia forense, o confirmar que un archivo no fue alterado).", 'hash_archivo "evidencia.pdf" -> huella'),
    "firmar_hmac": ("Firma un mensaje con una clave secreta (HMAC-SHA256), para verificar despues que no fue alterado ni falsificado.", "firmar_hmac mensaje con clave secreta -> firma"),
    "verificar_hmac": ("Verifica que una firma HMAC recibida sea autentica.", "verificar_hmac mensaje con clave secreta y firma firma_recibida -> es_valida"),
    "requerir_autenticacion": ("Exige una clave de API para todas las rutas de iniciar_api_web (excepto /salud). El cliente debe mandar el header 'Authorization: Bearer <clave>' o 'X-API-Key'.", 'requerir_autenticacion "clave-secreta-larga"'),
    "limitar_peticiones": ("Limita cuantas peticiones por minuto puede hacer cada IP a la API, para protegerla de abuso.", "limitar_peticiones 60 por_minuto"),
    "tipo_de": ("Devuelve el tipo de un valor: texto/numero/lista/diccionario/booleano.", "tipo_de x -> t"),
    "clase": ("Define una clase con campos y metodos (soporta herencia con hereda_de).", "clase Perro hereda_de Animal\n    metodo hacer_sonido()\n        devolver \"Guau!\"\n    fin\nfin"),
    "nuevo": ("Crea una instancia de una clase (llama al metodo 'constructor' si existe).", 'nuevo Perro("Rex") -> rex'),
    "llamar_metodo": ("Llama a un metodo de un objeto ya creado con 'nuevo'.", 'llamar_metodo rex "hacer_sonido"() -> sonido'),
    "ventana": ("Crea una ventana de escritorio (GUI).", 'ventana "Mi App" 400 300\n    ...\nfin'),
    "crear_juego": ("Inicia un juego 2D con motor grafico real.", 'crear_juego "Mi Juego" 800 600\n    ...\nfin'),
    "importar": ("Importa otro archivo .sipi como modulo.", 'importar "utilidades.sipi"'),
    "modo_debug": ("Activa el modo de depuracion: imprime cada linea antes de ejecutarla.", "modo_debug"),
    "variable": ("Declara/reasigna una variable. Opcionalmente con tipo: nombre: tipo = valor.", "variable edad: entero = 20"),
    "lista_crear": ("Crea una lista vacia. Opcionalmente tipada: nombre: lista<tipo>.", "lista_crear numeros: lista<entero>"),
    "diccionario_crear": ("Crea un diccionario vacio. Opcionalmente tipado: nombre: diccionario<tipo>.", "diccionario_crear precios: diccionario<decimal>"),
    "funcion": ("Define una funcion. Parametros y retorno pueden tener tipo opcional.", "funcion cuadrado(x: entero) -> entero\n    devolver x * x\nfin"),
    "fecha_sumar_dias": ("Suma (o resta con negativo) dias a una fecha AAAA-MM-DD.", 'fecha_sumar_dias "2026-01-01" 10 -> resultado'),
    "fecha_diferencia_dias": ("Calcula cuantos dias hay entre dos fechas.", 'fecha_diferencia_dias "2026-01-01" "2026-02-01" -> dias'),
    "fecha_formatear": ("Formatea una fecha con un patron estilo strftime.", 'fecha_formatear fecha "%d/%m/%Y" -> texto'),
    "imagen_info": ("Lee ancho, alto, formato y modo de una imagen (necesita Pillow).", 'imagen_info "foto.png" -> info'),
    "imagen_redimensionar": ("Redimensiona una imagen y guarda el resultado (necesita Pillow).", 'imagen_redimensionar "in.png" 800 600 "out.png"'),
    "audio_duracion": ("Calcula la duracion en segundos de un archivo .wav.", 'audio_duracion "sonido.wav" -> segundos'),
    "audio_generar_tono": ("Genera un archivo .wav con un tono puro de una frecuencia y duracion dadas.", 'audio_generar_tono 440 1.5 "tono.wav"'),
    "seleccionar": ("Pattern matching: compara un valor contra varios 'caso' y ejecuta el que coincide (o 'otro' si ninguno).", 'seleccionar dia\n    caso "lunes"\n        decir "Odio los lunes"\n    caso "viernes"\n        decir "Por fin!"\n    otro\n        decir "Dia normal"\nfin'),
    "escena_3d": ("3D basico v1: escena con figuras wireframe (cubo/piramide) rotando con perspectiva.", 'escena_3d "Escena" 640 480\n    figura cubo 0 0 0 100 "rojo"\n    rotacion_velocidad 2\nfin'),
    "interfaz": ("Declara metodos requeridos, sin implementarlos. Una clase 'implementa Nombre' si los tiene todos, verificado al definirla.", "interfaz Sonable\n    metodo hacer_sonido()\n    fin\nfin\n\nclase Perro implementa Sonable\n    metodo hacer_sonido()\n        devolver \"Guau!\"\n    fin\nfin"),
    "guardar_dato": ("Guarda un valor bajo una clave, en un almacen persistente en disco (sobrevive a cerrar el programa).", 'guardar_dato "puntaje_maximo" 9000'),
    "obtener_dato": ("Recupera un valor guardado antes con guardar_dato. Si la clave no existe, da texto vacio.", 'obtener_dato "puntaje_maximo" -> maximo'),
    "hash_texto": ("Calcula el hash SHA-256 de un texto (una huella digital, no reversible, SIN sal). Sirve para verificar integridad de archivos/datos. NO usar para contraseñas: es rapido y vulnerable a fuerza bruta/tablas arcoiris; para eso usar 'hash_seguro_contrasena'.", 'hash_texto contraseña -> huella'),
    "hash_seguro_contrasena": ("Deriva un hash seguro para GUARDAR contraseñas (PBKDF2-HMAC-SHA256, sal aleatoria de 16 bytes, 200.000 iteraciones -- mismo enfoque que usan frameworks reales como Django). El resultado ya incluye la sal, se guarda tal cual en la base de datos.", 'hash_seguro_contrasena clave_nueva -> hash_para_guardar'),
    "verificar_contrasena": ("Compara una contraseña ingresada contra un hash generado con 'hash_seguro_contrasena', en tiempo constante (protege contra ataques de timing). Da verdadero/falso.", 'verificar_contrasena clave_ingresada hash_guardado -> es_correcta'),
    "iniciar_servidor_web": ("Levanta un servidor web local que sirve los archivos de una carpeta.", 'iniciar_servidor_web "mi_sitio" 8000'),
    "generar_app_android": ("Genera un proyecto Android (Kivy) a partir de tu programa SiPi, listo para compilar a .apk.", 'generar_app_android "MiApp"'),
    "compilar_a_js": ("Traduce una o mas funciones SiPi a JavaScript real y las guarda en un .js. Ese JS corre en el navegador del usuario, sin servidor (equivalente practico a compilar SiPi para el frontend).", 'compilar_a_js saludar, doble "salida/logica.js"'),
    "compilar_a_python": ("Transpila TODO tu programa .sipi a un archivo .py real y standalone, que corre con 'python archivo.py' sin necesitar sipi.py. Mas rapido y portable (se puede empaquetar con PyInstaller directamente).", 'compilar_a_python "salida/programa_compilado.py"'),
    "publicar_nube": ("Empaqueta tu API web (la que definiste con escuchar_ruta) en una carpeta lista para desplegar, con vercel.json/netlify.toml/Procfile segun el proveedor elegido. Si detecta el CLI instalado (vercel/netlify/railway), intenta desplegar de una.", 'publicar_nube "mi_api" vercel'),
}

# Item 6 de tu feedback: "Documentacion de Casos de Uso Reales". La ayuda
# normal (AYUDA_COMANDOS) dice QUE hace un comando y COMO se escribe; esto
# agrega, para los comandos donde no es obvio, PARA QUE se usaria en un
# proyecto real -- conecta la sintaxis con la intencion. No cubre los ~190
# comandos (seria ruido para los obvios como 'decir' o 'sumar'), solo los
# que mas se benefician de un ejemplo de "para que sirve esto en la practica".
AYUDA_CASOS_DE_USO = {
    "guardar_dato": "guardar configuraciones de usuario, puntajes altos, o el estado de una partida sin tener que usar SQLite ni manejar archivos a mano.",
    "obtener_dato": "recuperar en la proxima ejecucion del programa algo que se guardo antes con guardar_dato (configuraciones, puntajes, progreso).",
    "sqlite_conectar": "cuando los datos crecen demasiado para guardar_dato (muchos registros, busquedas, relaciones entre tablas) -- un catalogo de productos, usuarios registrados, un inventario.",
    "sqlite_consultar": "traer varios registros a la vez desde una base SQLite (ej. 'todos los productos de una categoria') para despues recorrerlos con para_cada.",
    "hash_texto": "verificar que un archivo descargado no se corrompio, o cualquier huella digital de datos que NO sea una contraseña de usuario (para eso, ver hash_seguro_contrasena).",
    "hash_seguro_contrasena": "guardar la contraseña de un usuario en una base de datos de forma segura de verdad, para un sistema de login real (nunca guardar la contraseña en texto plano, ni con hash_texto solo).",
    "verificar_contrasena": "revisar si la contraseña que alguien tipeo al iniciar sesion coincide con la que se guardo con hash_seguro_contrasena.",
    "iniciar_servidor_web": "probar una pagina o API que hiciste con SiPi en tu propia computadora antes de subirla a un hosting real.",
    "generar_app_android": "convertir un programa SiPi en una app instalable en un celular Android, sin escribir Java/Kotlin.",
    "compilar_a_js": "convertir funciones SiPi en JavaScript real que corre en el navegador (frontend), sin depender de un servidor.",
    "compilar_a_python": "convertir todo tu programa SiPi en un archivo Python real, standalone y mas rapido, sin necesitar sipi.py.",
    "publicar_nube": "subir tu API web de SiPi a internet (Vercel, Netlify o Railway) con un solo comando, sin configurar un VPS.",
    "escena_3d": "prototipar rapido una idea con figuras 3D rotando (visualizaciones, demos, presentaciones) antes de armar un motor 3D mas completo.",
    "crear_juego": "arrancar un juego 2D (plataformas, arcade, puzzles) con sprites, colisiones y sonido sin configurar pygame a mano.",
    "interfaz": "garantizar que un grupo de clases distintas (Perro, Gato, Pato) cumplan el mismo contrato (ej. todas 'hacer_sonido') sin tener que acordarse de memoria de implementarlo -- si a alguna le falta, SiPi avisa al momento.",
    "lista_crear": "cuando necesitas guardar VARIOS valores del mismo tipo bajo un solo nombre (ej. todos los puntajes de una partida) en vez de crear una variable para cada uno.",
    "diccionario_crear": "guardar datos con nombre (ej. precios por producto, configuracion por clave) en vez de listas donde hay que acordarse la posicion de cada cosa.",
    "fecha_diferencia_dias": "calcular cuantos dias faltan para un evento, o hace cuanto se registro un usuario.",
    "lanzar_error": "cortar la ejecucion de una funcion con un mensaje claro cuando los datos que recibio no tienen sentido (ej. una edad negativa), en vez de dejar que el programa siga con datos invalidos.",
    "modo_debug": "ver, linea por linea, que esta ejecutando tu programa cuando algo no hace lo que esperabas y no encontras el motivo a simple vista.",
}


class RetornoFuncion(Exception):
    """Se usa internamente para propagar el valor de 'devolver' desde una funcion."""
    def __init__(self, valor):
        self.valor = valor
        super().__init__()


class RomperBucle(Exception):
    """Se usa internamente para implementar 'romper' (break) dentro de bucles."""
    pass


class ContinuarBucle(Exception):
    """Se usa internamente para implementar 'continuar' (continue) dentro de bucles."""
    pass


class DepuracionDetenida(Exception):
    """Se lanza desde 'hook_linea' (usado por el depurador visual del editor)
    cuando el usuario aprieta 'Detener'. A proposito NO es RetornoFuncion:
    si lo fuera, una llamada a funcion en curso la atraparia y la tomaria
    como un simple 'devolver', dejando que el programa siguiera corriendo
    en vez de detenerse de verdad (asi funcionaba antes: 'Detener' solo
    cortaba la ejecucion si el programa estaba en el nivel superior, no si
    estaba dentro de una funcion)."""
    pass


def asegurar_paquete(nombre_import, nombre_pip=None):
    """Instala automaticamente un paquete de Python si no esta disponible (auto-instalacion real)."""
    nombre_pip = nombre_pip or nombre_import
    try:
        __import__(nombre_import)
        return True
    except ImportError:
        print(f"[SiPi] El componente '{nombre_pip}' no esta instalado. Instalando automaticamente...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", nombre_pip],
                check=True,
            )
            __import__(nombre_import)
            print(f"[SiPi] '{nombre_pip}' instalado correctamente.")
            return True
        except Exception as e:
            print(f"[SiPi] No se pudo instalar '{nombre_pip}' automaticamente: {e}")
            print(f"[SiPi] Instalalo manualmente con: pip install {nombre_pip}")
            return False


COLORES_ESPANOL = {
    "rojo": "#dc2828", "verde": "#28c85a", "azul": "#3264e6",
    "blanco": "#ffffff", "negro": "#000000", "amarillo": "#f0dc28",
    "cian": "#00dcdc", "morado": "#9633c8", "violeta": "#9633c8",
    "gris": "#787878", "naranja": "#ff8c1a", "rosa": "#ff69b4",
    "marron": "#8b5a2b", "celeste": "#87ceeb", "dorado": "#ffd700",
}


def color_tkinter(color_texto):
    """Traduce un nombre de color en espanol (o un codigo hexadecimal ya
    valido) a un color que Tkinter entienda. Si no reconoce el nombre, lo
    deja pasar tal cual (por si el usuario ya escribio un color en ingles
    o un codigo hexadecimal, que Tkinter entiende de forma nativa)."""
    if not color_texto:
        return color_texto
    clave = color_texto.strip().lower()
    return COLORES_ESPANOL.get(clave, color_texto)


def hex_a_rgb(color_hex):
    """Convierte un color hexadecimal '#rrggbb' a una tupla (r, g, b) para pygame."""
    color_hex = color_hex.lstrip("#")
    if len(color_hex) != 6:
        return (200, 200, 200)
    try:
        return tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return (200, 200, 200)


def color_pygame(color_texto):
    """Traduce un nombre de color en espanol a una tupla RGB para pygame."""
    if not color_texto:
        return (200, 200, 200)
    clave = color_texto.strip().lower()
    if clave in COLORES_ESPANOL:
        return hex_a_rgb(COLORES_ESPANOL[clave])
    if color_texto.startswith("#"):
        return hex_a_rgb(color_texto)
    return (200, 200, 200)


def generar_wav_tono(frecuencia, duracion, volumen=0.5, framerate=44100):
    """Genera un archivo WAV real (una onda senoidal) sin depender de archivos
    externos ni de numpy. Devuelve la ruta del archivo temporal generado."""
    n_muestras = int(framerate * duracion)
    archivo_temporal = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    ruta = archivo_temporal.name
    archivo_temporal.close()
    with wave.open(ruta, "w") as onda:
        onda.setnchannels(1)
        onda.setsampwidth(2)
        onda.setframerate(framerate)
        amplitud = int(32767 * max(0.0, min(1.0, volumen)))
        cuadros = bytearray()
        for i in range(n_muestras):
            valor = int(amplitud * math.sin(2 * math.pi * frecuencia * i / framerate))
            cuadros += struct.pack("<h", valor)
        onda.writeframes(bytes(cuadros))
    return ruta


class SiPiError(Exception):
    def __init__(self, mensaje, pila=None, num_linea=None, texto_linea=None, archivo=None):
        super().__init__(mensaje)
        self.pila = pila or []
        # Item 26 del feedback ("sistema de errores excelente"): antes solo
        # se guardaba el mensaje armado ("Error en linea N: ..."), sin la
        # linea de codigo ni el archivo por separado, asi que no habia forma
        # de mostrar el codigo con un puntero debajo al momento de
        # imprimir el error final. Guardarlos aca, en el momento en que se
        # crea la excepcion (que es cuando se sabe con seguridad cual era
        # la linea que se estaba ejecutando), permite armar ese formato
        # mas claro en el catch de mas arriba sin tener que volver a
        # parsear nada.
        self.num_linea = num_linea
        self.texto_linea = texto_linea
        self.archivo = archivo


class PoolConexionesBD:
    """Pool real de conexiones a base de datos, reutilizables entre
    peticiones concurrentes. Sin esto, con el servidor de API multi-hilo,
    todas las peticiones simultaneas competirian por UNA sola conexion a
    Postgres/MySQL (los drivers no garantizan que sea seguro usar la misma
    conexion desde varios hilos a la vez) -- con el pool, cada peticion
    toma una conexion libre, la usa, y la devuelve, hasta un maximo
    configurable. Si estan todas ocupadas, espera un poco en vez de
    fallar de una (util bajo picos cortos de trafico)."""

    def __init__(self, fabrica_conexion, tamano):
        self._fabrica = fabrica_conexion
        self._tamano = tamano
        self._disponibles = queue.Queue()
        self._creadas = 0
        self._lock_creacion = threading.Lock()

    def precalentar_una(self):
        """Crea UNA conexion ya mismo (en vez de esperar a la primera
        peticion real) y la deja lista en el pool. Sirve para validar de
        entrada que las credenciales/host son correctos, en vez de
        enterarse recien con la primera peticion de un usuario real.
        A diferencia de llamar a la fabrica por fuera, esto SI cuenta
        correctamente para el limite del pool (evita el bug de crear una
        conexion de mas sin que el contador se entere)."""
        with self._lock_creacion:
            if self._creadas >= self._tamano:
                return
            self._creadas += 1
            conexion = self._fabrica()
        self._disponibles.put(conexion)

    def obtener(self, tiempo_espera=10):
        # Primero se intenta tomar una conexion ya creada y libre; si no
        # hay ninguna y todavia no se llego al tope, se crea una nueva de
        # una (perezoso: no abre las N conexiones de entrada si no hacen
        # falta todavia).
        try:
            return self._disponibles.get_nowait()
        except queue.Empty:
            pass
        with self._lock_creacion:
            if self._creadas < self._tamano:
                self._creadas += 1
                return self._fabrica()
        try:
            return self._disponibles.get(timeout=tiempo_espera)
        except queue.Empty:
            raise SiPiError(
                f"El pool de conexiones esta al limite ({self._tamano} conexiones, todas ocupadas) "
                f"y ninguna quedo libre en {tiempo_espera}s. Considera aumentar el tamano del pool."
            )

    def liberar(self, conexion):
        self._disponibles.put(conexion)

    def cerrar_todas(self):
        while not self._disponibles.empty():
            try:
                self._disponibles.get_nowait().close()
            except Exception:
                pass


class Entorno:
    """Guarda variables y funciones definidas por el usuario."""
    def __init__(self):
        self.variables = {"PI": math.pi, "E": math.e}
        self.funciones = {}
        self.constantes = {"PI", "E"}
        self.tipos_variables = {}  # sistema de tipos opcional: nombre -> tipo declarado ("entero", "decimal", "texto", "booleano", "lista", "diccionario")
        self.tipos_lista = {}  # listas tipadas opcionales (#21): nombre -> tipo de cada elemento (lista<entero>, etc.)
        self.tipos_diccionario = {}  # diccionarios tipados opcionales (#21): nombre -> tipo de cada valor (diccionario<texto>, etc.)
        self.interfaces = {}  # interfaces/protocolos (#22): nombre_interfaz -> set de nombres de metodo requeridos
        self.conexiones_sqlite = {}
        self.rutas_api = {}
        self.servidores_api = {}
        self.clases = {}
        self.clave_api_requerida = None  # None = sin autenticacion (compatibilidad de siempre)
        self.limite_peticiones_por_minuto = None  # None = sin limite


@functools.lru_cache(maxsize=16384)
def es_numero(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


# Patrones regex precompilados a nivel de modulo (evita recompilar/rebuscar
# en la cache interna de re en cada evaluacion, la ruta mas caliente del
# interprete). Esto mejora la velocidad real de ejecucion de bucles.
PATRON_IDENTIFICADOR = re.compile(r"[^\d\W][\w\u0900-\u097F\u0980-\u09FF]*", re.UNICODE)
PATRON_INTERPOLACION = re.compile(r"\{([^}]+)\}")
PATRON_BINARIA_SIMPLE = re.compile(r"^([A-Za-z_][\w\u0900-\u097F\u0980-\u09FF]*|\d+(?:\.\d+)?)\s*([+\-*/%])\s*([A-Za-z_][\w\u0900-\u097F\u0980-\u09FF]*|\d+(?:\.\d+)?)$")
PATRON_CONDICION_BINARIA = re.compile(r"^(.+?)\s*(==|!=|>=|<=|>|<)\s*(.+)$")


@functools.lru_cache(maxsize=16384)
def _analizar_condicion_binaria(cond):
    """Separa una condicion tipo 'i * i <= n' en (izquierda, operador,
    derecha), o None si no tiene esa forma. Es una funcion PURA (solo
    depende del texto), y en un bucle el mismo texto de condicion se re-
    evalua miles de veces con valores de variables distintos cada vez --
    pero la FORMA de la condicion (donde esta el operador, que texto va a
    cada lado) es siempre la misma. Cachearla evita repetir el regex y el
    escaneo de texto en cada vuelta del bucle, que era uno de los cuellos
    de botella reales medidos con cProfile en programas con muchas
    iteraciones."""
    m = PATRON_CONDICION_BINARIA.match(cond)
    if m:
        return (m.group(1).strip(), m.group(2), m.group(3).strip())
    return None


@functools.lru_cache(maxsize=16384)
def _analizar_binaria_simple(expr):
    """Igual que arriba, pero para expresiones aritmeticas simples de dos
    operandos (ej. 'i * i', 'n - 1'). Devuelve (izq, operador, der) o
    None."""
    m = PATRON_BINARIA_SIMPLE.match(expr)
    if m:
        return (m.group(1), m.group(2), m.group(3))
    return None


@functools.lru_cache(maxsize=16384)
def _es_texto_literal_puro(expr):
    """Version pura (sin 'self', cacheable) de la deteccion de 'esto es UN
    solo string literal completo'. Misma logica que antes, solo que ahora
    el resultado se recuerda por texto en vez de recalcularse cada vez que
    se evalua la misma linea dentro de un bucle o una funcion recursiva."""
    if not expr or expr[0] not in "\"'":
        return False
    comilla = expr[0]
    i = 1
    while i < len(expr):
        if expr[i] == comilla:
            return i == len(expr) - 1
        i += 1
    return False

# Palabras que abren un bloque que se cierra con 'fin'. Definidas UNA sola
# vez y reutilizadas en todo el archivo (antes esta misma lista estaba
# copiada y pegada mas de 15 veces; en algun momento se agregaron
# 'pagina_web'/'formulario' en 14 de esas copias pero se olvidaron en la
# del formateador de codigo, y eso causo un bug real donde --formatear no
# indentaba bien esos bloques. Tenerla en un solo lugar hace que ese tipo
# de bug ya no pueda volver a pasar).
# ---------------------------------------------------------------------------
# Soporte multi-idioma real: SiPi se puede escribir directamente con palabras
# clave en otros idiomas ademas de espanol. Un programa declara su idioma con
# una linea "#idioma <codigo>" al principio del archivo (zh=chino mandarin,
# hi=hindi, ar=arabe estandar moderno) y el traductor convierte esas palabras
# clave a su equivalente en espanol ANTES de que el resto del interprete (que
# sigue siendo 100% en espanol por dentro) procese una sola linea. Nombres de
# variables, funciones y el contenido de los textos entre comillas NUNCA se
# tocan: solo se traducen las palabras reservadas del lenguaje.
#
# Nota honesta: esta es una primera cobertura del nucleo del lenguaje (lo
# suficiente para programas reales con funciones, condicionales, bucles,
# listas y diccionarios). Se ira ampliando a mas palabras clave y mas
# idiomas con el tiempo, como cualquier lenguaje de programacion real que
# agrega localizaciones de forma incremental.
IDIOMAS_SIPI = {
    "zh": {  # Chino mandarin (simplificado)
        "程序": "programa", "版本": "version", "变量": "variable", "常量": "const",
        "如果": "si", "否则": "sino", "结束": "fin", "当": "mientras",
        "重复": "repetir", "次": "veces", "对每个": "para_cada", "在": "en",
        "跳出": "romper", "继续": "continuar",
        "函数": "funcion", "调用": "llamar", "调用_值": "llamar_valor", "返回": "devolver",
        "说": "decir", "加": "sumar", "减": "restar",
        "真": "verdadero", "假": "falso", "空": "nulo", "和": "y", "或": "o",
        "创建列表": "lista_crear", "添加到列表": "lista_agregar", "从列表获取": "lista_obtener",
        "列表长度": "lista_longitud", "从列表删除": "lista_eliminar",
        "创建字典": "diccionario_crear", "字典赋值": "diccionario_asignar",
        "从字典获取": "diccionario_obtener", "字典包含": "diccionario_tiene",
        "从字典删除": "diccionario_eliminar", "字典键": "diccionario_claves",
        "导入": "importar", "作为": "como", "抛出错误": "lanzar_error",
        "尝试": "intentar", "捕获": "capturar",
    },
    "hi": {  # Hindi
        "प्रोग्राम": "programa", "संस्करण": "version", "चर": "variable", "स्थिरांक": "const",
        "अगर": "si", "अन्यथा": "sino", "समाप्त": "fin", "जबतक": "mientras",
        "दोहराओ": "repetir", "बार": "veces", "हर_एक_के_लिए": "para_cada", "में": "en",
        "तोड़ो": "romper", "जारी_रखो": "continuar",
        "फ़ंक्शन": "funcion", "बुलाओ": "llamar", "बुलाओ_मान": "llamar_valor", "वापस": "devolver",
        "बोलो": "decir", "जोड़ो": "sumar", "घटाओ": "restar",
        "सच": "verdadero", "झूठ": "falso", "शून्य": "nulo", "और": "y", "या": "o",
        "सूची_बनाओ": "lista_crear", "सूची_में_जोड़ो": "lista_agregar", "सूची_से_प्राप्त_करो": "lista_obtener",
        "सूची_लंबाई": "lista_longitud", "सूची_से_हटाओ": "lista_eliminar",
        "शब्दकोश_बनाओ": "diccionario_crear", "शब्दकोश_में_रखो": "diccionario_asignar",
        "शब्दकोश_से_प्राप्त_करो": "diccionario_obtener", "शब्दकोश_में_है": "diccionario_tiene",
        "शब्दकोश_से_हटाओ": "diccionario_eliminar", "शब्दकोश_कुंजियाँ": "diccionario_claves",
        "आयात_करो": "importar", "के_रूप_में": "como", "त्रुटि_फेंको": "lanzar_error",
        "कोशिश_करो": "intentar", "पकड़ो": "capturar",
    },
    "ar": {  # Arabe estandar moderno
        "برنامج": "programa", "إصدار": "version", "متغير": "variable", "ثابت": "const",
        "إذا": "si", "وإلا": "sino", "نهاية": "fin", "بينما": "mientras",
        "كرر": "repetir", "مرات": "veces", "لكل": "para_cada", "في": "en",
        "اكسر": "romper", "استمر": "continuar",
        "دالة": "funcion", "نادي": "llamar", "نادي_قيمة": "llamar_valor", "أرجع": "devolver",
        "قل": "decir", "أضف": "sumar", "اطرح": "restar",
        "صحيح": "verdadero", "خطأ": "falso", "فارغ": "nulo", "و": "y", "أو": "o",
        "أنشئ_قائمة": "lista_crear", "أضف_إلى_القائمة": "lista_agregar", "احصل_من_القائمة": "lista_obtener",
        "طول_القائمة": "lista_longitud", "احذف_من_القائمة": "lista_eliminar",
        "أنشئ_قاموس": "diccionario_crear", "عيّن_في_القاموس": "diccionario_asignar",
        "احصل_من_القاموس": "diccionario_obtener", "القاموس_يحتوي": "diccionario_tiene",
        "احذف_من_القاموس": "diccionario_eliminar", "مفاتيح_القاموس": "diccionario_claves",
        "استورد": "importar", "كـ": "como", "ارم_خطأ": "lanzar_error",
        "حاول": "intentar", "التقط": "capturar",
    },
    "en": {  # Ingles
        "program": "programa", "version": "version", "var": "variable", "const": "const",
        "if": "si", "else": "sino", "end": "fin", "while": "mientras",
        "repeat": "repetir", "times": "veces", "foreach": "para_cada", "in": "en",
        "break": "romper", "continue": "continuar",
        "function": "funcion", "call": "llamar", "call_value": "llamar_valor", "return": "devolver",
        "say": "decir", "add": "sumar", "subtract": "restar",
        "true": "verdadero", "false": "falso", "null": "nulo", "and": "y", "or": "o",
        "list_create": "lista_crear", "list_add": "lista_agregar", "list_get": "lista_obtener",
        "list_length": "lista_longitud", "list_remove": "lista_eliminar",
        "dict_create": "diccionario_crear", "dict_set": "diccionario_asignar",
        "dict_get": "diccionario_obtener", "dict_has": "diccionario_tiene",
        "dict_remove": "diccionario_eliminar", "dict_keys": "diccionario_claves",
        "import": "importar", "as": "como", "throw_error": "lanzar_error",
        "try": "intentar", "catch": "capturar",
    },
    "fr": {  # Frances
        "programme": "programa", "version": "version", "variable": "variable", "constante": "const",
        "si": "si", "sinon": "sino", "fin": "fin", "tantque": "mientras",
        "repeter": "repetir", "fois": "veces", "pour_chaque": "para_cada", "dans": "en",
        "arreter": "romper", "continuer": "continuar",
        "fonction": "funcion", "appeler": "llamar", "appeler_valeur": "llamar_valor", "retourner": "devolver",
        "dire": "decir", "ajouter": "sumar", "soustraire": "restar",
        "vrai": "verdadero", "faux": "falso", "nul": "nulo", "et": "y", "ou": "o",
        "liste_creer": "lista_crear", "liste_ajouter": "lista_agregar", "liste_obtenir": "lista_obtener",
        "liste_longueur": "lista_longitud", "liste_supprimer": "lista_eliminar",
        "dico_creer": "diccionario_crear", "dico_assigner": "diccionario_asignar",
        "dico_obtenir": "diccionario_obtener", "dico_contient": "diccionario_tiene",
        "dico_supprimer": "diccionario_eliminar", "dico_cles": "diccionario_claves",
        "importer": "importar", "comme": "como", "lancer_erreur": "lanzar_error",
        "essayer": "intentar", "attraper": "capturar",
    },
    "bn": {  # Bengali
        "প্রোগ্রাম": "programa", "সংস্করণ": "version", "চলক": "variable", "ধ্রুবক": "const",
        "যদি": "si", "নাহলে": "sino", "শেষ": "fin", "যতক্ষণ": "mientras",
        "পুনরাবৃত্তি": "repetir", "বার": "veces", "প্রতিটির_জন্য": "para_cada", "মধ্যে": "en",
        "থামো": "romper", "চালিয়ে_যাও": "continuar",
        "ফাংশন": "funcion", "ডাকো": "llamar", "ডাকো_মান": "llamar_valor", "ফেরত_দাও": "devolver",
        "বলো": "decir", "যোগ_করো": "sumar", "বিয়োগ_করো": "restar",
        "সত্য": "verdadero", "মিথ্যা": "falso", "শূন্য": "nulo", "এবং": "y", "অথবা": "o",
        "তালিকা_তৈরি_করো": "lista_crear", "তালিকায়_যোগ_করো": "lista_agregar", "তালিকা_থেকে_নাও": "lista_obtener",
        "তালিকার_দৈর্ঘ্য": "lista_longitud", "তালিকা_থেকে_মুছো": "lista_eliminar",
        "অভিধান_তৈরি_করো": "diccionario_crear", "অভিধানে_রাখো": "diccionario_asignar",
        "অভিধান_থেকে_নাও": "diccionario_obtener", "অভিধানে_আছে": "diccionario_tiene",
        "অভিধান_থেকে_মুছো": "diccionario_eliminar", "অভিধানের_চাবি": "diccionario_claves",
        "আমদানি_করো": "importar", "হিসেবে": "como", "ত্রুটি_ছুঁড়ো": "lanzar_error",
        "চেষ্টা_করো": "intentar", "ধরো": "capturar",
    },
}

NOMBRES_IDIOMAS_SIPI = {
    "zh": "chino mandarin", "hi": "hindi", "ar": "arabe estandar moderno",
    "en": "ingles", "fr": "frances", "bn": "bengali", "es": "espanol",
}

def _dividir_respetando_cadenas(linea):
    """Separa una linea en segmentos, alternando texto normal y texto
    literal entre comillas dobles (incluidas). Los indices impares del
    resultado son SIEMPRE cadenas literales; nunca hay que traducir
    palabras clave ahi adentro, son datos del usuario."""
    return re.split(r'("(?:[^"\\]|\\.)*")', linea)


def _dividir_dos_argumentos_por_espacio(texto):
    """Separa 'texto' en dos expresiones top-level por el PRIMER espacio
    que este fuera de comillas, parentesis, corchetes y llaves -- a
    diferencia de un regex simple como r'(.+?)\\s+(.+)', esto no se
    confunde con los espacios INTERNOS de una lista literal como
    '[1, 2, 3]' (el regex simple corta en el primer espacio que
    encuentra, sea cual sea, partiendo '[1,' y '2, 3] [4, 5, 6]' -- un
    desastre). Usado por los comandos 'vector_*' para separar sus dos
    argumentos (dos vectores, o un vector y un escalar) antes del '->'.
    Devuelve (expr_a, expr_b) o None si no encuentra un punto de corte
    valido."""
    profundidad = 0
    en_comillas = False
    i = 0
    n = len(texto)
    while i < n:
        c = texto[i]
        if en_comillas:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                en_comillas = False
        elif c == '"':
            en_comillas = True
        elif c in "([{":
            profundidad += 1
        elif c in ")]}":
            profundidad -= 1
        elif c == " " and profundidad == 0 and i > 0:
            resto = texto[i + 1:].strip()
            if resto:
                return texto[:i].strip(), resto
        i += 1
    return None


def _quitar_comentario_linea(linea):
    """Corta un comentario '//' al final de una linea, pero SOLO si ese
    '//' esta fuera de un texto entre comillas. Sin esto, cualquier URL
    (http://, https://) dentro de un string quedaba cortada a la mitad,
    porque el '//' de la URL se interpretaba como el inicio de un
    comentario. Reutiliza el mismo separador de segmentos que ya usan el
    traductor de idiomas y el de operadores naturales."""
    if "//" not in linea:
        return linea
    segmentos = _dividir_respetando_cadenas(linea)
    for idx in range(0, len(segmentos), 2):  # pares = fuera de comillas
        pos = segmentos[idx].find("//")
        if pos != -1:
            segmentos[idx] = segmentos[idx][:pos]
            return "".join(segmentos[:idx + 1])
    return "".join(segmentos)


_COMILLAS_CURVAS = {
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
}


def _autocorregir_linea(num_linea, texto):
    """Corrige automaticamente errores tipograficos chicos y comunes en UNA
    linea ya sin comentarios: espacios de mas entre palabras, comillas
    'curvas' (las que pone Word/el celular en vez de comillas rectas),
    espacios/tabs sobrantes al final, un punto suelto al final de la
    linea que no pertenece a ningun texto, y un comando mal escrito por
    poco (ej. 'decid' en vez de 'decir') cuando hay una sola opcion
    razonable. Nunca toca el CONTENIDO de un texto entre comillas dobles
    (ej. 'decir "hola  mundo"' conserva el espacio doble adentro, porque
    ahi es una decision del usuario, no un error).

    Devuelve (texto_corregido, lista_de_descripciones) -- la lista queda
    vacia si no hizo falta corregir nada."""
    if texto.strip() == "":
        return texto, []

    correcciones = []
    segmentos = _dividir_respetando_cadenas(texto)

    # Comillas curvas -> comillas rectas. Se aplica en TODOS los segmentos
    # (incluso dentro de un texto ya delimitado por comillas rectas, para
    # el caso de una comilla curva escrita sin querer en el medio de una
    # palabra). No es ambiguo: SiPi no le da ningun significado especial
    # a las comillas curvas, asi que no hay forma de que esto rompa algo
    # que el usuario quiso escribir a proposito.
    hubo_comillas_curvas = False
    for i, seg in enumerate(segmentos):
        nuevo = seg
        for curva, recta in _COMILLAS_CURVAS.items():
            if curva in nuevo:
                nuevo = nuevo.replace(curva, recta)
                hubo_comillas_curvas = True
        segmentos[i] = nuevo
    if hubo_comillas_curvas:
        correcciones.append("comillas 'curvas' (tipográficas) cambiadas por comillas rectas")

    # Espacios dobles/triples -> un solo espacio, PERO solo fuera de texto
    # entre comillas (indices pares de 'segmentos') y sin tocar la
    # indentacion inicial (los espacios/tabs antes de la primera palabra
    # real, que en SiPi pueden ser sintacticamente significativos --
    # ver _inferir_fin_por_indentacion).
    hubo_espacios_dobles = False
    for i in range(0, len(segmentos), 2):
        seg = segmentos[i]
        sin_indent = seg.lstrip(" \t")
        indent = seg[:len(seg) - len(sin_indent)]
        # Solo colapsar espacios dobles si esta linea YA tiene contenido
        # antes de este segmento (i > 0) o si este segmento no es
        # puramente la indentacion inicial de la linea completa.
        if i == 0:
            resto = sin_indent
            colapsado = re.sub(r"(?<=\S) {2,}", " ", resto)
            if colapsado != resto:
                hubo_espacios_dobles = True
            segmentos[i] = indent + colapsado
        else:
            colapsado = re.sub(r"(?<=\S) {2,}", " ", seg)
            if colapsado != seg:
                hubo_espacios_dobles = True
            segmentos[i] = colapsado
    if hubo_espacios_dobles:
        correcciones.append("espacio(s) de más entre palabras, colapsados a uno solo")

    texto_corregido = "".join(segmentos)

    # Espacios/tabs sobrantes al final de la linea (invisibles, pero
    # ensucian el archivo y pueden confundir a otras herramientas).
    sin_trailing = texto_corregido.rstrip(" \t")
    if sin_trailing != texto_corregido:
        correcciones.append("espacios en blanco sobrantes al final de la línea")
        texto_corregido = sin_trailing

    # Punto suelto al final de la linea, fuera de cualquier texto entre
    # comillas (osea, terminamos la linea en un numero par de comillas,
    # no a mitad de un string). No es un separador valido en ningun lugar
    # de la sintaxis de SiPi, asi que sacarlo es siempre seguro.
    if (texto_corregido.count('"') % 2 == 0 and texto_corregido.endswith(".")
            and not texto_corregido.endswith("...") and len(texto_corregido) > 1
            and texto_corregido[-2] != "."):
        texto_corregido = texto_corregido[:-1].rstrip(" \t")
        correcciones.append("punto suelto al final de la línea, que no pertenecía a ningún texto")

    # Comando mal escrito por poco (ej. 'decid' -> 'decir'), solo si hay
    # una UNICA opcion razonablemente cercana y la linea tiene pinta de
    # ser un comando (no una asignacion tipo 'campo = valor', que es
    # sintaxis valida de SiPi para structs/enums y no debe tocarse).
    stripped = texto_corregido.strip()
    if stripped and stripped != "fin":
        primera_palabra = stripped.split(" ", 1)[0]
        resto = stripped[len(primera_palabra):].strip()
        es_asignacion = resto.startswith("=") and not resto.startswith("==")
        palabra_valida = (
            primera_palabra in COMANDOS_CONOCIDOS_SET
            or primera_palabra in PALABRAS_MISMO_NIVEL
            or primera_palabra in BLOQUES_QUE_ABREN
        )
        if not es_asignacion and not palabra_valida and len(primera_palabra) >= 4 and primera_palabra.isalpha():
            candidatos = difflib.get_close_matches(primera_palabra, COMANDOS_CONOCIDOS, n=2, cutoff=0.75)
            if len(candidatos) == 1:
                comando_correcto = candidatos[0]
                indent_inicial = texto_corregido[:len(texto_corregido) - len(texto_corregido.lstrip(" \t"))]
                resto_linea = texto_corregido.strip()[len(primera_palabra):]
                texto_corregido = indent_inicial + comando_correcto + resto_linea
                correcciones.append(f"'{primera_palabra}' no es un comando de SiPi, se cambió por '{comando_correcto}' (la única opción parecida)")

    return texto_corregido, correcciones


def traducir_linea_a_espanol(linea, tabla_idioma):
    """Traduce las palabras clave de una linea de un idioma soportado al
    espanol (el idioma interno real del interprete), dejando intacto
    cualquier texto entre comillas y cualquier identificador que el
    usuario haya elegido (nombres de variables/funciones no reservados).

    Nota tecnica: en vez de '\\b' (limite de palabra basado en la clase
    Unicode \\w), se usa un limite basado en espacios en blanco. Escrituras
    como el hindi (devanagari, con signos vocalicos combinados/matras) o
    el arabe (con diacriticos opcionales) tienen caracteres que Python no
    siempre clasifica como '\\w', lo que rompe '\\b' justo en medio o al
    final de una palabra clave real. Delimitar por espacios es mas robusto
    para cualquier escritura, ya que la gramatica de SiPi ya exige palabras
    separadas por espacios."""
    segmentos = _dividir_respetando_cadenas(linea)
    # Palabras mas largas primero, para que 'llamar_valor' (en su idioma)
    # no quede parcialmente reemplazada por la traduccion de 'llamar'.
    claves_ordenadas = sorted(tabla_idioma.keys(), key=len, reverse=True)
    for idx, segmento in enumerate(segmentos):
        if idx % 2 == 1:  # cadena literal: no tocar
            continue
        for clave in claves_ordenadas:
            patron = rf"(?<!\S){re.escape(clave)}(?!\S)"
            segmento = re.sub(patron, tabla_idioma[clave], segmento)
        segmentos[idx] = segmento
    return "".join(segmentos)


NIVELES_SIPI = {
    "principiante": 1, "facil": 2, "fácil": 2, "medio": 3, "dificil": 4, "difícil": 4, "extremo": 5,
}
NOMBRES_NIVELES_SIPI = {1: "principiante", 2: "facil", 3: "medio", 4: "dificil", 5: "extremo"}

# Progreso acumulativo real: cada nivel agrega SOLO lo nuevo respecto al
# anterior (el conjunto de comandos permitidos en un nivel es la union de
# todos los niveles hasta ese punto). Curado a mano para que la progresion
# tenga sentido pedagogico real -- no es una lista alfabetica al azar.
PALABRAS_NIVEL_1_PRINCIPIANTE = {
    "programa", "version", "variable", "const", "si", "sino", "fin", "mientras",
    "repetir", "veces", "decir", "funcion", "llamar", "llamar_valor", "devolver",
    "verdadero", "falso", "nulo", "sumar", "restar", "leer", "preguntar",
    "romper", "continuar", "ayuda", "modo_principiante", "modo_debug", "nivel",
}
PALABRAS_NIVEL_2_FACIL = PALABRAS_NIVEL_1_PRINCIPIANTE | {
    "para_cada", "en", "como",
    "lista_crear", "lista_agregar", "lista_obtener", "lista_longitud", "lista_eliminar",
    "diccionario_crear", "diccionario_asignar", "diccionario_obtener", "diccionario_tiene",
    "diccionario_eliminar", "diccionario_claves",
    "mayusculas", "minusculas", "texto_contiene", "texto_reemplazar", "texto_dividir",
    "texto_unir", "longitud_texto", "redondear", "raiz_cuadrada", "potencia",
    "aleatorio", "elegir_al_azar", "fecha_actual", "hora_actual",
    "convertir_a_numero", "convertir_a_texto", "tipo_de", "esperar",
    "estadistica_media", "estadistica_mediana", "estadistica_moda",
    "estadistica_desviacion", "estadistica_varianza", "estadistica_rango",
}
PALABRAS_NIVEL_3_MEDIO = PALABRAS_NIVEL_2_FACIL | {
    "clase", "hereda_de", "metodo", "interfaz", "estructura", "enum", "instanciar",
    "intentar", "capturar", "lanzar_error", "seleccionar", "caso",
    "leer_archivo", "crear_archivo", "existe_archivo", "listar_archivos",
    "json_a_texto", "texto_a_json", "hash_texto", "hash_seguro_contrasena", "verificar_contrasena",
    "bd_conectar", "bd_consultar", "bd_ejecutar", "bd_cerrar",
    "sqlite_conectar", "sqlite_ejecutar", "sqlite_consultar", "sqlite_cerrar",
    "postgres_conectar", "postgres_ejecutar", "postgres_consultar", "postgres_cerrar",
    "mysql_conectar", "mysql_ejecutar", "mysql_consultar", "mysql_cerrar",
    "migracion_crear", "migracion_aplicar", "migracion_revertir", "migracion_estado",
    "importar", "instalar_modulo", "instalar_repositorio", "buscar_paquete",
    "listar_repositorios", "listar_modulos", "desinstalar_modulo", "instalar_dependencias",
    "compilar_a_python",
    "variable_entorno", "existe_variable_entorno", "registrar_log", "log_info",
    "log_advertencia", "log_error", "afirmar", "iniciar_pruebas", "resumen_pruebas",
    "regresion_lineal", "distancia_gps", "generar_contrasena_segura", "generar_token_seguro",
    "evaluar_fortaleza_contrasena", "hash_archivo", "firmar_hmac", "verificar_hmac",
}
PALABRAS_NIVEL_4_DIFICIL = PALABRAS_NIVEL_3_MEDIO | {
    "ventana", "boton", "etiqueta", "entrada", "imagen", "cuadro", "casilla",
    "lista", "barra_progreso", "menu_desplegable", "pestanias", "pestana",
    "crear_juego", "sprite", "mover_sprite", "detectar_colision", "reproducir_sonido",
    "reproducir_tono", "pagina_web", "formulario", "iniciar_api_web", "escuchar_ruta",
    "responder_json", "detener_api_web", "iniciar_servidor_web",
    "requerir_autenticacion", "limitar_peticiones",
    "hilo", "paralelo", "hilo_crear", "hilo_esperar", "hilo_resultado",
    "hilo_esta_vivo", "hilo_esperar_todos", "bloqueo_crear", "con_bloqueo",
    "capturar_pantalla", "editor_visual", "compilar_a_js",
}
# Nivel 5 (Extremo) no tiene lista propia: es TODO lo que exista en
# COMANDOS_CONOCIDOS y no este en los niveles anteriores (compiladores,
# publicacion a la nube, generacion de apps nativas, motor 3D, proteccion
# de codigo, automatizacion de sistema, etc.). Se calcula solo, asi que
# cualquier comando nuevo que se agregue a SiPi en el futuro automaticamente
# queda en el nivel mas alto hasta que alguien decida bajarlo a un nivel
# anterior -- nunca al reves, que seria inseguro (un comando peligroso o
# avanzado quedando disponible por descuido en modo principiante).


CONJUNTOS_POR_NIVEL = {
    1: PALABRAS_NIVEL_1_PRINCIPIANTE,
    2: PALABRAS_NIVEL_2_FACIL,
    3: PALABRAS_NIVEL_3_MEDIO,
    4: PALABRAS_NIVEL_4_DIFICIL,
}


def _nivel_que_desbloquea_comando(cmd):
    """Encuentra el nivel MAS BAJO en el que un comando ya esta disponible.
    Si no aparece en ningun conjunto 1-4, es de nivel 5 (Extremo) por
    definicion (ver comentario en CONJUNTOS_POR_NIVEL)."""
    for n in (1, 2, 3, 4):
        if cmd in CONJUNTOS_POR_NIVEL[n]:
            return n
    return 5


# ---------------------------------------------------------------------------
# Operadores en lenguaje natural: SiPi ya es mas simple que Python en varias
# cosas, pero seguia obligando a usar simbolos (==, >=, <=, !=) que a alguien
# recien empezando le cuestan mas que las palabras. Esto es 100% ADITIVO: los
# simbolos de toda la vida siguen funcionando identico, esto solo agrega una
# forma mas de escribir lo mismo. Se traduce en memoria antes de ejecutar
# (nunca se reescribe el archivo del usuario), asi que no hay ningun riesgo
# de romper nada existente.
FRASES_COMPARACION_NATURAL = [
    # Mas largas primero, para que "es mayor o igual a" no quede a mitad de
    # camino traducido como "es mayor" + " o igual a" suelto.
    (r"\bes\s+mayor\s+o\s+igual\s+a\b", ">="),
    (r"\bes\s+menor\s+o\s+igual\s+a\b", "<="),
    (r"\bno\s+es\s+igual\s+a\b", "!="),
    (r"\bes\s+distinto\s+de\b", "!="),
    (r"\bes\s+diferente\s+de\b", "!="),
    (r"\bes\s+igual\s+a\b", "=="),
    (r"\bes\s+mayor\s+que\b", ">"),
    (r"\bes\s+menor\s+que\b", "<"),
]

# Palabras aritmeticas: se activan SOLO cuando estan claramente entre dos
# operandos (numero, variable, o cierre de parentesis a la izquierda /
# numero, variable o apertura de parentesis a la derecha). Esto evita que
# se disparen por accidente dentro de una linea que no es una cuenta
# matematica (ej. un comentario que diga "hecho por el usuario").
_OPERANDO_IZQ = r"(?<=[\w\u0900-\u097F\u0980-\u09FF)])"
_OPERANDO_DER = r"(?=[\s]*[\w\u0900-\u097F\u0980-\u09FF(])"
PALABRAS_ARITMETICA_NATURAL = [
    (rf"{_OPERANDO_IZQ}\s+mas\s+{_OPERANDO_DER}", " + "),
    (rf"{_OPERANDO_IZQ}\s+menos\s+{_OPERANDO_DER}", " - "),
    (rf"{_OPERANDO_IZQ}\s+por\s+{_OPERANDO_DER}", " * "),
    (rf"{_OPERANDO_IZQ}\s+dividido\s+entre\s+{_OPERANDO_DER}", " / "),
    (rf"{_OPERANDO_IZQ}\s+entre\s+{_OPERANDO_DER}", " / "),
]

_PATRONES_OPERADORES_NATURALES = [
    (re.compile(patron, re.IGNORECASE), reemplazo)
    for patron, reemplazo in FRASES_COMPARACION_NATURAL + PALABRAS_ARITMETICA_NATURAL
]


def simplificar_operadores_naturales(contenido_completo):
    """Reemplaza frases en lenguaje natural ('es mayor que', 'mas', 'por')
    por su simbolo equivalente (>, +, *...), SOLO fuera de textos entre
    comillas (nunca toca lo que el usuario quiere imprimir tal cual) --
    excepto DENTRO de un {...} de interpolacion, donde el contenido es una
    expresion real que se evalua (ahi si tiene sentido poder escribir
    'decir "El total es {precio mas impuesto}"'). Funciona en cualquier
    nivel y con cualquier idioma ya traducido a espanol; es puramente
    adicional."""
    def _aplicar_patrones(texto):
        for patron, reemplazo in _PATRONES_OPERADORES_NATURALES:
            texto = patron.sub(reemplazo, texto)
        return texto

    lineas_resultado = []
    for linea in contenido_completo.split("\n"):
        segmentos = _dividir_respetando_cadenas(linea)
        for idx in range(len(segmentos)):
            if idx % 2 == 0:  # fuera de comillas: se traduce entero
                segmentos[idx] = _aplicar_patrones(segmentos[idx])
            else:  # es un string literal: solo se traduce dentro de {...}
                segmentos[idx] = PATRON_INTERPOLACION.sub(
                    lambda mi: "{" + _aplicar_patrones(mi.group(1)) + "}", segmentos[idx]
                )
        lineas_resultado.append("".join(segmentos))
    return "\n".join(lineas_resultado)


def extraer_nivel_dificultad(contenido_completo):
    """Busca una directiva '#nivel <nombre>' entre las primeras lineas del
    archivo (puede ir antes o despues de '#idioma', en cualquier orden) y
    la quita del codigo. Devuelve (nivel_numerico_o_None, contenido_sin_la_directiva).
    Sin la directiva, SiPi funciona exactamente como siempre (sin ninguna
    restriccion) -- el sistema de niveles es 100% opt-in."""
    lineas_crudas = contenido_completo.split("\n")
    for i, linea in enumerate(lineas_crudas[:5]):
        limpia = linea.strip()
        if not limpia:
            continue
        m = re.match(r"^#\s*nivel\s+(\w+)\s*$", limpia, re.IGNORECASE)
        if m:
            nombre_nivel = m.group(1).lower()
            if nombre_nivel not in NIVELES_SIPI:
                niveles_disponibles = ", ".join(NOMBRES_NIVELES_SIPI.values())
                raise SiPiError(
                    f"Nivel '{nombre_nivel}' no reconocido en la directiva '#nivel'. "
                    f"Niveles disponibles: {niveles_disponibles}."
                )
            lineas_crudas[i] = ""
            return NIVELES_SIPI[nombre_nivel], "\n".join(lineas_crudas)
        if not limpia.startswith("#"):
            break  # ya empezo el codigo real, no hay mas directivas que buscar
    return None, contenido_completo


def traducir_programa_multilenguaje(contenido_completo):
    """Si el archivo empieza con una directiva '#idioma <codigo>' (ej.
    '#idioma zh'), traduce TODO el codigo de ese idioma a espanol antes de
    seguir, y quita la linea de la directiva. Si no hay directiva (o el
    codigo es 'es'), devuelve el contenido tal cual, sin ningun costo
    extra para los programas que ya estan en espanol."""
    lineas_crudas = contenido_completo.split("\n")
    idx_directiva = None
    codigo_idioma = None
    for i, linea in enumerate(lineas_crudas):
        limpia = linea.strip()
        if not limpia:
            continue
        m = re.match(r"^#\s*idioma\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*$", limpia, re.IGNORECASE)
        if m:
            idx_directiva = i
            codigo_idioma = m.group(1).lower()
        break  # solo la primera linea no vacia cuenta como directiva

    if idx_directiva is None or codigo_idioma in (None, "es"):
        return contenido_completo

    # Item 45 del feedback ("Modo ambos: Español / English / Ambos"): las
    # palabras clave en español SIEMPRE pasan sin traducir (no estan en
    # ninguna tabla de idioma), asi que activar la tabla de ingles ya
    # permite mezclar libremente español e ingles en el mismo archivo sin
    # ningun mecanismo adicional -- 'ambos'/'mixto' son alias explicitos
    # de esa misma tabla, para que la directiva diga lo que el usuario
    # realmente quiere ("quiero poder usar los dos") en vez de tener que
    # saber este detalle interno.
    if codigo_idioma in ("ambos", "mixto", "both"):
        codigo_idioma = "en"

    tabla_idioma = IDIOMAS_SIPI.get(codigo_idioma)
    if tabla_idioma is None:
        idiomas_disponibles = ", ".join(sorted(IDIOMAS_SIPI.keys()))
        raise SiPiError(
            f"Idioma '{codigo_idioma}' no soportado todavia en la directiva '#idioma'. "
            f"Idiomas disponibles por ahora: {idiomas_disponibles} (se iran agregando mas)."
        )

    lineas_crudas[idx_directiva] = ""  # la directiva no es codigo, se quita
    lineas_traducidas = [
        traducir_linea_a_espanol(linea, tabla_idioma) for linea in lineas_crudas
    ]
    return "\n".join(lineas_traducidas)


BLOQUES_QUE_ABREN = {
    "si", "repetir", "mientras", "funcion", "ventana", "crear_juego",
    "para_cada", "intentar", "pestanias", "pestana", "cada", "enum", "estructura",
    "pagina_web", "formulario", "clase", "metodo", "interfaz", "escena_3d",
    "seleccionar", "con_bloqueo",
}

# Cache propia de patrones compilados para las coincidencias de sintaxis del
# interprete (una por cada 'if cmd == ...'). El modulo 're' ya cachea
# internamente los patrones que le pasamos como texto, pero esa cache
# generica tiene el costo extra de un lock + hash del string en cada
# llamada. Como estos patrones de sintaxis se re-evaluan muchisimas veces
# en bucles y funciones (la ruta mas caliente del interprete), tener una
# cache propia, directa y sin ese overhead, se nota de verdad en programas
# con muchas iteraciones o funciones que se llaman miles de veces.
_CACHE_PATRONES_SINTAXIS = {}


def _m(patron, texto, flags=0):
    clave = (patron, flags)
    rx = _CACHE_PATRONES_SINTAXIS.get(clave)
    if rx is None:
        rx = re.compile(patron, flags)
        _CACHE_PATRONES_SINTAXIS[clave] = rx
    return rx.match(texto)


class Interprete:
    def __init__(self, archivo_path):
        self.archivo_path = archivo_path
        self.base_dir = os.path.dirname(os.path.abspath(archivo_path)) or "."
        self.entorno = Entorno()
        self.lineas = []
        self.nivel_dificultad = None  # sin directiva '#nivel': sin restricciones, como siempre
        self.ventana_tk = None
        self.widgets = {}
        self._tk = None
        self._pygame_ctx = None
        self.pila_scopes = []  # ambitos locales de las llamadas a funciones activas (para que la recursion funcione de verdad)
        self.profundidad_bucles = 0  # cuantos bucles nos rodean ahora mismo (para validar 'romper'/'continuar' y que no se escapen de una funcion)
        self._cache_fin_bloque = {}  # memoiza _encontrar_fin: evita re-escanear el mismo bloque (ej. un bucle dentro de una funcion) en cada llamada
        self._hilos_sipi = {}  # id_hilo -> {"hilo": Thread, "terminado": Event, "valor": ..., "error": ...} (ver 'hilo_crear'/'hilo_esperar')
        self._contador_hilos = 0
        self._bloqueos_sipi = {}  # id_bloqueo -> threading.Lock() real (ver 'bloqueo_crear'/'con_bloqueo')

    # ---------- Manejo de ambito de variables (soporta recursion real) ----------

    def _buscar_variable(self, nombre):
        """Busca una variable primero en el ambito local (si estamos dentro
        de una funcion) y despues en el global. Devuelve (valor, encontrada)."""
        for scope in reversed(self.pila_scopes):
            if nombre in scope:
                return scope[nombre], True
        if nombre in self.entorno.variables:
            return self.entorno.variables[nombre], True
        return None, False

    def _existe_variable(self, nombre):
        return self._buscar_variable(nombre)[1]

    def _obtener_variable(self, nombre, default=None):
        valor, encontrada = self._buscar_variable(nombre)
        return valor if encontrada else default

    def _declarar_variable_local(self, nombre, valor):
        """Usado por 'variable'/'const' y por los parametros de una funcion:
        si estamos dentro de una llamada a funcion, crea la variable en el
        ambito local de ESA llamada (no se filtra a otras llamadas ni al
        resto del programa); si no, la crea en el ambito global de siempre."""
        if self.pila_scopes:
            self.pila_scopes[-1][nombre] = valor
        else:
            self.entorno.variables[nombre] = valor

    def _mutar_variable(self, nombre, valor):
        """Usado por 'sumar'/'restar': modifica la variable donde ya exista
        (local si es local, global si es global), para que cosas como
        'sumar puntaje 1' dentro de una funcion sigan afectando la variable
        global de siempre. Si no existe en ningun lado, la crea en el
        ambito actual (local si estamos dentro de una funcion)."""
        for scope in reversed(self.pila_scopes):
            if nombre in scope:
                scope[nombre] = valor
                return
        self.entorno.variables[nombre] = valor

    @staticmethod
    def _parsear_fecha(texto):
        """Convierte 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS' (los formatos que
        devuelve fecha_hora_actual) a datetime. Usado por todos los
        comandos fecha_*, para que acepten tanto fechas simples como
        marcas de tiempo completas de forma transparente."""
        texto = texto.strip()
        for patron in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.datetime.strptime(texto, patron)
            except ValueError:
                continue
        raise SiPiError(f"Fecha invalida: '{texto}'. Se espera formato AAAA-MM-DD u AAAA-MM-DD HH:MM:SS.")

    # ---------- Sistema de tipos opcional (#21) ----------
    # SiPi sigue siendo dinamico por defecto: 'variable x = 5' no exige nada.
    # Pero si el usuario escribe 'variable x: entero = 5', a partir de ahi
    # esa variable queda "marcada" y cualquier reasignacion (variable, sumar,
    # restar) que le de un tipo distinto lanza un SiPiError claro en vez de
    # dejar pasar un bug silencioso. Esto es opt-in: proyectos chicos pueden
    # ignorarlo por completo, proyectos grandes pueden usarlo donde importa.
    _TIPOS_VALIDOS = {"entero", "decimal", "numero", "texto", "booleano", "lista", "diccionario"}

    def _verificar_es_vector(self, comando, valor):
        """Items #71-73: validacion compartida por todos los comandos
        'vector_*' -- un mensaje de error claro (que dice cual es el
        problema real: no es lista, o tiene elementos no numericos) en
        vez de dejar que explote mas abajo con un TypeError de Python
        crudo sobre 'x + y' entre tipos incompatibles."""
        if not isinstance(valor, list):
            raise SiPiError(f"'{comando}' necesita una lista de numeros, recibio: {valor!r}")
        for elemento in valor:
            if not isinstance(elemento, (int, float)) or isinstance(elemento, bool):
                raise SiPiError(f"'{comando}' necesita una lista de SOLO numeros, encontro: {elemento!r}")

    def _verificar_vectores_misma_longitud(self, comando, a, b):
        self._verificar_es_vector(comando, a)
        self._verificar_es_vector(comando, b)
        if len(a) != len(b):
            raise SiPiError(
                f"'{comando}' necesita dos vectores de la misma longitud "
                f"(recibio uno de {len(a)} y otro de {len(b)})."
            )

    def _verificar_tipo(self, nombre, tipo_decl, valor):
        if tipo_decl not in self._TIPOS_VALIDOS:
            raise SiPiError(
                f"Tipo desconocido '{tipo_decl}' para '{nombre}'. "
                f"Tipos validos: {', '.join(sorted(self._TIPOS_VALIDOS))}"
            )
        ok = True
        if tipo_decl == "entero":
            ok = isinstance(valor, int) and not isinstance(valor, bool)
        elif tipo_decl == "decimal":
            ok = isinstance(valor, float) or (isinstance(valor, int) and not isinstance(valor, bool))
        elif tipo_decl == "numero":
            ok = isinstance(valor, (int, float)) and not isinstance(valor, bool)
        elif tipo_decl == "texto":
            ok = isinstance(valor, str)
        elif tipo_decl == "booleano":
            ok = isinstance(valor, bool)
        elif tipo_decl == "lista":
            ok = isinstance(valor, list)
        elif tipo_decl == "diccionario":
            ok = isinstance(valor, dict)
        if not ok:
            raise SiPiError(
                f"Error de tipo: '{nombre}' fue declarada como '{tipo_decl}' "
                f"pero se le intento asignar un valor de tipo '{type(valor).__name__}' ({valor!r})."
            )

    # ---------- Utilidades de parsing ----------

    @staticmethod
    def _preprocesar_contenido(contenido_completo, autocorregir=True):
        """Convierte el texto crudo de un archivo .sipi en una lista de
        (numero_de_linea, linea_limpia), quitando comentarios de una linea
        (//) y de bloque (/* */), codificando cadenas multilinea (triple
        comilla), e infiriendo 'fin' por indentacion cuando el usuario no
        los escribe (ver _inferir_fin_por_indentacion). Se usa tanto para
        el archivo principal como para modulos importados, para que ambos
        soporten exactamente la misma sintaxis.

        Ademas, corrige automaticamente errores tipograficos chicos (ver
        _autocorregir_linea): espacios de mas, comillas curvas, puntos
        sueltos, comandos mal escritos por poco. Devuelve una tupla
        (lineas, correcciones) -- 'correcciones' es una lista de
        (numero_de_linea, descripcion) con todo lo que se corrigio solo,
        vacia si autocorregir=False o si no hizo falta corregir nada."""
        contenido_completo = re.sub(r"/\*.*?\*/", "", contenido_completo, flags=re.DOTALL)

        def _codificar_triple(m):
            interior = m.group(1).replace("\n", "\x01")
            return '"' + interior + '"'
        contenido_completo = re.sub(r'"""(.*?)"""', _codificar_triple, contenido_completo, flags=re.DOTALL)

        crudo = contenido_completo.split("\n")
        # Guardamos cada linea SIN sacarle la indentacion todavia (solo sin
        # comentarios), para poder medir cuantos espacios/tabs tiene antes
        # de decidir si el programa usa indentacion como alternativa a 'fin'.
        con_indentacion = []
        todas_las_correcciones = []
        for i, linea in enumerate(crudo, 1):
            l_sin_comentario = _quitar_comentario_linea(linea)
            if autocorregir:
                l_sin_comentario, correcciones_linea = _autocorregir_linea(i, l_sin_comentario)
                for desc in correcciones_linea:
                    todas_las_correcciones.append((i, desc))
            con_indentacion.append((i, l_sin_comentario))
        lineas_finales = Interprete._inferir_fin_por_indentacion(con_indentacion)
        return lineas_finales, todas_las_correcciones

    @staticmethod
    def _inferir_fin_por_indentacion(con_indentacion):
        """Item 4 de tu feedback: indentacion opcional como alternativa a
        'fin'. Si el CUERPO de un bloque especifico esta mas indentado que
        la linea que lo abre (si/mientras/funcion/clase/etc.), se infiere
        automaticamente donde termina ese bloque por la sangria (como
        Python): cuando la indentacion vuelve al nivel de la linea que
        abrio el bloque (o menos), se inserta un 'fin' invisible ahi.

        Es 100% compatible con el estilo de siempre: si el cuerpo de un
        bloque en particular NO esta mas indentado que su apertura (el
        estilo clasico de SiPi, sin sangria obligatoria), ese bloque
        especifico queda en modo 'solo fin' -- exactamente como funcionaba
        antes, sin inferir nada y exigiendo su 'fin' explicito. Los dos
        estilos pueden mezclarse libremente en el mismo archivo, incluso
        en bloques anidados unos dentro de otros.
        """
        def indentacion_de(texto):
            sin_sangria = texto.lstrip(" \t")
            return len(texto) - len(sin_sangria)

        n = len(con_indentacion)
        resultado = []
        pila = []  # cada item: {"indent": int, "sensible": bool}

        def primera_palabra(texto_stripped):
            return texto_stripped.split(" ", 1)[0] if texto_stripped else ""

        def proximo_no_vacio(desde):
            j = desde
            while j < n:
                _, t = con_indentacion[j]
                if t.strip() != "":
                    return j
                j += 1
            return None

        for idx, (num, texto) in enumerate(con_indentacion):
            stripped = texto.strip()
            if stripped == "":
                resultado.append((num, ""))
                continue

            indent_actual = indentacion_de(texto)
            palabra = primera_palabra(stripped)
            resto_de_la_linea = stripped[len(palabra):].strip()
            es_asignacion = resto_de_la_linea.startswith("=") and not resto_de_la_linea.startswith("==")

            if stripped == "fin":
                # 'fin' explicito: cierra SIEMPRE el bloque mas interno tal
                # cual funcionaba antes, sin importar la indentacion de este
                # 'fin' ni la del bloque. No se hace ningun cierre automatico
                # por sangria en esta linea.
                if pila:
                    pila.pop()
                resultado.append((num, stripped))
                continue

            # 'sino' y 'capturar' son continuaciones del MISMO bloque que
            # abrio 'si'/'intentar' (igual que 'elif'/'else' en Python son
            # parte del mismo 'if', no una linea nueva independiente). A
            # igual indentacion que su bloque, NO deben disparar un cierre
            # automatico -- si lo hicieran, un 'si ... sino ... fin' o
            # 'intentar ... capturar ... fin' indentado normalmente se
            # cortaria mal, insertando un 'fin' antes de 'sino'/'capturar'
            # en vez de dejarlos como parte del mismo bloque.
            if palabra in PALABRAS_MISMO_NIVEL:
                resultado.append((num, stripped))
                continue

            # Antes de procesar la linea, cerramos automaticamente los
            # bloques 'sensibles a indentacion' cuyo cuerpo ya termino
            # (la indentacion actual volvio a su nivel de apertura o menos).
            # Un bloque en modo 'solo fin' (no sensible) nunca se cierra
            # asi -- se detiene la busqueda ahi mismo, para no inferir nada
            # incorrecto por encima de un bloque de estilo clasico.
            while pila and pila[-1]["sensible"] and indent_actual <= pila[-1]["indent"]:
                pila.pop()
                resultado.append((num, "fin"))

            if palabra in BLOQUES_QUE_ABREN and not es_asignacion:
                idx_sig = proximo_no_vacio(idx + 1)
                sensible = False
                if idx_sig is not None:
                    _, texto_sig = con_indentacion[idx_sig]
                    if indentacion_de(texto_sig) > indent_actual:
                        sensible = True
                pila.append({"indent": indent_actual, "sensible": sensible})

            resultado.append((num, stripped))

        # Al llegar al final del archivo, cualquier bloque que haya quedado
        # abierto (sensible a indentacion, sin 'fin' explicito) se cierra
        # ahi -- tal cual pide el punto 4: "...o al final del archivo".
        # Los bloques en modo 'solo fin' que sigan abiertos NO se tocan:
        # deben seguir fallando con el error de "falta fin" de siempre,
        # porque en ese estilo 'fin' es obligatorio y de verdad falta.
        ultimo_num = con_indentacion[-1][0] if con_indentacion else 0
        while pila and pila[-1]["sensible"]:
            pila.pop()
            resultado.append((ultimo_num, "fin"))

        return resultado

    def cargar(self):
        with open(self.archivo_path, "r", encoding="utf-8") as f:
            contenido_completo = f.read()

        self.nivel_dificultad, contenido_completo = extraer_nivel_dificultad(contenido_completo)
        contenido_completo = traducir_programa_multilenguaje(contenido_completo)
        contenido_completo = simplificar_operadores_naturales(contenido_completo)

        # Item 5 de tu feedback: cache de "bytecode" (.sipic). El parseo en
        # si (sacar comentarios, resolver strings triples, inferir 'fin'
        # por indentacion) es barato para un programa chico, pero en un
        # proyecto grande (varios miles de lineas) se nota en cada
        # ejecucion. Si ya existe un .sipic para este archivo Y coincide en
        # tamano+fecha de modificacion con el .sipi actual, se carga
        # directo desde ahi, saltando el parseo entero.
        ruta_cache = self._ruta_cache_bytecode()
        lineas_desde_cache = self._intentar_cargar_cache(ruta_cache, contenido_completo)
        if lineas_desde_cache is not None:
            self.lineas = lineas_desde_cache
            return

        self.lineas, correcciones = self._preprocesar_contenido(contenido_completo)
        self._reportar_correcciones_automaticas(correcciones)
        self._guardar_cache_bytecode(ruta_cache, contenido_completo, self.lineas)

    def _reportar_correcciones_automaticas(self, correcciones):
        """Imprime un resumen de lo que _autocorregir_linea corrigio solo,
        para que el usuario sepa que su codigo cambio y por que (nunca
        corregir en silencio). No toca el archivo en disco -- eso solo
        pasa si se corre con la bandera '--corregir' (ver main()), que
        guarda la version corregida de vuelta en el .sipi."""
        if not correcciones:
            return
        MAX_MOSTRADAS = 15
        print(f"[SiPi] Se corrigieron automáticamente {len(correcciones)} cosa(s) menor(es) en tu código "
              f"(solo en memoria para esta ejecución -- el archivo en disco no cambió; "
              f"corré 'python sipi.py --corregir {os.path.basename(self.archivo_path)}' si querés guardar la corrección):")
        for num_linea, desc in correcciones[:MAX_MOSTRADAS]:
            print(f"  - Línea {num_linea}: {desc}")
        if len(correcciones) > MAX_MOSTRADAS:
            print(f"  ... y {len(correcciones) - MAX_MOSTRADAS} corrección(es) más (se omiten para no saturar la pantalla)")

    def _ruta_cache_bytecode(self):
        return os.path.splitext(self.archivo_path)[0] + ".sipic"

    def _intentar_cargar_cache(self, ruta_cache, contenido_completo):
        """Devuelve las lineas ya parseadas si el .sipic es valido y
        corresponde EXACTAMENTE a este contenido fuente (se compara por
        tamano+hash, no solo la fecha de modificacion, para no arriesgarse
        a usar una cache vieja si el archivo se edito sin que cambiara el
        mtime -- por ejemplo al copiarlo desde otro lado). Cualquier
        problema con la cache (no existe, esta corrupta, version distinta
        de SiPi) hace que se ignore y se parsee normal -- una cache rota
        nunca debe romper la ejecucion del programa."""
        if not os.path.exists(ruta_cache):
            return None
        try:
            with open(ruta_cache, "r", encoding="utf-8") as f:
                datos = json.load(f)
            if datos.get("version_sipi") != VERSION:
                return None
            if datos.get("tamano") != len(contenido_completo):
                return None
            if datos.get("hash") != hashlib.sha256(contenido_completo.encode("utf-8")).hexdigest():
                return None
            return [tuple(par) for par in datos["lineas"]]
        except (json.JSONDecodeError, KeyError, OSError, UnicodeDecodeError):
            return None

    def _guardar_cache_bytecode(self, ruta_cache, contenido_completo, lineas):
        """Guarda la cache para la proxima ejecucion. Si no se puede
        escribir (permisos, disco de solo lectura, etc.) simplemente no
        hay cache -- el programa igual corrio bien con el parseo normal,
        asi que esto nunca debe convertirse en un error visible."""
        try:
            datos = {
                "version_sipi": VERSION,
                "tamano": len(contenido_completo),
                "hash": hashlib.sha256(contenido_completo.encode("utf-8")).hexdigest(),
                "lineas": lineas,
            }
            with open(ruta_cache, "w", encoding="utf-8") as f:
                json.dump(datos, f)
        except OSError:
            pass

    def _resolver_token_numerico(self, token):
        """Resuelve un token (numero literal o nombre de variable) a un
        numero real, para el camino rapido de operaciones binarias simples.
        Devuelve None si el token no es un numero (por ejemplo, texto), para
        que el llamador use el camino general (eval) en ese caso."""
        if es_numero(token):
            v = float(token)
            return int(v) if v == int(v) else v
        valor_var, encontrada = self._buscar_variable(token)
        if encontrada and isinstance(valor_var, (int, float)) and not isinstance(valor_var, bool):
            return valor_var
        return None

    # Item 7 de tu feedback: adaptadores para las funciones de listas que
    # tiene sentido encadenar con el operador pipe '|>'. Cada adaptador
    # traduce los argumentos entre parentesis del estilo pipe
    # ('lista_filtrar(es_par)') a la sintaxis real de ese comando
    # ('lista con es_par'), para no duplicar la logica de cada comando.
    _ADAPTADORES_PIPE = {
        "lista_filtrar": lambda args: f"con {args[0]}",
        "lista_mapear": lambda args: f"con {args[0]}",
        "lista_reducir": lambda args: f"con {args[0]} desde {args[1]}",
        "suma_lista": lambda args: "",
        "promedio_lista": lambda args: "",
        "lista_contiene": lambda args: f"{args[0]}",
        "lista_longitud": lambda args: "",
    }

    def _evaluar_pipe(self, expr):
        """Item 7 de tu feedback: operador pipe |>, para encadenar
        transformaciones de listas sin anidar parentesis ni escribir una
        variable temporal por paso:
            numeros |> lista_filtrar(es_par) |> lista_mapear(doble) |> suma_lista
        Cada etapa despues del primer '|>' debe ser uno de los comandos de
        _ADAPTADORES_PIPE (los que tiene sentido encadenar sobre una
        lista); si se usa un comando no soportado en un pipe, se avisa con
        un error claro en vez de fallar de forma confusa."""
        etapas = [e.strip() for e in expr.split("|>")]
        valor_actual = self.evaluar_expresion(etapas[0])
        nombre_temp = "__pipe_valor__"
        for etapa in etapas[1:]:
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)(?:\((.*)\))?$", etapa)
            if not m:
                raise SiPiError(f"Etapa de pipe invalida: '{etapa}'. Se espera algo como 'comando(args)'.")
            nombre_cmd, args_texto = m.group(1), m.group(2)
            if nombre_cmd not in self._ADAPTADORES_PIPE:
                raise SiPiError(
                    f"'{nombre_cmd}' no se puede usar en un pipe ('|>'). "
                    f"Comandos soportados en pipe: {', '.join(sorted(self._ADAPTADORES_PIPE))}."
                )
            args = [a.strip() for a in args_texto.split(",")] if args_texto else []
            self._declarar_variable_local(nombre_temp, valor_actual)
            resto_adaptado = self._ADAPTADORES_PIPE[nombre_cmd](args)
            linea_sintetica = f"{nombre_temp} {resto_adaptado} -> {nombre_temp}".strip()
            linea_sintetica = re.sub(r"\s+", " ", linea_sintetica)
            self._ejecutar_linea(0, 0, 0, f"{nombre_cmd} {linea_sintetica}")
            valor_actual = self._obtener_variable(nombre_temp)
        return valor_actual

    def evaluar_expresion(self, expr):
        """Evalua una expresion SiPi: soporta variables, texto, numeros y operaciones matematicas basicas."""
        expr = expr.strip()
        if expr == "":
            return ""
        if "|>" in expr:
            return self._evaluar_pipe(expr)
        # Cadena de texto literal (ej. "hola {nombre}"). Importante: verificamos
        # que el string realmente termine ahi (que la primera comilla de cierre
        # sin escapar caiga justo en el ultimo caracter), no solo que el primer
        # y el ultimo caracter sean comillas. Antes, una concatenacion como
        # '"Hola " + nombre + " desde aca!"' tambien empieza y termina con
        # comillas, y se confundia con un unico literal, devolviendo el texto
        # crudo sin evaluar la concatenacion real.
        if expr[0] in "\"'" and _es_texto_literal_puro(expr):
            contenido = expr[1:-1]
            return self.interpolar(contenido)
        # Variable directa
        valor_var, encontrada = self._buscar_variable(expr)
        if encontrada:
            return valor_var
        # Numero
        if es_numero(expr):
            v = float(expr)
            return int(v) if v == int(v) else v
        # Booleanos
        if expr == "verdadero":
            return True
        if expr == "falso":
            return False
        # Item 8 de tu feedback: un valor "nulo" real y distinguible, para
        # poder escribir 'si correo != nulo' y que de verdad signifique
        # "la clave no estaba" en vez de confundirse con un texto vacio.
        if expr == "nulo":
            return None
        if expr == "aleatorio":
            return random.randint(0, 100)

        # Camino rapido: operaciones binarias simples ("a + b", "x * 2", etc.)
        # sin pasar por sustitucion de texto + eval(), que es mucho mas lento.
        m_binaria = _analizar_binaria_simple(expr)
        if m_binaria:
            izq_tok, operador, der_tok = m_binaria
            izq = self._resolver_token_numerico(izq_tok)
            der = self._resolver_token_numerico(der_tok)
            if izq is not None and der is not None:
                try:
                    if operador == "+":
                        return izq + der
                    if operador == "-":
                        return izq - der
                    if operador == "*":
                        return izq * der
                    if operador == "/":
                        return izq / der
                    if operador == "%":
                        return izq % der
                except ZeroDivisionError:
                    pass  # cae al camino general para mantener el mensaje de error habitual

        # Operaciones matematicas / concatenacion con variables: reemplazamos nombres de variables por sus valores
        # Primero resolvemos llamadas a funciones SiPi embebidas en la expresion
        # (ej. "doble(5) + 1", "contar_hasta(n - 1) + 1"). Antes de esto, una
        # llamada a funcion dentro de una expresion simplemente no se evaluaba
        # y la expresion se devolvia como texto crudo sin avisar del error.
        expr_con_llamadas, hubo_llamadas = self._sustituir_llamadas_funcion(expr)
        if hubo_llamadas:
            expr = expr_con_llamadas
        expr_sustituida = self._sustituir_variables_en_expr(expr)
        # Concatenacion de texto con '+'
        try:
            resultado = eval(expr_sustituida, {"__builtins__": {}}, {})
            return resultado
        except ZeroDivisionError:
            raise SiPiError(
                f"Division por cero al evaluar la expresion '{expr.strip()}'."
            )
        except (NameError, SyntaxError):
            # Lo mas probable es que sea una variable no declarada (un typo)
            # o el nombre de una funcion que no existe. Antes esto se
            # devolvia en silencio como el texto crudo de la expresion, lo
            # que ocultaba errores de tipeo (parecia que "funcionaba" pero
            # mostraba el nombre de la variable en vez de su valor).
            expr_simple = expr.strip()
            if PATRON_IDENTIFICADOR.fullmatch(expr_simple):
                sugerencia = self._sugerir_nombre_parecido(expr_simple)
                mensaje = f"Variable no declarada: '{expr_simple}'."
                if sugerencia:
                    mensaje += f" ¿Quisiste decir '{sugerencia}'?"
                else:
                    mensaje += f" Definila antes con 'variable {expr_simple} = ...' o revisa si tiene un error de tipeo."
                raise SiPiError(mensaje)
            return self.interpolar(expr)
        except TypeError:
            # Caso MUY comun: concatenar texto con un numero usando '+'
            # (ej. "Puntaje: " + puntaje). Python no convierte automaticamente
            # un numero a texto al sumarlo con un string (tira TypeError), pero
            # en SiPi eso deberia funcionar como en la mayoria de los lenguajes
            # pensados para principiantes. Antes esto cerraba en el fallback
            # generico de mas abajo y devolvia el texto crudo sin evaluar.
            try:
                return self._evaluar_con_coercion_de_texto(expr_sustituida)
            except Exception:
                return self.interpolar(expr)
        except Exception:
            # Si falla por otro motivo (una expresion rara, no una simple
            # variable suelta), devolvemos como texto interpolado para no
            # romper usos flexibles del lenguaje.
            return self.interpolar(expr)

    def _sugerir_nombre_parecido(self, nombre):
        """Busca, entre las variables y funciones conocidas en este punto del
        programa, el nombre mas parecido a 'nombre' (para sugerir una
        correccion de typo en los mensajes de error)."""
        candidatos = set(self.entorno.variables.keys())
        for scope in self.pila_scopes:
            candidatos.update(scope.keys())
        candidatos.update(self.entorno.funciones.keys())
        coincidencias = difflib.get_close_matches(nombre, list(candidatos), n=1, cutoff=0.6)
        return coincidencias[0] if coincidencias else None

    def _evaluar_con_coercion_de_texto(self, expr_sustituida):
        """Reevalua una expresion ya sustituida (solo literales, sin nombres
        de variables) nodo por nodo, tratando '+' entre texto y numero como
        concatenacion (convirtiendo el numero a texto), en vez de fallar
        como hace el '+' nativo de Python. Solo soporta lo que puede
        aparecer en una expresion de SiPi ya sustituida: numeros, texto,
        listas, diccionarios, operadores aritmeticos/comparacion/booleanos."""
        arbol = ast.parse(expr_sustituida, mode="eval")
        return self._evaluar_nodo_ast(arbol.body)

    def _evaluar_nodo_ast(self, nodo):
        if isinstance(nodo, ast.Constant):
            return nodo.value
        if isinstance(nodo, ast.List):
            return [self._evaluar_nodo_ast(e) for e in nodo.elts]
        if isinstance(nodo, ast.Dict):
            return {self._evaluar_nodo_ast(k): self._evaluar_nodo_ast(v) for k, v in zip(nodo.keys, nodo.values)}
        if isinstance(nodo, ast.UnaryOp):
            valor = self._evaluar_nodo_ast(nodo.operand)
            if isinstance(nodo.op, ast.USub):
                return -valor
            if isinstance(nodo.op, ast.UAdd):
                return +valor
            if isinstance(nodo.op, ast.Not):
                return not valor
        if isinstance(nodo, ast.BoolOp):
            valores = [self._evaluar_nodo_ast(v) for v in nodo.values]
            return all(valores) if isinstance(nodo.op, ast.And) else any(valores)
        if isinstance(nodo, ast.Compare):
            izq = self._evaluar_nodo_ast(nodo.left)
            resultado = True
            for op, comparador in zip(nodo.ops, nodo.comparators):
                der = self._evaluar_nodo_ast(comparador)
                if isinstance(op, ast.Eq):
                    resultado = resultado and (izq == der)
                elif isinstance(op, ast.NotEq):
                    resultado = resultado and (izq != der)
                elif isinstance(op, ast.Lt):
                    resultado = resultado and (izq < der)
                elif isinstance(op, ast.LtE):
                    resultado = resultado and (izq <= der)
                elif isinstance(op, ast.Gt):
                    resultado = resultado and (izq > der)
                elif isinstance(op, ast.GtE):
                    resultado = resultado and (izq >= der)
                else:
                    raise ValueError("Comparacion no soportada")
                izq = der
            return resultado
        if isinstance(nodo, ast.BinOp):
            izq = self._evaluar_nodo_ast(nodo.left)
            der = self._evaluar_nodo_ast(nodo.right)
            if isinstance(nodo.op, ast.Add):
                if isinstance(izq, str) or isinstance(der, str):
                    return self._formatear_valor(izq) + self._formatear_valor(der)
                return izq + der
            if isinstance(nodo.op, ast.Sub):
                return izq - der
            if isinstance(nodo.op, ast.Mult):
                if isinstance(izq, str) and isinstance(der, (int, float)):
                    return izq * int(der)
                if isinstance(der, str) and isinstance(izq, (int, float)):
                    return der * int(izq)
                return izq * der
            if isinstance(nodo.op, ast.Div):
                return izq / der
            if isinstance(nodo.op, ast.FloorDiv):
                return izq // der
            if isinstance(nodo.op, ast.Mod):
                return izq % der
            if isinstance(nodo.op, ast.Pow):
                return izq ** der
            raise ValueError("Operador no soportado")
        raise ValueError(f"No se pudo evaluar este tipo de expresion: {ast.dump(nodo)}")

    def _es_literal_de_texto_simple(self, expr):
        """True si 'expr' es exactamente UN string literal completo (la
        comilla de apertura y de cierre son un unico par que abarca toda la
        expresion), y no una concatenacion mas grande que solo da la
        casualidad de empezar y terminar con comillas."""
        comilla = expr[0]
        i = 1
        while i < len(expr):
            if expr[i] == comilla:
                return i == len(expr) - 1
            i += 1
        return False

    def _sustituir_llamadas_funcion(self, expr):
        """Busca llamadas a funciones SiPi definidas por el usuario dentro de
        una expresion (ej. 'doble(5) + 1') y las reemplaza por su resultado
        ya evaluado, respetando comillas y parentesis anidados. Devuelve
        (expresion_resultante, hubo_alguna_llamada)."""
        resultado = []
        i = 0
        n = len(expr)
        hubo_llamadas = False
        while i < n:
            c = expr[i]
            if c in "\"'":
                j = i + 1
                while j < n and expr[j] != c:
                    j += 1
                resultado.append(expr[i:min(j + 1, n)])
                i = j + 1
                continue
            m = PATRON_IDENTIFICADOR.match(expr, i)
            if m:
                nombre = m.group(0)
                k = m.end()
                while k < n and expr[k] == " ":
                    k += 1
                if k < n and expr[k] == "(" and nombre in self.entorno.funciones:
                    profundidad = 1
                    p = k + 1
                    while p < n and profundidad > 0:
                        if expr[p] == "(":
                            profundidad += 1
                        elif expr[p] == ")":
                            profundidad -= 1
                        p += 1
                    args_str = expr[k + 1:p - 1]
                    args = self._dividir_args_nivel_superior(args_str)
                    valores = [self.evaluar_expresion(a) for a in args if a.strip() != ""]
                    valor_resultado = self._invocar_funcion_con_valores(nombre, valores)
                    resultado.append(self._valor_a_literal_python(valor_resultado))
                    i = p
                    hubo_llamadas = True
                    continue
                resultado.append(nombre)
                i = m.end()
                continue
            resultado.append(c)
            i += 1
        return "".join(resultado), hubo_llamadas

    def _dividir_args_nivel_superior(self, texto):
        """Divide 'a, b, c' en ['a', 'b', 'c'] sin romper comas que estan
        dentro de parentesis anidados o de un string literal."""
        args = []
        actual = []
        profundidad = 0
        en_comilla = None
        for c in texto:
            if en_comilla:
                actual.append(c)
                if c == en_comilla:
                    en_comilla = None
                continue
            if c in "\"'":
                en_comilla = c
                actual.append(c)
                continue
            if c in "([":
                profundidad += 1
                actual.append(c)
                continue
            if c in ")]":
                profundidad -= 1
                actual.append(c)
                continue
            if c == "," and profundidad == 0:
                args.append("".join(actual))
                actual = []
                continue
            actual.append(c)
        if actual:
            args.append("".join(actual))
        return args

    def _valor_a_literal_python(self, valor):
        """Convierte un valor de Python real (el resultado de invocar una
        funcion SiPi) en un literal que 'eval()' pueda re-interpretar de
        forma segura como parte de una expresion mas grande."""
        if isinstance(valor, bool):
            return "True" if valor else "False"
        if valor is None:
            return "None"
        if isinstance(valor, (int, float)):
            return repr(valor)
        if isinstance(valor, str):
            return json.dumps(valor)
        if isinstance(valor, list):
            return "[" + ", ".join(self._valor_a_literal_python(v) for v in valor) + "]"
        if isinstance(valor, dict):
            return "{" + ", ".join(f"{json.dumps(str(k))}: {self._valor_a_literal_python(v)}" for k, v in valor.items()) + "}"
        return json.dumps(str(valor))

    def _sustituir_variables_en_expr(self, expr):
        """Reemplaza nombres de variables por su valor dentro de una
        expresion, SIN tocar el contenido de los strings literales. Antes
        se usaba un regex.sub sobre toda la expresion de una, lo que
        corrompia el texto si un string literal contenia una palabra que
        tambien era el nombre de una variable (ej. la variable 'vida' hacia
        que el texto literal " de vida" se convirtiera en " de 100")."""
        resultado = []
        i = 0
        n = len(expr)
        while i < n:
            c = expr[i]
            if c in "\"'":
                j = i + 1
                while j < n and expr[j] != c:
                    j += 1
                literal_completo = expr[i:min(j + 1, n)]
                # Decodificar escapes de Python (\n, \t, etc.) tal como
                # hacia eval() antes de forma implicita, ANTES de
                # interpolar {variable} -- si se interpola primero sobre
                # el texto crudo (todavia con los backslashes sin
                # procesar) y despues se vuelve a codificar con
                # json.dumps, un '\n' termina como el texto literal de
                # dos caracteres 'backslash + n' en vez de un salto de
                # linea real (bug encontrado probando esto mismo).
                try:
                    texto_decodificado = ast.literal_eval(literal_completo)
                except (ValueError, SyntaxError):
                    texto_decodificado = literal_completo[1:-1]  # fallback: sin decodificar escapes
                texto_interpolado = self.interpolar(texto_decodificado)
                resultado.append(json.dumps(texto_interpolado))
                i = j + 1
                continue
            m = PATRON_IDENTIFICADOR.match(expr, i)
            if m:
                nombre = m.group(0)
                valor_var, encontrada = self._buscar_variable(nombre)
                if encontrada:
                    resultado.append(json.dumps(valor_var) if isinstance(valor_var, str) else str(valor_var))
                else:
                    resultado.append(nombre)
                i = m.end()
                continue
            resultado.append(c)
            i += 1
        return "".join(resultado)

    def _texto_color(self, expr):
        """Como _texto_o_variable, pero pensado para argumentos de color
        (sprite, rectangulo, etc.): si es una palabra suelta sin comillas
        que coincide con un color conocido (COLORES_ESPANOL) Y no hay
        ninguna variable declarada con ese nombre, se usa directo como
        color, sin exigir comillas. Antes 'sprite j 1 1 1 1 azul' (sin
        comillas) fallaba con 'Variable no declarada: azul' -- un papercut
        comun, ya que en los ejemplos casi siempre se escribe con comillas
        pero nada en la sintaxis avisaba que hacia falta. Si el nombre SI
        esta declarado como variable, se respeta esa variable (compatibilidad
        con 'variable miColor = "rojo" ... sprite j 1 1 1 1 miColor').
        """
        expr = expr.strip()
        m = _m(r'^"([^"]*)"$', expr)
        if m:
            return self.interpolar(m.group(1))
        if PATRON_IDENTIFICADOR.fullmatch(expr) and expr in COLORES_ESPANOL and not self._existe_variable(expr):
            return expr
        return str(self.evaluar_expresion(expr))

    def _texto_o_variable(self, expr):
        """Acepta un argumento de texto ya sea como literal entre comillas
        (con interpolacion de {variables}) o como una variable/expresion sin
        comillas, y devuelve siempre el texto real resultante. Esto permite
        que comandos como leer_archivo funcionen tanto con "archivo.txt"
        como con una variable que contenga el nombre del archivo."""
        expr = expr.strip()
        m = _m(r'^"([^"]*)"$', expr)
        if m:
            return self.interpolar(m.group(1))
        return str(self.evaluar_expresion(expr))

    def _copiar_si_mutable(self, valor):
        """Devuelve una copia independiente si el valor es una lista o
        diccionario, para evitar que dos celdas/elementos distintos terminen
        compartiendo el mismo objeto por error (aliasing)."""
        if isinstance(valor, (list, dict)):
            return copy.deepcopy(valor)
        return valor

    def _formatear_valor(self, valor):
        """Formatea valores para mostrarlos de forma consistente con el lenguaje SiPi."""
        if valor is None:
            return "nulo"
        if isinstance(valor, bool):
            return "verdadero" if valor else "falso"
        if isinstance(valor, list):
            return "[" + ", ".join(self._formatear_valor(v) for v in valor) + "]"
        return str(valor)

    def interpolar(self, texto):
        """Reemplaza {variable} dentro de un texto por su valor real."""
        def reemplazar(m):
            nombre = m.group(1).strip()
            valor_var, encontrada = self._buscar_variable(nombre)
            if encontrada:
                return self._formatear_valor(valor_var)
            try:
                resultado = self.evaluar_expresion(nombre)
            except SiPiError:
                raise
            return self._formatear_valor(resultado)
        resultado = PATRON_INTERPOLACION.sub(reemplazar, texto)
        return resultado.replace("\x01", "\n")

    # ---------- Motor principal ----------

    def ejecutar(self):
        self.cargar()
        try:
            self._ejecutar_bloque(0, len(self.lineas))
        except RetornoFuncion:
            pass
        except DepuracionDetenida:
            pass
        except RomperBucle:
            raise SiPiError("Se uso 'romper' fuera de un bucle (mientras/repetir/para_cada).")
        except ContinuarBucle:
            raise SiPiError("Se uso 'continuar' fuera de un bucle (mientras/repetir/para_cada).")

    def _modulos_importados(self):
        """Devuelve el conjunto (compartido entre modulos) de rutas ya importadas,
        para evitar ciclos infinitos de 'importar'."""
        if not hasattr(self, "_modulos_compartidos"):
            self._modulos_compartidos = {os.path.abspath(self.archivo_path)}
        return self._modulos_compartidos

    def _encontrar_fin(self, inicio, apertura, cierre="fin"):
        clave_cache = (id(self.lineas), inicio)
        encontrado = self._cache_fin_bloque.get(clave_cache)
        if encontrado is not None:
            return encontrado
        profundidad = 1
        i = inicio + 1
        while i < len(self.lineas):
            _, l = self.lineas[i]
            palabra = l.split(" ")[0] if l else ""
            # Una linea como 'clase = 0' (un campo llamado igual que una
            # palabra reservada, ej. dentro de una 'estructura') NO es una
            # apertura de bloque real, aunque su primera palabra coincida
            # con una. Sin este chequeo, agregar una palabra clave nueva
            # (como 'clase' para el sistema de POO) podia romper cualquier
            # programa que ya tuviera una variable/campo con ese mismo
            # nombre, contando de mas los 'fin' y perdiendo la cuenta real.
            resto_de_la_linea = l[len(palabra):].strip()
            es_asignacion = resto_de_la_linea.startswith("=") and not resto_de_la_linea.startswith("==")
            if palabra in apertura and not es_asignacion:
                profundidad += 1
            elif palabra == cierre:
                profundidad -= 1
                if profundidad == 0:
                    self._cache_fin_bloque[clave_cache] = i
                    return i
            i += 1
        # Item 3 critico de tu feedback: en vez de solo decir 'no se
        # encontro fin', decimos que TIPO de bloque quedo sin cerrar
        # (si/mientras/funcion/etc.), en que linea empezo, y que la
        # busqueda llego hasta el final del archivo sin encontrarlo -- asi
        # el usuario sabe exactamente donde mirar en vez de tener que
        # revisar linea por linea un bloque de 50 lineas.
        num_inicio, texto_inicio = self.lineas[inicio]
        palabra_apertura = texto_inicio.split(" ")[0] if texto_inicio else "?"
        ultima_linea = self.lineas[-1][0] if self.lineas else num_inicio
        raise SiPiError(
            f"El bloque '{palabra_apertura}' que abriste en la linea {num_inicio} "
            f"no tiene su '{cierre}'. Se busco un '{cierre}' que lo cierre desde ahi "
            f"hasta el final del archivo (linea {ultima_linea}) y no aparecio. "
            f"Revisa que cada bloque que abras con '{palabra_apertura}' (u otro bloque "
            f"anidado adentro) tenga su '{cierre}' correspondiente."
        )

    def _ejecutar_bloque(self, inicio, fin_idx):
        i = inicio
        while i < fin_idx:
            num, linea = self.lineas[i]
            if linea == "":
                i += 1
                continue
            if getattr(self, "debug", False):
                print(f"[DEBUG] Linea {num}: {linea}")
            gancho = getattr(self, "hook_linea", None)
            if gancho is not None:
                gancho(num, linea)
            try:
                salto = self._ejecutar_linea(i, fin_idx, num, linea)
            except SiPiError as e:
                if not e.pila:
                    e.pila = list(getattr(self, "pila_llamadas", []))
                # Si el error ya viaja sin info de linea (por ejemplo, uno
                # lanzado desde muy adentro de una funcion auxiliar que no
                # tenia el numero de linea a mano), se completa aca con la
                # linea que se estaba ejecutando en este nivel -- mejor un
                # dato aproximado (la linea que llamo a lo que fallo) que
                # ninguno.
                if e.num_linea is None:
                    e.num_linea = num
                    e.texto_linea = linea
                    e.archivo = self.archivo_path
                raise
            except RetornoFuncion:
                raise
            except (RomperBucle, ContinuarBucle):
                raise
            except DepuracionDetenida:
                raise
            except Exception as e:
                raise SiPiError(
                    f"Error en linea {num}: {e}",
                    pila=list(getattr(self, "pila_llamadas", [])),
                    num_linea=num, texto_linea=linea, archivo=self.archivo_path,
                )
            if salto is not None:
                i = salto
            else:
                i += 1

    def _ejecutar_linea(self, i, fin_idx, num, linea):
        partes = linea.split(" ", 1)
        cmd = partes[0]
        resto = partes[1] if len(partes) > 1 else ""

        # ----- Sistema de niveles de dificultad (100% opt-in) -----
        # Solo se activa si el programa declaro '#nivel <nombre>' al
        # principio (o llamo al comando 'nivel'); sin eso, SiPi funciona
        # exactamente igual que siempre, sin restricciones de ningun tipo.
        if self.nivel_dificultad is not None and self.nivel_dificultad < 5 and cmd in COMANDOS_CONOCIDOS_SET:
            permitidos_en_este_nivel = CONJUNTOS_POR_NIVEL[self.nivel_dificultad]
            if cmd not in permitidos_en_este_nivel:
                nivel_necesario = _nivel_que_desbloquea_comando(cmd)
                nombre_necesario = NOMBRES_NIVELES_SIPI[nivel_necesario]
                nombre_actual = NOMBRES_NIVELES_SIPI[self.nivel_dificultad]
                raise SiPiError(
                    f"El comando '{cmd}' todavia no esta disponible en el nivel '{nombre_actual}'. "
                    f"Es un comando de nivel '{nombre_necesario}' o superior.\n"
                    f"       Para desbloquearlo, cambia la primera linea de tu programa a "
                    f"'#nivel {nombre_necesario}' (o cualquier nivel mas alto) cuando te sientas listo. "
                    f"Los niveles son: principiante -> facil -> medio -> dificil -> extremo, "
                    f"cada uno suma mas herramientas al anterior, nunca saca nada."
                )

        if cmd == "nivel":
            nombre_nuevo = resto.strip().strip('"').strip().lower()
            if nombre_nuevo not in NIVELES_SIPI:
                niveles_disponibles = ", ".join(NOMBRES_NIVELES_SIPI.values())
                raise SiPiError(f"Nivel '{nombre_nuevo}' no reconocido. Niveles disponibles: {niveles_disponibles}.")
            self.nivel_dificultad = NIVELES_SIPI[nombre_nuevo]
            print(f"[SiPi] Nivel cambiado a '{NOMBRES_NIVELES_SIPI[self.nivel_dificultad]}' desde aca en adelante.")
            return None

        # ----- Programa / metadatos -----
        if cmd == "programa":
            return None
        if cmd == "version":
            return None

        # ----- Modulos (importar otro archivo .sipi) -----
        if cmd == "importar":
            m = _m(r'^"([^"]+)"$', resto)
            if m:
                ruta_importar = os.path.abspath(os.path.join(self.base_dir, m.group(1)))
                if not os.path.exists(ruta_importar):
                    raise SiPiError(f"No se encontro el modulo: {ruta_importar}")

                modulos_ya_importados = self._modulos_importados()
                if ruta_importar in modulos_ya_importados:
                    print(f"[SiPi] El modulo '{m.group(1)}' ya fue importado antes, se omite (evita ciclos infinitos).")
                    return None
                modulos_ya_importados.add(ruta_importar)

                with open(ruta_importar, "r", encoding="utf-8") as f:
                    contenido_modulo = f.read()
                _, contenido_modulo = extraer_nivel_dificultad(contenido_modulo)
                contenido_modulo = traducir_programa_multilenguaje(contenido_modulo)
                contenido_modulo = simplificar_operadores_naturales(contenido_modulo)
                lineas_modulo, correcciones_modulo = self._preprocesar_contenido(contenido_modulo)
                if correcciones_modulo:
                    print(f"[SiPi] Se corrigieron automáticamente {len(correcciones_modulo)} cosa(s) menor(es) "
                          f"en el módulo '{os.path.basename(ruta_importar)}' (solo en memoria):")
                    for num_linea, desc in correcciones_modulo[:10]:
                        print(f"  - Línea {num_linea}: {desc}")
                interprete_modulo = Interprete(ruta_importar)
                interprete_modulo.entorno = self.entorno
                interprete_modulo.lineas = lineas_modulo
                interprete_modulo.base_dir = os.path.dirname(ruta_importar) or "."
                interprete_modulo.debug = getattr(self, "debug", False)
                interprete_modulo._modulos_compartidos = modulos_ya_importados
                interprete_modulo.pila_scopes = self.pila_scopes
                interprete_modulo.pila_llamadas = getattr(self, "pila_llamadas", [])
                try:
                    interprete_modulo._ejecutar_bloque(0, len(lineas_modulo))
                except RetornoFuncion:
                    pass
                print(f"[SiPi] Modulo importado: {m.group(1)}")
            return None

        # ----- Modo de depuracion paso a paso -----
        if cmd == "modo_debug":
            self.debug = True
            print("[SiPi] Modo debug activado: se mostrara cada linea antes de ejecutarla.")
            return None

        # ----- Documentacion interactiva (item de la lista: 'ayuda mostrar') -----
        if cmd == "ayuda":
            resto_limpio = resto.strip().strip('"').strip()
            if resto_limpio == "":
                print("[SiPi] Escribi 'ayuda \"nombre_comando\"' para ver que hace un comando.")
                print(f"[SiPi] Comandos con ayuda disponible: {', '.join(sorted(AYUDA_COMANDOS.keys()))}")
                print("[SiPi] Para la referencia completa de los 170 comandos, ver DOCUMENTACION.md")
            elif resto_limpio in AYUDA_COMANDOS:
                resumen, ejemplo = AYUDA_COMANDOS[resto_limpio]
                print(f"[SiPi] {resto_limpio}: {resumen}")
                print(f"[SiPi] Ejemplo:\n{ejemplo}")
                caso_de_uso = AYUDA_CASOS_DE_USO.get(resto_limpio)
                if caso_de_uso:
                    print(f"[SiPi] Util para: {caso_de_uso}")
            else:
                sugerencia = difflib.get_close_matches(resto_limpio, list(AYUDA_COMANDOS.keys()) + COMANDOS_CONOCIDOS, n=1, cutoff=0.6)
                if resto_limpio in COMANDOS_CONOCIDOS:
                    print(f"[SiPi] '{resto_limpio}' es un comando valido, pero todavia no tiene una ficha de ayuda corta.")
                    caso_de_uso = AYUDA_CASOS_DE_USO.get(resto_limpio)
                    if caso_de_uso:
                        print(f"[SiPi] Util para: {caso_de_uso}")
                    print("[SiPi] Buscalo en DOCUMENTACION.md para ver su sintaxis completa.")
                elif sugerencia:
                    print(f"[SiPi] No encontre ayuda para '{resto_limpio}'. ¿Quisiste decir '{sugerencia[0]}'?")
                else:
                    print(f"[SiPi] No encontre ayuda para '{resto_limpio}'.")
            return None

        # ----- Modo principiante: errores con mas contexto y consejos -----
        if cmd == "modo_principiante":
            self.modo_principiante = True
            print("[SiPi] Modo principiante activado: los errores van a incluir consejos extra.")
            return None

        # ----- Variables -----
        if cmd == "const":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*(?::\s*([\w\u0900-\u097F\u0980-\u09FF]+)\s*)?=\s*(.+)$", resto)
            if not m:
                raise SiPiError(f"Sintaxis invalida en 'const': {resto}")
            nombre, tipo_decl, expr = m.group(1), m.group(2), m.group(3)
            if nombre in self.entorno.constantes:
                raise SiPiError(f"No se puede redefinir la constante '{nombre}'")
            valor = self._copiar_si_mutable(self.evaluar_expresion(expr))
            if tipo_decl:
                self._verificar_tipo(nombre, tipo_decl, valor)
                self.entorno.tipos_variables[nombre] = tipo_decl
            self._declarar_variable_local(nombre, valor)
            self.entorno.constantes.add(nombre)
            return None

        if cmd == "variable" or cmd == "var":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*(?::\s*([\w\u0900-\u097F\u0980-\u09FF]+)\s*)?=\s*(.+)$", resto)
            if not m:
                raise SiPiError(f"Sintaxis invalida en 'variable': {resto}")
            nombre, tipo_decl, expr = m.group(1), m.group(2), m.group(3)
            if nombre in self.entorno.constantes:
                raise SiPiError(f"No se puede modificar la constante '{nombre}'")
            valor = self._copiar_si_mutable(self.evaluar_expresion(expr))
            if tipo_decl:
                self._verificar_tipo(nombre, tipo_decl, valor)
                self.entorno.tipos_variables[nombre] = tipo_decl
            elif nombre in self.entorno.tipos_variables:
                self._verificar_tipo(nombre, self.entorno.tipos_variables[nombre], valor)
            self._declarar_variable_local(nombre, valor)
            return None

        if cmd == "sumar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
            nombre, expr = m.group(1), m.group(2)
            if nombre in self.entorno.constantes:
                raise SiPiError(f"No se puede modificar la constante '{nombre}'")
            actual = self._obtener_variable(nombre, 0)
            nuevo_valor = actual + self.evaluar_expresion(expr)
            if nombre in self.entorno.tipos_variables:
                self._verificar_tipo(nombre, self.entorno.tipos_variables[nombre], nuevo_valor)
            self._mutar_variable(nombre, nuevo_valor)
            return None

        if cmd == "restar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
            nombre, expr = m.group(1), m.group(2)
            if nombre in self.entorno.constantes:
                raise SiPiError(f"No se puede modificar la constante '{nombre}'")
            actual = self._obtener_variable(nombre, 0)
            nuevo_valor = actual - self.evaluar_expresion(expr)
            if nombre in self.entorno.tipos_variables:
                self._verificar_tipo(nombre, self.entorno.tipos_variables[nombre], nuevo_valor)
            self._mutar_variable(nombre, nuevo_valor)
            return None

        # ----- Salida -----
        if cmd == "decir" or cmd == "imprimir":
            valor = self.evaluar_expresion(resto)
            print(self._formatear_valor(valor))
            return None

        if cmd == "preguntar":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                pregunta, var = self._texto_o_variable(m.group(1)), m.group(2)
                respuesta = input(pregunta + " ")
                if es_numero(respuesta):
                    v = float(respuesta)
                    self._declarar_variable_local(var, int(v) if v == int(v) else v)
                else:
                    self._declarar_variable_local(var, respuesta)
            return None

        # ----- Condicionales -----
        if cmd == "si":
            condicion = resto.strip()
            fin_si = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            # buscar 'sino' al mismo nivel
            idx_sino = None
            profundidad = 1
            j = i + 1
            while j < fin_si:
                _, lj = self.lineas[j]
                palabra = lj.split(" ")[0] if lj else ""
                resto_lj = lj[len(palabra):].strip()
                es_asignacion_lj = resto_lj.startswith("=") and not resto_lj.startswith("==")
                if palabra in BLOQUES_QUE_ABREN and not es_asignacion_lj:
                    profundidad += 1
                elif palabra == "fin":
                    profundidad -= 1
                elif palabra == "sino" and profundidad == 1:
                    idx_sino = j
                j += 1

            resultado_cond = self._evaluar_condicion(condicion)
            if resultado_cond:
                bloque_fin = idx_sino if idx_sino is not None else fin_si
                self._ejecutar_bloque(i + 1, bloque_fin)
            elif idx_sino is not None:
                self._ejecutar_bloque(idx_sino + 1, fin_si)
            return fin_si + 1

        # ----- Pattern matching: seleccionar/caso/otro -----
        if cmd == "seleccionar":
            expr_seleccionar = resto.strip()
            fin_sel = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            marcadores = []  # (indice_linea, "caso"|"otro", texto_valor_o_None)
            profundidad = 1
            j = i + 1
            while j < fin_sel:
                _, lj = self.lineas[j]
                palabra = lj.split(" ", 1)[0] if lj else ""
                resto_lj = lj[len(palabra):].strip()
                es_asignacion_lj = resto_lj.startswith("=") and not resto_lj.startswith("==")
                if palabra in BLOQUES_QUE_ABREN and not es_asignacion_lj:
                    profundidad += 1
                elif palabra == "fin":
                    profundidad -= 1
                elif palabra == "caso" and profundidad == 1:
                    marcadores.append((j, "caso", resto_lj))
                elif palabra == "otro" and profundidad == 1:
                    marcadores.append((j, "otro", None))
                j += 1

            valor_seleccionado = self.evaluar_expresion(expr_seleccionar)
            idx_elegido = None
            fin_bloque_elegido = fin_sel
            for k, (idx_m, tipo_m, valor_expr_m) in enumerate(marcadores):
                if tipo_m != "caso":
                    continue
                if self.evaluar_expresion(valor_expr_m) == valor_seleccionado:
                    idx_elegido = idx_m
                    fin_bloque_elegido = marcadores[k + 1][0] if k + 1 < len(marcadores) else fin_sel
                    break
            if idx_elegido is None:
                for k, (idx_m, tipo_m, _) in enumerate(marcadores):
                    if tipo_m == "otro":
                        idx_elegido = idx_m
                        fin_bloque_elegido = marcadores[k + 1][0] if k + 1 < len(marcadores) else fin_sel
                        break
            if idx_elegido is not None:
                self._ejecutar_bloque(idx_elegido + 1, fin_bloque_elegido)
            return fin_sel + 1

        # ----- Bucles -----
        if cmd == "repetir":
            m = _m(r"^(.+?)\s+veces$", resto)
            fin_rep = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                veces = int(self.evaluar_expresion(m.group(1)))
                self.profundidad_bucles += 1
                try:
                    for _ in range(veces):
                        try:
                            self._ejecutar_bloque(i + 1, fin_rep)
                        except ContinuarBucle:
                            continue
                        except RomperBucle:
                            break
                finally:
                    self.profundidad_bucles -= 1
            return fin_rep + 1

        if cmd == "romper":
            if self.profundidad_bucles <= 0:
                raise SiPiError("Se uso 'romper' fuera de un bucle (mientras/repetir/para_cada).")
            raise RomperBucle()

        if cmd == "continuar":
            if self.profundidad_bucles <= 0:
                raise SiPiError("Se uso 'continuar' fuera de un bucle (mientras/repetir/para_cada).")
            raise ContinuarBucle()

        if cmd == "mientras":
            condicion = resto.strip()
            fin_mientras = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            limite_seguridad = 0
            self.profundidad_bucles += 1
            try:
                while self._evaluar_condicion(condicion) and limite_seguridad < 1000000:
                    try:
                        self._ejecutar_bloque(i + 1, fin_mientras)
                    except ContinuarBucle:
                        pass
                    except RomperBucle:
                        break
                    limite_seguridad += 1
            finally:
                self.profundidad_bucles -= 1
            return fin_mientras + 1

        # ----- Funciones -----
        if cmd == "funcion":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)(?:\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+))?$", resto.strip())
            fin_fn = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                nombre = m.group(1)
                params_info = self._parsear_parametros(m.group(2))
                tipo_retorno = m.group(3)
                self.entorno.funciones[nombre] = (params_info, i + 1, fin_fn, self.lineas, tipo_retorno)
            return fin_fn + 1

        if cmd == "llamar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$", resto.strip())
            if m:
                nombre = m.group(1)
                args_txt = [a.strip() for a in m.group(2).split(",") if a.strip() != ""]
                self._invocar_funcion(nombre, args_txt)
            return None

        if cmd == "llamar_valor":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                nombre, args_str, var_destino = m.groups()
                args_txt = [a.strip() for a in args_str.split(",") if a.strip() != ""]
                self._declarar_variable_local(var_destino, self._invocar_funcion(nombre, args_txt))
            return None

        # ----- Concurrencia real (threading de verdad, no cooperativa) -----
        # Ver _clonar_para_hilo para el porque de la arquitectura elegida:
        # cada hilo corre en un interprete clonado, con su propia copia de
        # variables globales, para no arriesgar corromper el estado del
        # interprete principal con una condicion de carrera.
        if cmd == "hilo_crear":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                nombre_fn, args_str, var_id_hilo = m.groups()
                if nombre_fn not in self.entorno.funciones:
                    raise SiPiError(f"Funcion no definida: {nombre_fn}. 'hilo_crear' necesita una funcion ya declarada con 'funcion'.")
                args_txt = [a.strip() for a in args_str.split(",") if a.strip() != ""]
                # Los argumentos se evaluan ACA, en el contexto de quien
                # llama a 'hilo_crear' -- es donde esas variables existen
                # de verdad. El hilo nuevo recibe los valores ya resueltos.
                valores_params = [self.evaluar_expresion(a) for a in args_txt]

                self._contador_hilos += 1
                id_hilo = f"hilo_{self._contador_hilos}"
                estado = {"terminado": threading.Event(), "valor": None, "error": None}
                clon = self._clonar_para_hilo()

                def _correr_en_hilo(clon=clon, nombre_fn=nombre_fn, valores_params=valores_params, estado=estado):
                    try:
                        estado["valor"] = clon._invocar_funcion_con_valores(nombre_fn, valores_params)
                    except Exception as e:
                        estado["error"] = e
                    finally:
                        estado["terminado"].set()

                hilo = threading.Thread(target=_correr_en_hilo, daemon=True)
                estado["hilo"] = hilo
                self._hilos_sipi[id_hilo] = estado  # MISMO objeto que muta el hilo, no una copia (ver nota abajo)
                hilo.start()
                self._declarar_variable_local(var_id_hilo, id_hilo)
            return None

        if cmd in ("hilo_esperar", "hilo_resultado"):
            args_split = resto.strip()
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", args_split) if cmd == "hilo_resultado" else None
            expr_id_hilo = m.group(1) if m else args_split
            var_destino = m.group(2) if m else None
            id_hilo = self.evaluar_expresion(expr_id_hilo)
            info = self._hilos_sipi.get(id_hilo)
            if info is None:
                raise SiPiError(f"'{id_hilo}' no es un identificador de hilo valido (¿lo creaste con 'hilo_crear ... -> {id_hilo}'?).")
            info["terminado"].wait()
            if info["error"] is not None:
                raise SiPiError(f"El hilo '{id_hilo}' termino con un error: {info['error']}")
            if cmd == "hilo_resultado" and var_destino:
                self._declarar_variable_local(var_destino, info["valor"])
            return None

        if cmd == "hilo_esta_vivo":
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                id_hilo = self.evaluar_expresion(m.group(1))
                info = self._hilos_sipi.get(id_hilo)
                vivo = bool(info and not info["terminado"].is_set())
                self._declarar_variable_local(m.group(2), vivo)
            return None

        if cmd == "hilo_esperar_todos":
            for info in self._hilos_sipi.values():
                info["terminado"].wait()
            errores = [f"'{hid}': {info['error']}" for hid, info in self._hilos_sipi.items() if info["error"] is not None]
            if errores:
                raise SiPiError("Uno o mas hilos terminaron con error -- " + "; ".join(errores))
            return None

        if cmd == "bloqueo_crear":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                id_bloqueo = m.group(1)
                self._bloqueos_sipi[id_bloqueo] = threading.Lock()
                self._declarar_variable_local(id_bloqueo, id_bloqueo)
            return None

        if cmd == "con_bloqueo":
            m = _m(r"^(.+)$", resto.strip())
            fin_bloqueo = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                id_bloqueo = self.evaluar_expresion(m.group(1))
                candado = self._bloqueos_sipi.get(id_bloqueo)
                if candado is None:
                    raise SiPiError(f"'{id_bloqueo}' no es un bloqueo valido (¿lo creaste con 'bloqueo_crear {id_bloqueo}'?).")
                with candado:
                    self._ejecutar_bloque(i + 1, fin_bloqueo)
            return fin_bloqueo + 1

        if cmd == "devolver":
            valor = self.evaluar_expresion(resto)
            pila_llamadas = getattr(self, "pila_llamadas", [])
            if pila_llamadas:
                info_fn = self.entorno.funciones.get(pila_llamadas[-1])
                if info_fn and len(info_fn) >= 5 and info_fn[4]:
                    self._verificar_tipo(f"retorno de '{pila_llamadas[-1]}'", info_fn[4], valor)
            raise RetornoFuncion(valor)

        # ----- Excepciones propias reales (usables con intentar/capturar) -----
        if cmd == "lanzar_error":
            mensaje = self._texto_o_variable(resto)
            raise SiPiError(mensaje, pila=list(getattr(self, "pila_llamadas", [])))

        # ----- Listas reales -----
        if cmd == "lista_crear":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s*:\s*lista<([\w\u0900-\u097F\u0980-\u09FF]+)>)?$", resto.strip())
            if m:
                nombre, tipo_elem = m.group(1), m.group(2)
                self._declarar_variable_local(nombre, [])
                if tipo_elem:
                    self.entorno.tipos_lista[nombre] = tipo_elem
            return None

        if cmd == "lista_agregar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
            if m:
                nombre, expr = m.groups()
                lst = self._obtener_variable(nombre)
                if not isinstance(lst, list):
                    lst = []
                    self._declarar_variable_local(nombre, lst)
                valor = self._copiar_si_mutable(self.evaluar_expresion(expr))
                tipo_elem = self.entorno.tipos_lista.get(nombre)
                if tipo_elem:
                    self._verificar_tipo(f"elemento agregado a '{nombre}'", tipo_elem, valor)
                lst.append(valor)
            return None

        if cmd == "lista_obtener":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, idx_expr, var = m.groups()
                idx = int(self.evaluar_expresion(idx_expr))
                lst = self._obtener_variable(nombre, [])
                self._declarar_variable_local(var, lst[idx] if 0 <= idx < len(lst) else "")
            return None

        if cmd == "lista_longitud":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, var = m.groups()
                lst = self._obtener_variable(nombre, [])
                self._declarar_variable_local(var, len(lst) if isinstance(lst, list) else 0)
            return None

        if cmd == "lista_eliminar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
            if m:
                nombre, idx_expr = m.groups()
                idx = int(self.evaluar_expresion(idx_expr))
                lst = self._obtener_variable(nombre, [])
                if isinstance(lst, list) and 0 <= idx < len(lst):
                    lst.pop(idx)
            return None

        if cmd in ("vector_sumar", "vector_restar", "vector_producto_punto"):
            # Items #71-73 del feedback ("Arrays eficientes / Matematicas /
            # Operaciones vectoriales"): primero se preparan estas
            # operaciones basicas antes de pensar en nada de IA/ML mas
            # elaborado, como el propio feedback pide explicitamente
            # ("Y recien despues investigar si ... tiene alguna aplicacion
            # ... en IA/ML").
            m = _m(r"^(.+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                ambos, var = m.groups()
                partido = _dividir_dos_argumentos_por_espacio(ambos)
                if partido is None:
                    raise SiPiError(f"'{cmd}' necesita dos vectores separados por un espacio, antes de '->'.")
                expr_a, expr_b = partido
                a = self.evaluar_expresion(expr_a)
                b = self.evaluar_expresion(expr_b)
                self._verificar_vectores_misma_longitud(cmd, a, b)
                if cmd == "vector_sumar":
                    resultado = [x + y for x, y in zip(a, b)]
                elif cmd == "vector_restar":
                    resultado = [x - y for x, y in zip(a, b)]
                else:  # vector_producto_punto
                    resultado = sum(x * y for x, y in zip(a, b))
                self._declarar_variable_local(var, resultado)
            return None

        if cmd == "vector_escalar":
            m = _m(r"^(.+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                ambos, var = m.groups()
                partido = _dividir_dos_argumentos_por_espacio(ambos)
                if partido is None:
                    raise SiPiError("'vector_escalar' necesita un vector y un numero separados por un espacio, antes de '->'.")
                expr_vector, expr_escalar = partido
                vector = self.evaluar_expresion(expr_vector)
                escalar = self.evaluar_expresion(expr_escalar)
                self._verificar_es_vector("vector_escalar", vector)
                self._declarar_variable_local(var, [x * escalar for x in vector])
            return None

        if cmd in ("vector_magnitud", "vector_normalizar"):
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                expr_vector, var = m.groups()
                vector = self.evaluar_expresion(expr_vector)
                self._verificar_es_vector(cmd, vector)
                magnitud = math.sqrt(sum(x * x for x in vector))
                if cmd == "vector_magnitud":
                    self._declarar_variable_local(var, magnitud)
                else:  # vector_normalizar
                    if magnitud == 0:
                        raise SiPiError(
                            f"No se puede normalizar el vector {vector}: su magnitud es 0 "
                            f"(seria una division por cero)."
                        )
                    self._declarar_variable_local(var, [x / magnitud for x in vector])
            return None

        if cmd == "para_cada":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            fin_pc = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                var_item, nombre_lista = m.groups()
                lst = self._obtener_variable(nombre_lista, [])
                if isinstance(lst, list):
                    self.profundidad_bucles += 1
                    try:
                        for elemento in list(lst):
                            self._declarar_variable_local(var_item, elemento)
                            try:
                                self._ejecutar_bloque(i + 1, fin_pc)
                            except ContinuarBucle:
                                continue
                            except RomperBucle:
                                break
                    finally:
                        self.profundidad_bucles -= 1
            return fin_pc + 1

        # ----- Temporizadores reales -----
        if cmd == "cada":
            m = _m(r"^(.+?)\s+segundos?(?:\s+(.+?)\s+veces)?$", resto.strip())
            fin_cada = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                intervalo = float(self.evaluar_expresion(m.group(1)))
                veces_expr = m.group(2)
                root_gui = getattr(self, "ventana_tk", None)
                if veces_expr:
                    veces = int(self.evaluar_expresion(veces_expr))
                    if root_gui is not None:
                        # Item 2 critico de tu feedback: si 'cada' esta
                        # dentro de una 'ventana', NO bloqueamos el hilo con
                        # time.sleep en un bucle -- eso es exactamente lo que
                        # congelaba la ventana entera y disparaba
                        # 'Tcl_AsyncDelete'/'main thread is not in main
                        # loop': el mainloop de Tkinter nunca llegaba a
                        # correr porque este bucle no soltaba el hilo.
                        # Ahora programamos cada repeticion con root.after(),
                        # que el propio mainloop dispara en su momento --
                        # la actualizacion de widgets ocurre siempre desde
                        # el mismo hilo que corre mainloop, nunca cruzado.
                        self._temporizador_activo = True
                        ms = max(1, int(intervalo * 1000))
                        restantes = {"n": veces}

                        def _tick_n():
                            if not self._temporizador_activo or restantes["n"] <= 0:
                                return
                            restantes["n"] -= 1
                            try:
                                self._ejecutar_bloque(i + 1, fin_cada)
                            except SiPiError as e:
                                print(f"[SiPi] ERROR en 'cada': {e}")
                                return
                            if self._temporizador_activo and restantes["n"] > 0:
                                root_gui.after(ms, _tick_n)

                        root_gui.after(ms, _tick_n)
                    else:
                        for _ in range(veces):
                            if not getattr(self, "_temporizador_activo", True):
                                break
                            self._ejecutar_bloque(i + 1, fin_cada)
                            time.sleep(intervalo)
                else:
                    self._temporizador_activo = True
                    if root_gui is not None:
                        ms = max(1, int(intervalo * 1000))

                        def _tick_infinito():
                            if not self._temporizador_activo:
                                return
                            try:
                                self._ejecutar_bloque(i + 1, fin_cada)
                            except SiPiError as e:
                                print(f"[SiPi] ERROR en 'cada': {e}")
                                return
                            if self._temporizador_activo:
                                root_gui.after(ms, _tick_infinito)

                        root_gui.after(ms, _tick_infinito)
                    else:
                        while self._temporizador_activo:
                            self._ejecutar_bloque(i + 1, fin_cada)
                            if not self._temporizador_activo:
                                break
                            time.sleep(intervalo)
            return fin_cada + 1

        if cmd == "detener_temporizador":
            self._temporizador_activo = False
            return None

        # ----- Enumeraciones reales -----
        if cmd == "enum":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            fin_enum = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                nombre_enum = m.group(1)
                valores = {}
                contador = 0
                for _, linea_interna in self.lineas[i + 1:fin_enum]:
                    if linea_interna:
                        valores[linea_interna] = contador
                        nombre_var_valor = f"{nombre_enum}_{linea_interna}"
                        self._declarar_variable_local(nombre_var_valor, contador)
                        self.entorno.constantes.add(nombre_var_valor)
                        contador += 1
                self._declarar_variable_local(nombre_enum, valores)
                self.entorno.constantes.add(nombre_enum)
            return fin_enum + 1

        # ----- Estructuras reales (plantillas de diccionario) -----
        if cmd == "estructura":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            fin_est = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                nombre_est = m.group(1)
                plantilla = {}
                for _, linea_interna in self.lineas[i + 1:fin_est]:
                    if linea_interna:
                        mm = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*=\s*(.+)$", linea_interna)
                        if mm:
                            campo, expr = mm.groups()
                            plantilla[campo] = self.evaluar_expresion(expr)
                self._declarar_variable_local(nombre_est, plantilla)
                self.entorno.constantes.add(nombre_est)
            return fin_est + 1

        if cmd == "instanciar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre_est, var_destino = m.groups()
                plantilla = self._obtener_variable(nombre_est, {})
                self._declarar_variable_local(var_destino, copy.deepcopy(plantilla) if isinstance(plantilla, dict) else {})
            return None

        # ----- Programacion orientada a objetos real: clases, herencia, metodos -----
        # clase Nombre [hereda_de Padre]
        #     campo = valor_por_defecto
        #     metodo constructor(param)
        #         diccionario_asignar este "campo" param
        #     fin
        #     metodo hacer_algo()
        #         ...
        #     fin
        # fin
        # ----- Interfaces/protocolos (#22): declaran que metodos debe tener
        # una clase, sin implementarlos. Se verifican al definir la clase
        # (fail fast), no recien cuando alguien intenta usar el metodo. -----
        if cmd == "interfaz":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            fin_interfaz = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                nombre_interfaz = m.group(1)
                requeridos = set()
                j = i + 1
                while j < fin_interfaz:
                    _, linea_j = self.lineas[j]
                    if linea_j == "":
                        j += 1
                        continue
                    mm = _m(r"^metodo\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$", linea_j)
                    if mm:
                        requeridos.add(mm.group(1))
                        fin_metodo_decl = self._encontrar_fin(j, BLOQUES_QUE_ABREN)
                        j = fin_metodo_decl + 1
                        continue
                    j += 1
                self.entorno.interfaces[nombre_interfaz] = requeridos
            return fin_interfaz + 1

        if cmd == "clase":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s+hereda_de\s+([\w\u0900-\u097F\u0980-\u09FF]+))?(?:\s+implementa\s+([\w\s,]+))?$", resto.strip())
            fin_clase = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                nombre_clase, nombre_padre, interfaces_txt = m.groups()
                campos = {}
                metodos = {}
                j = i + 1
                while j < fin_clase:
                    _, linea_j = self.lineas[j]
                    if linea_j == "":
                        j += 1
                        continue
                    mm = _m(r"^metodo\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$", linea_j)
                    if mm:
                        nombre_metodo = mm.group(1)
                        params_metodo = [p.strip() for p in mm.group(2).split(",") if p.strip()]
                        fin_metodo = self._encontrar_fin(j, BLOQUES_QUE_ABREN)
                        metodos[nombre_metodo] = (params_metodo, j + 1, fin_metodo, self.lineas)
                        j = fin_metodo + 1
                        continue
                    mc = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*=\s*(.+)$", linea_j)
                    if mc:
                        campos[mc.group(1)] = self.evaluar_expresion(mc.group(2))
                    j += 1
                nombres_interfaces = [n.strip() for n in interfaces_txt.split(",") if n.strip()] if interfaces_txt else []
                self.entorno.clases[nombre_clase] = {
                    "campos": campos, "metodos": metodos, "padre": nombre_padre,
                    "implementa": nombres_interfaces,
                }
                for nombre_interfaz in nombres_interfaces:
                    requeridos = self.entorno.interfaces.get(nombre_interfaz)
                    if requeridos is None:
                        raise SiPiError(f"La clase '{nombre_clase}' implementa la interfaz no definida '{nombre_interfaz}'")
                    faltantes = [
                        nombre_m for nombre_m in requeridos
                        if self._buscar_metodo_en_cadena(nombre_clase, nombre_m) is None
                    ]
                    if faltantes:
                        raise SiPiError(
                            f"La clase '{nombre_clase}' dice implementar '{nombre_interfaz}' pero le "
                            f"falta(n) el/los metodo(s): {', '.join(sorted(faltantes))}"
                        )
            return fin_clase + 1

        if cmd == "metodo":
            # Solo tiene sentido dentro de un bloque 'clase' (se parsea arriba,
            # sin ejecutarse linea por linea); si aparece suelto, lo saltamos.
            fin_metodo_suelto = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            return fin_metodo_suelto + 1

        if cmd == "nuevo":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if not m:
                raise SiPiError('Sintaxis: nuevo NombreClase(argumentos) -> variable')
            nombre_clase, args_str, var_destino = m.groups()
            objeto = self._instanciar_clase(nombre_clase)
            args_txt = [a.strip() for a in args_str.split(",") if a.strip() != ""]
            valores = [self.evaluar_expresion(a) for a in args_txt]
            metodo_constructor = self._buscar_metodo_en_cadena(nombre_clase, "constructor")
            if metodo_constructor:
                self._invocar_metodo_resuelto(metodo_constructor, objeto, valores)
            self._declarar_variable_local(var_destino, objeto)
            return None

        if cmd == "es_instancia_de":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                nombre_obj, nombre_clase, var_destino = m.groups()
                objeto = self._obtener_variable(nombre_obj, {})
                cadena = self._cadena_de_clases(objeto.get("__clase__")) if isinstance(objeto, dict) else []
                self._declarar_variable_local(var_destino, nombre_clase in cadena)
            return None

        if cmd == "llamar_metodo":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+"([\w\u0900-\u097F\u0980-\u09FF]+)"\((.*)\)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto.strip())
            sin_retorno = False
            if not m:
                m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+"([\w\u0900-\u097F\u0980-\u09FF]+)"\((.*)\)$', resto.strip())
                sin_retorno = True
            if not m:
                raise SiPiError('Sintaxis: llamar_metodo objeto "nombre_metodo"(args) -> variable')
            if sin_retorno:
                nombre_obj, nombre_metodo, args_str = m.groups()
                var_destino = None
            else:
                nombre_obj, nombre_metodo, args_str, var_destino = m.groups()
            objeto = self._obtener_variable(nombre_obj)
            if not isinstance(objeto, dict) or "__clase__" not in objeto:
                raise SiPiError(f"'{nombre_obj}' no es una instancia de una clase (usa 'nuevo' para crear una).")
            metodo_resuelto = self._buscar_metodo_en_cadena(objeto["__clase__"], nombre_metodo)
            if metodo_resuelto is None:
                raise SiPiError(f"La clase '{objeto['__clase__']}' no tiene un metodo llamado '{nombre_metodo}'.")
            args_txt = [a.strip() for a in args_str.split(",") if a.strip() != ""]
            valores = [self.evaluar_expresion(a) for a in args_txt]
            resultado = self._invocar_metodo_resuelto(metodo_resuelto, objeto, valores)
            if var_destino:
                self._declarar_variable_local(var_destino, resultado)
            return None

        # ----- Manejo de errores real -----
        if cmd == "intentar":
            fin_intentar = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            idx_capturar = None
            profundidad = 1
            j = i + 1
            while j < fin_intentar:
                _, lj = self.lineas[j]
                palabra = lj.split(" ")[0] if lj else ""
                resto_lj = lj[len(palabra):].strip()
                es_asignacion_lj = resto_lj.startswith("=") and not resto_lj.startswith("==")
                if palabra in BLOQUES_QUE_ABREN and not es_asignacion_lj:
                    profundidad += 1
                elif palabra == "fin":
                    profundidad -= 1
                elif palabra == "capturar" and profundidad == 1:
                    idx_capturar = j
                j += 1

            bloque_normal_fin = idx_capturar if idx_capturar is not None else fin_intentar
            try:
                self._ejecutar_bloque(i + 1, bloque_normal_fin)
            except RetornoFuncion:
                raise
            except SiPiError as e:
                if idx_capturar is not None:
                    self._declarar_variable_local("error", str(e))
                    self._ejecutar_bloque(idx_capturar + 1, fin_intentar)
                else:
                    print(f"[SiPi] Error capturado silenciosamente: {e}")
            return fin_intentar + 1

        # ----- Diccionarios reales (clave -> valor) -----
        if cmd == "diccionario_crear":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s*:\s*diccionario<([\w\u0900-\u097F\u0980-\u09FF]+)>)?$", resto.strip())
            if m:
                nombre, tipo_valor = m.group(1), m.group(2)
                self._declarar_variable_local(nombre, {})
                if tipo_valor:
                    self.entorno.tipos_diccionario[nombre] = tipo_valor
            return None

        if cmd == "diccionario_asignar":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+("(?:[^"]*)"|\S+)\s+(.+)$', resto)
            if m:
                nombre, clave_expr, expr = m.groups()
                clave = self._texto_o_variable(clave_expr)
                dic = self._obtener_variable(nombre)
                if not isinstance(dic, dict):
                    dic = {}
                    self._declarar_variable_local(nombre, dic)
                valor = self._copiar_si_mutable(self.evaluar_expresion(expr))
                tipo_valor = self.entorno.tipos_diccionario.get(nombre)
                if tipo_valor:
                    self._verificar_tipo(f"valor asignado en '{nombre}[{clave!r}]'", tipo_valor, valor)
                dic[clave] = valor
            return None

        if cmd == "diccionario_obtener":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)(\?)?\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                nombre, clave_expr, con_signo_pregunta, var = m.groups()
                clave = self._texto_o_variable(clave_expr)
                dic = self._obtener_variable(nombre, {})
                if con_signo_pregunta:
                    # Item 8 de tu feedback (navegacion segura): con el '?'
                    # una clave faltante da 'nulo' de verdad, distinguible
                    # de un texto vacio guardado a proposito. Sin el '?' se
                    # mantiene el comportamiento de siempre (texto vacio),
                    # para no romper ningun programa ya escrito.
                    valor = dic.get(clave, None) if isinstance(dic, dict) else None
                else:
                    valor = dic.get(clave, "") if isinstance(dic, dict) else ""
                self._declarar_variable_local(var, valor)
            return None

        if cmd == "diccionario_tiene":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                nombre, clave_expr, var = m.groups()
                clave = self._texto_o_variable(clave_expr)
                dic = self._obtener_variable(nombre, {})
                self._declarar_variable_local(var, isinstance(dic, dict) and clave in dic)
            return None

        if cmd == "diccionario_eliminar":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$', resto)
            if m:
                nombre, clave_expr = m.groups()
                clave = self._texto_o_variable(clave_expr)
                dic = self._obtener_variable(nombre, {})
                if isinstance(dic, dict):
                    dic.pop(clave, None)
            return None

        if cmd == "diccionario_claves":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, var = m.groups()
                dic = self._obtener_variable(nombre, {})
                self._declarar_variable_local(var, list(dic.keys()) if isinstance(dic, dict) else [])
            return None

        # ----- Texto avanzado -----
        if cmd == "texto_dividir":
            m = _m(r'^(.+?)\s+"([^"]*)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                expr, separador, var = m.groups()
                valor = str(self.evaluar_expresion(expr))
                self._declarar_variable_local(var, valor.split(separador) if separador else list(valor))
            return None

        if cmd == "texto_reemplazar":
            m = _m(r'^(.+?)\s+"([^"]*)"\s+"([^"]*)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                expr, buscado, reemplazo, var = m.groups()
                valor = str(self.evaluar_expresion(expr))
                self._declarar_variable_local(var, valor.replace(buscado, reemplazo))
            return None

        if cmd == "texto_contiene":
            m = _m(r'^(.+?)\s+"([^"]*)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                expr, buscado, var = m.groups()
                valor = str(self.evaluar_expresion(expr))
                self._declarar_variable_local(var, buscado in valor)
            return None

        if cmd == "texto_recortar":
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                expr, var = m.groups()
                valor = str(self.evaluar_expresion(expr))
                self._declarar_variable_local(var, valor.strip())
            return None

        if cmd == "texto_empieza_con":
            m = _m(r'^(.+?)\s+"([^"]*)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                expr, prefijo, var = m.groups()
                valor = str(self.evaluar_expresion(expr))
                self._declarar_variable_local(var, valor.startswith(prefijo))
            return None

        if cmd == "texto_termina_con":
            m = _m(r'^(.+?)\s+"([^"]*)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                expr, sufijo, var = m.groups()
                valor = str(self.evaluar_expresion(expr))
                self._declarar_variable_local(var, valor.endswith(sufijo))
            return None

        if cmd == "texto_repetir":
            m = _m(r"^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                expr, veces_expr, var = m.groups()
                valor = str(self.evaluar_expresion(expr))
                veces = int(self.evaluar_expresion(veces_expr))
                self._declarar_variable_local(var, valor * veces)
            return None

        if cmd == "tipo_de":
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                expr, var = m.groups()
                valor = self.evaluar_expresion(expr)
                if valor is None:
                    tipo_texto = "nulo"
                elif isinstance(valor, bool):
                    tipo_texto = "booleano"
                elif isinstance(valor, (int, float)):
                    tipo_texto = "numero"
                elif isinstance(valor, str):
                    tipo_texto = "texto"
                elif isinstance(valor, list):
                    tipo_texto = "lista"
                elif isinstance(valor, dict):
                    tipo_texto = "diccionario"
                else:
                    tipo_texto = "desconocido"
                self._declarar_variable_local(var, tipo_texto)
            return None

        # ----- Listas avanzadas -----
        if cmd == "lista_ordenar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                lst = self._obtener_variable(m.group(1))
                if isinstance(lst, list):
                    try:
                        lst.sort()
                    except TypeError:
                        lst.sort(key=str)
            return None

        if cmd == "lista_invertir":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                lst = self._obtener_variable(m.group(1))
                if isinstance(lst, list):
                    lst.reverse()
            return None

        if cmd == "lista_contiene":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, expr, var = m.groups()
                lst = self._obtener_variable(nombre, [])
                valor = self.evaluar_expresion(expr)
                self._declarar_variable_local(var, valor in lst if isinstance(lst, list) else False)
            return None

        # ----- Matrices reales (arrays 2D) -----
        if cmd == "matriz_crear":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s+(.+?)\s+(.+)$", resto)
            if m:
                nombre, filas_expr, cols_expr, valor_expr = m.groups()
                filas = int(self.evaluar_expresion(filas_expr))
                columnas = int(self.evaluar_expresion(cols_expr))
                valor_inicial = self.evaluar_expresion(valor_expr)
                self._declarar_variable_local(nombre, [
                    [copy.deepcopy(valor_inicial) for _ in range(columnas)] for _ in range(filas)
                ])
            return None

        if cmd == "matriz_asignar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s+(.+?)\s+(.+)$", resto)
            if m:
                nombre, fila_expr, col_expr, valor_expr = m.groups()
                fila = int(self.evaluar_expresion(fila_expr))
                col = int(self.evaluar_expresion(col_expr))
                valor = self._copiar_si_mutable(self.evaluar_expresion(valor_expr))
                matriz = self._obtener_variable(nombre)
                if isinstance(matriz, list) and 0 <= fila < len(matriz) and 0 <= col < len(matriz[fila]):
                    matriz[fila][col] = valor
            return None

        if cmd == "matriz_obtener":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, fila_expr, col_expr, var = m.groups()
                fila = int(self.evaluar_expresion(fila_expr))
                col = int(self.evaluar_expresion(col_expr))
                matriz = self._obtener_variable(nombre)
                if isinstance(matriz, list) and 0 <= fila < len(matriz) and 0 <= col < len(matriz[fila]):
                    self._declarar_variable_local(var, matriz[fila][col])
                else:
                    self._declarar_variable_local(var, "")
            return None

        if cmd == "matriz_filas":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, var = m.groups()
                matriz = self._obtener_variable(nombre, [])
                self._declarar_variable_local(var, len(matriz) if isinstance(matriz, list) else 0)
            return None

        if cmd == "matriz_columnas":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, var = m.groups()
                matriz = self._obtener_variable(nombre, [])
                self._declarar_variable_local(var, len(matriz[0]) if isinstance(matriz, list) and matriz else 0)
            return None

        if cmd == "suma_lista":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, var = m.groups()
                lst = self._obtener_variable(nombre, [])
                try:
                    self._declarar_variable_local(var, sum(float(x) for x in lst))
                except (TypeError, ValueError):
                    self._declarar_variable_local(var, 0)
            return None

        if cmd == "promedio_lista":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre, var = m.groups()
                lst = self._obtener_variable(nombre, [])
                try:
                    numeros = [float(x) for x in lst]
                    self._declarar_variable_local(var, sum(numeros) / len(numeros) if numeros else 0)
                except (TypeError, ValueError):
                    self._declarar_variable_local(var, 0)
            return None

        # ----- Programacion funcional real sobre listas (usando funciones SiPi) -----
        if cmd == "lista_mapear":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+con\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if not m:
                raise SiPiError('Sintaxis: lista_mapear lista con nombre_funcion -> variable')
            nombre_lista, nombre_funcion, var = m.groups()
            lst = self._obtener_variable(nombre_lista, [])
            resultado = [self._invocar_funcion_con_valores(nombre_funcion, [elemento]) for elemento in lst]
            self._declarar_variable_local(var, resultado)
            return None

        if cmd == "lista_filtrar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+con\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if not m:
                raise SiPiError('Sintaxis: lista_filtrar lista con nombre_funcion -> variable')
            nombre_lista, nombre_funcion, var = m.groups()
            lst = self._obtener_variable(nombre_lista, [])
            resultado = [elemento for elemento in lst if self._invocar_funcion_con_valores(nombre_funcion, [elemento])]
            self._declarar_variable_local(var, resultado)
            return None

        if cmd == "lista_reducir":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+con\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+desde\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if not m:
                raise SiPiError('Sintaxis: lista_reducir lista con nombre_funcion desde valor_inicial -> variable')
            nombre_lista, nombre_funcion, expr_inicial, var = m.groups()
            lst = self._obtener_variable(nombre_lista, [])
            acumulado = self.evaluar_expresion(expr_inicial)
            for elemento in lst:
                acumulado = self._invocar_funcion_con_valores(nombre_funcion, [acumulado, elemento])
            self._declarar_variable_local(var, acumulado)
            return None

        if cmd == "lista_unir":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+"([^"]*)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: lista_unir lista "separador" -> variable')
            nombre_lista, separador, var = m.groups()
            lst = self._obtener_variable(nombre_lista, [])
            self._declarar_variable_local(var, separador.join(self._formatear_valor(x) for x in lst))
            return None

        if cmd == "lista_aplanar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre_lista, var = m.groups()
                lst = self._obtener_variable(nombre_lista, [])
                aplanada = []
                for elemento in lst:
                    if isinstance(elemento, list):
                        aplanada.extend(elemento)
                    else:
                        aplanada.append(elemento)
                self._declarar_variable_local(var, aplanada)
            return None

        # ----- Matematica adicional -----
        if cmd == "minimo":
            m = _m(r"^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                a = self.evaluar_expresion(m.group(1))
                b = self.evaluar_expresion(m.group(2))
                self._declarar_variable_local(m.group(3), min(a, b))
            return None

        if cmd == "maximo":
            m = _m(r"^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                a = self.evaluar_expresion(m.group(1))
                b = self.evaluar_expresion(m.group(2))
                self._declarar_variable_local(m.group(3), max(a, b))
            return None

        if cmd == "redondear":
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                valor = float(self.evaluar_expresion(m.group(1)))
                self._declarar_variable_local(m.group(2), round(valor))
            return None

        if cmd == "actualizar_barra":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
            if m:
                var, expr = m.groups()
                nuevo_valor = float(self.evaluar_expresion(expr))
                self._mutar_variable(var, nuevo_valor)
                if var in self.widgets:
                    self.widgets[var].set(nuevo_valor)
            return None

        # ----- Registro de eventos (logs reales) -----
        if cmd == "registrar_evento":
            m = _m(r'^(.+?)\s+"([^"]+)"$', resto)
            if m:
                mensaje_expr, archivo_log = m.groups()
                mensaje = self.evaluar_expresion(mensaje_expr)
                ruta_log = os.path.join(self.base_dir, archivo_log)
                marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(ruta_log, "a", encoding="utf-8") as f:
                    f.write(f"[{marca_tiempo}] {mensaje}\n")
            return None

        # ----- Utilidades varias -----
        if cmd == "fecha_hora_actual":
            m = _m(r"^->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                self._declarar_variable_local(m.group(1), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return None

        # ----- Fechas (#13: biblioteca estandar mas completa) -----
        # Todas trabajan con fechas en formato "YYYY-MM-DD" o "YYYY-MM-DD HH:MM:SS"
        # (el mismo que devuelve fecha_hora_actual), para que se puedan
        # combinar sin conversiones manuales.
        if cmd == "fecha_sumar_dias":
            m = _m(r'^(.+?)\s+(-?\d+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: fecha_sumar_dias "2026-01-01" 10 -> resultado')
            fecha_txt = self._texto_o_variable(m.group(1))
            dias = int(m.group(2))
            fecha = self._parsear_fecha(fecha_txt)
            nueva = fecha + datetime.timedelta(days=dias)
            self._declarar_variable_local(m.group(3), nueva.strftime("%Y-%m-%d") if fecha_txt.count(":") == 0 else nueva.strftime("%Y-%m-%d %H:%M:%S"))
            return None

        if cmd == "fecha_diferencia_dias":
            m = _m(r'^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: fecha_diferencia_dias "2026-01-01" "2026-02-01" -> dias')
            f1 = self._parsear_fecha(self._texto_o_variable(m.group(1)))
            f2 = self._parsear_fecha(self._texto_o_variable(m.group(2)))
            self._declarar_variable_local(m.group(3), (f2 - f1).days)
            return None

        if cmd == "fecha_es_mayor":
            m = _m(r'^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: fecha_es_mayor "2026-02-01" "2026-01-01" -> resultado')
            f1 = self._parsear_fecha(self._texto_o_variable(m.group(1)))
            f2 = self._parsear_fecha(self._texto_o_variable(m.group(2)))
            self._declarar_variable_local(m.group(3), f1 > f2)
            return None

        if cmd == "fecha_formatear":
            m = _m(r'^(.+?)\s+"([^"]+)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: fecha_formatear fecha "%d/%m/%Y" -> texto_formateado')
            fecha = self._parsear_fecha(self._texto_o_variable(m.group(1)))
            try:
                formateada = fecha.strftime(m.group(2))
            except ValueError as e:
                raise SiPiError(f"Formato de fecha invalido: {e}")
            self._declarar_variable_local(m.group(3), formateada)
            return None

        if cmd == "fecha_dia_semana":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: fecha_dia_semana fecha -> nombre_dia')
            fecha = self._parsear_fecha(self._texto_o_variable(m.group(1)))
            dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
            self._declarar_variable_local(m.group(2), dias[fecha.weekday()])
            return None

        if cmd == "listar_archivos":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                carpeta = self._texto_o_variable(m.group(1))
                var = m.group(2)
                ruta = os.path.join(self.base_dir, carpeta) if carpeta else self.base_dir
                try:
                    self._declarar_variable_local(var, os.listdir(ruta))
                except OSError as e:
                    print(f"[SiPi] No se pudo listar '{carpeta}': {e}")
                    self._declarar_variable_local(var, [])
            return None

        if cmd == "hash_texto":
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                valor = str(self.evaluar_expresion(m.group(1)))
                self._declarar_variable_local(m.group(2), hashlib.sha256(valor.encode("utf-8")).hexdigest())
            return None

        if cmd == "hash_seguro_contrasena":
            # A diferencia de 'hash_texto' (SHA-256 simple, rapido y SIN sal
            # -- vulnerable a tablas arcoiris y fuerza bruta con GPU, NO apto
            # para guardar contraseñas reales), esto usa PBKDF2-HMAC-SHA256
            # con una sal aleatoria de 16 bytes y 200.000 iteraciones (mismo
            # algoritmo de fondo que usan Django/Werkzeug para contraseñas).
            # El resultado incluye la sal, asi que 'verificar_contrasena'
            # no necesita que se la pases aparte.
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                clave = str(self.evaluar_expresion(m.group(1)))
                sal = os.urandom(16)
                derivado = hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), sal, 200_000)
                # Formato guardable en una sola columna de texto: algoritmo$iteraciones$sal_hex$hash_hex
                paquete = f"pbkdf2_sha256$200000${sal.hex()}${derivado.hex()}"
                self._declarar_variable_local(m.group(2), paquete)
            return None

        if cmd == "verificar_contrasena":
            # Uso: verificar_contrasena clave_ingresada hash_guardado -> variable
            m = _m(r'^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                clave_ingresada = str(self.evaluar_expresion(m.group(1)))
                hash_guardado = str(self.evaluar_expresion(m.group(2)))
                coincide = False
                try:
                    algoritmo, iteraciones_txt, sal_hex, hash_hex = hash_guardado.split("$")
                    if algoritmo == "pbkdf2_sha256":
                        sal = bytes.fromhex(sal_hex)
                        derivado = hashlib.pbkdf2_hmac(
                            "sha256", clave_ingresada.encode("utf-8"), sal, int(iteraciones_txt)
                        )
                        # Comparacion en tiempo constante: evita que un atacante
                        # infiera el hash correcto midiendo cuanto tarda la
                        # comparacion caracter a caracter (ataque de timing).
                        coincide = hmac.compare_digest(derivado.hex(), hash_hex)
                except (ValueError, AttributeError):
                    coincide = False  # formato invalido/corrupto -> tratar como no coincide, nunca como error fatal
                self._declarar_variable_local(m.group(3), coincide)
            return None

        # ---------- Ciencia / analisis de datos ----------
        # Funciones estadisticas reales sobre listas, para investigadores,
        # analistas, ingenieros, o cualquier trabajo que necesite sacarle
        # sentido a datos medidos (temperaturas, muestras de laboratorio,
        # tiempos de respuesta, lo que sea).
        if cmd in ("estadistica_media", "estadistica_mediana", "estadistica_moda",
                   "estadistica_desviacion", "estadistica_varianza", "estadistica_rango"):
            m = _m(r"^(\w+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if not m:
                raise SiPiError(f"Sintaxis: {cmd} nombre_lista -> variable")
            datos, encontrada = self._buscar_variable(m.group(1))
            if not encontrada or not isinstance(datos, list) or not datos:
                raise SiPiError(f"{cmd}: '{m.group(1)}' debe ser una lista con al menos un numero.")
            valores = [float(v) for v in datos]
            try:
                if cmd == "estadistica_media":
                    resultado = statistics.mean(valores)
                elif cmd == "estadistica_mediana":
                    resultado = statistics.median(valores)
                elif cmd == "estadistica_moda":
                    resultado = statistics.mode(valores)
                elif cmd == "estadistica_desviacion":
                    resultado = statistics.stdev(valores) if len(valores) > 1 else 0.0
                elif cmd == "estadistica_varianza":
                    resultado = statistics.variance(valores) if len(valores) > 1 else 0.0
                elif cmd == "estadistica_rango":
                    resultado = max(valores) - min(valores)
            except statistics.StatisticsError as e:
                raise SiPiError(f"{cmd}: {e}")
            self._declarar_variable_local(m.group(2), resultado)
            return None

        if cmd == "regresion_lineal":
            m = _m(r"^(\w+)\s+(\w+)\s*->\s*(\w+)\s+(\w+)$", resto.strip())
            if not m:
                raise SiPiError("Sintaxis: regresion_lineal lista_x lista_y -> pendiente ordenada_origen")
            datos_x, encontrada_x = self._buscar_variable(m.group(1))
            datos_y, encontrada_y = self._buscar_variable(m.group(2))
            if not encontrada_x or not encontrada_y:
                raise SiPiError("regresion_lineal: las dos listas deben existir.")
            xs, ys = [float(v) for v in datos_x], [float(v) for v in datos_y]
            if len(xs) != len(ys) or len(xs) < 2:
                raise SiPiError("regresion_lineal: las listas deben tener la misma cantidad de elementos (minimo 2).")
            n = len(xs)
            media_x, media_y = sum(xs) / n, sum(ys) / n
            numerador = sum((xs[i] - media_x) * (ys[i] - media_y) for i in range(n))
            denominador = sum((xs[i] - media_x) ** 2 for i in range(n))
            pendiente = numerador / denominador if denominador != 0 else 0.0
            ordenada = media_y - pendiente * media_x
            self._declarar_variable_local(m.group(3), pendiente)
            self._declarar_variable_local(m.group(4), ordenada)
            return None

        # ---------- Geolocalizacion ----------
        # Distancia real entre dos coordenadas GPS (formula de Haversine,
        # tiene en cuenta la curvatura de la Tierra). Util para despacho de
        # emergencias (bomberos/policia/ambulancias: encontrar el recurso
        # mas cercano), logistica, trabajo de campo cientifico, entrega de
        # pedidos, lo que sea que necesite "que tan lejos esta esto".
        if cmd == "distancia_gps":
            m = _m(r"^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s*->\s*(\w+)$", resto.strip())
            if not m:
                raise SiPiError("Sintaxis: distancia_gps lat1 lon1 lat2 lon2 -> variable  (resultado en kilometros)")
            lat1, lon1, lat2, lon2 = (self.evaluar_expresion(g) for g in m.groups()[:4])
            R = 6371.0  # radio de la Tierra en km
            f1, f2 = math.radians(lat1), math.radians(lat2)
            df, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
            a = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
            distancia_km = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            self._declarar_variable_local(m.group(5), round(distancia_km, 3))
            return None

        # ---------- Seguridad defensiva ----------
        # Herramientas de proteccion real (generar credenciales seguras,
        # verificar integridad, firmar mensajes) para quien trabaje
        # protegiendo sistemas. SiPi no incluye ni va a incluir herramientas
        # de ataque/intrusion (escaneo de puertos ajenos, exploits, etc.):
        # el trabajo de seguridad legitimo -- defensivo o "hacking etico"
        # con autorizacion -- se apoya en construir defensas solidas, que es
        # exactamente lo que esto ofrece.
        if cmd == "generar_contrasena_segura":
            m = _m(r"^(.+?)\s*->\s*(\w+)$", resto.strip())
            if not m:
                raise SiPiError("Sintaxis: generar_contrasena_segura 16 -> variable")
            longitud = int(self.evaluar_expresion(m.group(1)))
            longitud = max(8, min(longitud, 256))
            alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_=+"
            contrasena = "".join(secrets.choice(alfabeto) for _ in range(longitud))
            self._declarar_variable_local(m.group(2), contrasena)
            return None

        if cmd == "generar_token_seguro":
            m = _m(r"^(.+?)\s*->\s*(\w+)$", resto.strip())
            if not m:
                raise SiPiError("Sintaxis: generar_token_seguro 32 -> variable  (bytes de aleatoriedad real, en hexadecimal)")
            n_bytes = int(self.evaluar_expresion(m.group(1)))
            self._declarar_variable_local(m.group(2), secrets.token_hex(max(8, min(n_bytes, 256))))
            return None

        if cmd == "evaluar_fortaleza_contrasena":
            m = _m(r"^(.+?)\s*->\s*(\w+)$", resto.strip())
            if not m:
                raise SiPiError("Sintaxis: evaluar_fortaleza_contrasena clave -> variable")
            clave = str(self.evaluar_expresion(m.group(1)))
            self._declarar_variable_local(m.group(2), self._evaluar_fortaleza_contrasena(clave))
            return None

        if cmd == "hash_archivo":
            m = _m(r"^(.+?)\s*->\s*(\w+)$", resto.strip())
            if not m:
                raise SiPiError("Sintaxis: hash_archivo \"ruta\" -> variable  (SHA-256, para verificar integridad / cadena de custodia)")
            ruta = self._texto_o_variable(m.group(1))
            ruta_completa = os.path.join(self.base_dir, ruta) if not os.path.isabs(ruta) else ruta
            if not os.path.exists(ruta_completa):
                raise SiPiError(f"hash_archivo: no existe el archivo '{ruta}'.")
            hasher = hashlib.sha256()
            with open(ruta_completa, "rb") as f:
                for bloque in iter(lambda: f.read(65536), b""):
                    hasher.update(bloque)
            self._declarar_variable_local(m.group(2), hasher.hexdigest())
            return None

        if cmd == "firmar_hmac":
            m = _m(r"^(.+?)\s+con\s+clave\s+(.+?)\s*->\s*(\w+)$", resto.strip())
            if not m:
                raise SiPiError('Sintaxis: firmar_hmac mensaje con clave secreta -> variable')
            mensaje = str(self.evaluar_expresion(m.group(1)))
            clave = str(self.evaluar_expresion(m.group(2)))
            firma = hmac.new(clave.encode("utf-8"), mensaje.encode("utf-8"), hashlib.sha256).hexdigest()
            self._declarar_variable_local(m.group(3), firma)
            return None

        if cmd == "verificar_hmac":
            m = _m(r"^(.+?)\s+con\s+clave\s+(.+?)\s+y\s+firma\s+(.+?)\s*->\s*(\w+)$", resto.strip())
            if not m:
                raise SiPiError('Sintaxis: verificar_hmac mensaje con clave secreta y firma firma_recibida -> variable')
            mensaje = str(self.evaluar_expresion(m.group(1)))
            clave = str(self.evaluar_expresion(m.group(2)))
            firma_recibida = str(self.evaluar_expresion(m.group(3)))
            firma_esperada = hmac.new(clave.encode("utf-8"), mensaje.encode("utf-8"), hashlib.sha256).hexdigest()
            self._declarar_variable_local(m.group(4), hmac.compare_digest(firma_esperada, firma_recibida))
            return None

        if cmd == "elegir_al_azar":
            m = _m(r'^"([^"]*)"\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                opciones = [self.interpolar(o) for o in m.group(1).split("|") if o != ""]
                self._declarar_variable_local(m.group(2), random.choice(opciones) if opciones else "")
            return None

        # ----- Imagenes (#13): usan Pillow si esta instalado. Si no, se
        # avisa con un error claro en vez de fallar de forma confusa. -----
        if cmd == "imagen_info":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: imagen_info "foto.png" -> info')
            ruta = os.path.join(self.base_dir, self._texto_o_variable(m.group(1)))
            try:
                from PIL import Image
            except ImportError:
                raise SiPiError("imagen_info necesita el paquete 'Pillow'. Instalalo con: pip install Pillow")
            with Image.open(ruta) as img:
                info = {"ancho": img.width, "alto": img.height, "formato": img.format or "", "modo": img.mode}
            self._declarar_variable_local(m.group(2), info)
            return None

        if cmd == "imagen_redimensionar":
            m = _m(r'^(.+?)\s+(\d+)\s+(\d+)\s+(.+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: imagen_redimensionar "entrada.png" 800 600 "salida.png"')
            origen = os.path.join(self.base_dir, self._texto_o_variable(m.group(1)))
            ancho, alto = int(m.group(2)), int(m.group(3))
            destino = os.path.join(self.base_dir, self._texto_o_variable(m.group(4)))
            try:
                from PIL import Image
            except ImportError:
                raise SiPiError("imagen_redimensionar necesita el paquete 'Pillow'. Instalalo con: pip install Pillow")
            with Image.open(origen) as img:
                img.resize((ancho, alto)).save(destino)
            print(f"[SiPi] Imagen redimensionada guardada en: {destino}")
            return None

        if cmd == "imagen_convertir":
            m = _m(r'^(.+?)\s+(.+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: imagen_convertir "entrada.png" "salida.jpg"')
            origen = os.path.join(self.base_dir, self._texto_o_variable(m.group(1)))
            destino = os.path.join(self.base_dir, self._texto_o_variable(m.group(2)))
            try:
                from PIL import Image
            except ImportError:
                raise SiPiError("imagen_convertir necesita el paquete 'Pillow'. Instalalo con: pip install Pillow")
            with Image.open(origen) as img:
                if destino.lower().endswith((".jpg", ".jpeg")) and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(destino)
            print(f"[SiPi] Imagen convertida guardada en: {destino}")
            return None

        # ----- Audio (#13): duracion/combinacion real de tonos con 'wave',
        # sin dependencias externas (ya se usa 'wave' para reproducir_tono). -----
        if cmd == "audio_duracion":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: audio_duracion "sonido.wav" -> segundos')
            ruta = os.path.join(self.base_dir, self._texto_o_variable(m.group(1)))
            with wave.open(ruta, "rb") as w:
                duracion = w.getnframes() / float(w.getframerate())
            self._declarar_variable_local(m.group(2), round(duracion, 3))
            return None

        if cmd == "audio_generar_tono":
            m = _m(r'^(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(.+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: audio_generar_tono 440 1.5 "tono.wav"  (frecuencia_hz duracion_seg archivo)')
            frecuencia = float(m.group(1))
            duracion = float(m.group(2))
            destino = os.path.join(self.base_dir, self._texto_o_variable(m.group(3)))
            tasa = 44100
            n_muestras = int(tasa * duracion)
            with wave.open(destino, "w") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(tasa)
                for i in range(n_muestras):
                    valor = int(32767 * math.sin(2 * math.pi * frecuencia * (i / tasa)))
                    w.writeframesraw(struct.pack("<h", valor))
            print(f"[SiPi] Tono generado en: {destino}")
            return None

        if cmd == "comprimir_carpeta":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+("(?:[^"]*)"|\S+)$', resto)
            if m:
                carpeta = self._texto_o_variable(m.group(1))
                destino_zip = self._texto_o_variable(m.group(2))
                ruta_carpeta = os.path.join(self.base_dir, carpeta)
                ruta_zip = os.path.join(self.base_dir, destino_zip)
                base_zip = ruta_zip[:-4] if ruta_zip.lower().endswith(".zip") else ruta_zip
                shutil.make_archive(base_zip, "zip", ruta_carpeta)
                print(f"[SiPi] Carpeta comprimida en: {base_zip}.zip")
            return None

        if cmd == "descomprimir_zip":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+("(?:[^"]*)"|\S+)$', resto)
            if m:
                archivo_zip = self._texto_o_variable(m.group(1))
                destino = self._texto_o_variable(m.group(2))
                ruta_zip = os.path.join(self.base_dir, archivo_zip)
                ruta_destino = os.path.join(self.base_dir, destino)
                shutil.unpack_archive(ruta_zip, ruta_destino)
                print(f"[SiPi] Descomprimido en: {ruta_destino}")
            return None

        # ----- Archivos y automatizacion real -----
        if cmd == "crear_archivo":
            m = _m(r'^("(?:[^"\\]|\\.)*"|\S+)\s+(.+)$', resto, re.DOTALL)
            if m:
                ruta = self._texto_o_variable(m.group(1))
                contenido = self._formatear_valor(self.evaluar_expresion(m.group(2)))
                ruta_final = os.path.join(self.base_dir, ruta)
                os.makedirs(os.path.dirname(ruta_final) or ".", exist_ok=True)
                with open(ruta_final, "w", encoding="utf-8") as f:
                    f.write(contenido)
                print(f"[SiPi] Archivo creado: {ruta_final}")
            else:
                raise SiPiError(
                    "Sintaxis invalida en 'crear_archivo'. Se esperaba: crear_archivo \"ruta\" contenido "
                    "(el contenido puede ser un texto, una variable, o una expresion como variable + \"texto\")."
                )
            return None

        if cmd == "leer_archivo":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                ruta = self._texto_o_variable(m.group(1))
                var = m.group(2)
                ruta_final = os.path.join(self.base_dir, ruta)
                with open(ruta_final, "r", encoding="utf-8") as f:
                    self._declarar_variable_local(var, f.read())
            return None

        if cmd == "borrar_archivo":
            ruta_final = os.path.join(self.base_dir, self._texto_o_variable(resto))
            if os.path.exists(ruta_final):
                os.remove(ruta_final)
                print(f"[SiPi] Archivo borrado: {ruta_final}")
            return None

        if cmd == "crear_carpeta":
            ruta_final = os.path.join(self.base_dir, self._texto_o_variable(resto))
            os.makedirs(ruta_final, exist_ok=True)
            print(f"[SiPi] Carpeta creada: {ruta_final}")
            return None

        if cmd == "ejecutar":
            comando = self._texto_o_variable(resto)
            print(f"[SiPi] Ejecutando: {comando}")
            subprocess.run(comando, shell=True, cwd=self.base_dir)
            return None

        if cmd == "esperar":
            segundos = float(self.evaluar_expresion(resto))
            time.sleep(segundos)
            return None

        if cmd == "reproducir_tono":
            m = _m(r"^(.+?)\s+(.+)$", resto)
            if m:
                if not asegurar_paquete("pygame"):
                    return None
                import pygame
                frecuencia = float(self.evaluar_expresion(m.group(1)))
                duracion = float(self.evaluar_expresion(m.group(2)))
                try:
                    pygame.mixer.init()
                    ruta_tono = generar_wav_tono(frecuencia, duracion)
                    sonido = pygame.mixer.Sound(ruta_tono)
                    sonido.play()
                    time.sleep(duracion)
                    os.remove(ruta_tono)
                except Exception as e:
                    print(f"[SiPi] No se pudo reproducir el tono: {e}")
            return None

        if cmd in ("particulas", "explosion", "humo", "fuego"):
            if cmd == "particulas":
                m = _m(r'^(.+?)\s+(.+?)\s+(.+?)\s+"([\w\u0900-\u097F\u0980-\u09FF]+)"$', resto)
                if m:
                    x_expr, y_expr, cant_expr, tipo_p = m.groups()
                else:
                    return None
            else:
                m = _m(r"^(.+?)\s+(.+?)(?:\s+(.+))?$", resto)
                if not m:
                    return None
                x_expr, y_expr, cant_expr = m.group(1), m.group(2), m.group(3) or "20"
                tipo_p = cmd  # "explosion", "humo" o "fuego"
            x_p = int(self.evaluar_expresion(x_expr))
            y_p = int(self.evaluar_expresion(y_expr))
            cantidad_p = int(self.evaluar_expresion(cant_expr))
            if not hasattr(self, "particulas_pendientes"):
                self.particulas_pendientes = []
            self.particulas_pendientes.append({"x": x_p, "y": y_p, "cantidad": cantidad_p, "tipo": tipo_p})
            return None

        # ----- Automatizacion de escritorio real -----
        if cmd == "captura_pantalla":
            ruta = self._texto_o_variable(resto) if resto.strip() else "captura.png"
            if not asegurar_paquete("PIL", "Pillow"):
                return None
            from PIL import ImageGrab
            ruta_final = os.path.join(self.base_dir, ruta)
            os.makedirs(os.path.dirname(ruta_final) or ".", exist_ok=True)
            try:
                imagen = ImageGrab.grab()
                imagen.save(ruta_final)
                print(f"[SiPi] Captura de pantalla guardada: {ruta_final}")
            except Exception as e:
                print(f"[SiPi] No se pudo capturar la pantalla: {e}")
            return None

        if cmd == "copiar_portapapeles":
            texto = self._texto_o_variable(resto)
            try:
                import tkinter as tk
                raiz_oculta = tk.Tk()
                raiz_oculta.withdraw()
                raiz_oculta.clipboard_clear()
                raiz_oculta.clipboard_append(texto)
                raiz_oculta.update()
                raiz_oculta.destroy()
                print("[SiPi] Texto copiado al portapapeles.")
            except Exception as e:
                print(f"[SiPi] No se pudo copiar al portapapeles: {e}")
            return None

        if cmd == "pegar_portapapeles":
            m = _m(r"^->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                var = m.group(1)
                try:
                    import tkinter as tk
                    raiz_oculta = tk.Tk()
                    raiz_oculta.withdraw()
                    self._declarar_variable_local(var, raiz_oculta.clipboard_get())
                    raiz_oculta.destroy()
                except Exception as e:
                    print(f"[SiPi] No se pudo leer el portapapeles: {e}")
                    self._declarar_variable_local(var, "")
            return None

        if cmd == "copiar_archivo":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+("(?:[^"]*)"|\S+)$', resto)
            if m:
                origen = os.path.join(self.base_dir, self._texto_o_variable(m.group(1)))
                destino = os.path.join(self.base_dir, self._texto_o_variable(m.group(2)))
                os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
                shutil.copy(origen, destino)
                print(f"[SiPi] Copiado: {origen} -> {destino}")
            return None

        # ----- Auto-instalacion de componentes -----
        if cmd == "instalar_paquete":
            nombre_paquete = self._texto_o_variable(resto)
            asegurar_paquete(nombre_paquete.replace("-", "_"), nombre_paquete)
            return None

        # ----- Administrador de modulos SiPi (como "pip"/"npm" para SiPi) -----
        # Descarga un modulo .sipi real desde una URL (o desde el registro por
        # defecto) y lo deja listo en modulos_instalados/ para poder usarlo
        # con 'importar'. Cualquier programador puede publicar sus propios
        # modulos .sipi subiendolos a un repositorio (por ejemplo GitHub) y
        # compartiendo el nombre o la URL directa.
        if cmd == "instalar_modulo":
            m = _m(r'^(.+?)(?:\s+como\s+([\w\u0900-\u097F\u0980-\u09FF]+))?$', resto)
            nombre_o_url = self._texto_o_variable(m.group(1)) if m else self._texto_o_variable(resto)
            alias_import = m.group(2) if m else None
            self._instalar_modulo(nombre_o_url, alias_import)
            return None

        if cmd == "listar_modulos":
            m = _m(r"^\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip()) if resto.strip() else None
            registro = self._leer_registro_modulos()
            if m:
                self._declarar_variable_local(m.group(1), list(registro.keys()))
            else:
                if registro:
                    print("[SiPi] Modulos instalados:")
                    for nombre_mod, info in registro.items():
                        print(f"  - {nombre_mod}  (desde: {info.get('url', '?')}, instalado: {info.get('instalado', '?')})")
                else:
                    print("[SiPi] No hay modulos instalados todavia.")
            return None

        if cmd == "desinstalar_modulo":
            nombre_modulo = self._texto_o_variable(resto)
            carpeta_modulos = os.path.join(self.base_dir, "modulos_instalados")
            ruta_modulo = os.path.join(carpeta_modulos, f"{nombre_modulo}.sipi")
            if os.path.exists(ruta_modulo):
                os.remove(ruta_modulo)
                registro = self._leer_registro_modulos()
                registro.pop(nombre_modulo, None)
                self._escribir_registro_modulos(registro)
                print(f"[SiPi] Modulo '{nombre_modulo}' desinstalado.")
            else:
                print(f"[SiPi] El modulo '{nombre_modulo}' no estaba instalado.")
            return None

        if cmd == "instalar_dependencias":
            self._instalar_dependencias()
            return None

        # Item 1 del roadmap ("repositorio de paquetes"): en vez de montar
        # un sitio web propio (fuera de alcance real aca), SiPi usa GitHub
        # como el repositorio -- igual que hace 'go get' o 'pip install
        # git+...'. Cualquier repo publico con archivos .sipi ES un paquete
        # instalable, sin que nadie tenga que registrarse en ningun lado.
        if cmd == "instalar_repositorio":
            m = _m(r'^(.+?)(?:\s+rama\s+(\S+))?$', resto.strip())
            if m:
                repo_o_url = self._texto_o_variable(m.group(1))
                rama = m.group(2)
            else:
                repo_o_url, rama = self._texto_o_variable(resto), None
            self._instalar_paquete_github(repo_o_url, rama)
            return None

        if cmd == "listar_repositorios":
            m = _m(r"^\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip()) if resto.strip() else None
            registro = self._leer_registro_paquetes()
            if m:
                self._declarar_variable_local(m.group(1), list(registro.keys()))
            else:
                if registro:
                    print("[SiPi] Paquetes instalados:")
                    for nombre_pkg, info in registro.items():
                        print(f"  - {nombre_pkg}  (desde: {info.get('repo', '?')}, instalado: {info.get('instalado', '?')})")
                else:
                    print("[SiPi] No hay paquetes instalados todavia.")
            return None

        # Buscador real (sin indice inventado ni curado a mano): usa la API
        # publica de busqueda de repositorios de GitHub, filtrando por
        # archivos .sipi cuando es posible. Complementa a instalar_repositorio:
        # primero buscas, despues instalas el resultado que te sirva.
        if cmd == "buscar_paquete":
            texto_busqueda = self._texto_o_variable(resto)
            self._buscar_paquetes_github(texto_busqueda)
            return None

        # ----- Base de datos local real (JSON persistente) -----
        if cmd == "guardar_dato":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+(.+)$', resto)
            if m:
                clave, expr = self._texto_o_variable(m.group(1)), m.group(2)
                valor = self._copiar_si_mutable(self.evaluar_expresion(expr))
                datos = self._leer_base_datos()
                datos[clave] = valor
                self._escribir_base_datos(datos)
                print(f"[SiPi] Dato guardado: {clave} = {valor}")
            return None

        if cmd == "obtener_dato":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                clave, var = self._texto_o_variable(m.group(1)), m.group(2)
                datos = self._leer_base_datos()
                self._declarar_variable_local(var, datos.get(clave, ""))
            return None

        if cmd == "borrar_dato":
            clave = self._texto_o_variable(resto)
            datos = self._leer_base_datos()
            datos.pop(clave, None)
            self._escribir_base_datos(datos)
            return None

        # ----- Base de datos SQLite real (para apps medianas/grandes) -----
        if cmd == "sqlite_conectar":
            m = _m(r'^(.+?)\s+como\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: sqlite_conectar "archivo.db" como nombre')
            ruta_bd = self._texto_o_variable(m.group(1))
            alias = m.group(2)
            ruta_completa = os.path.join(self.base_dir, ruta_bd) if not os.path.isabs(ruta_bd) else ruta_bd
            conexion = sqlite3.connect(ruta_completa, check_same_thread=False)
            conexion.row_factory = sqlite3.Row
            self.entorno.conexiones_sqlite[alias] = conexion
            print(f"[SiPi] Conectado a base de datos SQLite '{ruta_bd}' como '{alias}'")
            return None

        if cmd == "sqlite_ejecutar":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: sqlite_ejecutar nombre "SENTENCIA SQL"')
            alias, sql_expr = m.group(1), m.group(2)
            if alias not in self.entorno.conexiones_sqlite:
                raise SiPiError(f"No hay ninguna conexion SQLite abierta llamada '{alias}'. Usa sqlite_conectar primero.")
            sentencia = self._texto_o_variable(sql_expr)
            conexion = self.entorno.conexiones_sqlite[alias]
            try:
                conexion.execute(sentencia)
                conexion.commit()
            except sqlite3.Error as e:
                raise SiPiError(f"Error SQL en '{alias}': {e}")
            return None

        if cmd == "sqlite_consultar":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: sqlite_consultar nombre "SELECT ..." en variable')
            alias, sql_expr, var = m.group(1), m.group(2), m.group(3)
            if alias not in self.entorno.conexiones_sqlite:
                raise SiPiError(f"No hay ninguna conexion SQLite abierta llamada '{alias}'. Usa sqlite_conectar primero.")
            sentencia = self._texto_o_variable(sql_expr)
            conexion = self.entorno.conexiones_sqlite[alias]
            try:
                cursor = conexion.execute(sentencia)
                filas = [dict(fila) for fila in cursor.fetchall()]
            except sqlite3.Error as e:
                raise SiPiError(f"Error SQL en '{alias}': {e}")
            self._declarar_variable_local(var, filas)
            return None

        if cmd == "sqlite_cerrar":
            alias = resto.strip()
            conexion = self.entorno.conexiones_sqlite.pop(alias, None)
            if conexion:
                conexion.close()
                print(f"[SiPi] Conexion SQLite '{alias}' cerrada.")
            return None

        # ----- PostgreSQL y MySQL reales (para sistemas de empresa) -----
        # SQLite es perfecto para apps chicas/medianas, pero una empresa
        # grande casi siempre ya tiene (o necesita) Postgres o MySQL: mas
        # capacidad para muchos usuarios escribiendo a la vez, replicas,
        # backups administrados por su equipo de infraestructura, etc.
        # Usa drivers 100% Python puro (pg8000 / PyMySQL, sin compilar
        # nada), instalados automaticamente la primera vez que se usan,
        # asi que funciona igual en Windows, Linux, Mac o un contenedor
        # Docker sin instalar herramientas de compilacion en ningun lado.
        if cmd == "postgres_conectar":
            m = _m(r'^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+como\s+([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s+con\s+pool\s+(\d+))?$', resto)
            if not m:
                raise SiPiError('Sintaxis: postgres_conectar "host" puerto "basedatos" "usuario" "clave" como nombre  (opcional: con pool N)')
            if not asegurar_paquete("pg8000"):
                raise SiPiError("No se pudo preparar el driver de PostgreSQL (pg8000).")
            import pg8000.native
            host = self._texto_o_variable(m.group(1))
            puerto = int(self.evaluar_expresion(m.group(2)))
            basedatos = self._texto_o_variable(m.group(3))
            usuario = self._texto_o_variable(m.group(4))
            clave = self._texto_o_variable(m.group(5))
            alias = m.group(6)
            tamano_pool = int(m.group(7)) if m.group(7) else None

            def _crear_conexion_postgres():
                return pg8000.native.Connection(usuario, password=clave, host=host, port=puerto, database=basedatos)

            try:
                if tamano_pool:
                    pool = PoolConexionesBD(_crear_conexion_postgres, tamano_pool)
                    pool.precalentar_una()  # valida la conexion de una, no espera al primer uso para fallar
                    self.entorno.conexiones_sqlite[alias] = ("postgres_pool", pool)
                    print(f"[SiPi] Conectado a PostgreSQL en '{host}:{puerto}/{basedatos}' como '{alias}' (pool de {tamano_pool} conexiones)")
                else:
                    conexion = _crear_conexion_postgres()
                    self.entorno.conexiones_sqlite[alias] = ("postgres", conexion)
                    print(f"[SiPi] Conectado a PostgreSQL en '{host}:{puerto}/{basedatos}' como '{alias}'")
            except Exception as e:
                raise SiPiError(f"No se pudo conectar a PostgreSQL: {e}")
            return None

        if cmd == "mysql_conectar":
            m = _m(r'^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+(.+?)\s+como\s+([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s+con\s+pool\s+(\d+))?$', resto)
            if not m:
                raise SiPiError('Sintaxis: mysql_conectar "host" puerto "basedatos" "usuario" "clave" como nombre  (opcional: con pool N)')
            if not asegurar_paquete("pymysql", "PyMySQL"):
                raise SiPiError("No se pudo preparar el driver de MySQL (PyMySQL).")
            import pymysql
            import pymysql.cursors
            host = self._texto_o_variable(m.group(1))
            puerto = int(self.evaluar_expresion(m.group(2)))
            basedatos = self._texto_o_variable(m.group(3))
            usuario = self._texto_o_variable(m.group(4))
            clave = self._texto_o_variable(m.group(5))
            alias = m.group(6)
            tamano_pool = int(m.group(7)) if m.group(7) else None

            def _crear_conexion_mysql():
                return pymysql.connect(host=host, port=puerto, user=usuario, password=clave,
                                        database=basedatos, cursorclass=pymysql.cursors.DictCursor,
                                        autocommit=True)

            try:
                if tamano_pool:
                    pool = PoolConexionesBD(_crear_conexion_mysql, tamano_pool)
                    pool.precalentar_una()
                    self.entorno.conexiones_sqlite[alias] = ("mysql_pool", pool)
                    print(f"[SiPi] Conectado a MySQL en '{host}:{puerto}/{basedatos}' como '{alias}' (pool de {tamano_pool} conexiones)")
                else:
                    conexion = _crear_conexion_mysql()
                    self.entorno.conexiones_sqlite[alias] = ("mysql", conexion)
                    print(f"[SiPi] Conectado a MySQL en '{host}:{puerto}/{basedatos}' como '{alias}'")
            except Exception as e:
                raise SiPiError(f"No se pudo conectar a MySQL: {e}")
            return None

        if cmd in ("postgres_ejecutar", "mysql_ejecutar"):
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$', resto)
            if not m:
                raise SiPiError(f'Sintaxis: {cmd} nombre "SENTENCIA SQL"')
            alias, sql_expr = m.group(1), m.group(2)
            conexion_guardada = self.entorno.conexiones_sqlite.get(alias)
            if not conexion_guardada or not isinstance(conexion_guardada, tuple):
                raise SiPiError(f"No hay ninguna conexion abierta llamada '{alias}'. Conectate primero con {cmd.split('_')[0]}_conectar.")
            motor, recurso = conexion_guardada
            sentencia = self._texto_o_variable(sql_expr)
            es_pool = motor.endswith("_pool")
            conexion = recurso.obtener() if es_pool else recurso
            try:
                if motor.startswith("postgres"):
                    conexion.run(sentencia)
                else:
                    with conexion.cursor() as cursor:
                        cursor.execute(sentencia)
            except Exception as e:
                raise SiPiError(f"Error SQL en '{alias}' ({motor}): {e}")
            finally:
                if es_pool:
                    recurso.liberar(conexion)
            return None

        if cmd in ("postgres_consultar", "mysql_consultar"):
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError(f'Sintaxis: {cmd} nombre "SELECT ..." en variable')
            alias, sql_expr, var = m.group(1), m.group(2), m.group(3)
            conexion_guardada = self.entorno.conexiones_sqlite.get(alias)
            if not conexion_guardada or not isinstance(conexion_guardada, tuple):
                raise SiPiError(f"No hay ninguna conexion abierta llamada '{alias}'. Conectate primero con {cmd.split('_')[0]}_conectar.")
            motor, recurso = conexion_guardada
            sentencia = self._texto_o_variable(sql_expr)
            es_pool = motor.endswith("_pool")
            conexion = recurso.obtener() if es_pool else recurso
            try:
                if motor.startswith("postgres"):
                    filas_crudas = conexion.run(sentencia)
                    columnas = [c["name"] for c in conexion.columns] if conexion.columns else []
                    filas = [dict(zip(columnas, fila)) for fila in filas_crudas]
                else:
                    with conexion.cursor() as cursor:
                        cursor.execute(sentencia)
                        filas = list(cursor.fetchall())
            except Exception as e:
                raise SiPiError(f"Error SQL en '{alias}' ({motor}): {e}")
            finally:
                if es_pool:
                    recurso.liberar(conexion)
            self._declarar_variable_local(var, filas)
            return None

        if cmd in ("postgres_cerrar", "mysql_cerrar"):
            alias = resto.strip()
            conexion_guardada = self.entorno.conexiones_sqlite.pop(alias, None)
            if conexion_guardada and isinstance(conexion_guardada, tuple):
                motor, recurso = conexion_guardada
                if motor.endswith("_pool"):
                    recurso.cerrar_todas()
                else:
                    recurso.close()
                print(f"[SiPi] Conexion '{alias}' cerrada.")
            return None

        # ----- Migraciones de esquema (para desplegar cambios a la base de
        # datos de forma controlada y versionada, tipo Flyway/Alembic pero
        # simple). Funciona igual sobre SQLite, PostgreSQL o MySQL (con o
        # sin pool), porque usa los helpers genericos de mas abajo que ya
        # saben hablar con cualquiera de los tres. -----
        if cmd == "migracion_crear":
            m = _m(r'^(.+?)\s+(.+)$', resto.strip())
            if not m:
                raise SiPiError('Sintaxis: migracion_crear "carpeta" "nombre_descriptivo"')
            carpeta = self._texto_o_variable(m.group(1))
            nombre_descriptivo = self._texto_o_variable(m.group(2))
            self._migracion_crear(carpeta, nombre_descriptivo)
            return None

        if cmd == "migracion_aplicar":
            m = _m(r'^(.+?)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto.strip())
            if not m:
                raise SiPiError('Sintaxis: migracion_aplicar "carpeta" en nombre_conexion')
            carpeta = self._texto_o_variable(m.group(1))
            alias = m.group(2)
            self._migracion_aplicar(carpeta, alias)
            return None

        if cmd == "migracion_revertir":
            m = _m(r'^(.+?)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto.strip())
            if not m:
                raise SiPiError('Sintaxis: migracion_revertir "carpeta" en nombre_conexion')
            carpeta = self._texto_o_variable(m.group(1))
            alias = m.group(2)
            self._migracion_revertir(carpeta, alias)
            return None

        if cmd == "migracion_estado":
            m = _m(r'^(.+?)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto.strip())
            if not m:
                raise SiPiError('Sintaxis: migracion_estado "carpeta" en nombre_conexion')
            carpeta = self._texto_o_variable(m.group(1))
            alias = m.group(2)
            self._migracion_estado(carpeta, alias)
            return None

        # ----- JSON real (lee/escribe archivos .json de verdad) -----
        if cmd == "json_guardar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
            if m:
                nombre_var, ruta_expr = m.groups()
                ruta = self._texto_o_variable(ruta_expr)
                ruta_final = os.path.join(self.base_dir, ruta)
                valor = self._obtener_variable(nombre_var)
                os.makedirs(os.path.dirname(ruta_final) or ".", exist_ok=True)
                with open(ruta_final, "w", encoding="utf-8") as f:
                    json.dump(valor, f, ensure_ascii=False, indent=2)
                print(f"[SiPi] JSON guardado: {ruta_final}")
            return None

        if cmd == "json_leer":
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                ruta = self._texto_o_variable(m.group(1))
                var = m.group(2)
                ruta_final = os.path.join(self.base_dir, ruta)
                with open(ruta_final, "r", encoding="utf-8") as f:
                    self._declarar_variable_local(var, json.load(f))
            return None

        if cmd == "json_crear":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)$", resto.strip())
            if m:
                self._declarar_variable_local(m.group(1), {})
            return None

        if cmd == "json_texto":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                nombre_var, var_destino = m.groups()
                valor = self._obtener_variable(nombre_var)
                self._declarar_variable_local(var_destino, json.dumps(valor, ensure_ascii=False, indent=2))
            return None

        # ----- CSV real (lee/escribe archivos .csv de verdad, ideal para Excel) -----
        if cmd == "csv_leer":
            m = _m(r"^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", resto)
            if m:
                ruta = self._texto_o_variable(m.group(1))
                var = m.group(2)
                ruta_final = os.path.join(self.base_dir, ruta)
                with open(ruta_final, "r", encoding="utf-8", newline="") as f:
                    lector = csv.DictReader(f)
                    filas = [dict(fila) for fila in lector]
                self._declarar_variable_local(var, filas)
            return None

        if cmd == "csv_guardar":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
            if m:
                nombre_var, ruta_expr = m.groups()
                ruta = self._texto_o_variable(ruta_expr)
                ruta_final = os.path.join(self.base_dir, ruta)
                filas = self._obtener_variable(nombre_var, [])
                os.makedirs(os.path.dirname(ruta_final) or ".", exist_ok=True)
                with open(ruta_final, "w", encoding="utf-8", newline="") as f:
                    if isinstance(filas, list) and filas and isinstance(filas[0], dict):
                        columnas = list(filas[0].keys())
                        escritor = csv.DictWriter(f, fieldnames=columnas)
                        escritor.writeheader()
                        for fila in filas:
                            escritor.writerow(fila)
                    else:
                        escritor = csv.writer(f)
                        for fila in filas:
                            escritor.writerow(fila if isinstance(fila, list) else [fila])
                print(f"[SiPi] CSV guardado: {ruta_final}")
            return None

        # ----- Peticiones web reales (HTTP) -----
        if cmd == "obtener_url":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                url, var = self._texto_o_variable(m.group(1)), m.group(2)
                try:
                    with urllib.request.urlopen(url, timeout=15) as resp:
                        self._declarar_variable_local(var, resp.read().decode("utf-8", errors="replace"))
                except Exception as e:
                    print(f"[SiPi] Error al obtener la URL: {e}")
                    self._declarar_variable_local(var, "")
            return None

        # ----- Texto -----
        if cmd == "longitud":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                valor = self.evaluar_expresion(m.group(1))
                self._declarar_variable_local(m.group(2), len(str(valor)))
            return None

        if cmd == "mayusculas":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                valor = self.evaluar_expresion(m.group(1))
                self._declarar_variable_local(m.group(2), str(valor).upper())
            return None

        if cmd == "minusculas":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                valor = self.evaluar_expresion(m.group(1))
                self._declarar_variable_local(m.group(2), str(valor).lower())
            return None

        # ----- Matematica extendida -----
        if cmd == "azar_entre":
            m = _m(r'^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                a = int(self.evaluar_expresion(m.group(1)))
                b = int(self.evaluar_expresion(m.group(2)))
                self._declarar_variable_local(m.group(3), random.randint(a, b))
            return None

        if cmd == "raiz":
            m = _m(r'^(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                valor = float(self.evaluar_expresion(m.group(1)))
                self._declarar_variable_local(m.group(2), math.sqrt(valor))
            return None

        if cmd == "potencia":
            m = _m(r'^(.+?)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                base = float(self.evaluar_expresion(m.group(1)))
                exp = float(self.evaluar_expresion(m.group(2)))
                resultado = base ** exp
                self._declarar_variable_local(m.group(3), int(resultado) if resultado == int(resultado) else resultado)
            return None

        # ----- Generador de sitios web reales -----
        if cmd == "generar_pagina_web":
            nombre_sitio = self._texto_o_variable(resto) if resto.strip() else "MiSitioSiPi"
            self._generar_sitio_web(nombre_sitio)
            return None

        if cmd == "iniciar_servidor_web":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+(.+)$', resto)
            if m:
                carpeta = self._texto_o_variable(m.group(1))
                puerto = int(self.evaluar_expresion(m.group(2)))
                self._iniciar_servidor_web(carpeta, puerto)
            return None

        # ----- API Web real: backend completo, no solo archivos estaticos -----
        # escuchar_ruta "/api/usuarios" con manejar_usuarios
        if cmd == "escuchar_ruta":
            m = _m(r'^(".+?"|\S+)\s+con\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if not m:
                raise SiPiError('Sintaxis: escuchar_ruta "/api/ruta" con nombre_funcion')
            ruta_api = self._texto_o_variable(m.group(1))
            if not ruta_api.startswith("/"):
                ruta_api = "/" + ruta_api
            nombre_funcion = m.group(2)
            self.entorno.rutas_api[ruta_api] = nombre_funcion
            print(f"[SiPi] Ruta registrada: {ruta_api} -> {nombre_funcion}()")
            return None

        # Autenticacion real para la API: sin esto, cualquiera que
        # encuentre la URL puede llamar cualquier ruta. Con una clave
        # (API key) requerida, el cliente tiene que mandar el header
        # 'Authorization: Bearer <clave>' o 'X-API-Key: <clave>'. Las rutas
        # de salud (/salud, /health, /healthz) quedan siempre abiertas a
        # proposito, porque un balanceador de carga o Kubernetes necesita
        # poder chequearlas sin credenciales.
        if cmd == "requerir_autenticacion":
            clave = self.evaluar_expresion(resto)
            self.entorno.clave_api_requerida = str(clave)
            return None

        # Limite de peticiones por IP en una ventana de tiempo (rate
        # limiting real, no simbolico): protege contra un cliente
        # (malicioso o con un bug) que bombardee la API, y es algo que
        # cualquier API publica seria necesita de entrada.
        if cmd == "limitar_peticiones":
            m = _m(r"^(\d+)\s+por_minuto$", resto.strip())
            if not m:
                raise SiPiError("Sintaxis: limitar_peticiones 60 por_minuto")
            self.entorno.limite_peticiones_por_minuto = int(m.group(1))
            return None

        # iniciar_api_web 8000
        if cmd == "iniciar_api_web":
            m_hilos = _m(r"^(.+?)\s+con\s+hasta\s+(\d+)\s+conexiones$", resto.strip())
            if m_hilos:
                puerto = int(self.evaluar_expresion(m_hilos.group(1)))
                self._iniciar_api_web(puerto, max_hilos=int(m_hilos.group(2)))
            else:
                puerto = int(self.evaluar_expresion(resto))
                self._iniciar_api_web(puerto)
            return None

        if cmd == "detener_api_web":
            self._detener_api_web()
            return None

        # ----- Paginas web declarativas: HTML sin escribir HTML -----
        if cmd == "pagina_web":
            m = _m(r'^"([^"]*)"$', resto.strip())
            fin_pagina = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                nombre_sitio = self.interpolar(m.group(1))
                elementos_html, tema, color_acento = self._construir_elementos_pagina(i + 1, fin_pagina)
                self._generar_pagina_declarativa(nombre_sitio, elementos_html, tema, color_acento)
            return fin_pagina + 1

        # ----- GUI real con tkinter -----
        if cmd == "ventana":
            m = _m(r'^"([^"]*)"\s+(\d+)\s+(\d+)$', resto)
            fin_ventana = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                titulo, ancho, alto = m.group(1), int(m.group(2)), int(m.group(3))
                self._crear_ventana_gui(titulo, ancho, alto, i + 1, fin_ventana)
            return fin_ventana + 1

        if cmd in ("boton", "etiqueta", "entrada", "imagen", "cuadro", "casilla", "lista", "barra_progreso", "menu_desplegable"):
            self._widget_gui(cmd, resto)
            return None

        if cmd == "pestanias":
            m = _m(r"^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$", resto)
            fin_pestanias = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                x, y, ancho, alto = (int(v) for v in m.groups())
                from tkinter import ttk
                nb = ttk.Notebook(self.ventana_tk, width=ancho, height=alto)
                nb.place(x=x, y=y)
                anterior_nb = getattr(self, "notebook_actual", None)
                self.notebook_actual = nb
                self._ejecutar_bloque(i + 1, fin_pestanias)
                self.notebook_actual = anterior_nb
            return fin_pestanias + 1

        if cmd == "pestana":
            m = _m(r'^"([^"]*)"$', resto.strip())
            fin_pestana = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m and getattr(self, "notebook_actual", None) is not None:
                titulo_pestana = self.interpolar(m.group(1))
                marco = self._tk.Frame(self.notebook_actual, bg="#1e1e2e")
                self.notebook_actual.add(marco, text=titulo_pestana)
                anterior_contenedor = getattr(self, "contenedor_actual", None)
                self.contenedor_actual = marco
                self._ejecutar_bloque(i + 1, fin_pestana)
                self.contenedor_actual = anterior_contenedor
            return fin_pestana + 1

        if cmd == "generar_app_android":
            nombre_app = self._texto_o_variable(resto) if resto.strip() else "MiAppSiPi"
            self._generar_proyecto_android(nombre_app)
            return None

        if cmd == "generar_app_windows":
            nombre_app = self._texto_o_variable(resto) if resto.strip() else "MiAppSiPi"
            self._generar_proyecto_windows(nombre_app)
            return None

        # Item 4 del roadmap: transpilar TODO el programa a Python real
        # (no solo funciones sueltas), para correr sin sipi.py y mas rapido.
        if cmd == "compilar_a_python":
            ruta_salida = self._texto_o_variable(resto) if resto.strip() else "programa_compilado.py"
            self._compilar_programa_a_python(ruta_salida)
            return None

        # Item 9 del roadmap: compilar funciones SiPi a JavaScript real,
        # para que corran en el navegador del usuario (sin servidor).
        if cmd == "compilar_a_js":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+(?:\s*,\s*[\w\u0900-\u097F\u0980-\u09FF]+)*)\s+(".*")$', resto)
            if m:
                nombres = [n.strip() for n in m.group(1).split(",")]
                ruta_salida = self._texto_o_variable(m.group(2))
            else:
                nombres = [resto.strip()]
                ruta_salida = f"{resto.strip()}.js"
            self._compilar_funciones_a_js(nombres, ruta_salida)
            return None

        # Item 11 del roadmap: empaquetar la API web (iniciar_api_web /
        # escuchar_ruta) y desplegarla de verdad a la nube.
        if cmd == "publicar_nube":
            m = _m(r'^(".*"|\S+)(?:\s+(vercel|netlify|railway))?$', resto.strip())
            if m:
                nombre_app = self._texto_o_variable(m.group(1))
                proveedor = m.group(2) or "vercel"
            else:
                nombre_app, proveedor = "mi_api_sipi", "vercel"
            self._publicar_nube(nombre_app, proveedor)
            return None

        # Sistema "Visual": editor WYSIWYG real que corre en el navegador.
        # Muestra la ventana tal como se va a ver, permite arrastrar
        # widgets con el mouse y editar texto con un click -- y todo eso
        # reescribe el .sipi de origen automaticamente, sin tocar nada a
        # mano. Uso: 'editor_visual' en cualquier punto del programa (no
        # hace falta que la ventana ya se haya ejecutado).
        if cmd == "editor_visual":
            self._lanzar_editor_visual()
            return None

        # ---------- Preparado para produccion / empresas ----------

        # Variables de entorno: la forma estandar en la industria de pasar
        # configuracion y secretos (claves de API, cadenas de conexion a
        # bases de datos, etc.) sin escribirlos en el codigo fuente. Es lo
        # primero que pide cualquier plataforma de hosting (Docker, Vercel,
        # Railway, Kubernetes...).
        if cmd == "variable_entorno":
            m = _m(r'^("(?:[^"]*)"|\S+)(?:\s+o\s+(.+))?\s*->\s*(\w+)$', resto.strip())
            if not m:
                raise SiPiError('Sintaxis: variable_entorno "NOMBRE" -> variable  (opcional: "NOMBRE" o "valor_por_defecto" -> variable)')
            nombre_env = self._texto_o_variable(m.group(1))
            valor_default = self.evaluar_expresion(m.group(2)) if m.group(2) else None
            valor = os.environ.get(nombre_env, valor_default)
            self._declarar_variable_local(m.group(3), valor)
            return None

        if cmd == "existe_variable_entorno":
            m = _m(r'^("(?:[^"]*)"|\S+)\s*->\s*(\w+)$', resto.strip())
            if m:
                nombre_env = self._texto_o_variable(m.group(1))
                self._declarar_variable_local(m.group(2), nombre_env in os.environ)
            return None

        # Logging estructurado (formato JSON Lines, un objeto JSON por
        # linea): el estandar real que usan los sistemas de monitoreo en
        # produccion (Datadog, CloudWatch, ELK, Grafana Loki...) para poder
        # buscar y graficar logs automaticamente, en vez de parsear texto
        # libre con regex. Se escribe en 'sipi.log' junto al programa Y se
        # imprime en pantalla, asi sirve tanto para desarrollo como para
        # produccion real.
        if cmd in ("registrar_log", "log_info", "log_advertencia", "log_error"):
            nivel = {"registrar_log": None, "log_info": "info",
                      "log_advertencia": "advertencia", "log_error": "error"}[cmd]
            if nivel is None:
                m = _m(r'^(info|advertencia|error)\s+(.+)$', resto.strip())
                if not m:
                    raise SiPiError('Sintaxis: registrar_log info|advertencia|error "mensaje"')
                nivel, mensaje_expr = m.group(1), m.group(2)
            else:
                mensaje_expr = resto
            mensaje = self.evaluar_expresion(mensaje_expr)
            self._escribir_log(nivel, mensaje)
            return None

        # Aserciones para pruebas automatizadas: la base de cualquier
        # sistema en el que una empresa pueda confiar es poder verificar
        # que sigue funcionando despues de cada cambio, sin probarlo a
        # mano cada vez.
        if cmd == "afirmar":
            m = _m(r'^(.+?)(?:\s*,\s*(".*"))?$', resto.strip())
            condicion_txt = m.group(1) if m else resto.strip()
            mensaje_custom = self._texto_o_variable(m.group(2)) if m and m.group(2) else None
            if not self._evaluar_condicion(condicion_txt):
                mensaje = mensaje_custom or f"Se esperaba que se cumpliera: {condicion_txt}"
                self._pruebas_fallidas = getattr(self, "_pruebas_fallidas", 0) + 1
                if getattr(self, "_modo_pruebas", False):
                    print(f"[SiPi] ✗ FALLO: {mensaje}")
                else:
                    raise SiPiError(f"Afirmacion falsa: {mensaje}")
            else:
                self._pruebas_exitosas = getattr(self, "_pruebas_exitosas", 0) + 1
                if getattr(self, "_modo_pruebas", False):
                    print(f"[SiPi] ✓ OK: {condicion_txt}")
            return None

        if cmd == "iniciar_pruebas":
            self._modo_pruebas = True
            self._pruebas_exitosas = 0
            self._pruebas_fallidas = 0
            print("[SiPi] Modo de pruebas activado: 'afirmar' ahora reporta cada caso en vez de detener el programa.")
            return None

        if cmd == "resumen_pruebas":
            exitosas = getattr(self, "_pruebas_exitosas", 0)
            fallidas = getattr(self, "_pruebas_fallidas", 0)
            total = exitosas + fallidas
            print(f"[SiPi] Resumen de pruebas: {exitosas}/{total} exitosas.")
            if fallidas > 0:
                print(f"[SiPi] {fallidas} prueba(s) fallaron.")
                sys.exit(1)  # codigo de salida distinto de 0: para que un pipeline de CI/CD detecte el fallo
            return None

        # Contenedor Docker real: el estandar de facto para que una empresa
        # despliegue cualquier sistema en su propia infraestructura (nube
        # privada, Kubernetes, lo que sea), sin depender de un proveedor
        # especifico como en 'publicar_nube'.
        if cmd == "generar_dockerfile":
            nombre_app = self._texto_o_variable(resto) if resto.strip() else "app_sipi"
            self._generar_dockerfile(nombre_app)
            return None

        # ----- Juegos reales con pygame -----
        if cmd == "crear_juego":
            m = _m(r'^"([^"]*)"\s+(\d+)\s+(\d+)$', resto)
            fin_juego = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                titulo, ancho, alto = m.group(1), int(m.group(2)), int(m.group(3))
                cuerpo = self.lineas[i + 1:fin_juego]
                self._crear_juego_pygame(titulo, ancho, alto, cuerpo)
            return fin_juego + 1

        # ----- 3D basico v1 (primera version): wireframe con proyeccion en
        # perspectiva, sin texturas ni iluminacion todavia. Es un punto de
        # partida real y probado, no una simulacion; ver DOCUMENTACION.md
        # para el alcance exacto y lo que falta para un motor 3D completo. -----
        if cmd == "escena_3d":
            m = _m(r'^"([^"]*)"\s+(\d+)\s+(\d+)$', resto)
            fin_escena = self._encontrar_fin(i, BLOQUES_QUE_ABREN)
            if m:
                titulo, ancho, alto = m.group(1), int(m.group(2)), int(m.group(3))
                cuerpo = self.lineas[i + 1:fin_escena]
                self._crear_escena_3d(titulo, ancho, alto, cuerpo)
            return fin_escena + 1

        # ----- Reasignacion sin 'variable' (CRITICO #1 de tu feedback) -----
        # Antes, escribir 'carga = 5' en vez de 'variable carga = 5' para
        # reasignar una variable YA EXISTENTE tiraba 'Comando desconocido:
        # carga', algo confuso para quien viene de otros lenguajes donde
        # reasignar no necesita una palabra magica. Ahora: si la linea
        # completa tiene forma 'nombre = expr' y 'nombre' YA es una
        # variable declarada en el ambito actual, se trata como un
        # 'sumar'/'variable' implicito (reasignacion). 'variable' sigue
        # siendo obligatorio para la PRIMERA declaracion (si 'nombre' no
        # existe todavia, cae al mensaje de 'Comando desconocido' de
        # siempre, que ya sugiere el comando mas parecido).
        m_reasignacion = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s*=\s*(?!=)(.+)$", linea)
        if m_reasignacion and cmd not in COMANDOS_CONOCIDOS:
            nombre_var, expr_var = m_reasignacion.groups()
            if self._existe_variable(nombre_var):
                if nombre_var in self.entorno.constantes:
                    raise SiPiError(f"No se puede modificar la constante '{nombre_var}'")
                valor_nuevo = self._copiar_si_mutable(self.evaluar_expresion(expr_var))
                if nombre_var in self.entorno.tipos_variables:
                    self._verificar_tipo(nombre_var, self.entorno.tipos_variables[nombre_var], valor_nuevo)
                self._mutar_variable(nombre_var, valor_nuevo)
                return None

        sugerencias = difflib.get_close_matches(cmd, COMANDOS_CONOCIDOS, n=1, cutoff=0.6)
        if sugerencias:
            raise SiPiError(f"Comando desconocido: '{cmd}'. ¿Quisiste decir '{sugerencias[0]}'?")
        raise SiPiError(f"Comando desconocido: '{cmd}'")

    # ---------- Condiciones ----------

    def _separar_nivel_superior(self, texto, separador):
        """Separa un texto por un separador, ignorando lo que este entre comillas."""
        partes = []
        actual = ""
        dentro_comillas = False
        i = 0
        while i < len(texto):
            c = texto[i]
            if c == '"':
                dentro_comillas = not dentro_comillas
            if not dentro_comillas and texto[i:i + len(separador)] == separador:
                partes.append(actual)
                actual = ""
                i += len(separador)
                continue
            actual += c
            i += 1
        partes.append(actual)
        return partes

    @staticmethod
    def _parsear_parametros(texto_params):
        """Convierte 'a, b: entero, c' en [('a', None), ('b', 'entero'), ('c', None)].
        Tipos opcionales (#21) tambien en parametros de funcion: si se
        declara, se valida el valor recibido en cada llamada."""
        params_info = []
        for p in texto_params.split(","):
            p = p.strip()
            if not p:
                continue
            if ":" in p:
                nombre_p, tipo_p = p.split(":", 1)
                params_info.append((nombre_p.strip(), tipo_p.strip()))
            else:
                params_info.append((p, None))
        return params_info

    def _armar_scope_de_llamada(self, nombre_fn, params_info, valores):
        """Crea el ambito local de una llamada a funcion, verificando los
        tipos declarados en los parametros (si los hay)."""
        scope = {}
        for (nombre_p, tipo_p), valor in zip(params_info, valores):
            if tipo_p:
                self._verificar_tipo(f"{nombre_p} (parametro de {nombre_fn})", tipo_p, valor)
            scope[nombre_p] = valor
        return scope

    def _invocar_funcion(self, nombre, args_txt):
        """Invoca una funcion definida en el programa o en un modulo importado,
        cambiando temporalmente el contexto de lineas si la funcion vino de otro
        archivo. Cada llamada tiene su propio ambito local de variables (para
        que la recursion funcione correctamente: llamadas anidadas a la misma
        funcion no se pisan entre si). Devuelve el valor de 'devolver', o None
        si no hubo retorno."""
        if nombre not in self.entorno.funciones:
            sugerencias = difflib.get_close_matches(nombre, list(self.entorno.funciones.keys()), n=1, cutoff=0.6)
            extra = f" ¿Quisiste decir '{sugerencias[0]}'?" if sugerencias else ""
            raise SiPiError(f"Funcion no definida: {nombre}.{extra}")
        # Los argumentos se evaluan en el ambito de quien llama, ANTES de
        # entrar al nuevo ambito local de la funcion invocada.
        valores_params = [self.evaluar_expresion(a) for a in args_txt]
        return self._invocar_funcion_con_valores(nombre, valores_params)

    def _cadena_de_clases(self, nombre_clase):
        """Devuelve [nombre_clase, padre, abuelo, ...] siguiendo 'hereda_de'.
        Detecta herencia circular para no colgarse en un bucle infinito."""
        cadena = []
        actual = nombre_clase
        vistos = set()
        while actual is not None and actual not in vistos:
            vistos.add(actual)
            cadena.append(actual)
            info = self.entorno.clases.get(actual)
            actual = info["padre"] if info else None
        return cadena

    def _instanciar_clase(self, nombre_clase):
        """Crea un objeto nuevo de 'nombre_clase': combina los campos por
        defecto de toda la cadena de herencia (los de la clase padre
        primero, para que la clase hija pueda pisarlos con los suyos)."""
        if nombre_clase not in self.entorno.clases:
            raise SiPiError(f"Clase no definida: '{nombre_clase}'")
        cadena = list(reversed(self._cadena_de_clases(nombre_clase)))
        objeto = {}
        for nombre_c in cadena:
            campos = self.entorno.clases[nombre_c]["campos"]
            objeto.update(copy.deepcopy(campos))
        objeto["__clase__"] = nombre_clase
        return objeto

    def _buscar_metodo_en_cadena(self, nombre_clase, nombre_metodo):
        """Busca un metodo empezando por 'nombre_clase' y subiendo por sus
        clases padre (asi una subclase puede heredar metodos que no
        redefine, y sobreescribir los que si)."""
        for nombre_c in self._cadena_de_clases(nombre_clase):
            info = self.entorno.clases.get(nombre_c)
            if info and nombre_metodo in info["metodos"]:
                return info["metodos"][nombre_metodo]
        return None

    def _invocar_metodo_resuelto(self, metodo, objeto, valores):
        """Ejecuta un metodo ya resuelto (params, ini, fin, lineas), con el
        objeto disponible dentro del metodo como la variable implicita
        'este' (equivalente a 'self'/'this'). Como los diccionarios de
        Python se pasan por referencia, cualquier
        'diccionario_asignar este "campo" valor' dentro del metodo modifica
        el objeto real, no una copia."""
        params, ini, fin_m, lineas_m = metodo
        lineas_anteriores = self.lineas
        self.lineas = lineas_m
        if not hasattr(self, "pila_llamadas"):
            self.pila_llamadas = []
        self.pila_llamadas.append(f"{objeto.get('__clase__', '?')}.metodo")
        nuevo_scope = dict(zip(params, valores))
        nuevo_scope["este"] = objeto
        self.pila_scopes.append(nuevo_scope)
        profundidad_anterior = self.profundidad_bucles
        self.profundidad_bucles = 0
        try:
            self._ejecutar_bloque(ini, fin_m)
            return None
        except RetornoFuncion as r:
            return r.valor
        finally:
            self.lineas = lineas_anteriores
            self.pila_scopes.pop()
            self.pila_llamadas.pop()
            self.profundidad_bucles = profundidad_anterior

    def _clonar_para_hilo(self):
        """Prepara un Interprete independiente para correr una funcion en un
        hilo de sistema operativo real (threading.Thread), SIN arriesgar
        los datos internos del interprete original a una condicion de
        carrera.

        Por que hace falta esto y no alcanza con llamar _invocar_funcion
        directo desde el hilo nuevo: ese metodo reasigna temporalmente
        'self.lineas', y apila/desapila en 'self.pila_scopes' y
        'self.pila_llamadas' -- son atributos MUTABLES de una sola
        instancia compartida. Si dos hilos llamaran funciones al mismo
        tiempo sobre el mismo 'self', se pisarian esos atributos entre si
        (una funcion podria terminar ejecutando el codigo de otra, o la
        pila de llamadas para los mensajes de error quedar corrupta).

        La solucion: cada hilo corre sobre un CLON liviano que tiene sus
        propias pila_scopes/pila_llamadas/profundidad_bucles, y su propia
        COPIA de las variables globales tomada en el momento de crear el
        hilo (para que el hilo pueda leer el estado actual, pero sin que
        sus escrituras internas puedan pisar variables del programa
        principal por accidente). 'funciones' y 'clases' SI se comparten
        por referencia (son de solo lectura durante la ejecucion: un
        programa SiPi normal las define al principio y no las modifica
        dinamicamente), igual que 'self.lineas' del archivo principal.

        Si necesitas que un hilo comunique un resultado hacia afuera, la
        forma segura es el valor de 'devolver' de la funcion (leelo con
        'hilo_resultado'), no una variable global compartida."""
        clon = copy.copy(self)
        clon.entorno = copy.copy(self.entorno)
        clon.entorno.variables = dict(self.entorno.variables)  # copia propia, no compartida
        clon.pila_scopes = []
        clon.pila_llamadas = []
        clon.profundidad_bucles = 0
        clon._cache_fin_bloque = self._cache_fin_bloque  # indices de bloques: no cambian en tiempo de ejecucion, seguro compartir
        return clon

    def _invocar_funcion_con_valores(self, nombre, valores):
        """Igual que _invocar_funcion, pero recibe los argumentos ya evaluados
        (valores de Python reales) en lugar de texto a evaluar. Se usa para
        invocar funciones SiPi desde codigo externo al lenguaje mismo, como
        el manejador de rutas de la API web."""
        if nombre not in self.entorno.funciones:
            raise SiPiError(f"Funcion no definida: {nombre}")
        params_info, ini, fin_fn, lineas_fn = self.entorno.funciones[nombre][:4]
        lineas_anteriores = self.lineas
        self.lineas = lineas_fn
        if not hasattr(self, "pila_llamadas"):
            self.pila_llamadas = []
        self.pila_llamadas.append(nombre)
        nuevo_scope = self._armar_scope_de_llamada(nombre, params_info, valores)
        self.pila_scopes.append(nuevo_scope)
        profundidad_anterior = self.profundidad_bucles
        self.profundidad_bucles = 0
        try:
            self._ejecutar_bloque(ini, fin_fn)
            return None
        except RetornoFuncion as r:
            return r.valor
        finally:
            self.lineas = lineas_anteriores
            self.pila_scopes.pop()
            self.pila_llamadas.pop()
            self.profundidad_bucles = profundidad_anterior

    def _evaluar_condicion(self, cond):
        cond = cond.strip()

        # Optimizacion (#16): _separar_nivel_superior escanea el texto
        # caracter por caracter (para no partir dentro de comillas), asi
        # que hacerlo dos veces en CADA condicion evaluada (la mayoria sin
        # ' o '/' y ') era el cuello de botella real en bucles largos
        # (mientras/repetir), confirmado con cProfile: era ~30% del tiempo
        # total de ejecucion. Un 'in' de Python (implementado en C) descarta
        # el caso comun sin pagar el costo del escaneo manual.
        if " o " in cond:
            partes_o = self._separar_nivel_superior(cond, " o ")
            if len(partes_o) > 1:
                return any(self._evaluar_condicion(p) for p in partes_o)

        if " y " in cond:
            partes_y = self._separar_nivel_superior(cond, " y ")
            if len(partes_y) > 1:
                return all(self._evaluar_condicion(p) for p in partes_y)

        if cond.startswith("no "):
            return not self._evaluar_condicion(cond[3:])

        analizado = _analizar_condicion_binaria(cond)
        if analizado:
            izq_txt, op, der_txt = analizado
            izq = self.evaluar_expresion(izq_txt)
            der = self.evaluar_expresion(der_txt)
            try:
                if op == "==":
                    return izq == der
                if op == "!=":
                    return izq != der
                if op == ">":
                    return float(izq) > float(der)
                if op == "<":
                    return float(izq) < float(der)
                if op == ">=":
                    return float(izq) >= float(der)
                if op == "<=":
                    return float(izq) <= float(der)
            except (TypeError, ValueError):
                return str(izq) == str(der) if op == "==" else False
        valor = self.evaluar_expresion(cond)
        return bool(valor)

    # ---------- GUI con tkinter (real, funcional en Windows) ----------

    def _crear_ventana_gui(self, titulo, ancho, alto, inicio, fin):
        import tkinter as tk
        self._tk = tk
        root = tk.Tk()
        root.title(self.interpolar(titulo))
        root.geometry(f"{ancho}x{alto}")
        self.ventana_tk = root
        self.widgets = {}
        self.contenedor_actual = None
        self.notebook_actual = None
        self._ejecutar_bloque(inicio, fin)
        root.mainloop()

    def _widget_gui(self, tipo, resto):
        tk = self._tk
        root = getattr(self, "contenedor_actual", None) or self.ventana_tk
        if tipo == "etiqueta":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+(\S+)\s+(\S+)$', resto)
            if m:
                texto_expr, x_expr, y_expr = m.groups()
                texto = self._texto_o_variable(texto_expr)
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                lbl = tk.Label(root, text=texto, font=("Segoe UI", 11))
                lbl.place(x=x, y=y)
        elif tipo == "boton":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+(\S+)\s+(\S+)\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$', resto)
            if m:
                texto_expr, x_expr, y_expr, fn, args = m.groups()
                texto = self._texto_o_variable(texto_expr)
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                def accion(fn=fn, args=args):
                    args_txt = [a.strip() for a in args.split(",") if a.strip() != ""]
                    if fn in self.entorno.funciones:
                        self._invocar_funcion(fn, args_txt)
                btn = tk.Button(root, text=texto, command=accion)
                btn.place(x=x, y=y)
        elif tipo == "entrada":
            m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(\S+)\s+(\S+)$', resto)
            if m:
                var, x_expr, y_expr = m.groups()
                x, y = int(self.evaluar_expresion(x_expr)), int(self.evaluar_expresion(y_expr))
                sv = tk.StringVar()
                ent = tk.Entry(root, textvariable=sv)
                ent.place(x=x, y=y)
                self.widgets[var] = sv
                self._mutar_variable(var, "")

                def actualizar(*_, sv=sv, var=var):
                    texto_actual = sv.get()
                    if es_numero(texto_actual) and texto_actual.strip() != "":
                        valor_num = float(texto_actual)
                        self._mutar_variable(var, int(valor_num) if valor_num == int(valor_num) else valor_num)
                    else:
                        self._mutar_variable(var, texto_actual)
                sv.trace_add("write", actualizar)
        elif tipo == "cuadro":
            m = _m(r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+("(?:[^"]*)"|\S+)$', resto)
            if m:
                x_expr, y_expr, ancho_expr, alto_expr, color_expr = m.groups()
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                ancho = int(self.evaluar_expresion(ancho_expr))
                alto = int(self.evaluar_expresion(alto_expr))
                color = self._texto_color(color_expr)
                cv = tk.Canvas(root, width=ancho, height=alto, bg=color_tkinter(color), highlightthickness=0)
                cv.place(x=x, y=y)
        elif tipo == "imagen":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+(\S+)\s+(\S+)(?:\s+(\S+)\s+(\S+))?$', resto)
            if m:
                ruta_expr, x_expr, y_expr, ancho_expr, alto_expr = m.groups()
                ruta_imagen = self._texto_o_variable(ruta_expr)
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                ancho_deseado = int(self.evaluar_expresion(ancho_expr)) if ancho_expr else None
                alto_deseado = int(self.evaluar_expresion(alto_expr)) if alto_expr else None
                ruta_final = os.path.join(self.base_dir, ruta_imagen)
                if not asegurar_paquete("PIL", "Pillow"):
                    return
                from PIL import Image, ImageTk
                try:
                    img = Image.open(ruta_final)
                    if ancho_deseado and alto_deseado:
                        img = img.resize((ancho_deseado, alto_deseado))
                    foto = ImageTk.PhotoImage(img)
                    etiqueta_img = tk.Label(root, image=foto, bd=0)
                    etiqueta_img.image = foto  # evita que el recolector de basura la borre
                    etiqueta_img.place(x=x, y=y)
                    if not hasattr(self, "_imagenes_gui"):
                        self._imagenes_gui = []
                    self._imagenes_gui.append(foto)
                except Exception as e:
                    print(f"[SiPi] No se pudo cargar la imagen '{ruta_imagen}': {e}")
        elif tipo == "casilla":
            m = _m(r'^("(?:[^"]*)"|\S+)\s+(\S+)\s+(\S+)\s+([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                texto_expr, x_expr, y_expr, var = m.groups()
                texto = self._texto_o_variable(texto_expr)
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                iv = tk.IntVar()
                self._mutar_variable(var, False)

                def actualizar(*_args, iv=iv, var=var):
                    self._mutar_variable(var, bool(iv.get()))
                iv.trace_add("write", actualizar)
                chk = tk.Checkbutton(root, text=texto, variable=iv)
                chk.place(x=x, y=y)
                self.widgets[var] = iv
        elif tipo == "lista":
            m = _m(r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+("(?:[^"]*)"|\S+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                x_expr, y_expr, ancho_expr, alto_expr, items_expr, var = m.groups()
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                ancho = int(self.evaluar_expresion(ancho_expr))
                alto = int(self.evaluar_expresion(alto_expr))
                if items_expr.startswith('"'):
                    items_txt = items_expr[1:-1]
                    items = [self.interpolar(it) for it in items_txt.split("|") if it != ""]
                else:
                    valor_lista = self._obtener_variable(items_expr, [])
                    items = [self._formatear_valor(it) for it in valor_lista] if isinstance(valor_lista, list) else []
                lb = tk.Listbox(root, width=int(ancho), height=int(alto))
                for it in items:
                    lb.insert(tk.END, it)
                lb.place(x=int(x), y=int(y))
                self._mutar_variable(var, "")

                def al_seleccionar(evento, lb=lb, var=var):
                    seleccion = lb.curselection()
                    if seleccion:
                        self._mutar_variable(var, lb.get(seleccion[0]))
                lb.bind("<<ListboxSelect>>", al_seleccionar)
                self.widgets[var] = lb
        elif tipo == "barra_progreso":
            m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)$", resto)
            if m:
                var, x_expr, y_expr, ancho_expr, expr_valor = m.groups()
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                ancho = int(self.evaluar_expresion(ancho_expr))
                from tkinter import ttk
                valor_inicial = self.evaluar_expresion(expr_valor)
                dv = tk.DoubleVar(value=float(valor_inicial))
                barra = ttk.Progressbar(root, orient="horizontal", length=ancho,
                                         mode="determinate", variable=dv, maximum=100)
                barra.place(x=x, y=y)
                self.widgets[var] = dv
                self._mutar_variable(var, float(valor_inicial))
        elif tipo == "menu_desplegable":
            m = _m(r'^(\S+)\s+(\S+)\s+(\S+)\s+("(?:[^"]*)"|\S+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', resto)
            if m:
                x_expr, y_expr, ancho_expr, items_expr, var = m.groups()
                x = int(self.evaluar_expresion(x_expr))
                y = int(self.evaluar_expresion(y_expr))
                ancho = int(self.evaluar_expresion(ancho_expr))
                from tkinter import ttk
                if items_expr.startswith('"'):
                    items_txt = items_expr[1:-1]
                    items = [self.interpolar(it) for it in items_txt.split("|") if it != ""]
                else:
                    valor_lista = self._obtener_variable(items_expr, [])
                    items = [self._formatear_valor(it) for it in valor_lista] if isinstance(valor_lista, list) else []
                sv = tk.StringVar(value=items[0] if items else "")
                combo = ttk.Combobox(root, textvariable=sv, values=items, width=int(ancho), state="readonly")
                combo.place(x=int(x), y=int(y))
                self._mutar_variable(var, items[0] if items else "")

                def al_elegir(*_args, sv=sv, var=var):
                    self._mutar_variable(var, sv.get())
                sv.trace_add("write", al_elegir)
                self.widgets[var] = sv

    # ---------- Juegos con pygame (real) ----------

    def _crear_escena_3d(self, titulo, ancho, alto, cuerpo_lineas):
        """3D basico v1: figuras (cubo/piramide) definidas por el usuario,
        rotando alrededor del eje Y, dibujadas como wireframe con una
        proyeccion en perspectiva simple. Sin texturas, sin iluminacion,
        sin z-buffer todavia -- es la base sobre la que se puede construir
        mas adelante, no un motor 3D completo."""
        if not asegurar_paquete("pygame"):
            return
        import pygame
        pygame.init()
        pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(self.interpolar(titulo))
        reloj = pygame.time.Clock()
        colores = {nombre: hex_a_rgb(codigo) for nombre, codigo in COLORES_ESPANOL.items()}

        # Vertices base de cada tipo de figura, centrados en el origen.
        def vertices_cubo(t):
            r = t / 2.0
            return [(-r, -r, -r), (r, -r, -r), (r, r, -r), (-r, r, -r),
                    (-r, -r, r), (r, -r, r), (r, r, r), (-r, r, r)]

        def aristas_cubo():
            return [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
                    (0, 4), (1, 5), (2, 6), (3, 7)]

        def vertices_piramide(t):
            r = t / 2.0
            return [(-r, r, -r), (r, r, -r), (r, r, r), (-r, r, r), (0, -r, 0)]

        def aristas_piramide():
            return [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4), (2, 4), (3, 4)]

        figuras = []
        rotacion_vel_y = 1.0  # grados por fotograma
        rotacion_vel_x = 0.4

        for _, linea in cuerpo_lineas:
            if not linea:
                continue
            partes = linea.split(" ", 1)
            cmd = partes[0]
            resto = partes[1] if len(partes) > 1 else ""
            if cmd == "figura":
                m = _m(r'^(cubo|piramide)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)$', resto)
                if m:
                    tipo, x_e, y_e, z_e, tam_e, color_e = m.groups()
                    cx = float(self.evaluar_expresion(x_e))
                    cy = float(self.evaluar_expresion(y_e))
                    cz = float(self.evaluar_expresion(z_e))
                    tam = float(self.evaluar_expresion(tam_e))
                    color_nombre = self._texto_color(color_e)
                    color_rgb = colores.get(color_nombre, hex_a_rgb(color_nombre) if color_nombre.startswith("#") else (255, 255, 255))
                    verts = vertices_cubo(tam) if tipo == "cubo" else vertices_piramide(tam)
                    aristas = aristas_cubo() if tipo == "cubo" else aristas_piramide()
                    figuras.append({
                        "centro": (cx, cy, cz), "vertices": verts, "aristas": aristas,
                        "color": color_rgb, "angulo_y": 0.0, "angulo_x": 0.0,
                    })
            elif cmd == "rotacion_velocidad":
                mv = _m(r'^(\S+)(?:\s+(\S+))?$', resto)
                if mv:
                    rotacion_vel_y = float(self.evaluar_expresion(mv.group(1)))
                    if mv.group(2):
                        rotacion_vel_x = float(self.evaluar_expresion(mv.group(2)))

        distancia_camara = max(ancho, alto) * 1.4
        fov = max(ancho, alto) * 0.9
        cx_pantalla, cy_pantalla = ancho // 2, alto // 2

        def rotar_y(p, ang):
            s, c = math.sin(ang), math.cos(ang)
            x, y, z = p
            return (x * c + z * s, y, -x * s + z * c)

        def rotar_x(p, ang):
            s, c = math.sin(ang), math.cos(ang)
            x, y, z = p
            return (x, y * c - z * s, y * s + z * c)

        def proyectar(p):
            x, y, z = p
            z_cam = z + distancia_camara
            if z_cam <= 1:
                z_cam = 1
            factor = fov / z_cam
            return (cx_pantalla + x * factor, cy_pantalla - y * factor)

        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    corriendo = False

            pantalla.fill((17, 17, 27))
            for fig in figuras:
                fig["angulo_y"] += math.radians(rotacion_vel_y)
                fig["angulo_x"] += math.radians(rotacion_vel_x)
                cx_f, cy_f, cz_f = fig["centro"]
                puntos_2d = []
                for vx, vy, vz in fig["vertices"]:
                    p = rotar_y((vx, vy, vz), fig["angulo_y"])
                    p = rotar_x(p, fig["angulo_x"])
                    p = (p[0] + cx_f, p[1] + cy_f, p[2] + cz_f)
                    puntos_2d.append(proyectar(p))
                for a, b in fig["aristas"]:
                    pygame.draw.line(pantalla, fig["color"], puntos_2d[a], puntos_2d[b], 2)

            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()

    def _crear_juego_pygame(self, titulo, ancho, alto, cuerpo_lineas):
        if not asegurar_paquete("pygame"):
            return
        import pygame
        pygame.init()
        pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(self.interpolar(titulo))
        reloj = pygame.time.Clock()

        sprites = {}
        sonidos = {}
        colisiones_config = []
        mostrar_puntaje = False
        velocidad = 5
        sprites_moviles = {}
        sprites_ia = {}
        particulas_activas = []
        self.particulas_pendientes = []

        gravedad = 0.0
        rebote = 0.0
        friccion_valor = 0.0
        mundo_ancho = ancho
        mundo_alto = alto
        camara_objetivo = None

        if not self._existe_variable("puntaje"):
            self._mutar_variable("puntaje", 0)

        for _, linea in cuerpo_lineas:
            if not linea:
                continue
            partes = linea.split(" ", 1)
            cmd = partes[0]
            resto = partes[1] if len(partes) > 1 else ""
            if cmd == "sprite":
                m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+("(?:[^"]*)"|\S+)$', resto)
                if m:
                    nombre, x_expr, y_expr, w_expr, h_expr, color_expr = m.groups()
                    x = int(self.evaluar_expresion(x_expr))
                    y = int(self.evaluar_expresion(y_expr))
                    w = int(self.evaluar_expresion(w_expr))
                    h = int(self.evaluar_expresion(h_expr))
                    color = self._texto_color(color_expr)
                    sprites[nombre] = {"x": x, "y": y, "w": w, "h": h, "color": color}
            elif cmd == "velocidad":
                velocidad = float(self.evaluar_expresion(resto))
            elif cmd == "gravedad":
                gravedad = float(self.evaluar_expresion(resto))
            elif cmd == "rebote":
                rebote = float(self.evaluar_expresion(resto))
            elif cmd == "friccion":
                friccion_valor = float(self.evaluar_expresion(resto))
            elif cmd == "tamano_mundo":
                m = _m(r"^(\S+)\s+(\S+)$", resto)
                if m:
                    mundo_ancho = int(self.evaluar_expresion(m.group(1)))
                    mundo_alto = int(self.evaluar_expresion(m.group(2)))
            elif cmd == "camara_seguir":
                camara_objetivo = resto.strip()
            elif cmd == "mover_aleatorio":
                m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
                if m:
                    nombre_spr, vel_expr = m.groups()
                    vel = float(self.evaluar_expresion(vel_expr))
                    direccion_x = random.choice([-1, 1])
                    direccion_y = random.choice([-1, 1])
                    sprites_moviles[nombre_spr] = {"vx": vel * direccion_x, "vy": vel * direccion_y}
            elif cmd == "ia":
                m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(seguir|escapar)\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", resto)
                if m:
                    nombre_spr, comportamiento, objetivo, vel_expr = m.groups()
                    vel = float(self.evaluar_expresion(vel_expr))
                    sprites_ia[nombre_spr] = {"tipo": comportamiento, "objetivo": objetivo, "velocidad": vel}
                else:
                    m2 = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+patrullar\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.+)$", resto)
                    if m2:
                        nombre_spr, x1, y1, x2, y2, vel_expr = m2.groups()
                        vel = float(self.evaluar_expresion(vel_expr))
                        sprites_ia[nombre_spr] = {
                            "tipo": "patrullar", "x1": int(x1), "y1": int(y1),
                            "x2": int(x2), "y2": int(y2), "velocidad": vel, "yendo_a_2": True,
                        }
            elif cmd == "sonido":
                m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+"([^"]+)"$', resto)
                if m:
                    nombre_snd, archivo = m.groups()
                    ruta = os.path.join(self.base_dir, archivo)
                    try:
                        pygame.mixer.init()
                        sonidos[nombre_snd] = pygame.mixer.Sound(ruta)
                    except Exception as e:
                        print(f"[SiPi] No se pudo cargar el sonido '{archivo}': {e}")
            elif cmd == "tono":
                m = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s+(.+)$", resto)
                if m:
                    nombre_snd, frec_expr, dur_expr = m.groups()
                    frecuencia = float(self.evaluar_expresion(frec_expr))
                    duracion = float(self.evaluar_expresion(dur_expr))
                    try:
                        pygame.mixer.init()
                        ruta_tono = generar_wav_tono(frecuencia, duracion)
                        sonidos[nombre_snd] = pygame.mixer.Sound(ruta_tono)
                        os.remove(ruta_tono)
                    except Exception as e:
                        print(f"[SiPi] No se pudo generar el tono '{nombre_snd}': {e}")
            elif cmd == "chocar":
                m = _m(r'^([\w\u0900-\u097F\u0980-\u09FF]+)\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)(?:\s+([\w\u0900-\u097F\u0980-\u09FF]+))?$', resto)
                if m:
                    spr_a, spr_b, fn, args, nombre_sonido = m.groups()
                    colisiones_config.append({
                        "a": spr_a, "b": spr_b, "fn": fn, "args": args,
                        "activo": True, "sonido": nombre_sonido, "estaba_colisionando": False,
                    })
            elif cmd == "puntaje_inicial":
                self._mutar_variable("puntaje", int(self.evaluar_expresion(resto)))
            elif cmd == "mostrar_puntaje":
                mostrar_puntaje = True

        pygame.font.init()
        fuente = pygame.font.SysFont("Arial", 26)

        def ejecutar_funcion_usuario(fn, args):
            args_txt = [a.strip() for a in args.split(",") if a.strip() != ""]
            if fn in self.entorno.funciones:
                self._invocar_funcion(fn, args_txt)

        velocidad_x_jugador = 0.0
        velocidad_y_jugador = 0.0
        suelo_tocado = True
        usar_fisica = gravedad > 0

        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            teclas = pygame.key.get_pressed()
            jugador = sprites.get("jugador")
            if jugador:
                if usar_fisica:
                    # Movimiento horizontal con friccion opcional
                    if teclas[pygame.K_LEFT]:
                        velocidad_x_jugador = -velocidad
                    elif teclas[pygame.K_RIGHT]:
                        velocidad_x_jugador = velocidad
                    elif friccion_valor > 0:
                        velocidad_x_jugador *= max(0.0, 1 - friccion_valor)
                        if abs(velocidad_x_jugador) < 0.15:
                            velocidad_x_jugador = 0.0
                    else:
                        velocidad_x_jugador = 0.0

                    # Salto real con la barra espaciadora
                    if teclas[pygame.K_SPACE] and suelo_tocado:
                        velocidad_y_jugador = -gravedad * 14
                        suelo_tocado = False

                    velocidad_y_jugador += gravedad
                    jugador["x"] += velocidad_x_jugador
                    jugador["y"] += velocidad_y_jugador

                    # Colision real con el "piso" (limite inferior del mundo)
                    if jugador["y"] + jugador["h"] >= mundo_alto:
                        jugador["y"] = mundo_alto - jugador["h"]
                        if rebote > 0 and abs(velocidad_y_jugador) > 1:
                            velocidad_y_jugador = -velocidad_y_jugador * rebote
                        else:
                            velocidad_y_jugador = 0.0
                        suelo_tocado = True
                    else:
                        suelo_tocado = False

                    jugador["x"] = max(0, min(mundo_ancho - jugador["w"], jugador["x"]))
                else:
                    if teclas[pygame.K_LEFT]:
                        jugador["x"] -= velocidad
                    if teclas[pygame.K_RIGHT]:
                        jugador["x"] += velocidad
                    if teclas[pygame.K_UP]:
                        jugador["y"] -= velocidad
                    if teclas[pygame.K_DOWN]:
                        jugador["y"] += velocidad
                    jugador["x"] = max(0, min(mundo_ancho - jugador["w"], jugador["x"]))
                    jugador["y"] = max(0, min(mundo_alto - jugador["h"], jugador["y"]))

            # Movimiento automatico de sprites con rebote en los bordes del mundo
            for nombre_m, mov in sprites_moviles.items():
                spr = sprites.get(nombre_m)
                if spr:
                    spr["x"] += mov["vx"]
                    spr["y"] += mov["vy"]
                    if spr["x"] <= 0 or spr["x"] + spr["w"] >= mundo_ancho:
                        mov["vx"] *= -1
                        spr["x"] = max(0, min(mundo_ancho - spr["w"], spr["x"]))
                    if spr["y"] <= 0 or spr["y"] + spr["h"] >= mundo_alto:
                        mov["vy"] *= -1
                        spr["y"] = max(0, min(mundo_alto - spr["h"], spr["y"]))

            # IA simple: seguir, escapar o patrullar
            for nombre_ia, config_ia in sprites_ia.items():
                spr = sprites.get(nombre_ia)
                if not spr:
                    continue
                if config_ia["tipo"] in ("seguir", "escapar"):
                    objetivo = sprites.get(config_ia["objetivo"])
                    if objetivo:
                        dx = (objetivo["x"] - spr["x"])
                        dy = (objetivo["y"] - spr["y"])
                        distancia = max(1.0, (dx ** 2 + dy ** 2) ** 0.5)
                        vel_ia = config_ia["velocidad"]
                        signo = 1 if config_ia["tipo"] == "seguir" else -1
                        spr["x"] += signo * vel_ia * dx / distancia
                        spr["y"] += signo * vel_ia * dy / distancia
                        spr["x"] = max(0, min(mundo_ancho - spr["w"], spr["x"]))
                        spr["y"] = max(0, min(mundo_alto - spr["h"], spr["y"]))
                elif config_ia["tipo"] == "patrullar":
                    destino_x = config_ia["x2"] if config_ia["yendo_a_2"] else config_ia["x1"]
                    destino_y = config_ia["y2"] if config_ia["yendo_a_2"] else config_ia["y1"]
                    dx = destino_x - spr["x"]
                    dy = destino_y - spr["y"]
                    distancia = (dx ** 2 + dy ** 2) ** 0.5
                    vel_ia = config_ia["velocidad"]
                    if distancia < max(2.0, vel_ia):
                        config_ia["yendo_a_2"] = not config_ia["yendo_a_2"]
                    else:
                        spr["x"] += vel_ia * dx / distancia
                        spr["y"] += vel_ia * dy / distancia

            # Particulas reales: explosion, humo, fuego (disparadas con el comando 'particulas'/'explosion'/'humo'/'fuego')
            for solicitud in self.particulas_pendientes:
                paletas = {
                    "explosion": [(255, 200, 60), (255, 120, 40), (220, 40, 40)],
                    "humo": [(140, 140, 140), (100, 100, 100), (180, 180, 180)],
                    "fuego": [(255, 80, 20), (255, 160, 40), (255, 220, 80)],
                }
                paleta = paletas.get(solicitud["tipo"], paletas["explosion"])
                for _ in range(solicitud["cantidad"]):
                    angulo = random.uniform(0, 2 * math.pi)
                    velocidad_p = random.uniform(1.0, 4.0)
                    particulas_activas.append({
                        "x": float(solicitud["x"]), "y": float(solicitud["y"]),
                        "vx": math.cos(angulo) * velocidad_p,
                        "vy": math.sin(angulo) * velocidad_p - (1.5 if solicitud["tipo"] != "explosion" else 0),
                        "vida": random.randint(20, 45),
                        "vida_maxima": 45,
                        "color": random.choice(paleta),
                        "radio": random.uniform(2, 5),
                    })
            self.particulas_pendientes = []

            for particula in particulas_activas:
                particula["x"] += particula["vx"]
                particula["y"] += particula["vy"]
                particula["vida"] -= 1
            particulas_activas = [p for p in particulas_activas if p["vida"] > 0]

            # Exponer la posicion de cada sprite como variables reales
            # (nombre_x, nombre_y) para que las funciones de colision puedan usarlas
            for nombre_spr_pos, spr_pos in sprites.items():
                self._mutar_variable(f"{nombre_spr_pos}_x", int(spr_pos["x"]))
                self._mutar_variable(f"{nombre_spr_pos}_y", int(spr_pos["y"]))

            # Deteccion de colisiones real (rectangulos), disparando la
            # funcion solo en el instante en que EMPIEZAN a tocarse (flanco
            # de entrada), no en cada uno de los 60 cuadros por segundo
            # mientras siguen superpuestos.
            for conf in colisiones_config:
                a = sprites.get(conf["a"])
                b = sprites.get(conf["b"])
                if a and b and conf["activo"]:
                    rect_a = pygame.Rect(a["x"], a["y"], a["w"], a["h"])
                    rect_b = pygame.Rect(b["x"], b["y"], b["w"], b["h"])
                    colisionando_ahora = rect_a.colliderect(rect_b)
                    if colisionando_ahora and not conf["estaba_colisionando"]:
                        ejecutar_funcion_usuario(conf["fn"], conf["args"])
                        nombre_sonido = conf.get("sonido")
                        if nombre_sonido and nombre_sonido in sonidos:
                            sonidos[nombre_sonido].play()
                    conf["estaba_colisionando"] = colisionando_ahora

            # Camara: sigue al sprite indicado si el mundo es mas grande que la pantalla
            offset_x, offset_y = 0, 0
            if camara_objetivo and camara_objetivo in sprites:
                objetivo = sprites[camara_objetivo]
                offset_x = int(objetivo["x"] + objetivo["w"] / 2 - ancho / 2)
                offset_y = int(objetivo["y"] + objetivo["h"] / 2 - alto / 2)
                offset_x = max(0, min(mundo_ancho - ancho, offset_x)) if mundo_ancho > ancho else 0
                offset_y = max(0, min(mundo_alto - alto, offset_y)) if mundo_alto > alto else 0

            pantalla.fill((15, 15, 25))
            for nombre, s in sprites.items():
                color = color_pygame(s["color"])
                pygame.draw.rect(pantalla, color, (s["x"] - offset_x, s["y"] - offset_y, s["w"], s["h"]))

            for particula in particulas_activas:
                proporcion_vida = max(0.0, particula["vida"] / particula["vida_maxima"])
                radio_actual = max(1, int(particula["radio"] * proporcion_vida))
                pygame.draw.circle(
                    pantalla, particula["color"],
                    (int(particula["x"] - offset_x), int(particula["y"] - offset_y)),
                    radio_actual,
                )

            if mostrar_puntaje:
                texto_render = fuente.render(
                    f"Puntaje: {self._obtener_variable('puntaje', 0)}", True, (255, 255, 255)
                )
                pantalla.blit(texto_render, (10, 10))

            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()

    # ---------- Base de datos local real (JSON) ----------

    REGISTRO_MODULOS_POR_DEFECTO = os.environ.get(
        "SIPI_REGISTRO_MODULOS",
        "https://raw.githubusercontent.com/sipi-lang/modulos/main"
    )

    def _buscar_paquetes_github(self, texto_busqueda):
        """Busca repositorios reales en GitHub usando su API publica de
        busqueda (sin necesitar API key). Es la version honesta de un
        'buscador de paquetes': no hay ningun indice curado ni inventado a
        mano por SiPi -- se pregunta directamente a GitHub y se muestran
        los resultados reales, para que el usuario elija cual instalar
        con 'instalar_repositorio'. Primero intenta acotar la busqueda a
        repos que tambien mencionen 'sipi' (mas relevante para este
        lenguaje); si eso no da resultados, cae a una busqueda general del
        termino tal cual, avisando el cambio."""
        intentos = [f"{texto_busqueda} sipi", texto_busqueda]
        datos = None
        for intento in intentos:
            query = urllib.parse.quote(intento)
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=8"
            print(f"[SiPi] Buscando en GitHub: '{intento}'...")
            try:
                peticion = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                                                  "User-Agent": "SiPi-lang"})
                with urllib.request.urlopen(peticion, timeout=15) as respuesta:
                    datos = json.loads(respuesta.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print("[SiPi] GitHub limito las busquedas sin autenticacion por ahora (limite de 10/min). "
                          "Espera un minuto e intenta de nuevo.")
                else:
                    print(f"[SiPi] No se pudo buscar en GitHub: {e}")
                return
            except urllib.error.URLError as e:
                print(f"[SiPi] No se pudo conectar con GitHub: {e}")
                return

            if datos.get("items"):
                if intento != intentos[0]:
                    print(f"[SiPi] (no hubo resultados combinando con 'sipi'; estos son resultados generales de '{texto_busqueda}')")
                break

        items = (datos or {}).get("items", [])
        if not items:
            print(f"[SiPi] No se encontraron repositorios para '{texto_busqueda}'. "
                  "Proba con otras palabras, o busca directamente en github.com.")
            return

        print(f"[SiPi] {datos.get('total_count', len(items))} resultado(s) encontrados (mostrando los mas relevantes):")
        for item in items:
            nombre_completo = item.get("full_name", "?")
            descripcion = item.get("description") or "(sin descripcion)"
            estrellas = item.get("stargazers_count", 0)
            print(f"  - {nombre_completo}  (⭐ {estrellas})")
            print(f"      {descripcion}")
            print(f'      Para instalarlo: instalar_repositorio "{nombre_completo}"')
        print("[SiPi] Nota honesta: esta busqueda es sobre TODOS los repos de GitHub que mencionen esas "
              "palabras (no hay ningun catalogo curado o verificado de paquetes SiPi todavia). Revisa el "
              "repo antes de instalarlo, como harias con cualquier codigo de un tercero.")

    def _instalar_paquete_github(self, repo_o_url, rama=None):
        """Descarga un repositorio COMPLETO de GitHub (multiples archivos
        .sipi, no solo uno) y lo deja en 'paquetes/<repo>/', listo para
        'importar'. Uso:
            instalar_repositorio "usuario/repo"
            instalar_repositorio "usuario/repo" rama desarrollo
            instalar_repositorio "https://github.com/usuario/repo"

        Esto es el equivalente real y funcional de un "repositorio central
        de paquetes SiPi" sin necesitar montar un sitio propio: GitHub ya
        es el hosting, la busqueda y el control de versiones. Cualquiera
        puede publicar un paquete SiPi con solo subir un repo publico."""
        m_url = _m(r"^https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", repo_o_url.strip())
        if m_url:
            usuario, repo = m_url.group(1), m_url.group(2)
        else:
            m_corto = _m(r"^([^/\s]+)/([^/\s]+)$", repo_o_url.strip())
            if not m_corto:
                raise SiPiError(
                    'Sintaxis: instalar_repositorio "usuario/repo" (o la URL completa de GitHub). '
                    f"Recibido: '{repo_o_url}'"
                )
            usuario, repo = m_corto.groups()

        carpeta_paquetes = os.path.join(self.base_dir, "paquetes")
        os.makedirs(carpeta_paquetes, exist_ok=True)
        carpeta_destino = os.path.join(carpeta_paquetes, repo)

        ramas_a_probar = [rama] if rama else ["main", "master"]
        ultimo_error = None
        for rama_probada in ramas_a_probar:
            url_zip = f"https://codeload.github.com/{usuario}/{repo}/zip/refs/heads/{rama_probada}"
            print(f"[SiPi] Instalando paquete '{usuario}/{repo}' (rama {rama_probada}) desde GitHub...")
            try:
                with urllib.request.urlopen(url_zip, timeout=30) as respuesta:
                    contenido_zip = respuesta.read()
            except urllib.error.URLError as e:
                ultimo_error = e
                continue

            with zipfile.ZipFile(io.BytesIO(contenido_zip)) as z:
                if os.path.isdir(carpeta_destino):
                    shutil.rmtree(carpeta_destino)
                os.makedirs(carpeta_destino, exist_ok=True)
                nombres = z.namelist()
                # GitHub empaqueta todo dentro de una carpeta raiz tipo
                # "repo-main/"; la aplanamos para que quede directamente
                # en paquetes/<repo>/ y las rutas de 'importar' sean cortas.
                prefijo_raiz = nombres[0].split("/")[0] + "/" if nombres else ""
                for nombre in nombres:
                    if nombre.endswith("/"):
                        continue
                    nombre_relativo = nombre[len(prefijo_raiz):] if nombre.startswith(prefijo_raiz) else nombre
                    if not nombre_relativo:
                        continue
                    ruta_final = os.path.join(carpeta_destino, nombre_relativo)
                    os.makedirs(os.path.dirname(ruta_final) or ".", exist_ok=True)
                    with z.open(nombre) as origen, open(ruta_final, "wb") as destino_f:
                        shutil.copyfileobj(origen, destino_f)

            archivos_sipi = [f for f in os.listdir(carpeta_destino) if f.endswith(".sipi")]
            print(f"[SiPi] Paquete '{usuario}/{repo}' instalado en paquetes/{repo}/")
            if archivos_sipi:
                print(f"[SiPi] Archivos .sipi encontrados: {', '.join(archivos_sipi)}")
                print(f'[SiPi] Para usarlo: importar "paquetes/{repo}/{archivos_sipi[0]}"')
            else:
                print("[SiPi] Aviso: no se encontraron archivos .sipi en la raiz del repo; revisa sus subcarpetas.")

            registro = self._leer_registro_paquetes()
            registro[repo] = {
                "repo": f"{usuario}/{repo}",
                "rama": rama_probada,
                "instalado": datetime.datetime.now().isoformat(),
            }
            self._escribir_registro_paquetes(registro)
            return

        raise SiPiError(
            f"No se pudo instalar el paquete '{usuario}/{repo}': {ultimo_error}\n"
            f"Se probaron las ramas {ramas_a_probar}. Verifica que el repo sea publico, que el\n"
            f"nombre de usuario/repo sea correcto, o indica la rama exacta con 'rama <nombre>'."
        )

    def _ruta_registro_paquetes(self):
        carpeta_paquetes = os.path.join(self.base_dir, "paquetes")
        os.makedirs(carpeta_paquetes, exist_ok=True)
        return os.path.join(carpeta_paquetes, "_registro.json")

    def _leer_registro_paquetes(self):
        ruta = self._ruta_registro_paquetes()
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _escribir_registro_paquetes(self, registro):
        with open(self._ruta_registro_paquetes(), "w", encoding="utf-8") as f:
            json.dump(registro, f, indent=2, ensure_ascii=False)

    def _instalar_modulo(self, nombre_o_url, alias_import=None):
        """Descarga real (via HTTP) de un modulo .sipi y lo guarda localmente
        en la carpeta 'modulos_instalados/'. Permite dos formas de uso:
          instalar_modulo "nombre_del_modulo"   -> lo busca en el registro
                                                    configurado (variable de
                                                    entorno SIPI_REGISTRO_MODULOS)
          instalar_modulo "https://.../modulo.sipi" -> descarga directa desde
                                                    cualquier URL (por ejemplo
                                                    un repositorio de GitHub de
                                                    un tercero)
        Esto es real: cualquier programador puede publicar un archivo .sipi
        en internet (un repo publico, un gist, su propia web) y otro usuario
        de SiPi lo instala con una sola linea, sin que el autor de SiPi tenga
        que tocar nada. No incluye un registro central poblado por Anthropic;
        cada comunidad/usuario puede montar el suyo (basta un repo con
        archivos nombre.sipi) y apuntar SIPI_REGISTRO_MODULOS a el.
        """
        carpeta_modulos = os.path.join(self.base_dir, "modulos_instalados")
        os.makedirs(carpeta_modulos, exist_ok=True)

        if nombre_o_url.startswith("http://") or nombre_o_url.startswith("https://"):
            url = nombre_o_url
            nombre_modulo = os.path.splitext(os.path.basename(url.split("?")[0]))[0]
        else:
            nombre_modulo = nombre_o_url
            url = f"{self.REGISTRO_MODULOS_POR_DEFECTO.rstrip('/')}/{nombre_modulo}.sipi"

        destino = os.path.join(carpeta_modulos, f"{nombre_modulo}.sipi")
        print(f"[SiPi] Instalando modulo '{nombre_modulo}' desde {url} ...")
        try:
            with urllib.request.urlopen(url, timeout=15) as respuesta:
                contenido = respuesta.read().decode("utf-8")
        except urllib.error.URLError as e:
            raise SiPiError(
                f"No se pudo descargar el modulo '{nombre_modulo}' desde {url}: {e}\n"
                f"Verifica tu conexion a internet, el nombre del modulo, o si necesitas\n"
                f"indicar la URL completa del archivo .sipi."
            )
        with open(destino, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"[SiPi] Modulo '{nombre_modulo}' instalado en modulos_instalados/{nombre_modulo}.sipi")

        # Registro local de modulos instalados (util para listar/versionar mas adelante)
        registro = self._leer_registro_modulos()
        registro[nombre_modulo] = {"url": url, "instalado": datetime.datetime.now().isoformat()}
        self._escribir_registro_modulos(registro)

        ruta_relativa = os.path.join("modulos_instalados", f"{nombre_modulo}.sipi")
        print(f"[SiPi] Para usarlo en tu programa: importar \"{ruta_relativa}\"")

        if alias_import:
            # Import automatico e inmediato si el usuario escribio
            # 'instalar_modulo "nombre" como alias'
            self._ejecutar_linea(-1, -1, -1, f'importar "{ruta_relativa}"')

    def _ruta_registro_modulos(self):
        carpeta_modulos = os.path.join(self.base_dir, "modulos_instalados")
        os.makedirs(carpeta_modulos, exist_ok=True)
        return os.path.join(carpeta_modulos, "_registro.json")

    def _leer_registro_modulos(self):
        ruta = self._ruta_registro_modulos()
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _escribir_registro_modulos(self, registro):
        with open(self._ruta_registro_modulos(), "w", encoding="utf-8") as f:
            json.dump(registro, f, indent=2, ensure_ascii=False)

    def _instalar_dependencias(self):
        """Lee 'sipi_paquetes.json' (el equivalente de un package.json/
        requirements.txt para SiPi) en la carpeta del proyecto, e instala
        automaticamente todos los modulos .sipi que declara, sin que el
        programador tenga que escribir un 'instalar_modulo' por cada uno.

        Formato esperado de sipi_paquetes.json:
        {
          "modulos": {
            "telegram": "https://raw.githubusercontent.com/usuario/repo/main/telegram.sipi",
            "reconocimiento_facial": "reconocimiento_facial"
          }
        }
        Cada valor puede ser una URL directa, o solo el nombre (se busca
        en el registro configurado con SIPI_REGISTRO_MODULOS).
        """
        ruta_manifiesto = os.path.join(self.base_dir, "sipi_paquetes.json")
        if not os.path.exists(ruta_manifiesto):
            print("[SiPi] No se encontro 'sipi_paquetes.json' en esta carpeta.")
            print("       Crealo con el formato: {\"modulos\": {\"nombre\": \"url_o_nombre\"}}")
            return
        try:
            with open(ruta_manifiesto, "r", encoding="utf-8") as f:
                manifiesto = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise SiPiError(f"No se pudo leer 'sipi_paquetes.json': {e}")

        modulos = manifiesto.get("modulos", {})
        if not modulos:
            print("[SiPi] 'sipi_paquetes.json' no tiene modulos declarados.")
            return

        print(f"[SiPi] Instalando {len(modulos)} dependencia(s) declaradas en sipi_paquetes.json...")
        fallidos = []
        for nombre_dep, origen in modulos.items():
            try:
                self._instalar_modulo(origen)
            except SiPiError as e:
                print(f"[SiPi] Aviso: no se pudo instalar '{nombre_dep}': {e}")
                fallidos.append(nombre_dep)
        if fallidos:
            print(f"[SiPi] Instalacion terminada con errores en: {', '.join(fallidos)}")
        else:
            print("[SiPi] Todas las dependencias se instalaron correctamente.")

    def _ruta_base_datos(self):
        return os.path.join(self.base_dir, "sipi_datos.json")

    def _leer_base_datos(self):
        ruta = self._ruta_base_datos()
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _escribir_base_datos(self, datos):
        with open(self._ruta_base_datos(), "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    # ---------- Generador de sitios web reales ----------

    def _construir_elementos_pagina(self, inicio, fin):
        """Recorre el cuerpo de un bloque 'pagina_web' y genera HTML real a
        partir de comandos declarativos simples, sin que el usuario escriba
        una sola linea de HTML. Devuelve (elementos, tema, color_acento)."""
        elementos = []
        tema = "claro"
        color_acento = None
        idx = inicio
        while idx < fin:
            _, linea_interna = self.lineas[idx]
            if not linea_interna:
                idx += 1
                continue
            partes = linea_interna.split(" ", 1)
            subcmd = partes[0]
            resto_sub = partes[1] if len(partes) > 1 else ""

            if subcmd == "tema":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    tema = self.interpolar(mm.group(1)).strip().lower()
            elif subcmd == "color":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    color_acento = color_tkinter(self.interpolar(mm.group(1)).strip())
            elif subcmd == "titulo":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    elementos.append(f"<h1>{self.interpolar(mm.group(1))}</h1>")
            elif subcmd == "subtitulo":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    elementos.append(f"<h2>{self.interpolar(mm.group(1))}</h2>")
            elif subcmd == "texto":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    elementos.append(f"<p>{self.interpolar(mm.group(1))}</p>")
            elif subcmd == "boton":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    elementos.append(f'<button class="boton-sipi">{self.interpolar(mm.group(1))}</button>')
            elif subcmd == "imagen":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    ruta_img = self.interpolar(mm.group(1))
                    elementos.append(f'<img src="{ruta_img}" alt="" class="imagen-sipi">')
            elif subcmd == "enlace":
                mm = _m(r'^"([^"]*)"\s+"([^"]*)"$', resto_sub)
                if mm:
                    texto_enlace, url = mm.groups()
                    elementos.append(f'<a href="{self.interpolar(url)}">{self.interpolar(texto_enlace)}</a>')
            elif subcmd == "lista_web":
                mm = _m(r'^"([^"]*)"$', resto_sub)
                if mm:
                    items = [self.interpolar(it) for it in mm.group(1).split("|") if it != ""]
                    elementos.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            elif subcmd == "separador":
                elementos.append("<hr>")
            elif subcmd == "tarjeta":
                mm = _m(r'^"([^"]*)"\s+"([^"]*)"$', resto_sub)
                if mm:
                    titulo_tarjeta, texto_tarjeta = mm.groups()
                    elementos.append(
                        '<div class="tarjeta-sipi">'
                        f"<h3>{self.interpolar(titulo_tarjeta)}</h3>"
                        f"<p>{self.interpolar(texto_tarjeta)}</p>"
                        "</div>"
                    )
            elif subcmd == "formulario":
                fin_formulario = None
                profundidad = 1
                j = idx + 1
                while j < fin:
                    _, linea_j = self.lineas[j]
                    palabra_j = linea_j.split(" ")[0] if linea_j else ""
                    if palabra_j == "formulario":
                        profundidad += 1
                    elif palabra_j == "fin":
                        profundidad -= 1
                        if profundidad == 0:
                            fin_formulario = j
                            break
                    j += 1

                if fin_formulario is not None:
                    accion_mm = _m(r'^"([^"]*)"$', resto_sub.strip())
                    accion = self.interpolar(accion_mm.group(1)) if accion_mm else "#"
                    campos_html = []
                    for _, linea_form in self.lineas[idx + 1:fin_formulario]:
                        if not linea_form:
                            continue
                        partes_f = linea_form.split(" ", 1)
                        subcmd_f = partes_f[0]
                        resto_f = partes_f[1] if len(partes_f) > 1 else ""
                        if subcmd_f == "campo":
                            mm_f = _m(r'^"([^"]*)"(?:\s+([\w\u0900-\u097F\u0980-\u09FF]+))?$', resto_f)
                            if mm_f:
                                etiqueta_campo, tipo_campo = mm_f.groups()
                                tipo_campo = (tipo_campo or "texto").lower()
                                etiqueta_i = self.interpolar(etiqueta_campo)
                                id_campo = re.sub(r"[^a-zA-Z0-9]+", "_", etiqueta_i).strip("_").lower() or "campo"
                                if tipo_campo == "area":
                                    campos_html.append(
                                        f'<label for="{id_campo}">{etiqueta_i}</label>'
                                        f'<textarea id="{id_campo}" name="{id_campo}" class="campo-sipi" rows="4"></textarea>'
                                    )
                                else:
                                    tipo_html = {
                                        "texto": "text", "email": "email",
                                        "numero": "number", "clave": "password",
                                    }.get(tipo_campo, "text")
                                    campos_html.append(
                                        f'<label for="{id_campo}">{etiqueta_i}</label>'
                                        f'<input type="{tipo_html}" id="{id_campo}" name="{id_campo}" class="campo-sipi">'
                                    )
                        elif subcmd_f == "boton":
                            mm_f = _m(r'^"([^"]*)"$', resto_f)
                            if mm_f:
                                campos_html.append(
                                    f'<button type="submit" class="boton-sipi">{self.interpolar(mm_f.group(1))}</button>'
                                )
                    elementos.append(
                        f'<form class="formulario-sipi" action="{accion}" method="post">'
                        + "".join(campos_html) + "</form>"
                    )
                    idx = fin_formulario
            idx += 1
        return elementos, tema, color_acento

    def _generar_pagina_declarativa(self, nombre_sitio, elementos_html, tema="claro", color_acento=None):
        carpeta = os.path.join(self.base_dir, f"{nombre_sitio}_web")
        os.makedirs(carpeta, exist_ok=True)

        oscuro = tema in ("oscuro", "dark", "negro")
        acento = color_acento or "#3498db"

        if oscuro:
            color_fondo = "#0f0f17"
            color_texto = "#e6e6f0"
            color_tarjeta = "#1a1a2a"
            color_borde = "#2a2a3d"
            color_pie = "#6c7086"
        else:
            color_fondo = "#f4f6fb"
            color_texto = "#1e1e2e"
            color_tarjeta = "white"
            color_borde = "#e2e5ec"
            color_pie = "#8a8fa3"

        cuerpo = "\n  ".join(elementos_html)
        index_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{nombre_sitio}</title>
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<main class="contenedor-sipi">
  {cuerpo}
</main>
<footer class="pie-sipi"><p>Generado por SiPi - sin escribir HTML</p></footer>
</body>
</html>
'''
        estilo_css = f'''* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: "Segoe UI", system-ui, sans-serif;
  background: {color_fondo};
  color: {color_texto};
  line-height: 1.6;
}}
.contenedor-sipi {{ max-width: 760px; margin: 50px auto; padding: 0 20px; }}
h1 {{ font-size: 2.2rem; margin-bottom: 10px; color: {color_texto}; }}
h2 {{ font-size: 1.5rem; margin: 20px 0 8px; }}
p {{ margin-bottom: 12px; }}
.boton-sipi {{
  background: {acento};
  color: white;
  border: none;
  padding: 12px 22px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin: 8px 0;
}}
.boton-sipi:hover {{ filter: brightness(1.1); }}
.imagen-sipi {{ max-width: 100%; border-radius: 8px; margin: 12px 0; }}
ul {{ margin: 10px 0 10px 24px; }}
hr {{ border: none; border-top: 1px solid {color_borde}; margin: 24px 0; }}
a {{ color: {acento}; }}
.tarjeta-sipi {{
  background: {color_tarjeta};
  border: 1px solid {color_borde};
  border-radius: 10px;
  padding: 18px;
  margin: 14px 0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}}
.formulario-sipi {{
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: {color_tarjeta};
  border: 1px solid {color_borde};
  border-radius: 10px;
  padding: 20px;
  margin: 16px 0;
}}
.formulario-sipi label {{ font-size: 0.9rem; font-weight: 600; margin-top: 8px; }}
.campo-sipi {{
  padding: 10px;
  border-radius: 6px;
  border: 1px solid {color_borde};
  background: {color_fondo};
  color: {color_texto};
  font-size: 1rem;
  font-family: inherit;
}}
.pie-sipi {{ text-align: center; padding: 20px; color: {color_pie}; font-size: 0.9rem; }}
'''
        with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)
        with open(os.path.join(carpeta, "estilo.css"), "w", encoding="utf-8") as f:
            f.write(estilo_css)

        print(f"[SiPi] Pagina web declarativa generada en: {carpeta}")
        print(f"[SiPi] Abri {os.path.join(carpeta, 'index.html')} en tu navegador para verla.")

    def _generar_sitio_web(self, nombre_sitio):
        carpeta = os.path.join(self.base_dir, f"{nombre_sitio}_web")
        os.makedirs(carpeta, exist_ok=True)

        index_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{nombre_sitio}</title>
<link rel="stylesheet" href="estilo.css">
</head>
<body>
  <header class="encabezado">
    <h1>{nombre_sitio}</h1>
    <p>Sitio web real generado con SiPi</p>
  </header>

  <main>
    <section class="tarjeta">
      <h2>Bienvenido</h2>
      <p>Esta pagina es codigo HTML, CSS y JavaScript 100% real y editable.
         Podes modificar los archivos <code>index.html</code>, <code>estilo.css</code>
         y <code>script.js</code> como cualquier proyecto web comun.</p>
      <button id="boton-principal">Presioname</button>
      <p id="mensaje"></p>
    </section>
  </main>

  <footer class="pie">
    <p>Generado por SiPi - NovaLab Corporation</p>
  </footer>

  <script src="script.js"></script>
</body>
</html>
'''
        estilo_css = '''* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Segoe UI", system-ui, sans-serif;
  background: #0f0f17;
  color: #e6e6f0;
  line-height: 1.5;
}
.encabezado {
  padding: 60px 20px;
  text-align: center;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
}
.encabezado h1 { font-size: 2.5rem; color: #7ec4ff; }
main { max-width: 700px; margin: 40px auto; padding: 0 20px; }
.tarjeta {
  background: #1a1a2a;
  border: 1px solid #2a2a3d;
  border-radius: 12px;
  padding: 30px;
}
button {
  margin-top: 20px;
  background: #7ec4ff;
  color: #0f0f17;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
}
button:hover { background: #a6dbff; }
.pie { text-align: center; padding: 20px; color: #6c7086; }
'''
        script_js = '''document.getElementById("boton-principal").addEventListener("click", function () {
  const contador = (script_js_contador = (window.script_js_contador || 0) + 1);
  window.script_js_contador = contador;
  document.getElementById("mensaje").textContent = "Presionaste el boton " + contador + " veces (esto es JavaScript real).";
});
'''
        with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)
        with open(os.path.join(carpeta, "estilo.css"), "w", encoding="utf-8") as f:
            f.write(estilo_css)
        with open(os.path.join(carpeta, "script.js"), "w", encoding="utf-8") as f:
            f.write(script_js)

        leeme = f'''SITIO WEB: {nombre_sitio}
Generado por SiPi - 100% real y editable.

Para verlo, abri "index.html" con doble clic (se abre en tu navegador), o desde
SiPi corre:  iniciar_servidor_web "{nombre_sitio}_web" 8000

Esto sirve la carpeta como un sitio web real en http://localhost:8000
'''
        with open(os.path.join(carpeta, "LEEME.txt"), "w", encoding="utf-8") as f:
            f.write(leeme)

        print(f"[SiPi] Sitio web real generado en: {carpeta}")
        print(f"[SiPi] Abri {os.path.join(carpeta, 'index.html')} en tu navegador para verlo.")

    def _iniciar_servidor_web(self, carpeta, puerto):
        carpeta_final = os.path.join(self.base_dir, carpeta)
        if not os.path.isdir(carpeta_final):
            print(f"[SiPi] No existe la carpeta: {carpeta_final}")
            return

        class ManejadorSilencioso(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=carpeta_final, **kwargs)

            def log_message(self, formato, *args):
                pass

        try:
            servidor = socketserver.TCPServer(("", puerto), ManejadorSilencioso)
        except OSError as e:
            print(f"[SiPi] No se pudo iniciar el servidor en el puerto {puerto}: {e}")
            return

        url = f"http://localhost:{puerto}"
        print(f"[SiPi] Servidor web real corriendo en {url}  (Ctrl+C para detenerlo)")
        hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[SiPi] Deteniendo el servidor web...")
            servidor.shutdown()

    def _iniciar_api_web(self, puerto, max_hilos=64):
        """Levanta un servidor HTTP real (sin frameworks externos, solo la
        libreria estandar de Python) capaz de recibir peticiones GET/POST
        desde cualquier parte (una app movil, una web externa, curl, etc.)
        y despacharlas a funciones SiPi registradas con 'escuchar_ruta'.

        La funcion SiPi que atiende la ruta recibe un unico parametro con un
        diccionario 'peticion' que incluye: metodo, ruta, query (parametros
        de la URL) y cuerpo (el JSON recibido, ya convertido a
        diccionario/lista, o texto crudo si no era JSON valido). Lo que la
        funcion 'devuelva' con 'devolver' se envia de vuelta como respuesta
        JSON real al cliente.

        Concurrencia real: el servidor acepta y atiende muchas conexiones
        al mismo tiempo (un hilo del sistema operativo por conexion, con un
        techo de 'max_hilos' para no agotar recursos si llegan miles de
        clientes de golpe -- los que se pasan del limite esperan en cola en
        vez de tirar el proceso abajo). Eso ya es una mejora real para
        clientes lentos o con muchas conexiones simultaneas.

        Nota honesta sobre el limite real: el interprete de SiPi (las
        variables globales, la pila de funciones) NO es thread-safe por
        dentro, asi que la EJECUCION de tu funcion SiPi para cada peticion
        se serializa con un lock (una peticion corre su logica a la vez).
        Para la enorme mayoria de sistemas (paneles, APIs internas,
        automatizaciones, integraciones) esto es mas que suficiente, porque
        el cuello de botella real casi siempre es la base de datos o la red,
        no la CPU del propio SiPi. Para servir trafico masivo real (miles de
        peticiones por segundo con logica pesada) lo correcto es correr
        varios PROCESOS de SiPi detras de un balanceador de carga (Nginx,
        el load balancer de la nube, Kubernetes con varias replicas) -- que
        es ademas exactamente como escalan en la practica Python/Node/Ruby
        en produccion, no una limitacion especial de SiPi.
        """
        interprete = self
        interprete._hora_inicio_api = time.time()
        interprete._metricas_api = {"peticiones_totales": 0, "errores_totales": 0, "peticiones_activas": 0,
                                     "peticiones_rechazadas_auth": 0, "peticiones_rechazadas_limite": 0,
                                     "por_ruta": {}}
        lock_ejecucion = threading.Lock()
        semaforo_hilos = threading.BoundedSemaphore(max_hilos)
        lock_rate_limit = threading.Lock()
        peticiones_por_ip = {}  # ip -> lista de timestamps recientes (ventana deslizante de 60s)

        def _ip_permitida(ip):
            limite = interprete.entorno.limite_peticiones_por_minuto
            if limite is None:
                return True
            ahora = time.time()
            with lock_rate_limit:
                historial = peticiones_por_ip.setdefault(ip, [])
                # Purgar marcas de tiempo de hace mas de 60 segundos (ventana deslizante real, no un contador que resetea de golpe cada minuto).
                historial[:] = [t for t in historial if ahora - t < 60]
                if len(historial) >= limite:
                    return False
                historial.append(ahora)
                return True

        def _autenticacion_valida(headers):
            clave_requerida = interprete.entorno.clave_api_requerida
            if clave_requerida is None:
                return True
            auth = headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                clave_recibida = auth[len("Bearer "):].strip()
            else:
                clave_recibida = headers.get("X-API-Key", "")
            # comparacion en tiempo constante: evita que un atacante pueda
            # adivinar la clave caracter por caracter midiendo cuanto tarda
            # la respuesta (timing attack), un detalle de seguridad real.
            return hmac.compare_digest(clave_recibida, clave_requerida)

        class ManejadorAPI(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"  # conexiones persistentes (keep-alive) reales, no una conexion TCP nueva por cada request

            def log_message(self, formato, *args):
                pass

            def _procesar(self, metodo):
                adquirido = semaforo_hilos.acquire(timeout=10)
                if not adquirido:
                    self._responder(503, {"error": "Servidor con demasiadas conexiones simultaneas en este momento, intenta de nuevo."})
                    return
                try:
                    self._procesar_real(metodo)
                finally:
                    semaforo_hilos.release()

            def _procesar_real(self, metodo):
                partes_url = self.path.split("?", 1)
                ruta = partes_url[0]
                query = {}
                if len(partes_url) > 1:
                    for par in partes_url[1].split("&"):
                        if "=" in par:
                            clave, _, valor = par.partition("=")
                            query[urllib.parse.unquote(clave)] = urllib.parse.unquote(valor)

                largo = int(self.headers.get("Content-Length", 0) or 0)
                cuerpo_crudo = self.rfile.read(largo).decode("utf-8") if largo else ""
                cuerpo = cuerpo_crudo
                if cuerpo_crudo:
                    try:
                        cuerpo = json.loads(cuerpo_crudo)
                    except json.JSONDecodeError:
                        cuerpo = cuerpo_crudo

                nombre_funcion = interprete.entorno.rutas_api.get(ruta)
                if nombre_funcion is None:
                    # Endpoint de salud automatico: SIEMPRE disponible, sin
                    # que el usuario tenga que registrarlo. Es lo primero
                    # que un balanceador de carga, Kubernetes o un sistema
                    # de monitoreo va a pedir para saber si el servicio
                    # sigue vivo, asi que SiPi lo da de entrada. Ahora
                    # ademas trae metricas reales de carga.
                    if ruta in ("/salud", "/health", "/healthz"):
                        m = interprete._metricas_api
                        self._responder(200, {
                            "estado": "ok",
                            "version_sipi": VERSION,
                            "tiempo_activo_segundos": round(time.time() - interprete._hora_inicio_api, 1),
                            "rutas_registradas": len(interprete.entorno.rutas_api),
                            "peticiones_totales": m["peticiones_totales"],
                            "peticiones_activas": m["peticiones_activas"],
                            "errores_totales": m["errores_totales"],
                            "limite_conexiones_simultaneas": max_hilos,
                            "peticiones_rechazadas_auth": m["peticiones_rechazadas_auth"],
                            "peticiones_rechazadas_limite": m["peticiones_rechazadas_limite"],
                            "autenticacion_requerida": interprete.entorno.clave_api_requerida is not None,
                            "limite_peticiones_por_minuto": interprete.entorno.limite_peticiones_por_minuto,
                        })
                        return
                    # Metricas en formato Prometheus (texto plano, el
                    # estandar real que Grafana/Prometheus/casi cualquier
                    # sistema de monitoreo de empresa sabe leer sin ningun
                    # adaptador especial): un scraper de Prometheus apunta
                    # directo a esta ruta y ya esta.
                    if ruta in ("/metricas", "/metrics"):
                        self._responder_prometheus(interprete, max_hilos)
                        return
                    self._responder(404, {"error": f"Ruta no encontrada: {ruta}"})
                    return

                m = interprete._metricas_api
                m["peticiones_totales"] += 1

                ip_cliente = self.client_address[0]
                if not _ip_permitida(ip_cliente):
                    m["peticiones_rechazadas_limite"] += 1
                    self._responder(429, {"error": "Demasiadas peticiones. Espera un poco antes de volver a intentar."})
                    return

                if not _autenticacion_valida(self.headers):
                    m["peticiones_rechazadas_auth"] += 1
                    self._responder(401, {"error": "No autorizado. Falta o es incorrecta la clave de API (header 'Authorization: Bearer <clave>' o 'X-API-Key')."})
                    return

                m["peticiones_activas"] += 1
                m["por_ruta"][ruta] = m["por_ruta"].get(ruta, 0) + 1
                try:
                    peticion = {"metodo": metodo, "ruta": ruta, "query": query, "cuerpo": cuerpo}
                    # Solo la EJECUCION de la logica SiPi se serializa (el
                    # accept(), la lectura del socket y el armado de la
                    # respuesta ya pasaron sin bloquear a nadie mas).
                    with lock_ejecucion:
                        resultado = interprete._invocar_funcion_con_valores(nombre_funcion, [peticion])
                    if resultado is None:
                        resultado = {"ok": True}
                    self._responder(200, resultado)
                except SiPiError as e:
                    m["errores_totales"] += 1
                    self._responder(500, {"error": str(e)})
                except Exception as e:
                    m["errores_totales"] += 1
                    self._responder(500, {"error": f"Error interno: {e}"})
                finally:
                    m["peticiones_activas"] -= 1

            def _responder(self, codigo, datos):
                cuerpo_json = json.dumps(datos, ensure_ascii=False).encode("utf-8")
                self.send_response(codigo)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(cuerpo_json)))
                self.end_headers()
                self.wfile.write(cuerpo_json)

            def _responder_prometheus(self, interprete, max_hilos):
                m = interprete._metricas_api
                nombre_app = re.sub(r"[^a-zA-Z0-9_]", "_", os.path.basename(interprete.archivo_path))
                lineas = [
                    "# HELP sipi_peticiones_totales Cantidad total de peticiones HTTP recibidas.",
                    "# TYPE sipi_peticiones_totales counter",
                    f'sipi_peticiones_totales{{programa="{nombre_app}"}} {m["peticiones_totales"]}',
                    "# HELP sipi_errores_totales Cantidad total de peticiones que terminaron en error.",
                    "# TYPE sipi_errores_totales counter",
                    f'sipi_errores_totales{{programa="{nombre_app}"}} {m["errores_totales"]}',
                    "# HELP sipi_peticiones_activas Peticiones siendo procesadas en este momento.",
                    "# TYPE sipi_peticiones_activas gauge",
                    f'sipi_peticiones_activas{{programa="{nombre_app}"}} {m["peticiones_activas"]}',
                    "# HELP sipi_peticiones_rechazadas_totales Peticiones rechazadas por autenticacion o limite de tasa.",
                    "# TYPE sipi_peticiones_rechazadas_totales counter",
                    f'sipi_peticiones_rechazadas_totales{{programa="{nombre_app}",motivo="autenticacion"}} {m["peticiones_rechazadas_auth"]}',
                    f'sipi_peticiones_rechazadas_totales{{programa="{nombre_app}",motivo="limite_de_tasa"}} {m["peticiones_rechazadas_limite"]}',
                    "# HELP sipi_tiempo_activo_segundos Segundos desde que arranco el servidor.",
                    "# TYPE sipi_tiempo_activo_segundos counter",
                    f'sipi_tiempo_activo_segundos{{programa="{nombre_app}"}} {round(time.time() - interprete._hora_inicio_api, 1)}',
                    "# HELP sipi_limite_conexiones_simultaneas Techo configurado de conexiones concurrentes.",
                    "# TYPE sipi_limite_conexiones_simultaneas gauge",
                    f'sipi_limite_conexiones_simultaneas{{programa="{nombre_app}"}} {max_hilos}',
                    "# HELP sipi_peticiones_por_ruta_totales Peticiones recibidas, desglosadas por ruta.",
                    "# TYPE sipi_peticiones_por_ruta_totales counter",
                ]
                for ruta_contada, cantidad in m["por_ruta"].items():
                    ruta_escapada = ruta_contada.replace('"', '\\"')
                    lineas.append(f'sipi_peticiones_por_ruta_totales{{programa="{nombre_app}",ruta="{ruta_escapada}"}} {cantidad}')

                cuerpo = ("\n".join(lineas) + "\n").encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
                self.send_header("Content-Length", str(len(cuerpo)))
                self.end_headers()
                self.wfile.write(cuerpo)

            def do_GET(self):
                self._procesar("GET")

            def do_POST(self):
                self._procesar("POST")

            def do_PUT(self):
                self._procesar("PUT")

            def do_DELETE(self):
                self._procesar("DELETE")

        class ServidorAPIConcurrente(socketserver.ThreadingMixIn, http.server.HTTPServer):
            daemon_threads = True
            # Cola de conexiones TCP en espera antes de que el sistema
            # operativo empiece a rechazarlas de entrada (aparte del limite
            # de hilos activos de mas arriba, que es sobre peticiones ya
            # aceptadas y en proceso).
            request_queue_size = 128

        try:
            servidor = ServidorAPIConcurrente(("", puerto), ManejadorAPI)
        except OSError as e:
            print(f"[SiPi] No se pudo iniciar la API web en el puerto {puerto}: {e}")
            return

        self.entorno.servidores_api[puerto] = servidor
        print(f"[SiPi] API web real corriendo en http://localhost:{puerto} (hasta {max_hilos} conexiones simultaneas)")
        print(f"[SiPi] Rutas activas: {list(self.entorno.rutas_api.keys())}")
        hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        try:
            while puerto in self.entorno.servidores_api:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[SiPi] Deteniendo la API web...")
            self._detener_api_web(puerto)

    def _detener_api_web(self, puerto=None):
        puertos = [puerto] if puerto is not None else list(self.entorno.servidores_api.keys())
        for p in puertos:
            servidor = self.entorno.servidores_api.pop(p, None)
            if servidor:
                servidor.shutdown()
                servidor.server_close()
                print(f"[SiPi] API web en el puerto {p} detenida.")

    # ---------- Generadores de proyectos reales ----------

    def _generar_proyecto_android(self, nombre_app):
        """Genera un proyecto Kivy + Buildozer real y funcional (compilable
        a APK con buildozer en Linux/WSL). A diferencia de la version
        anterior, esto YA NO es una demo generica con un boton que cuenta
        clicks: empaqueta tu programa .sipi de verdad (el que estas
        corriendo ahora mismo) junto con el motor completo de SiPi
        (sipi_motor.py), y lo ejecuta dentro de la app cuando el usuario
        toca 'Ejecutar programa'. Todo lo que tu programa haga con 'decir'
        aparece en pantalla, en una lista con scroll, dentro del propio
        telefono."""
        carpeta = os.path.join(self.base_dir, f"{nombre_app}_android")
        os.makedirs(carpeta, exist_ok=True)

        ruta_sipi_actual = getattr(self, "archivo_path", None)
        nombre_programa_sipi = os.path.basename(ruta_sipi_actual) if ruta_sipi_actual else "programa.sipi"
        if ruta_sipi_actual and os.path.exists(ruta_sipi_actual):
            shutil.copy(ruta_sipi_actual, os.path.join(carpeta, nombre_programa_sipi))
        else:
            # Si por algun motivo no hay archivo de origen (ej. se llamo
            # desde un modo interactivo), se deja un programa de ejemplo
            # en vez de fallar en silencio.
            nombre_programa_sipi = "programa.sipi"
            with open(os.path.join(carpeta, nombre_programa_sipi), "w", encoding="utf-8") as f:
                f.write(f'programa "{nombre_app}"\n\ndecir "Hola desde {nombre_app}, hecho con SiPi!"\n')
        shutil.copy(os.path.abspath(__file__), os.path.join(carpeta, "sipi_motor.py"))

        app_class = re.sub(r"[^a-zA-Z0-9]", "", nombre_app) or "MiAppSiPi"
        main_py = f'''import io
import threading
import contextlib

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from sipi_motor import Interprete

NOMBRE_PROGRAMA = "{nombre_programa_sipi}"


class PantallaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.salida = Label(
            text="Toca 'Ejecutar programa' para correr {nombre_app}.",
            size_hint_y=None, halign="left", valign="top", font_size=16,
        )
        self.salida.bind(width=lambda *a: self.salida.setter("text_size")(self.salida, (self.salida.width, None)))
        self.salida.bind(texture_size=lambda *a: self.salida.setter("height")(self.salida, self.salida.texture_size[1]))

        scroll = ScrollView()
        scroll.add_widget(self.salida)
        self.add_widget(scroll)

        boton = Button(text="Ejecutar programa", size_hint_y=None, height=60, font_size=20)
        boton.bind(on_press=self.al_presionar)
        self.add_widget(boton)

    def al_presionar(self, instancia):
        self.salida.text = "Ejecutando..."
        hilo = threading.Thread(target=self._correr_programa, daemon=True)
        hilo.start()

    def _correr_programa(self):
        buffer_salida = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer_salida):
                interprete = Interprete(NOMBRE_PROGRAMA)
                interprete.ejecutar()
            texto = buffer_salida.getvalue() or "(El programa no imprimio nada con 'decir'.)"
        except Exception as e:
            texto = buffer_salida.getvalue() + f"\\n[Error al ejecutar el programa]\\n{{e}}"
        Clock.schedule_once(lambda dt: setattr(self.salida, "text", texto))


class {app_class}App(App):
    def build(self):
        self.title = "{nombre_app}"
        return PantallaPrincipal()


if __name__ == "__main__":
    {app_class}App().run()
'''
        with open(os.path.join(carpeta, "main.py"), "w", encoding="utf-8") as f:
            f.write(main_py)

        buildozer_spec = f'''[app]
title = {nombre_app}
package.name = {re.sub(r"[^a-zA-Z0-9]", "", nombre_app).lower()}
package.domain = org.sipi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,sipi
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
'''
        with open(os.path.join(carpeta, "buildozer.spec"), "w", encoding="utf-8") as f:
            f.write(buildozer_spec)

        instrucciones = f'''PROYECTO ANDROID: {nombre_app}
Generado por SiPi - 100% real y funcional.

Esta carpeta contiene:
  - {nombre_programa_sipi}   -> TU programa real, tal cual lo escribiste.
  - sipi_motor.py            -> el motor/interprete completo de SiPi, embebido.
  - main.py                  -> la app Kivy que carga y corre tu programa de verdad
                                 al tocar "Ejecutar programa", mostrando en pantalla
                                 todo lo que imprimas con 'decir'.
  - buildozer.spec           -> configuracion de compilacion a APK.

Este es un proyecto Kivy completo y listo para compilar a APK real, que ejecuta
TU LOGICA, no una demo generica.

COMO GENERAR EL APK (requiere Linux o WSL en Windows 10):
1. Instala WSL en Windows 10: abre PowerShell como administrador y ejecuta:
   wsl --install
2. Dentro de WSL (Ubuntu), instala buildozer:
   sudo apt update && sudo apt install -y python3-pip git zip openjdk-17-jdk
   pip install buildozer cython
3. Copia esta carpeta dentro de WSL y entra en ella:
   cd {nombre_app}_android
4. Compila el APK:
   buildozer android debug
5. El archivo .apk real aparecera en la carpeta bin/, listo para instalar en cualquier
   celular Android (activa "Origenes desconocidos" para instalarlo).

Nota honesta: compilar un APK requiere el SDK de Android y herramientas de compilacion
que ocupan varios GB y no pueden empaquetarse dentro de un .zip. Por eso SiPi te genera
el CODIGO REAL Y COMPLETO del proyecto (main.py + sipi_motor.py + tu programa +
buildozer.spec) listo para compilar, en vez de simular un boton "instalar automaticamente"
que en realidad no podria funcionar
sin esas herramientas del sistema.
'''
        with open(os.path.join(carpeta, "LEEME.txt"), "w", encoding="utf-8") as f:
            f.write(instrucciones)

        print(f"[SiPi] Proyecto Android real generado en: {carpeta}")
        print("[SiPi] Lee LEEME.txt dentro de esa carpeta para compilar el APK real.")

    def _generar_proyecto_windows(self, nombre_app):
        """Genera un proyecto de escritorio real para Windows usando tkinter + pyinstaller."""
        carpeta = os.path.join(self.base_dir, f"{nombre_app}_windows")
        os.makedirs(carpeta, exist_ok=True)

        app_py = f'''import tkinter as tk

def al_presionar():
    global contador
    contador += 1
    etiqueta.config(text=f"Presionaste {{contador}} veces")

contador = 0
root = tk.Tk()
root.title("{nombre_app}")
root.geometry("400x300")

etiqueta = tk.Label(root, text="Bienvenido a {nombre_app}\\nHecho con SiPi", font=("Segoe UI", 14))
etiqueta.pack(pady=40)

boton = tk.Button(root, text="Presioname", command=al_presionar, font=("Segoe UI", 12))
boton.pack()

root.mainloop()
'''
        with open(os.path.join(carpeta, "app.py"), "w", encoding="utf-8") as f:
            f.write(app_py)

        compilar_bat = '''@echo off
echo Compilando aplicacion .exe real con PyInstaller...
pip install pyinstaller
pyinstaller --onefile --windowed app.py
echo.
echo Listo. El archivo .exe real esta en la carpeta "dist".
pause
'''
        with open(os.path.join(carpeta, "compilar_exe.bat"), "w", encoding="utf-8") as f:
            f.write(compilar_bat)

        print(f"[SiPi] Proyecto de escritorio para Windows generado en: {carpeta}")
        print("[SiPi] Ejecuta compilar_exe.bat dentro de esa carpeta para crear el .exe real.")

    # ---------- Item 9: compilar SiPi -> JavaScript real (corre en el navegador) ----------

    def _js_expr(self, expr):
        """Traduce una expresion SiPi (subconjunto real: numeros, texto con
        interpolacion {var}, variables, +-*/, comparaciones ==/!=/<=/>=/</>,
        y/o, llamadas a otras funciones ya compiladas) a JavaScript."""
        expr = expr.strip()
        m_txt = _m(r'^"(.*)"$', expr, re.DOTALL)
        if m_txt:
            contenido = m_txt.group(1).replace("\\", "\\\\").replace("`", "\\`")

            def _reemplazar(mi):
                return "${" + self._js_expr(mi.group(1)) + "}"

            contenido = PATRON_INTERPOLACION.sub(_reemplazar, contenido)
            return "`" + contenido + "`"
        m_call = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$", expr)
        if m_call:
            nombre = m_call.group(1)
            args = [self._js_expr(a) for a in self._separar_args_top(m_call.group(2))]
            return f"{nombre}({', '.join(args)})"
        expr = re.sub(r"\bverdadero\b", "true", expr)
        expr = re.sub(r"\bfalso\b", "false", expr)
        expr = re.sub(r"\bnulo\b", "null", expr)
        expr = re.sub(r"\by\b", "&&", expr)
        expr = re.sub(r"\bo\b", "||", expr)
        expr = expr.replace("==", "===").replace("!=", "!==")
        expr = expr.replace("!==", "!==").replace("<===", "<=").replace(">===", ">=")
        # arreglar el reemplazo doble de <= y >= que pudo quedar mal formado
        expr = expr.replace("< ==", "<=").replace("> ==", ">=")
        return expr

    @staticmethod
    def _separar_args_top(texto):
        """Separa argumentos por comas, respetando parentesis y comillas anidadas."""
        args, actual, prof, en_cadena = [], "", 0, False
        for ch in texto:
            if ch == '"':
                en_cadena = not en_cadena
            if ch == "(" and not en_cadena:
                prof += 1
            if ch == ")" and not en_cadena:
                prof -= 1
            if ch == "," and prof == 0 and not en_cadena:
                args.append(actual.strip())
                actual = ""
                continue
            actual += ch
        if actual.strip():
            args.append(actual.strip())
        return args

    def _js_bloque(self, lineas_cuerpo, indent="  "):
        """Traduce linea por linea el subconjunto real soportado de SiPi:
        variable, sumar/restar, si/sino/fin, mientras/fin, decir, devolver
        y llamadas a funciones. Comandos sin equivalente de navegador
        (archivos, bases de datos, GUI, etc.) se marcan como comentario
        honesto en vez de fingir que se tradujeron."""
        salida = []
        idx = 0
        while idx < len(lineas_cuerpo):
            cruda = lineas_cuerpo[idx]
            texto_crudo = cruda[1] if isinstance(cruda, tuple) else cruda
            linea = texto_crudo.strip()
            if not linea or linea.startswith("//") or linea.startswith("#"):
                idx += 1
                continue

            m_var = _m(r"^variable\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*(?::\s*[\w\u0900-\u097F\u0980-\u09FF]+\s*)?=\s*(.+)$", linea)
            if m_var:
                salida.append(f"{indent}let {m_var.group(1)} = {self._js_expr(m_var.group(2))};")
                idx += 1
                continue

            m_sum = _m(r"^sumar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_sum:
                salida.append(f"{indent}{m_sum.group(1)} += {self._js_expr(m_sum.group(2))};")
                idx += 1
                continue

            m_res = _m(r"^restar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_res:
                salida.append(f"{indent}{m_res.group(1)} -= {self._js_expr(m_res.group(2))};")
                idx += 1
                continue

            if linea.startswith("si "):
                cond = self._js_expr(linea[3:])
                fin_si, inicio_sino = self._encontrar_fin_si_js(lineas_cuerpo, idx)
                limite_si = inicio_sino if inicio_sino is not None else fin_si
                salida.append(f"{indent}if ({cond}) {{")
                salida += self._js_bloque(lineas_cuerpo[idx + 1:limite_si], indent + "  ")
                if inicio_sino is not None:
                    salida.append(f"{indent}}} else {{")
                    salida += self._js_bloque(lineas_cuerpo[inicio_sino + 1:fin_si], indent + "  ")
                salida.append(f"{indent}}}")
                idx = fin_si + 1
                continue

            if linea.startswith("mientras "):
                cond = self._js_expr(linea[len("mientras "):])
                fin_m = self._encontrar_fin_simple_js(lineas_cuerpo, idx)
                salida.append(f"{indent}while ({cond}) {{")
                salida += self._js_bloque(lineas_cuerpo[idx + 1:fin_m], indent + "  ")
                salida.append(f"{indent}}}")
                idx = fin_m + 1
                continue

            m_pc = _m(r"^para_cada\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_pc:
                var_item, nombre_lista = m_pc.groups()
                fin_pc = self._encontrar_fin_simple_js(lineas_cuerpo, idx)
                salida.append(f"{indent}for (const {var_item} of {nombre_lista}) {{")
                salida += self._js_bloque(lineas_cuerpo[idx + 1:fin_pc], indent + "  ")
                salida.append(f"{indent}}}")
                idx = fin_pc + 1
                continue

            if linea == "romper":
                salida.append(f"{indent}break;")
                idx += 1
                continue
            if linea == "continuar":
                salida.append(f"{indent}continue;")
                idx += 1
                continue

            m_lc = _m(r"^lista_crear\s+([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s*:\s*lista<[\w\u0900-\u097F\u0980-\u09FF]+>)?$", linea)
            if m_lc:
                salida.append(f"{indent}let {m_lc.group(1)} = [];")
                idx += 1
                continue
            m_la = _m(r"^lista_agregar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_la:
                nombre, expr = m_la.groups()
                salida.append(f"{indent}{nombre}.push({self._js_expr(expr)});")
                idx += 1
                continue
            m_lo = _m(r"^lista_obtener\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_lo:
                nombre, idx_expr, var = m_lo.groups()
                salida.append(f"{indent}let {var} = {nombre}[{self._js_expr(idx_expr)}];")
                idx += 1
                continue
            m_ll_len = _m(r"^lista_longitud\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_ll_len:
                nombre, var = m_ll_len.groups()
                salida.append(f"{indent}let {var} = {nombre}.length;")
                idx += 1
                continue
            m_le = _m(r"^lista_eliminar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_le:
                nombre, idx_expr = m_le.groups()
                salida.append(f"{indent}{nombre}.splice({self._js_expr(idx_expr)}, 1);")
                idx += 1
                continue

            m_dc = _m(r"^diccionario_crear\s+([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s*:\s*diccionario<[\w\u0900-\u097F\u0980-\u09FF]+>)?$", linea)
            if m_dc:
                salida.append(f"{indent}let {m_dc.group(1)} = {{}};")
                idx += 1
                continue
            m_da = _m(r'^diccionario_asignar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+("(?:[^"]*)"|\S+)\s+(.+)$', linea)
            if m_da:
                nombre, clave_expr, expr = m_da.groups()
                salida.append(f"{indent}{nombre}[{self._js_expr(clave_expr)}] = {self._js_expr(expr)};")
                idx += 1
                continue
            m_do = _m(r'^diccionario_obtener\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)(\?)?\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', linea)
            if m_do:
                nombre, clave_expr, con_signo, var = m_do.groups()
                default = "null" if con_signo else '""'
                salida.append(f"{indent}let {var} = ({nombre}[{self._js_expr(clave_expr)}] ?? {default});")
                idx += 1
                continue
            m_dt = _m(r'^diccionario_tiene\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', linea)
            if m_dt:
                nombre, clave_expr, var = m_dt.groups()
                salida.append(f"{indent}let {var} = Object.prototype.hasOwnProperty.call({nombre}, {self._js_expr(clave_expr)});")
                idx += 1
                continue
            m_de = _m(r'^diccionario_eliminar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$', linea)
            if m_de:
                nombre, clave_expr = m_de.groups()
                salida.append(f"{indent}delete {nombre}[{self._js_expr(clave_expr)}];")
                idx += 1
                continue
            m_dk = _m(r"^diccionario_claves\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_dk:
                nombre, var = m_dk.groups()
                salida.append(f"{indent}let {var} = Object.keys({nombre});")
                idx += 1
                continue

            m_dev = _m(r"^devolver\s+(.+)$", linea)
            if m_dev:
                salida.append(f"{indent}return {self._js_expr(m_dev.group(1))};")
                idx += 1
                continue

            m_decir = _m(r'^decir\s+(.+)$', linea)
            if m_decir:
                salida.append(f"{indent}console.log({self._js_expr(m_decir.group(1))});")
                idx += 1
                continue

            m_llv = _m(r"^llamar_valor\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_llv:
                nombre, args_str, var_destino = m_llv.groups()
                args = ", ".join(self._js_expr(a) for a in self._separar_args_top(args_str))
                salida.append(f"{indent}let {var_destino} = {nombre}({args});")
                idx += 1
                continue

            m_ll = _m(r"^llamar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$", linea)
            if m_ll:
                nombre, args_str = m_ll.groups()
                args = ", ".join(self._js_expr(a) for a in self._separar_args_top(args_str))
                salida.append(f"{indent}{nombre}({args});")
                idx += 1
                continue

            if linea == "fin":
                idx += 1
                continue

            # Comando no soportado en el navegador (archivos, sqlite, GUI de
            # escritorio, etc.): se documenta en vez de fingir soporte.
            salida.append(f"{indent}// [SiPi->JS] linea no soportada en navegador: {linea}")
            idx += 1
        return salida

    @staticmethod
    def _encontrar_fin_simple_js(lineas_cuerpo, idx_inicio):
        """Encuentra el 'fin' que cierra el bloque que abre en idx_inicio,
        contando anidamiento de cualquier bloque (si/mientras/repetir/etc)."""
        profundidad = 1
        j = idx_inicio + 1
        while j < len(lineas_cuerpo):
            cr = lineas_cuerpo[j]
            limpia = (cr[1] if isinstance(cr, tuple) else cr).strip()
            palabra = limpia.split(" ")[0] if limpia else ""
            if palabra in BLOQUES_QUE_ABREN or limpia.startswith(("si ", "mientras ")):
                profundidad += 1
            elif limpia == "fin":
                profundidad -= 1
                if profundidad == 0:
                    return j
            j += 1
        return len(lineas_cuerpo) - 1

    def _encontrar_fin_si_js(self, lineas_cuerpo, idx_inicio):
        """Como _encontrar_fin_simple_js pero ademas detecta un 'sino' al
        mismo nivel de anidamiento, para poder generar el 'else' en JS."""
        profundidad = 1
        inicio_sino = None
        j = idx_inicio + 1
        while j < len(lineas_cuerpo):
            cr = lineas_cuerpo[j]
            limpia = (cr[1] if isinstance(cr, tuple) else cr).strip()
            palabra = limpia.split(" ")[0] if limpia else ""
            if palabra in BLOQUES_QUE_ABREN or limpia.startswith(("si ", "mientras ")):
                profundidad += 1
            elif limpia == "sino" and profundidad == 1:
                inicio_sino = j
            elif limpia == "fin":
                profundidad -= 1
                if profundidad == 0:
                    return j, inicio_sino
            j += 1
        return len(lineas_cuerpo) - 1, inicio_sino

    def _compilar_funciones_a_js(self, nombres_funciones, ruta_salida):
        """Item 9 del roadmap ('Motor de WebAssembly para Frontend'): en vez
        de prometer un compilador a WASM que esta fuera del alcance real de
        un interprete escrito en Python puro, SiPi compila de verdad tus
        funciones a JavaScript nativo. El resultado es un archivo .js que
        corre tal cual en cualquier navegador (via <script src="...">),
        sin necesitar Python, sin servidor y sin runtime de SiPi instalado.
        Es la forma honesta y funcional de lograr el mismo objetivo del
        item 9: logica de SiPi ejecutandose del lado del cliente."""
        piezas = []
        piezas.append("// Generado automaticamente por SiPi (compilar_a_js).")
        piezas.append("// Este archivo es JavaScript real y corre en cualquier navegador,")
        piezas.append("// sin depender de Python ni de un servidor.\n")

        for nombre in nombres_funciones:
            info_fn = self.entorno.funciones.get(nombre)
            if info_fn is None:
                piezas.append(f"// [SiPi->JS] La funcion '{nombre}' no existe o no fue definida antes de este punto.\n")
                continue
            params_info, ini, fin_fn, lineas_fn = info_fn[:4]
            nombres_params = [p[0] if isinstance(p, tuple) else p for p in params_info]
            cuerpo = lineas_fn[ini:fin_fn]
            js_cuerpo = self._js_bloque(cuerpo, "  ")
            piezas.append(f"function {nombre}({', '.join(nombres_params)}) {{")
            piezas.extend(js_cuerpo)
            piezas.append("}\n")

        contenido = "\n".join(piezas)
        ruta_completa = os.path.join(self.base_dir, ruta_salida) if not os.path.isabs(ruta_salida) else ruta_salida
        os.makedirs(os.path.dirname(ruta_completa) or ".", exist_ok=True)
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(contenido)

        print(f"[SiPi] Funciones compiladas a JavaScript real: {ruta_completa}")
        print(f"[SiPi] Incluilas en tu HTML con: <script src=\"{os.path.basename(ruta_completa)}\"></script>")
        print("[SiPi] Nota honesta: se tradujo el subconjunto real soportado (variable, si/sino, mientras,")
        print("       sumar/restar, decir, devolver, llamadas entre funciones). Comandos de servidor,")
        print("       archivos o GUI de escritorio no tienen equivalente en el navegador y quedan como comentario.")

    # ---------- Item 4: transpilador SiPi -> Python standalone ----------
    # Un JIT bytecode real (tipo PyPy) esta fuera del alcance realista de
    # una sola sesion. Lo que SI se puede dar, y ataca el mismo problema de
    # fondo (rendimiento y portabilidad), es un TRANSPILADOR real: convierte
    # todo el programa .sipi en un archivo .py equivalente, que corre con
    # 'python archivo.py' sin el overhead del parser/interprete de SiPi
    # (sin regex por linea, sin recorrer el arbol de comandos en cada
    # ejecucion) y que ademas se puede compilar a .exe con pyinstaller o
    # subir a cualquier lado que tenga Python, sin necesitar sipi.py.

    def _py_expr(self, expr):
        """Traduce una expresion SiPi a Python. A diferencia de JS, la
        sintaxis de expresiones de SiPi ya es casi identica a Python
        (mismos operadores de comparacion, misma prioridad aritmetica), asi
        que el trabajo principal es: interpolacion {x} -> f-strings, y las
        palabras reservadas verdadero/falso/nulo/y/o -> True/False/None/and/or."""
        expr = expr.strip()
        m_txt = _m(r'^"(.*)"$', expr, re.DOTALL)
        if m_txt:
            contenido = m_txt.group(1).replace("\\", "\\\\").replace('"', '\\"')
            if PATRON_INTERPOLACION.search(contenido):
                def _reemplazar(mi):
                    return "{" + self._py_expr(mi.group(1)) + "}"
                contenido = PATRON_INTERPOLACION.sub(_reemplazar, contenido)
                return 'f"' + contenido + '"'
            return '"' + contenido + '"'
        m_call = _m(r"^([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$", expr)
        if m_call:
            nombre = m_call.group(1)
            args = [self._py_expr(a) for a in self._separar_args_top(m_call.group(2))]
            return f"{nombre}({', '.join(args)})"
        expr = re.sub(r"\bverdadero\b", "True", expr)
        expr = re.sub(r"\bfalso\b", "False", expr)
        expr = re.sub(r"\bnulo\b", "None", expr)
        expr = re.sub(r"\by\b", "and", expr)
        expr = re.sub(r"\bo\b", "or", expr)
        return expr

    def _py_bloque(self, lineas_cuerpo, indent="    "):
        """Equivalente a _js_bloque pero generando Python real. Mismo
        subconjunto soportado, mas 'repetir N veces' (-> for _ in range),
        'romper'/'continuar' (-> break/continue) ya que en Python son
        triviales de mapear 1 a 1, a diferencia de JS donde no hacian falta
        para el caso de uso tipico de frontend."""
        salida = []
        idx = 0
        while idx < len(lineas_cuerpo):
            cruda = lineas_cuerpo[idx]
            texto_crudo = cruda[1] if isinstance(cruda, tuple) else cruda
            linea = texto_crudo.strip()
            if not linea or linea.startswith("//") or linea.startswith("#"):
                idx += 1
                continue

            m_var = _m(r"^variable\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*(?::\s*[\w\u0900-\u097F\u0980-\u09FF]+\s*)?=\s*(.+)$", linea)
            if m_var:
                salida.append(f"{indent}{m_var.group(1)} = {self._py_expr(m_var.group(2))}")
                idx += 1
                continue

            m_sum = _m(r"^sumar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_sum:
                salida.append(f"{indent}{m_sum.group(1)} += {self._py_expr(m_sum.group(2))}")
                idx += 1
                continue

            m_res = _m(r"^restar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_res:
                salida.append(f"{indent}{m_res.group(1)} -= {self._py_expr(m_res.group(2))}")
                idx += 1
                continue

            if linea.startswith("si "):
                cond = self._py_expr(linea[3:])
                fin_si, inicio_sino = self._encontrar_fin_si_js(lineas_cuerpo, idx)
                limite_si = inicio_sino if inicio_sino is not None else fin_si
                salida.append(f"{indent}if {cond}:")
                cuerpo_si = self._py_bloque(lineas_cuerpo[idx + 1:limite_si], indent + "    ")
                salida += cuerpo_si if cuerpo_si else [f"{indent}    pass"]
                if inicio_sino is not None:
                    salida.append(f"{indent}else:")
                    cuerpo_sino = self._py_bloque(lineas_cuerpo[inicio_sino + 1:fin_si], indent + "    ")
                    salida += cuerpo_sino if cuerpo_sino else [f"{indent}    pass"]
                idx = fin_si + 1
                continue

            if linea.startswith("mientras "):
                cond = self._py_expr(linea[len("mientras "):])
                fin_m = self._encontrar_fin_simple_js(lineas_cuerpo, idx)
                salida.append(f"{indent}while {cond}:")
                cuerpo_m = self._py_bloque(lineas_cuerpo[idx + 1:fin_m], indent + "    ")
                salida += cuerpo_m if cuerpo_m else [f"{indent}    pass"]
                idx = fin_m + 1
                continue

            m_rep = _m(r"^repetir\s+(.+?)\s+veces$", linea)
            if m_rep:
                veces = self._py_expr(m_rep.group(1))
                fin_r = self._encontrar_fin_simple_js(lineas_cuerpo, idx)
                salida.append(f"{indent}for _ in range({veces}):")
                cuerpo_r = self._py_bloque(lineas_cuerpo[idx + 1:fin_r], indent + "    ")
                salida += cuerpo_r if cuerpo_r else [f"{indent}    pass"]
                idx = fin_r + 1
                continue

            m_pc = _m(r"^para_cada\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+en\s+([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_pc:
                var_item, nombre_lista = m_pc.groups()
                fin_pc = self._encontrar_fin_simple_js(lineas_cuerpo, idx)
                salida.append(f"{indent}for {var_item} in {nombre_lista}:")
                cuerpo_pc = self._py_bloque(lineas_cuerpo[idx + 1:fin_pc], indent + "    ")
                salida += cuerpo_pc if cuerpo_pc else [f"{indent}    pass"]
                idx = fin_pc + 1
                continue

            m_lc = _m(r"^lista_crear\s+([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s*:\s*lista<[\w\u0900-\u097F\u0980-\u09FF]+>)?$", linea)
            if m_lc:
                salida.append(f"{indent}{m_lc.group(1)} = []")
                idx += 1
                continue
            m_la = _m(r"^lista_agregar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_la:
                nombre, expr = m_la.groups()
                salida.append(f"{indent}{nombre}.append({self._py_expr(expr)})")
                idx += 1
                continue
            m_lo = _m(r"^lista_obtener\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_lo:
                nombre, idx_expr, var = m_lo.groups()
                salida.append(f"{indent}{var} = {nombre}[{self._py_expr(idx_expr)}]")
                idx += 1
                continue
            m_ll_len = _m(r"^lista_longitud\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_ll_len:
                nombre, var = m_ll_len.groups()
                salida.append(f"{indent}{var} = len({nombre})")
                idx += 1
                continue
            m_le = _m(r"^lista_eliminar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$", linea)
            if m_le:
                nombre, idx_expr = m_le.groups()
                salida.append(f"{indent}del {nombre}[{self._py_expr(idx_expr)}]")
                idx += 1
                continue

            m_dc = _m(r"^diccionario_crear\s+([\w\u0900-\u097F\u0980-\u09FF]+)(?:\s*:\s*diccionario<[\w\u0900-\u097F\u0980-\u09FF]+>)?$", linea)
            if m_dc:
                salida.append(f"{indent}{m_dc.group(1)} = {{}}")
                idx += 1
                continue
            m_da = _m(r'^diccionario_asignar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+("(?:[^"]*)"|\S+)\s+(.+)$', linea)
            if m_da:
                nombre, clave_expr, expr = m_da.groups()
                salida.append(f"{indent}{nombre}[{self._py_expr(clave_expr)}] = {self._py_expr(expr)}")
                idx += 1
                continue
            m_do = _m(r'^diccionario_obtener\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)(\?)?\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', linea)
            if m_do:
                nombre, clave_expr, con_signo, var = m_do.groups()
                default = "None" if con_signo else '""'
                salida.append(f"{indent}{var} = {nombre}.get({self._py_expr(clave_expr)}, {default})")
                idx += 1
                continue
            m_dt = _m(r'^diccionario_tiene\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+?)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$', linea)
            if m_dt:
                nombre, clave_expr, var = m_dt.groups()
                salida.append(f"{indent}{var} = {self._py_expr(clave_expr)} in {nombre}")
                idx += 1
                continue
            m_de2 = _m(r'^diccionario_eliminar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s+(.+)$', linea)
            if m_de2:
                nombre, clave_expr = m_de2.groups()
                salida.append(f"{indent}{nombre}.pop({self._py_expr(clave_expr)}, None)")
                idx += 1
                continue
            m_dk = _m(r"^diccionario_claves\s+([\w\u0900-\u097F\u0980-\u09FF]+)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_dk:
                nombre, var = m_dk.groups()
                salida.append(f"{indent}{var} = list({nombre}.keys())")
                idx += 1
                continue

            if linea == "romper":
                salida.append(f"{indent}break")
                idx += 1
                continue
            if linea == "continuar":
                salida.append(f"{indent}continue")
                idx += 1
                continue

            m_dev = _m(r"^devolver\s+(.+)$", linea)
            if m_dev:
                salida.append(f"{indent}return {self._py_expr(m_dev.group(1))}")
                idx += 1
                continue

            m_decir = _m(r'^decir\s+(.+)$', linea)
            if m_decir:
                salida.append(f"{indent}print({self._py_expr(m_decir.group(1))})")
                idx += 1
                continue

            m_llv = _m(r"^llamar_valor\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)\s*->\s*([\w\u0900-\u097F\u0980-\u09FF]+)$", linea)
            if m_llv:
                nombre, args_str, var_destino = m_llv.groups()
                args = ", ".join(self._py_expr(a) for a in self._separar_args_top(args_str))
                salida.append(f"{indent}{var_destino} = {nombre}({args})")
                idx += 1
                continue

            m_ll = _m(r"^llamar\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)$", linea)
            if m_ll:
                nombre, args_str = m_ll.groups()
                args = ", ".join(self._py_expr(a) for a in self._separar_args_top(args_str))
                salida.append(f"{indent}{nombre}({args})")
                idx += 1
                continue

            if linea == "fin":
                idx += 1
                continue

            salida.append(f"{indent}# [SiPi->Python] linea no soportada por el transpilador aun: {linea}")
            idx += 1
        return salida

    def _compilar_programa_a_python(self, ruta_salida):
        """Transpila TODO el programa (no solo funciones sueltas, a
        diferencia de compilar_a_js) a un .py standalone y ejecutable con
        'python archivo.py', sin depender de sipi.py."""
        piezas = [
            "#!/usr/bin/env python3",
            "# Generado automaticamente por SiPi (compilar_a_python).",
            "# Este archivo es Python real y NO necesita sipi.py para correr.\n",
        ]
        definiciones_funciones = []
        lineas_principal = []

        idx = 0
        while idx < len(self.lineas):
            _, cruda = self.lineas[idx]
            linea = cruda.strip()
            if not linea or linea.startswith("programa "):
                idx += 1
                continue

            m_fn = _m(r"^funcion\s+([\w\u0900-\u097F\u0980-\u09FF]+)\((.*)\)(?:\s*->\s*[\w\u0900-\u097F\u0980-\u09FF]+)?$", linea)
            if m_fn:
                nombre, params_txt = m_fn.groups()
                fin_fn = self._encontrar_fin(idx, BLOQUES_QUE_ABREN)
                cuerpo = self.lineas[idx + 1:fin_fn]
                definiciones_funciones.append(f"def {nombre}({params_txt.strip()}):")
                cuerpo_py = self._py_bloque(cuerpo, "    ")
                definiciones_funciones += (cuerpo_py if cuerpo_py else ["    pass"])
                definiciones_funciones.append("")
                idx = fin_fn + 1
                continue

            # Cualquier otro bloque de nivel superior (si/mientras/repetir
            # con top-level, o una linea suelta) se procesa con la misma
            # logica de _py_bloque, tomando de a un item de nivel superior
            # (buscando su propio 'fin' si abre bloque).
            primera_palabra = linea.split(" ")[0]
            if primera_palabra in BLOQUES_QUE_ABREN:
                fin_bloque = self._encontrar_fin(idx, BLOQUES_QUE_ABREN)
                lineas_principal += self._py_bloque(self.lineas[idx:fin_bloque + 1], "    ")
                idx = fin_bloque + 1
            else:
                lineas_principal += self._py_bloque([self.lineas[idx]], "    ")
                idx += 1

        piezas += definiciones_funciones
        piezas.append('if __name__ == "__main__":')
        piezas += (lineas_principal if lineas_principal else ["    pass"])

        contenido = "\n".join(piezas) + "\n"
        ruta_completa = os.path.join(self.base_dir, ruta_salida) if not os.path.isabs(ruta_salida) else ruta_salida
        os.makedirs(os.path.dirname(ruta_completa) or ".", exist_ok=True)
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(contenido)

        print(f"[SiPi] Programa completo transpilado a Python real: {ruta_completa}")
        print(f"[SiPi] Corre con: python3 {os.path.basename(ruta_completa)}  (no necesita sipi.py)")
        print("[SiPi] Nota honesta: se tradujo el subconjunto real soportado (funciones, variable,")
        print("       si/sino, mientras, repetir N veces, sumar/restar, decir, devolver, llamadas).")
        print("       Comandos avanzados (GUI, sqlite, archivos con formato SiPi especifico, API web)")
        print("       quedan como comentario '# [SiPi->Python] ...' en vez de fingir que se tradujeron.")

    # ---------- Sistema "Visual": editor WYSIWYG real en el navegador ----------
    # La idea: en vez de mover un boton cambiando numeros a mano en el
    # codigo, lo arrastras con el mouse. En vez de escribir el texto de una
    # etiqueta, hace click y lo escribis ahi mismo. El navegador manda esos
    # cambios a un mini-servidor local que reescribe LAS LINEAS EXACTAS del
    # .sipi de origen -- el resto del archivo (logica, funciones, todo) se
    # deja intacto. Cubre la primera 'ventana' de escritorio del programa;
    # es una primera version real y funcional, pensada para crecer (mas
    # tipos de widget, mas de una ventana, y el mismo enfoque para
    # pagina_web) de a poco.

    _PATRONES_WIDGET_VISUAL = {
        "etiqueta": re.compile(r'^(?P<texto>"(?:[^"]*)"|\S+)\s+(?P<x>\S+)\s+(?P<y>\S+)$'),
        "boton": re.compile(r'^(?P<texto>"(?:[^"]*)"|\S+)\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<accion>[\w\u0900-\u097F\u0980-\u09FF]+\(.*\))$'),
        "entrada": re.compile(r'^(?P<var>[\w\u0900-\u097F\u0980-\u09FF]+)\s+(?P<x>\S+)\s+(?P<y>\S+)$'),
        "cuadro": re.compile(r'^(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<ancho>\S+)\s+(?P<alto>\S+)\s+(?P<color>"(?:[^"]*)"|\S+)$'),
        "imagen": re.compile(r'^(?P<ruta>"(?:[^"]*)"|\S+)\s+(?P<x>\S+)\s+(?P<y>\S+)(?:\s+(?P<ancho>\S+)\s+(?P<alto>\S+))?$'),
    }

    # ---------- Extension del Sistema Visual a pagina_web ----------
    # A diferencia de 'ventana' (coordenadas x/y libres), una pagina web es
    # un flujo de elementos apilados en orden -- asi que "editar
    # visualmente" ahi significa dos cosas distintas: cambiar el TEXTO con
    # un click, y REORDENAR los elementos con flechas (no arrastrar a
    # coordenadas libres, que no tendria sentido en un documento). Los
    # bloques 'formulario ... fin' se muestran y se pueden reordenar como
    # un bloque opaco (para no arriesgar romper su contenido interno
    # multi-linea); sus campos se siguen editando en el codigo por ahora.

    _TIPOS_ELEMENTO_PAGINA_CON_TEXTO = {"titulo", "subtitulo", "texto", "boton", "imagen"}

    def _encontrar_primera_pagina_web(self):
        for idx, (_, cruda) in enumerate(self.lineas):
            m = _m(r'^pagina_web\s+"([^"]*)"$', cruda.strip())
            if m:
                fin_p = self._encontrar_fin(idx, BLOQUES_QUE_ABREN)
                return idx, fin_p, m.group(1)
        return None

    def _recolectar_elementos_pagina_visual(self, idx_inicio, idx_fin):
        elementos = []
        idx = idx_inicio + 1
        while idx < idx_fin:
            num_linea, cruda = self.lineas[idx]
            limpia = cruda.strip()
            if not limpia:
                idx += 1
                continue
            partes = limpia.split(" ", 1)
            tipo = partes[0]
            resto_el = partes[1] if len(partes) > 1 else ""

            if tipo == "formulario":
                fin_form = self._encontrar_fin(idx, BLOQUES_QUE_ABREN)
                mm = _m(r'^"([^"]*)"$', resto_el.strip())
                accion = mm.group(1) if mm else ""
                campos_internos = []
                for idx_campo in range(idx + 1, fin_form):
                    num_campo, cruda_campo = self.lineas[idx_campo]
                    limpia_campo = cruda_campo.strip()
                    if not limpia_campo:
                        continue
                    partes_campo = limpia_campo.split(" ", 1)
                    subtipo = partes_campo[0]
                    resto_campo = partes_campo[1] if len(partes_campo) > 1 else ""
                    if subtipo == "campo":
                        mmc = _m(r'^"([^"]*)"(?:\s+([\w\u0900-\u097F\u0980-\u09FF]+))?$', resto_campo)
                        if mmc:
                            etiqueta_campo, tipo_campo = mmc.groups()
                            campos_internos.append({"idx_interno": idx_campo, "tipo": "campo",
                                                     "texto": self.interpolar(etiqueta_campo),
                                                     "detalle": tipo_campo or "texto", "editable": True})
                    elif subtipo == "boton":
                        mmb = _m(r'^"([^"]*)"$', resto_campo.strip())
                        if mmb:
                            campos_internos.append({"idx_interno": idx_campo, "tipo": "boton",
                                                     "texto": self.interpolar(mmb.group(1)),
                                                     "detalle": None, "editable": True})
                elementos.append({"idx_interno": idx, "idx_fin_bloque": fin_form, "tipo": "formulario",
                                   "texto": f"Formulario ({accion})", "editable": False,
                                   "campos_internos": campos_internos})
                idx = fin_form + 1
                continue

            if tipo in ("tema", "color"):
                # No son elementos visuales en si, se dejan pasar de largo
                # sin mostrarlos en el lienzo (se siguen pudiendo editar en
                # el codigo).
                idx += 1
                continue

            texto_mostrado, editable = "", False
            if tipo in ("titulo", "subtitulo", "texto", "boton", "imagen"):
                mm = _m(r'^"([^"]*)"$', resto_el.strip())
                texto_mostrado = self.interpolar(mm.group(1)) if mm else resto_el
                editable = True
            elif tipo == "tarjeta":
                mm = _m(r'^"([^"]*)"\s+"([^"]*)"$', resto_el.strip())
                texto_mostrado = f"{mm.group(1)} — {mm.group(2)}" if mm else resto_el
                editable = True
            elif tipo == "enlace":
                mm = _m(r'^"([^"]*)"\s+"([^"]*)"$', resto_el.strip())
                texto_mostrado = mm.group(1) if mm else resto_el
                editable = True
            elif tipo == "lista_web":
                mm = _m(r'^"([^"]*)"$', resto_el.strip())
                texto_mostrado = mm.group(1).replace("|", ", ") if mm else resto_el
                editable = True
            elif tipo == "separador":
                texto_mostrado = "――――――"
                editable = False
            else:
                texto_mostrado = limpia
                editable = False

            elementos.append({"idx_interno": idx, "idx_fin_bloque": idx, "tipo": tipo,
                               "texto": texto_mostrado, "editable": editable, "linea_original": limpia})
            idx += 1
        return elementos

    def _html_editor_visual_web(self, titulo_pagina, elementos):
        etiquetas_tipo = {
            "titulo": "Título (H1)", "subtitulo": "Subtítulo (H2)", "texto": "Párrafo",
            "boton": "Botón", "imagen": "Imagen (ruta)", "enlace": "Enlace",
            "tarjeta": "Tarjeta", "lista_web": "Lista", "separador": "Separador",
            "formulario": "Formulario",
        }
        piezas = []
        total = len(elementos)
        for pos, el in enumerate(elementos):
            etiqueta = etiquetas_tipo.get(el["tipo"], el["tipo"])
            texto_html = el["texto"].replace("<", "&lt;").replace(">", "&gt;")
            deshabilitar_arriba = "disabled" if pos == 0 else ""
            deshabilitar_abajo = "disabled" if pos == total - 1 else ""

            campos_html = ""
            if el["tipo"] == "formulario" and el.get("campos_internos"):
                filas_campos = []
                for campo in el["campos_internos"]:
                    texto_campo_html = campo["texto"].replace("<", "&lt;").replace(">", "&gt;")
                    detalle = f'<span class="sipi-detalle-campo">({campo["detalle"]})</span>' if campo["detalle"] else ""
                    filas_campos.append(f'''
            <div class="sipi-campo-form">
              <span class="sipi-etiqueta-campo">{"Campo" if campo["tipo"] == "campo" else "Botón"}</span>
              <div class="sipi-texto-web sipi-texto-campo" contenteditable spellcheck="false"
                   data-idx="{campo["idx_interno"]}">{texto_campo_html}</div>
              {detalle}
            </div>''')
                campos_html = f'<div class="sipi-campos-formulario">{"".join(filas_campos)}</div>'

            piezas.append(f'''
      <div class="sipi-elemento-web" data-idx="{el["idx_interno"]}">
        <div class="sipi-flechas">
          <button class="sipi-flecha" {deshabilitar_arriba} onclick="moverElemento({el["idx_interno"]}, 'arriba')">▲</button>
          <button class="sipi-flecha" {deshabilitar_abajo} onclick="moverElemento({el["idx_interno"]}, 'abajo')">▼</button>
        </div>
        <div class="sipi-contenido">
          <span class="sipi-etiqueta-tipo">{etiqueta}</span>
          <div class="sipi-texto-web" {"contenteditable spellcheck='false'" if el["editable"] else ""}
               data-idx="{el["idx_interno"]}">{texto_html}</div>
          {campos_html}
        </div>
      </div>''')

        return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>SiPi Visual - {titulo_pagina}</title>
<style>
  body {{ margin:0; background:#111; color:#eee; font-family:'Segoe UI',sans-serif; }}
  #barra {{ padding:10px 16px; background:#1a1a2a; display:flex; align-items:center; gap:12px; position:sticky; top:0; z-index:10; }}
  #barra h1 {{ font-size:15px; margin:0; font-weight:600; }}
  #barra span {{ font-size:12px; color:#9a9ac0; }}
  button#guardar {{ background:#5865f2; color:#fff; border:none; padding:8px 18px; border-radius:6px;
                     font-size:13px; cursor:pointer; margin-left:auto; }}
  button#guardar:hover {{ background:#4752c4; }}
  #lienzo {{ max-width:700px; margin:20px auto; }}
  .sipi-elemento-web {{ display:flex; gap:10px; background:#1e1e2e; border:1px solid #333; border-radius:8px;
                         padding:12px 14px; margin-bottom:10px; }}
  .sipi-flechas {{ display:flex; flex-direction:column; gap:4px; }}
  .sipi-flecha {{ background:#2a2a3d; color:#ccc; border:1px solid #444; border-radius:4px; width:26px; height:26px;
                   cursor:pointer; font-size:11px; }}
  .sipi-flecha:hover:not(:disabled) {{ background:#3a3a52; }}
  .sipi-flecha:disabled {{ opacity:.25; cursor:default; }}
  .sipi-contenido {{ flex:1; min-width:0; }}
  .sipi-etiqueta-tipo {{ display:block; font-size:10px; text-transform:uppercase; letter-spacing:.05em;
                          color:#8f8fc0; margin-bottom:4px; }}
  .sipi-texto-web {{ font-size:14px; line-height:1.4; word-break:break-word; }}
  .sipi-texto-web[contenteditable="true"] {{ cursor:text; }}
  .sipi-texto-web[contenteditable="true"]:focus {{ outline:2px solid #f2c05e; background:rgba(255,255,255,.06);
                                                     border-radius:4px; padding:2px 4px; }}
  .sipi-campos-formulario {{ margin-top:10px; padding-top:10px; border-top:1px dashed #3a3a52; display:flex;
                              flex-direction:column; gap:8px; }}
  .sipi-campo-form {{ display:flex; align-items:center; gap:8px; font-size:13px; }}
  .sipi-etiqueta-campo {{ font-size:10px; text-transform:uppercase; color:#8f8fc0; min-width:44px; }}
  .sipi-texto-campo {{ background:rgba(255,255,255,.04); border-radius:4px; padding:3px 6px; flex:0 1 auto; }}
  .sipi-detalle-campo {{ color:#777; font-size:11px; }}
  #estado {{ position:fixed; bottom:14px; right:16px; font-size:12px; color:#8f8; }}
</style>
</head>
<body>
  <div id="barra">
    <h1>Editor Visual de SiPi &mdash; {titulo_pagina}</h1>
    <span>Click en el texto para editarlo &middot; flechas para reordenar</span>
    <button id="guardar">Guardar cambios de texto</button>
  </div>
  <div id="lienzo">{"".join(piezas)}</div>
  <div id="estado"></div>
<script>
async function moverElemento(idx, direccion) {{
  const estado = document.getElementById('estado');
  estado.textContent = 'Moviendo...';
  try {{
    const resp = await fetch('/__sipi_mover_web__', {{
      method: 'POST', headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{idx: idx, direccion: direccion}}),
    }});
    const datos = await resp.json();
    if (datos.ok) {{
      location.reload();  // la pagina se re-renderiza en el servidor con el nuevo orden
    }} else {{
      estado.textContent = 'Error: ' + datos.error;
    }}
  }} catch (err) {{
    estado.textContent = 'No se pudo conectar con SiPi: ' + err;
  }}
}}

document.getElementById('guardar').addEventListener('click', async () => {{
  const cambios = [];
  document.querySelectorAll('.sipi-texto-web[contenteditable="true"]').forEach(el => {{
    cambios.push({{idx: parseInt(el.dataset.idx, 10), texto: el.innerText}});
  }});
  const estado = document.getElementById('estado');
  estado.textContent = 'Guardando...';
  try {{
    const resp = await fetch('/__sipi_guardar_web__', {{
      method: 'POST', headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify(cambios),
    }});
    const datos = await resp.json();
    estado.textContent = datos.ok ? ('Guardado: ' + datos.cambios + ' elemento(s) actualizados') : ('Error: ' + datos.error);
  }} catch (err) {{
    estado.textContent = 'No se pudo conectar con SiPi: ' + err;
  }}
}});
</script>
</body>
</html>'''

    def _aplicar_cambios_editor_visual_web(self, archivo_path, cambios):
        """Reescribe SOLO el texto de los elementos editados, preservando
        el tipo de elemento y cualquier otro parametro que tuviera (por
        ejemplo la URL de un 'enlace', que no se edita desde el Visual
        todavia -- solo el texto visible)."""
        with open(archivo_path, "r", encoding="utf-8") as f:
            lineas_archivo = f.read().split("\n")

        n_aplicados = 0
        for cambio in cambios:
            idx_interno = cambio.get("idx")
            nuevo_texto = cambio.get("texto", "")
            if idx_interno is None or idx_interno >= len(self.lineas):
                continue
            num_linea, cruda = self.lineas[idx_interno]
            limpia = cruda.strip()
            partes = limpia.split(" ", 1)
            tipo = partes[0]
            resto_el = partes[1] if len(partes) > 1 else ""
            nuevo_texto_escapado = nuevo_texto.replace('"', '\\"')

            if tipo in ("titulo", "subtitulo", "texto", "boton", "imagen"):
                linea_nueva = f'{tipo} "{nuevo_texto_escapado}"'
            elif tipo == "campo":
                mmc = _m(r'^"([^"]*)"(?:\s+([\w\u0900-\u097F\u0980-\u09FF]+))?$', resto_el)
                tipo_campo_actual = (mmc.group(2) if mmc and mmc.group(2) else "texto")
                linea_nueva = f'campo "{nuevo_texto_escapado}" {tipo_campo_actual}'
            elif tipo == "tarjeta":
                mm = _m(r'^"([^"]*)"\s+"([^"]*)"$', resto_el.strip())
                titulo_actual = mm.group(1) if mm else ""
                # El editor muestra "titulo — texto" en un solo campo; si el
                # usuario lo edito ahi, lo partimos de vuelta por el mismo
                # separador para reconstruir los dos parametros originales.
                if " — " in nuevo_texto:
                    nuevo_titulo, nuevo_cuerpo = nuevo_texto.split(" — ", 1)
                else:
                    nuevo_titulo, nuevo_cuerpo = titulo_actual, nuevo_texto
                linea_nueva = f'tarjeta "{nuevo_titulo.replace(chr(34), chr(92)+chr(34))}" "{nuevo_cuerpo.replace(chr(34), chr(92)+chr(34))}"'
            elif tipo == "enlace":
                mm = _m(r'^"([^"]*)"\s+"([^"]*)"$', resto_el.strip())
                url_actual = mm.group(2) if mm else "#"
                linea_nueva = f'enlace "{nuevo_texto_escapado}" "{url_actual}"'
            elif tipo == "lista_web":
                items_nuevos = [it.strip() for it in nuevo_texto.split(",") if it.strip()]
                linea_nueva = 'lista_web "' + "|".join(items_nuevos) + '"'
            else:
                continue  # tipo no editable (separador, formulario): se ignora cualquier intento

            idx_en_archivo = num_linea - 1
            if 0 <= idx_en_archivo < len(lineas_archivo):
                linea_archivo_actual = lineas_archivo[idx_en_archivo]
                indentacion = linea_archivo_actual[:len(linea_archivo_actual) - len(linea_archivo_actual.lstrip())]
                lineas_archivo[idx_en_archivo] = indentacion + linea_nueva
                self.lineas[idx_interno] = (num_linea, linea_nueva)
                n_aplicados += 1

        with open(archivo_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_archivo))
        self._invalidar_cache_bytecode_si_existe()
        print(f"[SiPi] Editor Visual: {n_aplicados} elemento(s) de texto actualizados en {os.path.basename(archivo_path)}")
        return n_aplicados

    def _mover_elemento_pagina_visual(self, archivo_path, idx_interno, direccion):
        """Reordena un elemento de la pagina intercambiando el BLOQUE DE
        LINEAS completo (un elemento simple es 1 linea; un 'formulario' es
        varias) con el de su vecino inmediato -- nunca mezcla lineas de
        adentro de un formulario con las de afuera, porque siempre mueve
        el bloque entero de una."""
        idx_pagina, fin_pagina, _ = self._encontrar_primera_pagina_web()
        elementos = self._recolectar_elementos_pagina_visual(idx_pagina, fin_pagina)
        posiciones = {el["idx_interno"]: pos for pos, el in enumerate(elementos)}
        if idx_interno not in posiciones:
            raise SiPiError("El elemento que se intento mover ya no existe (el archivo pudo haber cambiado).")
        pos = posiciones[idx_interno]
        pos_vecino = pos - 1 if direccion == "arriba" else pos + 1
        if pos_vecino < 0 or pos_vecino >= len(elementos):
            return  # ya esta en la punta, no hay nada para hacer

        el_actual, el_vecino = elementos[pos], elementos[pos_vecino]
        with open(archivo_path, "r", encoding="utf-8") as f:
            lineas_archivo = f.read().split("\n")

        def _bloque(el):
            inicio = self.lineas[el["idx_interno"]][0] - 1
            fin = self.lineas[el["idx_fin_bloque"]][0] - 1
            return lineas_archivo[inicio:fin + 1]

        primero, segundo = (el_actual, el_vecino) if pos < pos_vecino else (el_vecino, el_actual)
        bloque_primero, bloque_segundo = _bloque(primero), _bloque(segundo)
        inicio_primero = self.lineas[primero["idx_interno"]][0] - 1
        fin_segundo = self.lineas[segundo["idx_fin_bloque"]][0] - 1
        lineas_archivo[inicio_primero:fin_segundo + 1] = bloque_segundo + bloque_primero

        with open(archivo_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_archivo))
        self._invalidar_cache_bytecode_si_existe()
        # self.lineas queda desactualizado despues de un movimiento (los
        # numeros de linea de todo lo que sigue cambiaron); se vuelve a
        # cargar completo para que la proxima operacion parta de datos
        # correctos, en vez de ir arrastrando un desfasaje.
        self.cargar()
        print(f"[SiPi] Editor Visual: elemento movido hacia {direccion}.")

    def _invalidar_cache_bytecode_si_existe(self):
        ruta_cache = self._ruta_cache_bytecode()
        if os.path.exists(ruta_cache):
            os.remove(ruta_cache)

    def _encontrar_primera_ventana(self):
        for idx, (_, cruda) in enumerate(self.lineas):
            m = _m(r'^ventana\s+"([^"]*)"\s+(\d+)\s+(\d+)$', cruda.strip())
            if m:
                fin_v = self._encontrar_fin(idx, BLOQUES_QUE_ABREN)
                return idx, fin_v, m.group(1), int(m.group(2)), int(m.group(3))
        return None

    def _encontrar_primer_juego(self):
        for idx, (_, cruda) in enumerate(self.lineas):
            m = _m(r'^crear_juego\s+"([^"]*)"\s+(\d+)\s+(\d+)$', cruda.strip())
            if m:
                fin_j = self._encontrar_fin(idx, BLOQUES_QUE_ABREN)
                return idx, fin_j, m.group(1), int(m.group(2)), int(m.group(3))
        return None

    _PATRON_SPRITE_VISUAL = re.compile(
        r'^(?P<nombre>[\w\u0900-\u097F\u0980-\u09FF]+)\s+(?P<x>\S+)\s+(?P<y>\S+)\s+'
        r'(?P<w>\S+)\s+(?P<h>\S+)\s+(?P<color>"(?:[^"]*)"|\S+)$'
    )

    def _recolectar_sprites_visuales(self, idx_juego, fin_juego):
        """Igual en espiritu a _recolectar_widgets_visuales pero para los
        'sprite nombre x y w h color' dentro de un bloque 'crear_juego'.
        Nombre y color siempre son editables desde el visual (tocar el
        sprite y escribir un nombre nuevo, o abrir el selector de color);
        posicion solo si x/y son literales numericos, igual que en las
        ventanas -- para no romper logica dinamica (sprites posicionados
        con una variable/formula)."""
        sprites = []
        for idx in range(idx_juego + 1, fin_juego):
            num_linea, cruda = self.lineas[idx]
            limpia = cruda.strip()
            partes = limpia.split(" ", 1)
            if partes[0] != "sprite" or len(partes) < 2:
                continue
            m = self._PATRON_SPRITE_VISUAL.match(partes[1])
            if not m:
                continue
            campos = m.groupdict()
            x_literal = campos["x"].lstrip("-").isdigit()
            y_literal = campos["y"].lstrip("-").isdigit()
            w_literal = campos["w"].isdigit()
            h_literal = campos["h"].isdigit()
            color_crudo = campos["color"].strip('"')
            sprites.append({
                "idx_interno": idx,
                "linea_archivo": num_linea,
                "campos": campos,
                "x": int(campos["x"]) if x_literal else 0,
                "y": int(campos["y"]) if y_literal else 0,
                "w": int(campos["w"]) if w_literal else 32,
                "h": int(campos["h"]) if h_literal else 32,
                "color": self._color_a_hex_web(color_crudo),
                "nombre": campos["nombre"],
                "editable_posicion": x_literal and y_literal,
            })
        return sprites

    def _color_a_hex_web(self, color_crudo):
        """Convierte un color de SiPi (nombre en español o ya un #hex) a un
        #hex valido para mostrarlo en un <input type=color> del navegador.
        Usa COLORES_ESPANOL (la misma tabla que usa el motor grafico real)
        como unica fuente de verdad, para que el color que se ve en el
        editor visual sea exactamente el mismo que se va a dibujar en el
        juego -- no una aproximacion separada que se pueda desincronizar."""
        color_crudo = color_crudo.strip()
        if color_crudo.startswith("#"):
            return color_crudo
        return COLORES_ESPANOL.get(color_crudo.lower(), "#999999")

    @staticmethod
    def _reconstruir_linea_sprite(campos, nuevo_x, nuevo_y, nuevo_nombre, nuevo_color_hex):
        # El color se guarda siempre como hex entre comillas: es valido en
        # SiPi (_texto_color acepta '#rrggbb') y preserva exactamente el
        # tono elegido en el selector de color del navegador, sin tener que
        # mapearlo de vuelta a un nombre en español con perdida de precision.
        return f'sprite {nuevo_nombre} {nuevo_x} {nuevo_y} {campos["w"]} {campos["h"]} "{nuevo_color_hex}"'

    def _recolectar_widgets_visuales(self, idx_ventana, fin_ventana):
        widgets = []
        for idx in range(idx_ventana + 1, fin_ventana):
            num_linea, cruda = self.lineas[idx]
            limpia = cruda.strip()
            partes = limpia.split(" ", 1)
            tipo = partes[0]
            patron = self._PATRONES_WIDGET_VISUAL.get(tipo)
            if not patron or len(partes) < 2:
                continue
            m = patron.match(partes[1])
            if not m:
                continue
            campos = m.groupdict()
            # Solo x/y literales (numeros) son editables arrastrando; si son
            # una expresion/variable, se muestran pero no se pueden mover
            # desde el visual todavia (evita romper logica dinamica).
            x_literal = campos.get("x", "").isdigit()
            y_literal = campos.get("y", "").isdigit()
            widgets.append({
                "idx_interno": idx,
                "linea_archivo": num_linea,
                "tipo": tipo,
                "campos": campos,
                "x": int(campos["x"]) if x_literal else 0,
                "y": int(campos["y"]) if y_literal else 0,
                "editable_posicion": x_literal and y_literal,
                "linea_original": limpia,
            })
        return widgets

    @staticmethod
    def _reconstruir_linea_widget(tipo, campos, nuevo_x, nuevo_y, nuevo_texto):
        """Reconstruye la linea de codigo de un widget con nueva posicion
        y/o texto, preservando todo lo demas (funcion del boton, color del
        cuadro, ruta de la imagen, variable de la entrada) tal cual estaba."""
        if tipo == "etiqueta":
            return f'etiqueta {nuevo_texto} {nuevo_x} {nuevo_y}'
        if tipo == "boton":
            return f'boton {nuevo_texto} {nuevo_x} {nuevo_y} {campos["accion"]}'
        if tipo == "entrada":
            return f'entrada {campos["var"]} {nuevo_x} {nuevo_y}'
        if tipo == "cuadro":
            return f'cuadro {nuevo_x} {nuevo_y} {campos["ancho"]} {campos["alto"]} {campos["color"]}'
        if tipo == "imagen":
            extra = f' {campos["ancho"]} {campos["alto"]}' if campos.get("ancho") else ""
            return f'imagen {nuevo_texto} {nuevo_x} {nuevo_y}{extra}'
        raise SiPiError(f"Tipo de widget visual no reconocido: {tipo}")

    def _html_editor_visual(self, titulo_ventana, ancho_v, alto_v, widgets):
        piezas_widgets = []
        for w in widgets:
            tipo, campos = w["tipo"], w["campos"]
            texto_mostrado = ""
            editable_texto = False
            estilo_extra = ""
            if tipo == "etiqueta":
                texto_mostrado = self._texto_o_variable(campos["texto"]) if campos["texto"].startswith('"') else campos["texto"]
                editable_texto = True
                estilo_extra = "color:#eee;font-family:'Segoe UI',sans-serif;font-size:14px;"
            elif tipo == "boton":
                texto_mostrado = self._texto_o_variable(campos["texto"]) if campos["texto"].startswith('"') else campos["texto"]
                editable_texto = True
                estilo_extra = ("background:#4a4a6a;color:#fff;border:1px solid #666;border-radius:6px;"
                                 "padding:6px 14px;font-family:'Segoe UI',sans-serif;font-size:14px;cursor:move;")
            elif tipo == "entrada":
                texto_mostrado = f'[{campos["var"]}]'
                estilo_extra = "background:#fff;border:1px solid #999;padding:4px 8px;min-width:120px;font-family:monospace;"
            elif tipo == "cuadro":
                color = campos["color"].strip('"')
                ancho, alto = campos.get("ancho", "60"), campos.get("alto", "40")
                estilo_extra = f"background:{color};width:{ancho}px;height:{alto}px;border:1px dashed #888;"
            elif tipo == "imagen":
                ruta = campos["ruta"].strip('"')
                ancho = campos.get("ancho") or "80"
                alto = campos.get("alto") or "80"
                estilo_extra = (f"width:{ancho}px;height:{alto}px;background:#333 center/cover no-repeat "
                                 f"url('/__sipi_imagen__?ruta={urllib.parse.quote(ruta)}');"
                                 "border:1px solid #555;color:#aaa;font-size:11px;display:flex;"
                                 "align-items:center;justify-content:center;text-align:center;")
                texto_mostrado = ruta

            piezas_widgets.append(f'''
      <div class="sipi-widget" data-idx="{w["idx_interno"]}" data-tipo="{tipo}"
           data-editable-pos="{"1" if w["editable_posicion"] else "0"}"
           data-editable-texto="{"1" if editable_texto else "0"}"
           style="position:absolute;left:{w["x"]}px;top:{w["y"]}px;{estilo_extra}"
           {"contenteditable-holder" if editable_texto else ""}>
        <span class="sipi-texto" {"contenteditable" if editable_texto else ""}
              spellcheck="false">{texto_mostrado if texto_mostrado else "&nbsp;"}</span>
      </div>''')

        return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>SiPi Visual - {titulo_ventana}</title>
<style>
  body {{ margin:0; background:#111; color:#eee; font-family:'Segoe UI',sans-serif; }}
  #barra {{ padding:10px 16px; background:#1a1a2a; display:flex; align-items:center; gap:12px; }}
  #barra h1 {{ font-size:15px; margin:0; font-weight:600; }}
  #barra span {{ font-size:12px; color:#9a9ac0; }}
  button#guardar {{ background:#5865f2; color:#fff; border:none; padding:8px 18px; border-radius:6px;
                     font-size:13px; cursor:pointer; margin-left:auto; }}
  button#guardar:hover {{ background:#4752c4; }}
  #lienzo {{ position:relative; margin:20px; background:#1e1e2e; border:1px solid #333;
             width:{ancho_v}px; height:{alto_v}px; box-shadow:0 4px 24px rgba(0,0,0,.4); }}
  .sipi-widget {{ user-select:none; }}
  .sipi-widget[data-editable-pos="1"] {{ cursor:move; }}
  .sipi-widget.arrastrando {{ opacity:.8; outline:2px solid #5865f2; }}
  .sipi-texto[contenteditable="true"]:focus {{ outline:2px solid #f2c05e; background:rgba(255,255,255,.08); }}
  #estado {{ position:fixed; bottom:14px; right:16px; font-size:12px; color:#8f8; }}
</style>
</head>
<body>
  <div id="barra">
    <h1>Editor Visual de SiPi &mdash; {titulo_ventana}</h1>
    <span>Arrastra para mover &middot; Doble click para editar texto</span>
    <button id="guardar">Guardar cambios</button>
  </div>
  <div id="lienzo">{"".join(piezas_widgets)}</div>
  <div id="estado"></div>
<script>
let activo = null, offX = 0, offY = 0;

document.querySelectorAll('.sipi-widget[data-editable-pos="1"]').forEach(el => {{
  el.addEventListener('mousedown', e => {{
    if (e.target.isContentEditable) return;
    activo = el;
    const r = el.getBoundingClientRect();
    offX = e.clientX - r.left;
    offY = e.clientY - r.top;
    el.classList.add('arrastrando');
    e.preventDefault();
  }});
}});

document.addEventListener('mousemove', e => {{
  if (!activo) return;
  const lienzo = document.getElementById('lienzo').getBoundingClientRect();
  let x = e.clientX - lienzo.left - offX;
  let y = e.clientY - lienzo.top - offY;
  x = Math.max(0, Math.round(x));
  y = Math.max(0, Math.round(y));
  activo.style.left = x + 'px';
  activo.style.top = y + 'px';
}});

document.addEventListener('mouseup', () => {{
  if (activo) activo.classList.remove('arrastrando');
  activo = null;
}});

document.getElementById('guardar').addEventListener('click', async () => {{
  const cambios = [];
  document.querySelectorAll('.sipi-widget').forEach(el => {{
    const span = el.querySelector('.sipi-texto');
    cambios.push({{
      idx: parseInt(el.dataset.idx, 10),
      x: parseInt(el.style.left, 10) || 0,
      y: parseInt(el.style.top, 10) || 0,
      texto: span ? span.innerText : "",
    }});
  }});
  const estado = document.getElementById('estado');
  estado.textContent = 'Guardando...';
  try {{
    const resp = await fetch('/__sipi_guardar__', {{
      method: 'POST', headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify(cambios),
    }});
    const datos = await resp.json();
    estado.textContent = datos.ok ? ('Guardado: ' + datos.cambios + ' widget(s) actualizados en el .sipi') : ('Error: ' + datos.error);
  }} catch (err) {{
    estado.textContent = 'No se pudo conectar con SiPi: ' + err;
  }}
}});
</script>
</body>
</html>'''

    def _html_editor_visual_juego(self, titulo_juego, ancho_j, alto_j, sprites):
        """Igual en espiritu a _html_editor_visual (ventanas) pero para
        sprites de un 'crear_juego': arrastrar para mover, tocar el nombre
        para renombrarlo, y un selector de color nativo del navegador para
        cambiar el color -- todo se escribe de vuelta en la linea 'sprite'
        exacta del .sipi al tocar 'Guardar cambios', sin tocar el resto del
        archivo (logica del juego, otros sprites, comentarios)."""
        piezas = []
        for s in sprites:
            piezas.append(f'''
      <div class="sipi-sprite" data-idx="{s["idx_interno"]}"
           data-editable-pos="{"1" if s["editable_posicion"] else "0"}"
           style="position:absolute;left:{s["x"]}px;top:{s["y"]}px;width:{s["w"]}px;height:{s["h"]}px;
                  background:{s["color"]};border:1px solid rgba(255,255,255,.35);box-sizing:border-box;">
        <input class="sipi-color" type="color" value="{s["color"]}" title="Cambiar color">
        <span class="sipi-nombre" contenteditable spellcheck="false">{s["nombre"]}</span>
      </div>''')

        return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>SiPi Visual (Juego) - {titulo_juego}</title>
<style>
  body {{ margin:0; background:#111; color:#eee; font-family:'Segoe UI',sans-serif; }}
  #barra {{ padding:10px 16px; background:#1a1a2a; display:flex; align-items:center; gap:12px; }}
  #barra h1 {{ font-size:15px; margin:0; font-weight:600; }}
  #barra span {{ font-size:12px; color:#9a9ac0; }}
  button#guardar {{ background:#5865f2; color:#fff; border:none; padding:8px 18px; border-radius:6px;
                     font-size:13px; cursor:pointer; margin-left:auto; }}
  button#guardar:hover {{ background:#4752c4; }}
  #lienzo {{ position:relative; margin:20px; background:#0b0b14 repeating-linear-gradient(
             0deg, rgba(255,255,255,.04) 0 1px, transparent 1px 32px),
             repeating-linear-gradient(90deg, rgba(255,255,255,.04) 0 1px, transparent 1px 32px);
             border:1px solid #333; width:{ancho_j}px; height:{alto_j}px; box-shadow:0 4px 24px rgba(0,0,0,.4); }}
  .sipi-sprite {{ user-select:none; display:flex; align-items:center; justify-content:center; }}
  .sipi-sprite[data-editable-pos="1"] {{ cursor:move; }}
  .sipi-sprite.arrastrando {{ opacity:.8; outline:2px solid #f2c05e; z-index:5; }}
  .sipi-color {{ position:absolute; top:-10px; left:-10px; width:18px; height:18px; padding:0;
                 border:2px solid #111; border-radius:50%; cursor:pointer; }}
  .sipi-nombre {{ font-size:11px; text-shadow:0 1px 2px #000; pointer-events:auto; padding:1px 3px;
                   background:rgba(0,0,0,.35); border-radius:3px; white-space:nowrap; }}
  .sipi-nombre:focus {{ outline:2px solid #f2c05e; background:rgba(0,0,0,.6); }}
  #estado {{ position:fixed; bottom:14px; right:16px; font-size:12px; color:#8f8; }}
</style>
</head>
<body>
  <div id="barra">
    <h1>Editor Visual de SiPi (Juego) &mdash; {titulo_juego}</h1>
    <span>Arrastra un sprite para moverlo &middot; toca el nombre para renombrarlo &middot; el circulo cambia el color</span>
    <button id="guardar">Guardar cambios</button>
  </div>
  <div id="lienzo">{"".join(piezas)}</div>
  <div id="estado"></div>
<script>
let activo = null, offX = 0, offY = 0;

document.querySelectorAll('.sipi-sprite[data-editable-pos="1"]').forEach(el => {{
  el.addEventListener('mousedown', e => {{
    if (e.target.isContentEditable || e.target.classList.contains('sipi-color')) return;
    activo = el;
    const r = el.getBoundingClientRect();
    offX = e.clientX - r.left;
    offY = e.clientY - r.top;
    el.classList.add('arrastrando');
    e.preventDefault();
  }});
}});

document.addEventListener('mousemove', e => {{
  if (!activo) return;
  const lienzo = document.getElementById('lienzo').getBoundingClientRect();
  let x = e.clientX - lienzo.left - offX;
  let y = e.clientY - lienzo.top - offY;
  x = Math.max(0, Math.round(x));
  y = Math.max(0, Math.round(y));
  activo.style.left = x + 'px';
  activo.style.top = y + 'px';
}});

document.addEventListener('mouseup', () => {{
  if (activo) activo.classList.remove('arrastrando');
  activo = null;
}});

document.getElementById('guardar').addEventListener('click', async () => {{
  const cambios = [];
  document.querySelectorAll('.sipi-sprite').forEach(el => {{
    const nombre = el.querySelector('.sipi-nombre');
    const color = el.querySelector('.sipi-color');
    cambios.push({{
      idx: parseInt(el.dataset.idx, 10),
      x: parseInt(el.style.left, 10) || 0,
      y: parseInt(el.style.top, 10) || 0,
      nombre: nombre ? nombre.innerText.trim() : "sprite",
      color: color ? color.value : "#999999",
    }});
  }});
  const estado = document.getElementById('estado');
  estado.textContent = 'Guardando...';
  try {{
    const resp = await fetch('/__sipi_guardar_juego__', {{
      method: 'POST', headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify(cambios),
    }});
    const datos = await resp.json();
    estado.textContent = datos.ok ? ('Guardado: ' + datos.cambios + ' sprite(s) actualizados en el .sipi') : ('Error: ' + datos.error);
  }} catch (err) {{
    estado.textContent = 'No se pudo conectar con SiPi: ' + err;
  }}
}});
</script>
</body>
</html>'''


        """Escribe un log en formato JSON Lines (un objeto JSON valido por
        renglon) a 'sipi.log', ademas de imprimirlo en pantalla. JSON Lines
        es el formato que entienden de forma nativa las herramientas de
        monitoreo reales (Datadog, CloudWatch, Grafana Loki, ELK/Logstash),
        asi que estos logs se pueden conectar directo a un sistema de
        observabilidad de produccion sin escribir ningun parser."""
        entrada = {
            "timestamp": datetime.datetime.now().isoformat(),
            "nivel": nivel,
            "mensaje": mensaje,
            "programa": os.path.basename(self.archivo_path),
        }
        linea_json = json.dumps(entrada, ensure_ascii=False)
        ruta_log = os.path.join(self.base_dir, "sipi.log")
        try:
            with open(ruta_log, "a", encoding="utf-8") as f:
                f.write(linea_json + "\n")
        except OSError:
            pass  # si no se puede escribir a disco (ej. filesystem de solo lectura en un contenedor), no frenar el programa por eso
        prefijo = {"info": "[INFO]", "advertencia": "[ADVERTENCIA]", "error": "[ERROR]"}.get(nivel, f"[{nivel.upper()}]")
        print(f"[SiPi] {prefijo} {mensaje}")

    def _generar_dockerfile(self, nombre_app):
        """Genera un Dockerfile real y funcional para empaquetar CUALQUIER
        programa SiPi (no solo APIs web) en un contenedor Docker estandar
        -- la forma en la que la enorme mayoria de empresas despliega
        software hoy, sin importar la nube que usen (AWS, GCP, Azure, su
        propio datacenter, Kubernetes, lo que sea). A diferencia de
        'publicar_nube' (atado a un proveedor especifico), esto corre en
        cualquier lugar que entienda Docker."""
        carpeta = os.path.join(self.base_dir, f"{nombre_app}_docker")
        os.makedirs(carpeta, exist_ok=True)

        nombre_programa_sipi = os.path.basename(self.archivo_path)
        shutil.copy(self.archivo_path, os.path.join(carpeta, nombre_programa_sipi))
        shutil.copy(os.path.abspath(__file__), os.path.join(carpeta, "sipi_motor.py"))

        dockerfile = f'''# Generado automaticamente por SiPi (generar_dockerfile).
# Imagen base liviana de Python (SiPi no tiene dependencias externas).
FROM python:3.12-slim

WORKDIR /app

COPY sipi_motor.py .
COPY {nombre_programa_sipi} .

# Variables de entorno que el programa puede leer con 'variable_entorno'.
# Se pueden sobreescribir al correr el contenedor con -e NOMBRE=valor,
# o en un docker-compose.yml / manifiesto de Kubernetes.
ENV SIPI_ENTORNO=produccion

# Si el programa usa 'iniciar_api_web', expone el puerto tipico.
EXPOSE 8000

# Verificacion de salud real: Docker/Kubernetes van a poder reiniciar el
# contenedor automaticamente si el programa deja de responder.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \\
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/salud', timeout=3)" || exit 1

CMD ["python3", "sipi_motor.py", "{nombre_programa_sipi}"]
'''
        with open(os.path.join(carpeta, "Dockerfile"), "w", encoding="utf-8") as f:
            f.write(dockerfile)

        dockerignore = "__pycache__/\n*.sipic\n*.log\n.git/\n"
        with open(os.path.join(carpeta, ".dockerignore"), "w", encoding="utf-8") as f:
            f.write(dockerignore)

        compose = f'''# docker-compose.yml generado por SiPi. Uso: docker compose up
services:
  {re.sub(r"[^a-z0-9_-]", "", nombre_app.lower().replace(" ", "_"))}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SIPI_ENTORNO=produccion
    restart: unless-stopped
'''
        with open(os.path.join(carpeta, "docker-compose.yml"), "w", encoding="utf-8") as f:
            f.write(compose)

        instrucciones = f'''CONTENEDOR DOCKER: {nombre_app}
Generado por SiPi - listo para desplegar en cualquier infraestructura.

Esta carpeta contiene:
  - {nombre_programa_sipi}    -> tu programa real
  - sipi_motor.py             -> el motor de SiPi embebido (no hace falta instalar nada mas)
  - Dockerfile                -> imagen lista para construir
  - docker-compose.yml        -> para levantarlo con un solo comando
  - .dockerignore

COMO USARLO:
  cd {nombre_app}_docker
  docker build -t {nombre_app.lower().replace(" ", "_")} .
  docker run -p 8000:8000 {nombre_app.lower().replace(" ", "_")}

  (o mas facil todavia: docker compose up)

Esto corre igual en tu maquina, en un servidor propio, en Kubernetes, o en
cualquier nube (AWS ECS/Fargate, Google Cloud Run, Azure Container Apps,
etc.) -- Docker es el estandar que todas entienden.
'''
        with open(os.path.join(carpeta, "LEEME.txt"), "w", encoding="utf-8") as f:
            f.write(instrucciones)

        print(f"[SiPi] Contenedor Docker generado en: {carpeta}")
        print("[SiPi] Lee LEEME.txt dentro de esa carpeta para construir y correr la imagen.")

    def _evaluar_fortaleza_contrasena(self, clave):
        """Puntaje de 0 a 100 evaluando una contrasena por criterios reales
        (longitud, variedad de caracteres, patrones obvios) -- la misma
        logica de fondo que usan los medidores de fortaleza de contrasena
        de verdad. Es una herramienta DEFENSIVA (ayuda a elegir mejores
        contrasenas / a que un sistema las rechace si son debiles), no
        ofensiva."""
        if not clave:
            return 0
        puntaje = 0
        largo = len(clave)
        puntaje += min(largo * 4, 40)
        tiene_minuscula = any(c.islower() for c in clave)
        tiene_mayuscula = any(c.isupper() for c in clave)
        tiene_digito = any(c.isdigit() for c in clave)
        tiene_simbolo = any(not c.isalnum() for c in clave)
        variedad = sum([tiene_minuscula, tiene_mayuscula, tiene_digito, tiene_simbolo])
        puntaje += variedad * 10

        clave_min = clave.lower()
        patrones_debiles = ["12345", "qwerty", "password", "contraseña", "abc123", "admin", "111111"]
        if any(patron in clave_min for patron in patrones_debiles):
            puntaje -= 30
        if largo >= 3 and len(set(clave)) == 1:  # todo el mismo caracter repetido
            puntaje -= 30
        secuencial = any(
            ord(clave_min[i + 1]) - ord(clave_min[i]) == 1 and ord(clave_min[i + 2]) - ord(clave_min[i + 1]) == 1
            for i in range(len(clave_min) - 2) if clave_min[i:i + 3].isalnum()
        )
        if secuencial:
            puntaje -= 15

        return max(0, min(100, puntaje))

    def _lanzar_editor_visual(self):
        encontrado = self._encontrar_primera_ventana()
        if encontrado is not None:
            idx_ventana, fin_ventana, titulo_ventana, ancho_v, alto_v = encontrado
            widgets = self._recolectar_widgets_visuales(idx_ventana, fin_ventana)
            html = self._html_editor_visual(titulo_ventana, ancho_v, alto_v, widgets)
            self._servir_editor_visual(html, modo="ventana")
            return

        encontrado_web = self._encontrar_primera_pagina_web()
        if encontrado_web is not None:
            idx_pagina, fin_pagina, titulo_pagina = encontrado_web
            elementos = self._recolectar_elementos_pagina_visual(idx_pagina, fin_pagina)
            html = self._html_editor_visual_web(titulo_pagina, elementos)
            self._servir_editor_visual(html, modo="pagina_web")
            return

        encontrado_juego = self._encontrar_primer_juego()
        if encontrado_juego is not None:
            idx_juego, fin_juego, titulo_juego, ancho_j, alto_j = encontrado_juego
            sprites = self._recolectar_sprites_visuales(idx_juego, fin_juego)
            html = self._html_editor_visual_juego(titulo_juego, ancho_j, alto_j, sprites)
            self._servir_editor_visual(html, modo="juego")
            return

        print("[SiPi] No se encontro ningun bloque 'ventana', 'pagina_web' ni 'crear_juego' en este programa. "
              "El editor Visual por ahora funciona sobre esos tres (mas tipos de UI se iran agregando).")

    def _servir_editor_visual(self, html, modo):
        interprete_self = self
        archivo_path = self.archivo_path
        base_dir = self.base_dir

        class ManejadorVisual(http.server.BaseHTTPRequestHandler):
            def log_message(self, formato, *args):
                pass  # silenciar el log por defecto, ya imprimimos lo relevante nosotros

            def do_GET(self):
                if self.path == "/" or self.path == "":
                    if modo == "pagina_web":
                        # A diferencia de la ventana (HTML fijo armado una
                        # sola vez), la pagina web se vuelve a renderizar en
                        # cada visita, para reflejar reordenamientos que ya
                        # se guardaron en el archivo.
                        idx_pagina, fin_pagina, titulo_pagina = interprete_self._encontrar_primera_pagina_web()
                        elementos = interprete_self._recolectar_elementos_pagina_visual(idx_pagina, fin_pagina)
                        cuerpo = interprete_self._html_editor_visual_web(titulo_pagina, elementos).encode("utf-8")
                    else:
                        cuerpo = html.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(cuerpo)))
                    self.end_headers()
                    self.wfile.write(cuerpo)
                elif self.path.startswith("/__sipi_imagen__?"):
                    qs = urllib.parse.parse_qs(self.path.split("?", 1)[1])
                    ruta = qs.get("ruta", [""])[0]
                    ruta_completa = os.path.join(base_dir, ruta)
                    if os.path.exists(ruta_completa):
                        with open(ruta_completa, "rb") as f:
                            datos = f.read()
                        self.send_response(200)
                        self.send_header("Content-Type", "application/octet-stream")
                        self.send_header("Content-Length", str(len(datos)))
                        self.end_headers()
                        self.wfile.write(datos)
                    else:
                        self.send_response(404)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()

            def _responder_json(self, codigo, datos):
                respuesta = json.dumps(datos, ensure_ascii=False).encode("utf-8")
                self.send_response(codigo)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(respuesta)))
                self.end_headers()
                self.wfile.write(respuesta)

            def do_POST(self):
                largo = int(self.headers.get("Content-Length", 0))
                cuerpo_pedido = self.rfile.read(largo).decode("utf-8") if largo else "{}"
                try:
                    if self.path == "/__sipi_guardar__":
                        cambios = json.loads(cuerpo_pedido)
                        n_cambios = interprete_self._aplicar_cambios_editor_visual(archivo_path, cambios)
                        self._responder_json(200, {"ok": True, "cambios": n_cambios})
                    elif self.path == "/__sipi_guardar_web__":
                        cambios = json.loads(cuerpo_pedido)
                        n_cambios = interprete_self._aplicar_cambios_editor_visual_web(archivo_path, cambios)
                        self._responder_json(200, {"ok": True, "cambios": n_cambios})
                    elif self.path == "/__sipi_mover_web__":
                        datos = json.loads(cuerpo_pedido)
                        interprete_self._mover_elemento_pagina_visual(archivo_path, datos["idx"], datos["direccion"])
                        self._responder_json(200, {"ok": True})
                    elif self.path == "/__sipi_guardar_juego__":
                        cambios = json.loads(cuerpo_pedido)
                        n_cambios = interprete_self._aplicar_cambios_editor_visual_juego(archivo_path, cambios)
                        self._responder_json(200, {"ok": True, "cambios": n_cambios})
                    else:
                        self.send_response(404)
                        self.end_headers()
                except Exception as e:
                    self._responder_json(500, {"ok": False, "error": str(e)})

        servidor = socketserver.TCPServer(("127.0.0.1", 0), ManejadorVisual)
        puerto = servidor.server_address[1]
        url = f"http://127.0.0.1:{puerto}/"
        print(f"[SiPi] Editor Visual abierto en: {url}")
        print("[SiPi] Arrastra los widgets con el mouse, doble click para editar el texto, "
              "y toca 'Guardar cambios' para escribirlo de vuelta en tu .sipi.")
        print("[SiPi] Deja esta ventana de SiPi abierta mientras edites. Presiona Ctrl+C para cerrar el editor.")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\n[SiPi] Editor Visual cerrado.")
        finally:
            servidor.server_close()

    def _aplicar_cambios_editor_visual(self, archivo_path, cambios):
        """Aplica los cambios que mando el editor Visual (posicion nueva y
        texto nuevo de cada widget) directamente sobre el archivo .sipi de
        origen, reescribiendo SOLO esas lineas exactas. El resto del
        archivo (logica, funciones, comentarios, formato) no se toca."""
        with open(archivo_path, "r", encoding="utf-8") as f:
            lineas_archivo = f.read().split("\n")

        n_aplicados = 0
        for cambio in cambios:
            idx_interno = cambio.get("idx")
            if idx_interno is None or idx_interno >= len(self.lineas):
                continue
            num_linea, cruda = self.lineas[idx_interno]
            limpia = cruda.strip()
            partes = limpia.split(" ", 1)
            tipo = partes[0]
            patron = self._PATRONES_WIDGET_VISUAL.get(tipo)
            if not patron or len(partes) < 2:
                continue
            m = patron.match(partes[1])
            if not m:
                continue
            campos = m.groupdict()

            nuevo_texto_crudo = cambio.get("texto", "")
            if tipo in ("etiqueta", "boton"):
                # Si el original era un literal entre comillas, el nuevo
                # texto tambien se guarda como literal (lo tipico); si el
                # original era una variable suelta (sin comillas), se
                # respeta esa forma y no se convierte en texto fijo.
                if campos["texto"].startswith('"'):
                    nuevo_texto = '"' + nuevo_texto_crudo.replace('"', '\\"') + '"'
                else:
                    nuevo_texto = campos["texto"]
            elif tipo == "imagen":
                nuevo_texto = campos["ruta"]
            else:
                nuevo_texto = ""

            x_nuevo = cambio.get("x", campos.get("x", 0))
            y_nuevo = cambio.get("y", campos.get("y", 0))
            linea_nueva = self._reconstruir_linea_widget(tipo, campos, x_nuevo, y_nuevo, nuevo_texto)

            # Preservar la indentacion original de la linea en el archivo.
            # self.lineas guarda el texto YA SIN indentar (se limpia en el
            # preprocesamiento), asi que la indentacion real hay que
            # sacarla de la linea tal cual esta todavia en el archivo.
            idx_en_archivo = num_linea - 1
            if 0 <= idx_en_archivo < len(lineas_archivo):
                linea_archivo_actual = lineas_archivo[idx_en_archivo]
                indentacion = linea_archivo_actual[:len(linea_archivo_actual) - len(linea_archivo_actual.lstrip())]
                lineas_archivo[idx_en_archivo] = indentacion + linea_nueva
                self.lineas[idx_interno] = (num_linea, linea_nueva)
                n_aplicados += 1

        with open(archivo_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_archivo))

        # El .sipic (cache de bytecode) queda desactualizado respecto al
        # archivo que se acaba de reescribir; se borra para que la proxima
        # ejecucion vuelva a parsear el .sipi real en vez de servir la
        # version vieja cacheada.
        ruta_cache = self._ruta_cache_bytecode()
        if os.path.exists(ruta_cache):
            os.remove(ruta_cache)

        print(f"[SiPi] Editor Visual: {n_aplicados} widget(s) actualizados en {os.path.basename(archivo_path)}")
        return n_aplicados

    def _aplicar_cambios_editor_visual_juego(self, archivo_path, cambios):
        """Version para sprites de _aplicar_cambios_editor_visual: reescribe
        SOLO las lineas 'sprite ...' que cambiaron (posicion/nombre/color),
        preservando indentacion y el resto del archivo intacto."""
        with open(archivo_path, "r", encoding="utf-8") as f:
            lineas_archivo = f.read().split("\n")

        n_aplicados = 0
        for cambio in cambios:
            idx_interno = cambio.get("idx")
            if idx_interno is None or idx_interno >= len(self.lineas):
                continue
            num_linea, cruda = self.lineas[idx_interno]
            limpia = cruda.strip()
            partes = limpia.split(" ", 1)
            if partes[0] != "sprite" or len(partes) < 2:
                continue
            m = self._PATRON_SPRITE_VISUAL.match(partes[1])
            if not m:
                continue
            campos = m.groupdict()

            x_nuevo = cambio.get("x", campos.get("x", 0))
            y_nuevo = cambio.get("y", campos.get("y", 0))
            nombre_nuevo = cambio.get("nombre") or campos["nombre"]
            # Un nombre de sprite es un identificador, no texto libre: si
            # el navegador mando algo con espacios/simbolos raros, se
            # sanitiza para no romper el parser en la proxima ejecucion.
            nombre_nuevo = re.sub(r"[^\wÀ-ÿ]", "_", nombre_nuevo.strip()) or campos["nombre"]
            color_nuevo = cambio.get("color") or self._color_a_hex_web(campos["color"].strip('"'))
            linea_nueva = self._reconstruir_linea_sprite(campos, x_nuevo, y_nuevo, nombre_nuevo, color_nuevo)

            idx_en_archivo = num_linea - 1
            if 0 <= idx_en_archivo < len(lineas_archivo):
                linea_archivo_actual = lineas_archivo[idx_en_archivo]
                indentacion = linea_archivo_actual[:len(linea_archivo_actual) - len(linea_archivo_actual.lstrip())]
                lineas_archivo[idx_en_archivo] = indentacion + linea_nueva
                self.lineas[idx_interno] = (num_linea, linea_nueva)
                n_aplicados += 1

        with open(archivo_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_archivo))

        ruta_cache = self._ruta_cache_bytecode()
        if os.path.exists(ruta_cache):
            os.remove(ruta_cache)

        print(f"[SiPi] Editor Visual: {n_aplicados} sprite(s) actualizados en {os.path.basename(archivo_path)}")
        return n_aplicados

    # ---------- Helpers genericos de base de datos (SQLite/Postgres/MySQL, con o sin pool) ----------

    def _resolver_conexion_bd(self, alias):
        """Devuelve (motor, ejecutar_fn, consultar_fn) para cualquier alias
        de conexion ya abierto, sin importar si es SQLite (conexion cruda),
        o Postgres/MySQL (con o sin pool). Centraliza en un solo lugar la
        logica de 'como se habla con esta conexion', para que las
        migraciones (y cualquier otra cosa futura que necesite ser
        agnostica al motor) no tengan que repetirla."""
        if alias not in self.entorno.conexiones_sqlite:
            raise SiPiError(f"No hay ninguna conexion abierta llamada '{alias}'.")
        guardado = self.entorno.conexiones_sqlite[alias]

        if not isinstance(guardado, tuple):
            # SQLite: conexion cruda (sqlite3.Connection).
            conexion = guardado

            def ejecutar(sql):
                conexion.execute(sql)
                conexion.commit()

            def consultar(sql):
                cursor = conexion.execute(sql)
                return [dict(fila) for fila in cursor.fetchall()]

            return "sqlite", ejecutar, consultar

        motor, recurso = guardado
        es_pool = motor.endswith("_pool")

        def ejecutar(sql):
            conexion = recurso.obtener() if es_pool else recurso
            try:
                if motor.startswith("postgres"):
                    conexion.run(sql)
                else:
                    with conexion.cursor() as cursor:
                        cursor.execute(sql)
            finally:
                if es_pool:
                    recurso.liberar(conexion)

        def consultar(sql):
            conexion = recurso.obtener() if es_pool else recurso
            try:
                if motor.startswith("postgres"):
                    filas_crudas = conexion.run(sql)
                    columnas = [c["name"] for c in conexion.columns] if conexion.columns else []
                    return [dict(zip(columnas, fila)) for fila in filas_crudas]
                with conexion.cursor() as cursor:
                    cursor.execute(sql)
                    return list(cursor.fetchall())
            finally:
                if es_pool:
                    recurso.liberar(conexion)

        return motor, ejecutar, consultar

    # ---------- Migraciones de esquema versionadas ----------

    def _migracion_crear(self, carpeta, nombre_descriptivo):
        """Crea un archivo de migracion nuevo, numerado en orden (0001,
        0002, ...), con una plantilla que separa el SQL de 'subir' cambios
        del SQL para 'revertirlos'."""
        ruta_carpeta = os.path.join(self.base_dir, carpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)
        existentes = sorted(f for f in os.listdir(ruta_carpeta) if f.endswith(".sql"))
        siguiente_numero = 1
        if existentes:
            ultimo = existentes[-1]
            m = re.match(r"^(\d+)_", ultimo)
            if m:
                siguiente_numero = int(m.group(1)) + 1
        slug = re.sub(r"[^a-z0-9_]+", "_", nombre_descriptivo.lower()).strip("_")
        nombre_archivo = f"{siguiente_numero:04d}_{slug}.sql"
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        contenido = (
            f"-- Migracion: {nombre_descriptivo}\n"
            f"-- Creada por SiPi\n\n"
            f"-- ARRIBA\n"
            f"-- Escribi aca el SQL que aplica el cambio (ej. CREATE TABLE, ALTER TABLE...)\n\n\n"
            f"-- ABAJO\n"
            f"-- Escribi aca el SQL que deshace el cambio de arriba (ej. DROP TABLE...)\n\n"
        )
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"[SiPi] Migracion creada: {os.path.join(carpeta, nombre_archivo)}")

    @staticmethod
    def _leer_migracion(ruta_archivo):
        """Separa un archivo de migracion en (sql_arriba, sql_abajo)."""
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        m = re.search(r"--\s*ARRIBA\s*\n(.*?)(?:--\s*ABAJO\s*\n(.*))?$", contenido, re.DOTALL | re.IGNORECASE)
        if not m:
            raise SiPiError(f"El archivo de migracion '{ruta_archivo}' no tiene el formato esperado (falta '-- ARRIBA').")
        sql_arriba = (m.group(1) or "").strip()
        sql_abajo = (m.group(2) or "").strip()
        return sql_arriba, sql_abajo

    def _migracion_asegurar_tabla_control(self, ejecutar_fn, consultar_fn):
        try:
            ejecutar_fn(
                "CREATE TABLE IF NOT EXISTS _sipi_migraciones ("
                "nombre_archivo VARCHAR(255) PRIMARY KEY, "
                "aplicada_en VARCHAR(64))"
            )
        except Exception as e:
            raise SiPiError(f"No se pudo preparar la tabla de control de migraciones: {e}")

    def _migracion_aplicar(self, carpeta, alias):
        ruta_carpeta = os.path.join(self.base_dir, carpeta)
        if not os.path.isdir(ruta_carpeta):
            raise SiPiError(f"No existe la carpeta de migraciones '{carpeta}'.")
        archivos = sorted(f for f in os.listdir(ruta_carpeta) if f.endswith(".sql"))
        if not archivos:
            print(f"[SiPi] No hay migraciones en '{carpeta}'.")
            return

        motor, ejecutar, consultar = self._resolver_conexion_bd(alias)
        self._migracion_asegurar_tabla_control(ejecutar, consultar)
        aplicadas = {fila.get("nombre_archivo") or fila.get(0) for fila in consultar("SELECT nombre_archivo FROM _sipi_migraciones")}

        n_aplicadas = 0
        for nombre_archivo in archivos:
            if nombre_archivo in aplicadas:
                continue
            ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
            sql_arriba, _ = self._leer_migracion(ruta_archivo)
            if not sql_arriba:
                print(f"[SiPi] Aviso: '{nombre_archivo}' no tiene SQL en la seccion ARRIBA, se omite.")
                continue
            print(f"[SiPi] Aplicando migracion: {nombre_archivo}...")
            try:
                for sentencia in [s.strip() for s in sql_arriba.split(";") if s.strip()]:
                    ejecutar(sentencia)
                marca_tiempo = datetime.datetime.now().isoformat()
                ejecutar(f"INSERT INTO _sipi_migraciones (nombre_archivo, aplicada_en) VALUES ('{nombre_archivo}', '{marca_tiempo}')")
            except Exception as e:
                raise SiPiError(
                    f"Fallo la migracion '{nombre_archivo}': {e}\n"
                    f"       Las migraciones anteriores a esta ya quedaron aplicadas; arregla el SQL de esta "
                    f"migracion y volve a correr 'migracion_aplicar' (las ya aplicadas se saltean solas)."
                )
            n_aplicadas += 1

        if n_aplicadas == 0:
            print(f"[SiPi] Ya estaba todo aplicado en '{alias}' ({len(archivos)} migracion(es), ninguna pendiente).")
        else:
            print(f"[SiPi] {n_aplicadas} migracion(es) aplicadas en '{alias}'.")

    def _migracion_revertir(self, carpeta, alias):
        ruta_carpeta = os.path.join(self.base_dir, carpeta)
        motor, ejecutar, consultar = self._resolver_conexion_bd(alias)
        self._migracion_asegurar_tabla_control(ejecutar, consultar)
        filas = consultar("SELECT nombre_archivo FROM _sipi_migraciones ORDER BY nombre_archivo DESC")
        if not filas:
            print(f"[SiPi] No hay ninguna migracion aplicada en '{alias}' para revertir.")
            return
        nombre_archivo = filas[0].get("nombre_archivo") or filas[0].get(0)
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        if not os.path.exists(ruta_archivo):
            raise SiPiError(f"La migracion '{nombre_archivo}' esta registrada como aplicada, pero el archivo ya no existe en '{carpeta}'.")
        _, sql_abajo = self._leer_migracion(ruta_archivo)
        if not sql_abajo:
            raise SiPiError(f"La migracion '{nombre_archivo}' no tiene SQL en la seccion ABAJO, no se puede revertir automaticamente.")
        print(f"[SiPi] Revirtiendo migracion: {nombre_archivo}...")
        try:
            for sentencia in [s.strip() for s in sql_abajo.split(";") if s.strip()]:
                ejecutar(sentencia)
            ejecutar(f"DELETE FROM _sipi_migraciones WHERE nombre_archivo = '{nombre_archivo}'")
        except Exception as e:
            raise SiPiError(f"Fallo al revertir '{nombre_archivo}': {e}")
        print(f"[SiPi] Migracion '{nombre_archivo}' revertida en '{alias}'.")

    def _migracion_estado(self, carpeta, alias):
        ruta_carpeta = os.path.join(self.base_dir, carpeta)
        if not os.path.isdir(ruta_carpeta):
            raise SiPiError(f"No existe la carpeta de migraciones '{carpeta}'.")
        archivos = sorted(f for f in os.listdir(ruta_carpeta) if f.endswith(".sql"))
        motor, ejecutar, consultar = self._resolver_conexion_bd(alias)
        self._migracion_asegurar_tabla_control(ejecutar, consultar)
        aplicadas = {fila.get("nombre_archivo") or fila.get(0) for fila in consultar("SELECT nombre_archivo FROM _sipi_migraciones")}
        print(f"[SiPi] Estado de migraciones en '{alias}' ({motor}):")
        for nombre_archivo in archivos:
            marca = "✓ aplicada" if nombre_archivo in aplicadas else "  pendiente"
            print(f"  [{marca}] {nombre_archivo}")
        if not archivos:
            print("  (no hay archivos de migracion en esta carpeta)")

    def _publicar_nube(self, nombre_app, proveedor):
        """Empaqueta la API web (rutas registradas con escuchar_ruta, mas el
        interprete de SiPi) en una carpeta autocontenida, lista para
        desplegar en Vercel, Netlify o Railway. Si el CLI correspondiente
        esta instalado, intenta el despliegue real; si no, deja la carpeta
        lista con instrucciones exactas para desplegar en menos de un
        minuto."""
        carpeta = os.path.join(self.base_dir, f"{nombre_app}_nube")
        os.makedirs(carpeta, exist_ok=True)

        ruta_sipi_actual = getattr(self, "archivo_path", None)
        nombre_programa_sipi = os.path.basename(ruta_sipi_actual) if ruta_sipi_actual else "programa.sipi"
        if ruta_sipi_actual and os.path.exists(ruta_sipi_actual):
            shutil.copy(ruta_sipi_actual, os.path.join(carpeta, nombre_programa_sipi))
        ruta_interprete = os.path.abspath(__file__)
        shutil.copy(ruta_interprete, os.path.join(carpeta, "sipi_motor.py"))

        # Servidor WSGI real (funciona en Vercel/Netlify Functions y en
        # Railway como proceso normal) que carga el programa SiPi y expone
        # sus rutas registradas con 'escuchar_ruta' como una API HTTP real.
        app_py = f'''"""
Envoltorio WSGI real generado por SiPi (publicar_nube).
Carga tu programa "{nombre_programa_sipi}", ejecuta el bloque principal
para registrar las rutas definidas con 'escuchar_ruta', y las expone como
una API HTTP real sobre WSGI (compatible con Vercel, Netlify y Railway).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sipi_motor import Interprete  # noqa: E402

_ruta_sipi = os.path.join(os.path.dirname(os.path.abspath(__file__)), "{nombre_programa_sipi}")
_interprete = Interprete(_ruta_sipi)
_interprete.ejecutar()


def app(environ, start_response):
    ruta = environ.get("PATH_INFO", "/")
    metodo = environ.get("REQUEST_METHOD", "GET")
    largo = int(environ.get("CONTENT_LENGTH", 0) or 0)
    cuerpo_crudo = environ["wsgi.input"].read(largo).decode("utf-8") if largo else ""
    try:
        cuerpo = json.loads(cuerpo_crudo) if cuerpo_crudo else {{}}
    except json.JSONDecodeError:
        cuerpo = cuerpo_crudo

    nombre_funcion = _interprete.entorno.rutas_api.get(ruta)
    if nombre_funcion is None:
        datos, codigo = {{"error": f"Ruta no encontrada: {{ruta}}"}}, "404 Not Found"
    else:
        peticion = {{"metodo": metodo, "ruta": ruta, "query": {{}}, "cuerpo": cuerpo}}
        try:
            resultado = _interprete._invocar_funcion_con_valores(nombre_funcion, [peticion])
            datos, codigo = (resultado or {{"ok": True}}), "200 OK"
        except Exception as e:
            datos, codigo = {{"error": str(e)}}, "500 Internal Server Error"

    cuerpo_json = json.dumps(datos, ensure_ascii=False).encode("utf-8")
    start_response(codigo, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Access-Control-Allow-Origin", "*"),
        ("Content-Length", str(len(cuerpo_json))),
    ])
    return [cuerpo_json]
'''
        with open(os.path.join(carpeta, "app.py"), "w", encoding="utf-8") as f:
            f.write(app_py)

        requirements = "# SiPi no necesita dependencias externas (solo la libreria estandar de Python)\n"
        with open(os.path.join(carpeta, "requirements.txt"), "w", encoding="utf-8") as f:
            f.write(requirements)

        if proveedor == "vercel":
            vercel_json = {
                "version": 2,
                "builds": [{"src": "app.py", "use": "@vercel/python"}],
                "routes": [{"src": "/(.*)", "dest": "app.py"}],
            }
            with open(os.path.join(carpeta, "vercel.json"), "w", encoding="utf-8") as f:
                json.dump(vercel_json, f, indent=2, ensure_ascii=False)
        elif proveedor == "netlify":
            netlify_toml = (
                "[build]\n  functions = \"netlify/functions\"\n\n"
                "[[redirects]]\n  from = \"/*\"\n  to = \"/.netlify/functions/app/:splat\"\n  status = 200\n"
            )
            with open(os.path.join(carpeta, "netlify.toml"), "w", encoding="utf-8") as f:
                f.write(netlify_toml)
            carpeta_fn = os.path.join(carpeta, "netlify", "functions")
            os.makedirs(carpeta_fn, exist_ok=True)
            shutil.copy(os.path.join(carpeta, "app.py"), os.path.join(carpeta_fn, "app.py"))
            shutil.copy(os.path.join(carpeta, "sipi_motor.py"), os.path.join(carpeta_fn, "sipi_motor.py"))
            if ruta_sipi_actual and os.path.exists(ruta_sipi_actual):
                shutil.copy(os.path.join(carpeta, nombre_programa_sipi), os.path.join(carpeta_fn, nombre_programa_sipi))
        else:  # railway
            procfile = "web: python -m gunicorn app:app --bind 0.0.0.0:$PORT\n"
            with open(os.path.join(carpeta, "Procfile"), "w", encoding="utf-8") as f:
                f.write(procfile)
            with open(os.path.join(carpeta, "requirements.txt"), "a", encoding="utf-8") as f:
                f.write("gunicorn\n")
            railway_json = {"$schema": "https://railway.app/railway.schema.json",
                             "build": {"builder": "NIXPACKS"},
                             "deploy": {"startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT"}}
            with open(os.path.join(carpeta, "railway.json"), "w", encoding="utf-8") as f:
                json.dump(railway_json, f, indent=2, ensure_ascii=False)

        print(f"[SiPi] Carpeta lista para desplegar en: {carpeta}")

        cli_por_proveedor = {"vercel": "vercel", "netlify": "netlify", "railway": "railway"}
        cli = cli_por_proveedor[proveedor]
        if shutil.which(cli):
            print(f"[SiPi] Se detecto el CLI de {proveedor} instalado, intentando desplegar de verdad...")
            try:
                comando = [cli, "deploy", "--prod", "--yes"] if proveedor == "vercel" else [cli, "deploy"]
                resultado = subprocess.run(comando, cwd=carpeta, capture_output=True, text=True, timeout=180)
                salida = (resultado.stdout or "") + (resultado.stderr or "")
                print(salida.strip()[-2000:])
                if resultado.returncode == 0:
                    print(f"[SiPi] Despliegue a {proveedor} completado.")
                else:
                    print(f"[SiPi] El CLI de {proveedor} devolvio un error (revisa el detalle arriba). "
                          f"La carpeta ya esta lista para intentarlo manualmente con '{cli} deploy' dentro de ella.")
            except Exception as e:
                print(f"[SiPi] No se pudo ejecutar el CLI de {proveedor} automaticamente ({e}). "
                      f"Corre '{cli} deploy' manualmente dentro de la carpeta.")
        else:
            print(f"[SiPi] No se encontro el CLI de {proveedor} instalado en este equipo.")
            print(f"[SiPi] Para desplegar en menos de un minuto:")
            print(f"       1. npm install -g {cli}")
            print(f"       2. cd {os.path.basename(carpeta)}")
            print(f"       3. {cli} deploy" + ("  (te va a pedir loguearte la primera vez)" if True else ""))


PALABRAS_APERTURA_BLOQUE = BLOQUES_QUE_ABREN
PALABRAS_MISMO_NIVEL = {"sino", "capturar", "caso", "otro"}


_PALABRAS_CREDENCIAL = ("clave", "password", "contrasena", "contraseña", "api_key", "apikey", "token", "secreto", "secret")
_COMANDOS_RIESGOSOS = (
    "leer_archivo", "crear_archivo", "sqlite_conectar", "sqlite_ejecutar", "sqlite_consultar",
    "postgres_conectar", "postgres_ejecutar", "postgres_consultar", "mysql_conectar", "mysql_ejecutar",
    "mysql_consultar", "peticion_http", "descargar_archivo", "instalar_modulo", "instalar_repositorio",
)
_COMANDOS_SQL_CON_QUERY = ("sqlite_ejecutar", "sqlite_consultar", "postgres_ejecutar", "postgres_consultar",
                           "mysql_ejecutar", "mysql_consultar", "bd_ejecutar", "bd_consultar")


def _analizar_codigo_estatico(contenido):
    """Revisor estatico basico de un programa SiPi: bugs comunes,
    vulnerabilidades tipicas, estilo, y sugerencias de que agregar.
    No reemplaza a un linter serio de un lenguaje maduro (SiPi es chico
    y esto es un primer paso), pero agarra los errores mas frecuentes y
    mas caros de un principiante -- y explica CADA hallazgo, para que
    sirva tambien como material para aprender, no solo como una lista de
    reproches.

    Devuelve un diccionario con 4 listas: 'seguridad', 'bugs', 'estilo',
    'sugerencias'. Cada item es un string ya redactado, listo para
    imprimir (con numero de linea adentro si aplica)."""
    lineas_crudas = contenido.split("\n")
    hallazgos = {"seguridad": [], "bugs": [], "estilo": [], "sugerencias": []}

    variables_declaradas = {}   # nombre -> numero de linea donde se declaro
    funciones_declaradas = {}   # nombre -> numero de linea donde se declaro
    todo_el_texto_sin_declaraciones = []  # para buscar usos despues
    usa_algun_comando_riesgoso = False
    usa_intentar = False
    profundidad_maxima = 0
    dentro_de_funcion = None  # (nombre, linea_inicio)
    lineas_funcion_actual = 0
    max_lineas_funcion = 0
    funcion_mas_larga = None

    for num, cruda in enumerate(lineas_crudas, 1):
        limpia = _quitar_comentario_linea(cruda)
        stripped = limpia.strip()
        if not stripped:
            continue

        indent = len(limpia) - len(limpia.lstrip(" \t"))
        profundidad_maxima = max(profundidad_maxima, indent // 4)

        if re.search(r"//\s*(TODO|FIXME|PENDIENTE|ARREGLAR)\b", cruda, re.IGNORECASE):
            hallazgos["estilo"].append(f"Línea {num}: quedó un comentario pendiente (TODO/FIXME) sin resolver.")

        m_var = re.match(r'^variable\s+([\w\u0900-\u097F]+)(?::\s*\w+)?\s*=\s*(.+)$', stripped)
        if m_var:
            nombre_var, valor_expr = m_var.group(1), m_var.group(2).strip()
            variables_declaradas[nombre_var] = num
            nombre_lower = nombre_var.lower()
            if any(p in nombre_lower for p in _PALABRAS_CREDENCIAL) and valor_expr.startswith('"') and valor_expr.strip('"') != "":
                hallazgos["seguridad"].append(
                    f"Línea {num}: la variable '{nombre_var}' parece una credencial escrita directo en el código "
                    f"(hardcodeada). Si subís este archivo a un repositorio, esa clave queda expuesta. "
                    f"Usá 'variable_entorno' para leerla desde afuera del código en vez de escribirla acá."
                )

        m_fn = re.match(r'^funcion\s+([\w\u0900-\u097F]+)\s*\(', stripped)
        if m_fn:
            if dentro_de_funcion and lineas_funcion_actual > max_lineas_funcion:
                max_lineas_funcion = lineas_funcion_actual
                funcion_mas_larga = dentro_de_funcion
            funciones_declaradas[m_fn.group(1)] = num
            dentro_de_funcion = (m_fn.group(1), num)
            lineas_funcion_actual = 0
        elif dentro_de_funcion:
            lineas_funcion_actual += 1
            if stripped == "fin" and indent == 0:
                if lineas_funcion_actual > max_lineas_funcion:
                    max_lineas_funcion = lineas_funcion_actual
                    funcion_mas_larga = dentro_de_funcion
                dentro_de_funcion = None
                lineas_funcion_actual = 0

        primera_palabra = stripped.split(" ", 1)[0]
        if primera_palabra in _COMANDOS_RIESGOSOS:
            usa_algun_comando_riesgoso = True
        if primera_palabra == "intentar":
            usa_intentar = True

        if primera_palabra == "hash_texto":
            resto_hash = stripped[len("hash_texto"):]
            if any(p in resto_hash.lower() for p in _PALABRAS_CREDENCIAL):
                hallazgos["seguridad"].append(
                    f"Línea {num}: se usó 'hash_texto' con algo que parece una contraseña. 'hash_texto' es SHA-256 "
                    f"simple SIN sal -- rápido de romper por fuerza bruta, no apto para contraseñas. "
                    f"Usá 'hash_seguro_contrasena' en su lugar (ver FUNCTIONS.md)."
                )

        if primera_palabra in _COMANDOS_SQL_CON_QUERY:
            m_sql = re.search(r'"([^"]*\{[^}]+\}[^"]*)"', stripped)
            if m_sql and re.search(r"\b(select|insert|update|delete)\b", m_sql.group(1), re.IGNORECASE):
                hallazgos["seguridad"].append(
                    f"Línea {num}: la consulta SQL de '{primera_palabra}' interpola una variable directo en el "
                    f"texto ({{...}}). Si ese valor viene de un usuario (un formulario, una entrada), es una "
                    f"inyección SQL: alguien podría escribir algo en el campo que altere la consulta entera. "
                    f"Vale la pena validar/sanear ese valor antes de meterlo en el SQL."
                )

        if stripped == "capturar":
            # Buscar si el cuerpo del 'capturar' (hasta su 'fin') esta vacio
            # o solo tiene comentarios -- error silenciado sin ningun aviso.
            j = num  # indice 1-based; lineas_crudas es 0-based, cuidado
            cuerpo_vacio = True
            profundidad_cap = 0
            for k in range(num, len(lineas_crudas)):
                sub = _quitar_comentario_linea(lineas_crudas[k]).strip()
                if sub == "" :
                    continue
                if sub == "fin" and profundidad_cap == 0:
                    break
                if sub.split(" ", 1)[0] in BLOQUES_QUE_ABREN:
                    profundidad_cap += 1
                if sub == "fin":
                    profundidad_cap -= 1
                    continue
                cuerpo_vacio = False
            if cuerpo_vacio:
                hallazgos["bugs"].append(
                    f"Línea {num}: el bloque 'capturar' está vacío -- el error se atrapa pero no se hace nada con "
                    f"él (ni se avisa, ni se registra). Un bug ahí adentro puede pasar totalmente desapercibido. "
                    f"Como mínimo, agregá un 'decir \"Error: {{error}}\"' o un 'registrar_log'."
                )

    if dentro_de_funcion and lineas_funcion_actual > max_lineas_funcion:
        max_lineas_funcion = lineas_funcion_actual
        funcion_mas_larga = dentro_de_funcion

    # Variables declaradas pero nunca mas mencionadas en el resto del
    # archivo (chequeo de texto simple, no un analisis de scope real --
    # puede tener falsos negativos/positivos en casos raros, pero agarra
    # el caso comun: "variable x = 5" y 'x' no vuelve a aparecer).
    texto_completo = contenido
    for nombre_var, linea_decl in variables_declaradas.items():
        apariciones = len(re.findall(r'\b' + re.escape(nombre_var) + r'\b', texto_completo))
        if apariciones <= 1:  # la unica aparicion es la propia declaracion
            hallazgos["bugs"].append(
                f"Línea {linea_decl}: la variable '{nombre_var}' se declara pero no se usa en ningún otro lado "
                f"del archivo. Puede ser código que sobró de una versión anterior."
            )

    for nombre_fn, linea_decl in funciones_declaradas.items():
        # Contar apariciones del nombre FUERA de su propia linea de definicion
        apariciones = len(re.findall(r'\b' + re.escape(nombre_fn) + r'\b', texto_completo))
        if apariciones <= 1:
            hallazgos["bugs"].append(
                f"Línea {linea_decl}: la función '{nombre_fn}' se define pero nunca se llama en este archivo. "
                f"Si la usás desde otro módulo con 'importar', ignorá este aviso."
            )

    if funcion_mas_larga and max_lineas_funcion > 60:
        hallazgos["estilo"].append(
            f"La función '{funcion_mas_larga[0]}' (línea {funcion_mas_larga[1]}) tiene alrededor de "
            f"{max_lineas_funcion} líneas. Funciones tan largas son más difíciles de leer y de probar -- "
            f"vale la pena evaluar si se puede partir en funciones más chicas, cada una con una sola responsabilidad."
        )

    if profundidad_maxima >= 6:
        hallazgos["estilo"].append(
            f"Hay bloques anidados hasta un nivel de indentación de {profundidad_maxima}. Tanta anidación suele "
            f"ser señal de que conviene extraer parte de la lógica a una función aparte, para que se lea más fácil."
        )

    if usa_algun_comando_riesgoso and not usa_intentar:
        hallazgos["sugerencias"].append(
            "Este programa usa operaciones que pueden fallar en tiempo real (archivos, red, bases de datos), "
            "pero no tiene ningún bloque 'intentar'/'capturar' en todo el archivo. Si algo de eso falla "
            "(el archivo no existe, no hay conexión, el servidor no responde), el programa se corta de golpe. "
            "Envolver esas operaciones en 'intentar ... capturar ... fin' deja el programa mucho más sólido."
        )

    if "afirmar" not in texto_completo and "iniciar_pruebas" not in texto_completo and len(lineas_crudas) > 80:
        hallazgos["sugerencias"].append(
            "Este es un programa de un tamaño considerable y no tiene ninguna prueba automatizada ('afirmar', "
            "'iniciar_pruebas'). No hace falta testear todo, pero un par de 'afirmar' sobre la lógica más "
            "importante ayuda mucho a notar si un cambio futuro rompe algo (ver 'afirmar' en FUNCTIONS.md)."
        )

    return hallazgos


def imprimir_reporte_revision(ruta, contenido):
    """Corre _analizar_codigo_estatico y imprime el resultado en un reporte
    legible, agrupado por categoria (igual espiritu que un 'linter' de
    cualquier lenguaje serio, adaptado al tamano y edad de SiPi)."""
    hallazgos = _analizar_codigo_estatico(contenido)
    total = sum(len(v) for v in hallazgos.values())

    print(f"[SiPi] Revisión de '{ruta}'")
    print("=" * 60)

    etiquetas = [
        ("seguridad", "🔒 SEGURIDAD"),
        ("bugs", "🐛 POSIBLES BUGS"),
        ("estilo", "🎨 ESTILO"),
        ("sugerencias", "💡 SUGERENCIAS"),
    ]
    for clave, titulo in etiquetas:
        items = hallazgos[clave]
        if not items:
            continue
        print(f"\n{titulo} ({len(items)})")
        for item in items:
            print(f"  - {item}")

    print("\n" + "=" * 60)
    if total == 0:
        print("[SiPi] No se encontró nada para señalar. Igual, esto es una revisión automática básica,")
        print("       no un reemplazo de leer el código con atención.")
    else:
        print(f"[SiPi] Total: {total} hallazgo(s). Ninguno de estos frena la ejecución del programa --")
        print("       son sugerencias para que decidas vos si aplicarlas.")


def formatear_codigo(ruta):
    """Formateador automatico real (estilo Black): reindenta un archivo .sipi
    segun el anidamiento real de sus bloques, con 4 espacios por nivel.
    Los comentarios de bloque (/* */) y las cadenas multilinea (\"\"\"...\"\"\")
    se dejan intactos, sin re-indentar su interior, ya que ahi los espacios
    son parte del contenido real. Devuelve el texto formateado."""
    with open(ruta, "r", encoding="utf-8") as f:
        lineas_originales = f.read().split("\n")

    resultado = []
    nivel = 0
    dentro_comentario_bloque = False
    dentro_cadena_multilinea = False

    for linea_cruda in lineas_originales:
        limpia = linea_cruda.strip()

        if dentro_comentario_bloque:
            resultado.append(linea_cruda)
            if "*/" in limpia:
                dentro_comentario_bloque = False
            continue
        if dentro_cadena_multilinea:
            resultado.append(linea_cruda)
            if '"""' in limpia:
                dentro_cadena_multilinea = False
            continue

        if limpia == "":
            resultado.append("")
            continue

        if limpia.startswith("/*") and "*/" not in limpia:
            resultado.append("    " * nivel + limpia)
            dentro_comentario_bloque = True
            continue
        if limpia.count('"""') == 1:
            resultado.append("    " * nivel + limpia)
            dentro_cadena_multilinea = True
            continue

        palabra = limpia.split(" ")[0]
        if palabra == "fin":
            nivel = max(0, nivel - 1)
            resultado.append("    " * nivel + limpia)
        elif palabra in PALABRAS_MISMO_NIVEL:
            resultado.append("    " * max(0, nivel - 1) + limpia)
        else:
            resultado.append("    " * nivel + limpia)
            if palabra in PALABRAS_APERTURA_BLOQUE:
                nivel += 1
    return "\n".join(resultado)


def _consejo_principiante(mensaje):
    """Da un consejo extra en lenguaje simple para los tipos de error mas
    comunes que se topa alguien recien empezando con SiPi (modo_principiante)."""
    if "Variable no declarada" in mensaje:
        return ("En SiPi hay que crear una variable antes de usarla, con "
                "'variable nombre = valor'. Revisa que el nombre este bien "
                "escrito (SiPi distingue mayusculas de minusculas).")
    if "Division por cero" in mensaje:
        return ("No se puede dividir por cero. Revisa el valor de la variable "
                "que estas usando como divisor antes de la division.")
    if "Comando desconocido" in mensaje:
        return ("Revisa que el nombre del comando este bien escrito, y que "
                "cada bloque (si/mientras/funcion/repetir) tenga su 'fin'.")
    if "No se encontro 'fin'" in mensaje:
        return ("Cada 'si', 'mientras', 'repetir ... veces', 'funcion' y "
                "'para_cada' necesita su propio 'fin' que lo cierre. Contalos: "
                "por cada bloque que abras, un 'fin'.")
    if "Funcion no definida" in mensaje:
        return ("Revisa que la funcion este definida ANTES de llamarla, y que "
                "el nombre este escrito exactamente igual (con guiones bajos "
                "incluidos).")
    if "No se puede modificar la constante" in mensaje:
        return ("Las variables declaradas con 'const' no se pueden cambiar "
                "despues. Si necesitas modificarla, declarala con 'variable' "
                "en vez de 'const'.")
    return None


def ejecutar_repl():
    """REPL real de SiPi: consola interactiva que mantiene el estado
    (variables, funciones, clases definidas) entre lineas, igual que el
    REPL de Python/Node. No es una simulacion aparte del interprete: usa
    la misma clase Interprete y el mismo camino de ejecucion real que
    correr un archivo .sipi (_preprocesar_contenido + _ejecutar_bloque),
    asi que cualquier programa que funcione en el REPL funciona exactamente
    igual guardado en un archivo, y viceversa.

    Soporta bloques multi-linea (si escribis 'si algo', sigue leyendo
    lineas hasta que el bloque cierra con 'fin', antes de ejecutar nada).
    Como comodidad extra (sin la cual un REPL se siente incompleto): si
    escribis algo que no es un comando conocido ni una asignacion, se
    interpreta como una expresion y se muestra su valor automaticamente
    (ej. escribir '2 + 2' imprime '4'), sin necesidad de escribir
    'decir 2 + 2' a mano.
    """
    print(f"SiPi {VERSION} -- REPL interactivo")
    print("Escribi codigo SiPi linea por linea. 'salir' o Ctrl+D para terminar.")
    print("Los bloques (si/funcion/mientras/etc.) se completan solos hasta su 'fin'.")
    print()

    interprete = Interprete("<repl>")
    interprete.base_dir = os.getcwd()
    interprete.lineas = []
    numero_logico = 0

    def es_expresion_no_comando(stripped):
        if not stripped:
            return False
        primera = stripped.split(" ", 1)[0]
        if primera in COMANDOS_CONOCIDOS_SET or primera in BLOQUES_QUE_ABREN or primera in PALABRAS_MISMO_NIVEL:
            return False
        if stripped == "fin":
            return False
        # 'nombre = valor' o 'nombre: tipo = valor' es una asignacion de
        # campo/struct valida tal cual esta (ver LANGUAGE_SPEC.md #3), no
        # una expresion para mostrar -- no hay que envolverla en 'decir'.
        if re.match(r"^[\w\u0900-\u097F]+(\s*:\s*\w+)?\s*=[^=]", stripped):
            return False
        return True

    buffer_bloque = []
    profundidad_bloque = 0
    while True:
        try:
            prompt = "sipi... " if buffer_bloque else "sipi> "
            linea = input(prompt)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

        stripped = linea.strip()
        if not buffer_bloque and stripped in ("salir", "exit", "quit", ".exit"):
            break
        if not buffer_bloque and stripped == "":
            continue

        primera_palabra = stripped.split(" ", 1)[0] if stripped else ""
        resto_palabra = stripped[len(primera_palabra):].strip()
        es_asignacion_campo = resto_palabra.startswith("=") and not resto_palabra.startswith("==")

        buffer_bloque.append(linea)
        if primera_palabra in BLOQUES_QUE_ABREN and not es_asignacion_campo:
            profundidad_bloque += 1
        elif stripped == "fin":
            profundidad_bloque -= 1

        if profundidad_bloque > 0:
            continue  # seguir leyendo lineas hasta que el bloque cierre

        entrada_completa = "\n".join(buffer_bloque)
        buffer_bloque = []
        profundidad_bloque = 0

        es_una_sola_linea = "\n" not in entrada_completa
        if es_una_sola_linea:
            # Primero intentamos autocorregir la linea TAL CUAL la escribio
            # el usuario (ej. 'decid "hola"' -> 'decir "hola"'). Solo si,
            # incluso corregida, sigue sin parecer un comando conocido, la
            # tratamos como una expresion para mostrar con 'decir'. El
            # orden importa: decidir esto ANTES de autocorregir causaba que
            # un comando mal escrito se envolviera mal (ej. terminaba
            # armando 'decir decid "hola"', que no es lo que nadie quiso).
            corregida, _ = _autocorregir_linea(1, entrada_completa)
            if es_expresion_no_comando(corregida.strip()):
                entrada_completa = f"decir {entrada_completa.strip()}"

        try:
            lineas_nuevas, correcciones = Interprete._preprocesar_contenido(entrada_completa)
            for _, desc in correcciones:
                print(f"[SiPi] (corregido automaticamente: {desc})")
            inicio = len(interprete.lineas)
            interprete.lineas.extend(
                (numero_logico + n, texto) for n, texto in lineas_nuevas
            )
            numero_logico += len(lineas_nuevas)
            interprete._ejecutar_bloque(inicio, len(interprete.lineas))
        except SiPiError as e:
            print(f"[SiPi] ERROR: {e}")
            # Sacar del historial las lineas que fallaron, para que no se
            # reintenten en la proxima entrada ni cuenten en el contexto.
            del interprete.lineas[inicio:]
        except (RetornoFuncion, RomperBucle, ContinuarBucle, DepuracionDetenida):
            pass
        except Exception as e:
            print(f"[SiPi] ERROR inesperado: {e}")
            del interprete.lineas[inicio:]


def main():
    # En consolas de Windows viejas (cmd.exe sin 'chcp 65001'), la
    # codificacion por defecto de stdout puede no soportar emojis u otros
    # caracteres Unicode que el propio usuario ponga en su programa SiPi
    # (ej. 'decir "Genial! 🎉"'), lo que tira un UnicodeEncodeError y
    # crashea el programa entero solo por imprimir un caracter. Se
    # reconfigura stdout/stderr a UTF-8 con 'replace' (nunca crashea, en
    # el peor caso reemplaza el caracter raro por un '?') de forma
    # defensiva, en un try/except porque 'reconfigure' no existe en
    # versiones muy viejas de Python ni en todos los tipos de stream.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    if len(sys.argv) < 2 or sys.argv[1] in ("--repl", "repl"):
        ejecutar_repl()
        return

    if sys.argv[1] in ("--ayuda", "-h", "--help"):
        print("SiPi", VERSION)
        print("Uso: python sipi.py archivo.sipi")
        print("     python sipi.py                      (sin argumentos: abre el REPL interactivo)")
        print("     python sipi.py --repl")
        print("     python sipi.py --formatear archivo.sipi")
        print("     python sipi.py --corregir archivo.sipi")
        print("     python sipi.py --revisar archivo.sipi")
        return

    if sys.argv[1] == "--corregir":
        if len(sys.argv) < 3:
            print("Uso: python sipi.py --corregir archivo.sipi")
            sys.exit(1)
        ruta = sys.argv[2]
        if not os.path.exists(ruta):
            print(f"[SiPi] Error: no se encontro el archivo '{ruta}'")
            sys.exit(1)
        with open(ruta, "r", encoding="utf-8") as f:
            original = f.read()
        lineas_corregidas = []
        correcciones_totales = []
        for i, linea in enumerate(original.split("\n"), 1):
            corregida, correcciones_linea = _autocorregir_linea(i, linea)
            lineas_corregidas.append(corregida)
            for desc in correcciones_linea:
                correcciones_totales.append((i, desc))
        nuevo_contenido = "\n".join(lineas_corregidas)
        if not correcciones_totales:
            print(f"[SiPi] '{ruta}' no tenia errores tipograficos para corregir.")
            return
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        print(f"[SiPi] Se corrigieron {len(correcciones_totales)} cosa(s) en '{ruta}' y se guardo el archivo:")
        for num_linea, desc in correcciones_totales[:30]:
            print(f"  - Linea {num_linea}: {desc}")
        if len(correcciones_totales) > 30:
            print(f"  ... y {len(correcciones_totales) - 30} correccion(es) mas")
        return

    if sys.argv[1] == "--revisar":
        if len(sys.argv) < 3:
            print("Uso: python sipi.py --revisar archivo.sipi")
            sys.exit(1)
        ruta = sys.argv[2]
        if not os.path.exists(ruta):
            print(f"[SiPi] Error: no se encontro el archivo '{ruta}'")
            sys.exit(1)
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        imprimir_reporte_revision(ruta, contenido)
        return

    if sys.argv[1] == "--formatear":
        if len(sys.argv) < 3:
            print("Uso: python sipi.py --formatear archivo.sipi")
            sys.exit(1)
        ruta = sys.argv[2]
        if not os.path.exists(ruta):
            print(f"[SiPi] Error: no se encontro el archivo '{ruta}'")
            sys.exit(1)
        texto_formateado = formatear_codigo(ruta)
        with open(ruta, "r", encoding="utf-8") as f:
            original = f.read()
        if original.rstrip("\n") == texto_formateado.rstrip("\n"):
            print(f"[SiPi] '{ruta}' ya estaba formateado correctamente.")
        else:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(texto_formateado + "\n")
            print(f"[SiPi] '{ruta}' formateado correctamente (reindentado con 4 espacios por nivel).")
        return

    banderas_conocidas = {"--sin-cache", "--depurar"}
    argumentos_resto = sys.argv[1:]
    banderas_activas = {a for a in argumentos_resto if a in banderas_conocidas}
    posicionales = [a for a in argumentos_resto if a not in banderas_conocidas]
    sin_cache = "--sin-cache" in banderas_activas
    depurar_activo = "--depurar" in banderas_activas
    if not posicionales:
        uso = "python sipi.py " + " ".join(sorted(banderas_activas)) + " archivo.sipi" if banderas_activas else "python sipi.py archivo.sipi"
        print(f"Uso: {uso}")
        sys.exit(1)
    archivo = posicionales[0]

    if not os.path.exists(archivo):
        print(f"[SiPi] Error: no se encontro el archivo '{archivo}'")
        sys.exit(1)
    interprete = Interprete(archivo)
    if sin_cache:
        # Item 5 de tu feedback (cache de bytecode .sipic): esta bandera
        # fuerza a ignorar cualquier .sipic existente y no generar uno
        # nuevo en esta corrida -- util para depurar si sospechas que la
        # cache esta desactualizada, sin tener que borrarla a mano.
        interprete._ruta_cache_bytecode = lambda: None
        interprete._intentar_cargar_cache = lambda *a, **k: None
        interprete._guardar_cache_bytecode = lambda *a, **k: None
    if depurar_activo:
        # Equivalente a poner 'modo_debug' como primera linea del programa,
        # pero sin tener que editar el archivo -- util para una depuracion
        # puntual (ej. 'sipi depurar archivo.sipi' desde la CLI).
        interprete.debug = True

    # Corremos la ejecucion en un hilo con una pila de sistema operativo mas
    # grande y un limite de recursion de Python mas alto. Esto permite que
    # funciones recursivas de SiPi (fibonacci, factorial, recorridos de
    # arboles/listas enlazadas, etc.) lleguen bastante mas profundo antes de
    # fallar, sin arriesgarse a un segfault por desbordar la pila real del
    # sistema operativo (que es lo que pasaria si solo subieramos
    # sys.setrecursionlimit sin agrandar tambien la pila del hilo).
    resultado_hilo = {"error": None, "codigo_salida": None}

    def _ejecutar_en_hilo():
        limite_anterior = sys.getrecursionlimit()
        sys.setrecursionlimit(200000)
        try:
            interprete.ejecutar()
        except SiPiError as e:
            resultado_hilo["error"] = e
        except SystemExit as e:
            # sys.exit() llamado DENTRO del programa SiPi (ej. desde
            # 'resumen_pruebas' cuando alguna prueba fallo) solo termina
            # este hilo, no el proceso completo -- si no se propaga el
            # codigo a mano, un pipeline de CI/CD veria "exit 0" aunque
            # las pruebas hayan fallado, lo cual es peor que no tener
            # codigo de salida: da una falsa sensacion de que todo esta bien.
            resultado_hilo["codigo_salida"] = e.code if isinstance(e.code, int) else 1
        finally:
            sys.setrecursionlimit(limite_anterior)

    # threading.stack_size() acepta rangos y granularidades distintas segun
    # el sistema operativo (en Windows, por ejemplo, rechaza tamanos que
    # Linux acepta sin problema, con 'ValueError: size not valid'). En vez
    # de asumir que 512 MB siempre funciona, probamos una lista de tamanos
    # de mayor a menor y nos quedamos con el primero que el sistema acepte;
    # si ninguno funciona, seguimos con el tamano de pila por defecto en
    # vez de romper el programa entero por esto.
    for tamano_pila in (512 * 1024 * 1024, 256 * 1024 * 1024, 64 * 1024 * 1024, 16 * 1024 * 1024):
        try:
            threading.stack_size(tamano_pila)
            break
        except (ValueError, RuntimeError):
            continue
    hilo = threading.Thread(target=_ejecutar_en_hilo)
    hilo.start()
    hilo.join()

    if resultado_hilo["codigo_salida"] is not None:
        sys.exit(resultado_hilo["codigo_salida"])

    if resultado_hilo["error"] is not None:
        e = resultado_hilo["error"]
        mensaje = str(e)
        if "maximum recursion depth exceeded" in mensaje:
            print("[SiPi] ERROR: la funcion se llamo a si misma demasiadas veces sin llegar")
            print("       a un caso base (recursion demasiado profunda o infinita).")
            print("       Revisa que la condicion de corte (el 'si ... devolver ...')")
            print("       se cumpla en algun momento.")
        elif getattr(e, "num_linea", None) is not None and getattr(e, "texto_linea", None):
            # Item 26 del feedback: en vez de una sola linea de texto tipo
            # "Error en linea 14: ...", se muestra el codigo real de esa
            # linea con un puntero debajo, mucho mas facil de ubicar de un
            # vistazo que un traceback de Python -- el formato pedido
            # explicitamente fue:
            #   Error en main.sipi:14
            #
            #   14 | mostrar(nombre
            #                      ^
            #   Falta cerrar ')'
            nombre_archivo = os.path.basename(e.archivo) if e.archivo else "programa.sipi"
            numero_texto = str(e.num_linea)
            prefijo = f"{numero_texto} | "
            print(f"[SiPi] Error en {nombre_archivo}:{numero_texto}")
            print()
            print(f"{prefijo}{e.texto_linea}")
            print(" " * len(prefijo) + " " * len(e.texto_linea.rstrip()) + "^")
            print()
            # El mensaje puede venir con el prefijo "Error en linea N: "
            # (cuando se genero automaticamente al envolver una excepcion
            # de Python) o sin el (cuando el propio interprete ya arma un
            # mensaje mas especifico, como "Variable no declarada: ...").
            # Solo se recorta ese prefijo especifico -- nunca el primer
            # ": " que aparezca, porque el mensaje real puede tener el
            # suyo propio (como en este mismo ejemplo) y cortar ahi se
            # comia parte del mensaje.
            prefijo_generico = f"Error en linea {e.num_linea}: "
            detalle = mensaje[len(prefijo_generico):] if mensaje.startswith(prefijo_generico) else mensaje
            print(detalle)
        else:
            print(f"[SiPi] ERROR: {mensaje}")
        if getattr(interprete, "modo_principiante", False):
            consejo = _consejo_principiante(mensaje)
            if consejo:
                print(f"[SiPi] Consejo: {consejo}")
        if getattr(e, "pila", None):
            pila = e.pila
            print("[SiPi] Pila de llamadas (la mas reciente primero):")
            MAX_FRAMES_MOSTRADOS = 12
            for nombre_fn in reversed(pila[-MAX_FRAMES_MOSTRADOS:]):
                print(f"  llamado desde: {nombre_fn}()")
            if len(pila) > MAX_FRAMES_MOSTRADOS:
                print(f"  ... y {len(pila) - MAX_FRAMES_MOSTRADOS} llamadas mas (se omiten para no saturar la pantalla)")
        sys.exit(1)


if __name__ == "__main__":
    main()
