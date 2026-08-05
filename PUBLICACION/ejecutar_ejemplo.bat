@echo off
title SiPi - Ejemplos
color 0B
:menu
cls
echo ============================================
echo   SiPi v28.0 - Elegi un ejemplo para ejecutar
echo ============================================
echo.
echo   1. Hola Mundo (consola)
echo   2. Calculadora con ventana (GUI real)
echo   3. Mini juego (con flechas del teclado)
echo   4. Automatizacion de archivos real
echo   5. Generar proyectos reales de Android y Windows
echo   6. Formulario completo (lista, casilla, botones)
echo   7. Juego avanzado (colisiones, sonido y puntaje)
echo   8. Crear y publicar un sitio web real
echo   9. Base de datos local (persistente)
echo   10. Lista de tareas (listas, funciones con retorno)
echo   11. Producto con errores (diccionarios, intentar/capturar)
echo   12. Modulos (importar otro archivo .sipi)
echo   13. Panel con pestanias y menu desplegable (GUI)
echo   14. Tres en raya (matrices reales)
echo   15. Juego con obstaculos que se mueven solos
echo   16. Agenda de contactos (GUI + base de datos)
echo   17. Sonido generado (sin archivos .wav externos)
echo   18. Abrir el Editor Visual de SiPi (con vista previa en vivo)
echo   19. Procesar archivos usando variables
echo   20. Funciones nuevas v11 (constantes, multilinea, errores)
echo   21. Inventario con JSON y CSV (compatible con Excel)
echo   22. Temporizadores reales (cuenta regresiva)
echo   23. Enum y estructuras (personajes con clases)
echo   24. Tienda sin escribir HTML (pagina web declarativa)
echo   25. Formulario de contacto (tema oscuro + color)
echo   26. Plataformas con fisica real (gravedad, salto, camara)
echo   27. Enemigos con IA y particulas reales
echo   28. Automatizacion de escritorio (captura + portapapeles)
echo   29. Galeria de imagenes reales en ventanas
echo   30. Calculadora con cuadro de color (bugs corregidos)
echo   31. Catalogo dinamico (widgets generados en un bucle)
echo   32. Lista y menu con datos dinamicos reales
echo   33. Panel completo con coordenadas dinamicas
echo   34. Enemigos en posiciones aleatorias reales
echo   35. Funciones recursivas (factorial y fibonacci)
echo   36. Estructuras de datos con recursion real
echo   37. Salir
echo.
set /p opcion="Elegi un numero y presiona Enter: "

if "%opcion%"=="1" python sipi.py ejemplos\hola_mundo.sipi & pause & goto menu
if "%opcion%"=="2" python sipi.py ejemplos\calculadora_gui.sipi & goto menu
if "%opcion%"=="3" python sipi.py ejemplos\juego_simple.sipi & goto menu
if "%opcion%"=="4" python sipi.py ejemplos\automatizacion.sipi & pause & goto menu
if "%opcion%"=="5" python sipi.py ejemplos\generar_apps.sipi & pause & goto menu
if "%opcion%"=="6" python sipi.py ejemplos\formulario_completo.sipi & goto menu
if "%opcion%"=="7" python sipi.py ejemplos\juego_avanzado.sipi & goto menu
if "%opcion%"=="8" python sipi.py ejemplos\crear_sitio_web.sipi & pause & goto menu
if "%opcion%"=="9" python sipi.py ejemplos\base_de_datos.sipi & pause & goto menu
if "%opcion%"=="10" python sipi.py ejemplos\lista_tareas.sipi & pause & goto menu
if "%opcion%"=="11" python sipi.py ejemplos\producto_con_errores.sipi & pause & goto menu
if "%opcion%"=="12" python sipi.py ejemplos\usar_modulo.sipi & pause & goto menu
if "%opcion%"=="13" python sipi.py ejemplos\panel_con_pestanias.sipi & goto menu
if "%opcion%"=="14" python sipi.py ejemplos\tres_en_raya.sipi & pause & goto menu
if "%opcion%"=="15" python sipi.py ejemplos\juego_obstaculos_moviles.sipi & goto menu
if "%opcion%"=="16" python sipi.py ejemplos\agenda_contactos.sipi & goto menu
if "%opcion%"=="17" python sipi.py ejemplos\sonido_generado.sipi & pause & goto menu
if "%opcion%"=="18" start python editor_sipi.py & goto menu
if "%opcion%"=="19" python sipi.py ejemplos\procesar_archivos_con_variables.sipi & pause & goto menu
if "%opcion%"=="20" python sipi.py ejemplos\funciones_nuevas_v11.sipi & pause & goto menu
if "%opcion%"=="21" python sipi.py ejemplos\inventario_json_csv.sipi & pause & goto menu
if "%opcion%"=="22" python sipi.py ejemplos\temporizadores.sipi & pause & goto menu
if "%opcion%"=="23" python sipi.py ejemplos\enum_y_estructuras.sipi & pause & goto menu
if "%opcion%"=="24" python sipi.py ejemplos\tienda_sin_html.sipi & pause & goto menu
if "%opcion%"=="25" python sipi.py ejemplos\formulario_contacto_web.sipi & pause & goto menu
if "%opcion%"=="26" python sipi.py ejemplos\plataformas_fisica.sipi & goto menu
if "%opcion%"=="27" python sipi.py ejemplos\enemigos_ia_particulas.sipi & goto menu
if "%opcion%"=="28" python sipi.py ejemplos\automatizacion_escritorio.sipi & pause & goto menu
if "%opcion%"=="29" python sipi.py ejemplos\galeria_imagenes.sipi & goto menu
if "%opcion%"=="30" python sipi.py ejemplos\calculadora_con_cuadro.sipi & goto menu
if "%opcion%"=="31" python sipi.py ejemplos\lista_dinamica_gui.sipi & goto menu
if "%opcion%"=="32" python sipi.py ejemplos\lista_menu_dinamicos.sipi & goto menu
if "%opcion%"=="33" python sipi.py ejemplos\panel_coordenadas_dinamicas.sipi & goto menu
if "%opcion%"=="34" python sipi.py ejemplos\sprites_posiciones_dinamicas.sipi & goto menu
if "%opcion%"=="35" python sipi.py ejemplos\funciones_recursivas.sipi & pause & goto menu
if "%opcion%"=="36" python sipi.py ejemplos\estructuras_recursivas.sipi & pause & goto menu
if "%opcion%"=="37" exit /b
goto menu
