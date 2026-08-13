#!/usr/bin/env python3
"""
editor_sipi.py - Editor visual propio para el lenguaje SiPi.
Real y funcional: resalta la sintaxis, muestra una vista previa en vivo del
resultado de tu programa mientras escribis, permite personalizar colores y
tipografia, guarda/abre archivos .sipi de verdad, y ejecuta o compila el
programa con el motor real de SiPi.
"""
import os
import sys
import re
import json
import subprocess
import threading
import importlib.util
import tempfile
import atexit
import shutil

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, colorchooser, ttk
except ImportError:
    print("=" * 60)
    print("[SiPi] No se encontro el modulo 'tkinter' en este Python.")
    print("El editor visual de SiPi necesita tkinter para mostrar su")
    print("interfaz grafica.")
    print()
    print("Como solucionarlo:")
    print(" - Windows: reinstala Python desde python.org y asegurate de")
    print("   marcar la casilla 'tcl/tk and IDLE' durante la instalacion")
    print("   (viene tildada por defecto en el instalador oficial).")
    print(" - Linux (Debian/Ubuntu): sudo apt install python3-tk")
    print(" - Linux (Fedora): sudo dnf install python3-tkinter")
    print(" - macOS (Homebrew): brew install python-tk")
    print("=" * 60)
    sys.exit(1)

PALABRAS_CLAVE_RESPALDO = [
    "programa", "version", "variable", "var", "sumar", "restar", "decir",
    "imprimir", "preguntar", "si", "sino", "fin", "repetir", "veces",
    "mientras", "funcion", "llamar", "llamar_valor", "devolver",
    "crear_archivo", "leer_archivo", "borrar_archivo", "crear_carpeta",
    "copiar_archivo", "ejecutar", "esperar", "ventana", "boton", "etiqueta",
    "entrada", "imagen", "cuadro", "casilla", "lista", "barra_progreso",
    "actualizar_barra", "menu_desplegable", "pestanias", "pestana",
    "crear_juego", "sprite", "sonido", "chocar",
    "velocidad", "puntaje_inicial", "mostrar_puntaje", "generar_app_android",
    "generar_app_windows", "verdadero", "falso", "instalar_paquete",
    "guardar_dato", "obtener_dato", "borrar_dato", "obtener_url", "longitud",
    "mayusculas", "minusculas", "azar_entre", "raiz", "potencia",
    "generar_pagina_web", "iniciar_servidor_web", "lista_crear",
    "lista_agregar", "lista_obtener", "lista_longitud", "lista_eliminar",
    "lista_ordenar", "lista_invertir", "lista_contiene", "suma_lista",
    "promedio_lista", "para_cada", "en", "fecha_hora_actual",
    "listar_archivos", "hash_texto", "elegir_al_azar", "comprimir_carpeta",
    "descomprimir_zip", "y", "o", "no", "intentar", "capturar",
    "diccionario_crear", "diccionario_asignar", "diccionario_obtener",
    "diccionario_tiene", "diccionario_eliminar", "diccionario_claves",
    "texto_dividir", "texto_reemplazar", "texto_contiene", "minimo",
    "maximo", "redondear", "registrar_evento", "PI", "E",
    "importar", "modo_debug", "matriz_crear", "matriz_asignar",
    "matriz_obtener", "matriz_filas", "matriz_columnas", "mover_aleatorio",
    "json_crear", "json_leer", "json_guardar", "json_texto",
    "csv_leer", "csv_guardar", "cada", "segundos", "detener_temporizador",
    "enum", "estructura", "instanciar", "pagina_web", "titulo", "subtitulo",
    "enlace", "lista_web", "separador", "tarjeta", "tema", "color",
    "formulario", "campo",
]


def _cargar_palabras_clave():
    """Obtiene la lista de comandos reales a resaltar directamente del
    motor de SiPi (sipi.py o sipi_protegido.py, el que este disponible en
    esta misma carpeta), en vez de mantener una segunda lista a mano en el
    editor. Antes 'PALABRAS_CLAVE' era una copia fija que se iba
    desactualizando cada vez que se agregaba un comando nuevo al lenguaje
    (llegamos a tener 26 comandos reales -romper, continuar, sqlite_*,
    escuchar_ruta, tipo_de, lanzar_error, etc.- que el resaltado de
    sintaxis nunca coloreaba). Si por algun motivo no se puede cargar el
    motor, se usa la lista de respaldo de arriba para que el editor nunca
    se rompa."""
    try:
        aqui = os.path.dirname(os.path.abspath(__file__))
        motor = _cargar_motor_sipi(aqui)
        comandos = list(getattr(motor, "COMANDOS_CONOCIDOS", []))
        if comandos:
            return sorted(set(comandos) | {"PI", "E", "en", "y", "o", "no", "como", "desde", "con"})
    except Exception:
        pass
    return PALABRAS_CLAVE_RESPALDO


PALABRAS_CLAVE = PALABRAS_CLAVE_RESPALDO  # valor inicial; se actualiza en tiempo real mas abajo

TEMAS = {
    "Cyberpunk (por defecto)": {
        "fondo": "#1e1e2e", "texto": "#e0e0f0", "clave": "#7ec4ff",
        "cadena": "#a6e3a1", "comentario": "#6c7086", "numero": "#f9c74f",
        "barra": "#181825", "acento": "#40a02b",
    },
    "Claro": {
        "fondo": "#fafafa", "texto": "#1e1e1e", "clave": "#0057b7",
        "cadena": "#0a7d34", "comentario": "#9a9a9a", "numero": "#b56900",
        "barra": "#e5e5e5", "acento": "#0a7d34",
    },
    "Alto contraste": {
        "fondo": "#000000", "texto": "#ffffff", "clave": "#00ffea",
        "cadena": "#00ff00", "comentario": "#888888", "numero": "#ffff00",
        "barra": "#111111", "acento": "#00ff00",
    },
}

def _carpeta_config_usuario():
    """Carpeta de configuracion del usuario, siguiendo XDG Base Directory
    en Linux/Mac ($XDG_CONFIG_HOME o ~/.config) y %APPDATA% en Windows.
    Bug real encontrado al empaquetar SiPi como .deb: antes,
    ARCHIVO_CONFIG vivia al lado de editor_sipi.py -- en una instalacion
    de sistema eso cae en /usr/share/sipi/, que un usuario sin privilegios
    de root no puede escribir. El editor tiraba un PermissionError apenas
    intentaba guardar el tema o el tamano de letra. Ahora la config vive
    en la carpeta de config del usuario, que siempre es escribible."""
    if os.name == "nt":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    carpeta = os.path.join(base, "sipi")
    try:
        os.makedirs(carpeta, exist_ok=True)
    except OSError:
        # Si por algun motivo ni siquiera esto es escribible, se sigue
        # igual -- el guardado de config ya maneja el error mas abajo y
        # simplemente no persiste nada, no crashea el editor.
        pass
    return carpeta


ARCHIVO_CONFIG = os.path.join(_carpeta_config_usuario(), "editor_config.json")
# Item 9 del feedback ("recuperacion automatica"): a diferencia de
# 'editor_config.json' (preferencias, ahora en la carpeta de config del
# usuario) este archivo vive en la carpeta HOME del usuario, porque tiene
# que sobrevivir aunque SiPi se este ejecutando desde una carpeta temporal
# distinta cada vez (ver el aviso de carpeta volatil mas abajo) y porque
# es exactamente el tipo de dato que un cierre inesperado no deberia
# perder.
ARCHIVO_RECUPERACION = os.path.join(os.path.expanduser("~"), ".sipi_editor_recuperacion.json")


def _cargar_motor_sipi(aqui):
    """Importa el motor de SiPi bajo un nombre de modulo consistente, sin
    depender de que el archivo se llame literalmente 'sipi.py'. En la
    carpeta de desarrollo existe 'sipi.py'; en una carpeta ya publicada
    (generada por publicar.py/proteger_codigo.py) solo existe
    'sipi_protegido.py'. Antes el editor hacia 'import sipi' a secas, que
    fallaba con ModuleNotFoundError apenas se abria 'editor_protegido.py'
    en una carpeta publicada, porque ese archivo no existe ahi."""
    ruta_normal = os.path.join(aqui, "sipi.py")
    ruta_protegida = os.path.join(aqui, "sipi_protegido.py")
    if os.path.exists(ruta_normal):
        ruta = ruta_normal
    elif os.path.exists(ruta_protegida):
        ruta = ruta_protegida
    else:
        raise ImportError(
            "No se encontro 'sipi.py' ni 'sipi_protegido.py' en esta carpeta."
        )
    spec = importlib.util.spec_from_file_location("motor_sipi_dinamico", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


PALABRAS_CLAVE = _cargar_palabras_clave()  # ahora si, con el motor ya definido arriba


class EditorSiPi:
    def __init__(self, root):
        self.root = root
        self.root.title("SiPi - Editor Visual")
        self.root.geometry("1250x700")
        self.archivo_actual = None
        self.proceso_vista_previa = None
        self.tarea_pendiente = None
        # Item 8 del feedback ("indicador de cambios"): rastrea si hay
        # cambios sin guardar para mostrar "main.sipi *" en titulo/estado,
        # igual que cualquier IDE. Se pone en True en cada tecla y en False
        # justo despues de guardar con exito.
        self.modificado = False
        # Item 6/7 ("ejecutar sin guardar"): carpeta temporal propia de
        # esta sesion del editor, creada una sola vez y NO borrada hasta
        # que el editor se cierra (o se vuelve a ejecutar). Antes no
        # existia ningun archivo temporal para el caso "sin guardar": el
        # boton Ejecutar directamente exigia guardar primero. Ahora, si no
        # hay archivo_actual (o el contenido no coincide con lo guardado),
        # se escribe el contenido actual aca y se ejecuta desde ahi -- el
        # archivo persiste el tiempo suficiente para que el proceso lo
        # lea, a diferencia de un NamedTemporaryFile(delete=True) que se
        # borra apenas se cierra el 'with', antes de que el proceso hijo
        # (que arranca async con Popen/'start cmd') llegue a abrirlo.
        self.carpeta_temporal_ejecucion = tempfile.mkdtemp(prefix="sipi_editor_")
        self._ruta_temporal_actual = None
        # Item 14 del feedback ("pestañas, poder abrir varios .sipi"):
        # cada pestaña guarda su propio archivo/contenido/estado de
        # modificado. Solo el buffer de la pestaña ACTIVA vive en
        # 'self.texto' en cada momento -- al cambiar de pestaña, el
        # contenido actual se guarda en 'self.pestanas[idx]' antes de
        # cargar el de la nueva (ver '_guardar_estado_pestana_actual' /
        # '_cambiar_a_pestana').
        self.pestanas = [{"archivo": None, "contenido": "", "modificado": False}]
        self.indice_pestana_actual = 0

        self.config = self._cargar_config()
        self.tema_actual = self.config.get("tema", "Cyberpunk (por defecto)")
        self.tamano_fuente = self.config.get("tamano_fuente", 12)
        self.vista_previa_activa = self.config.get("vista_previa_activa", True)

        self.root.configure(bg=self._colores()["fondo"])

        self._crear_barra_herramientas()
        self._crear_area_principal()
        self._crear_barra_estado()
        self._crear_panel_terminal()

        self.texto.bind("<KeyRelease>", self._al_escribir)
        self.popup_autocompletar = None
        self.lista_autocompletar = None
        self._motor_sipi_cache = None
        self.texto.bind("<Tab>", self._aceptar_autocompletado)
        self.texto.bind("<Return>", self._al_presionar_enter)
        self.texto.bind("<Escape>", self._cerrar_autocompletado)
        self.texto.bind("<Down>", self._mover_autocompletado)
        self.texto.bind("<Up>", self._mover_autocompletado)
        self._aplicar_tema()
        self._configurar_atajos_teclado()
        atexit.register(self._limpiar_carpeta_temporal)
        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar_ventana)

        plantilla = (
            'programa "Mi primer programa"\n\n'
            'variable nombre = "Mundo"\n'
            'decir "Hola, {nombre}! Esto corre en SiPi de verdad."\n'
        )
        self.texto.insert("1.0", plantilla)
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self._programar_vista_previa()
        self._actualizar_selector_nivel_desde_codigo()
        self.pestanas[0]["contenido"] = plantilla
        self._redibujar_barra_pestanas()
        self._id_recuperacion_pendiente = self.root.after(100, self._ofrecer_recuperacion_si_corresponde)

    # ------- Configuracion persistente -------
    def _cargar_config(self):
        if os.path.exists(ARCHIVO_CONFIG):
            try:
                with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _guardar_config(self):
        self.config["tema"] = self.tema_actual
        self.config["tamano_fuente"] = self.tamano_fuente
        self.config["vista_previa_activa"] = self.vista_previa_activa
        try:
            with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def _colores(self):
        return TEMAS.get(self.tema_actual, TEMAS["Cyberpunk (por defecto)"])

    # ------- Interfaz -------
    def _crear_barra_herramientas(self):
        colores = self._colores()
        self.barra = tk.Frame(self.root, bg=colores["barra"], height=44)
        self.barra.pack(side=tk.TOP, fill=tk.X)

        self.estilo_boton = {"bg": "#313244", "fg": colores["texto"], "bd": 0,
                              "activebackground": "#45475a", "activeforeground": "white",
                              "font": ("Segoe UI", 10), "padx": 10, "pady": 6}

        self._boton_barra("Nuevo", self.nuevo)
        self._boton_barra("Abrir", self.abrir)
        self._boton_barra("Guardar", self.guardar)
        self._boton_barra("Guardar como", self.guardar_como)

        tk.Button(self.barra, text="▶ Ejecutar", command=self.ejecutar, bg="#40a02b",
                  fg="white", bd=0, activebackground="#5fc93f", font=("Segoe UI", 10, "bold"),
                  padx=16, pady=6).pack(side=tk.LEFT, padx=10, pady=4)

        tk.Button(self.barra, text="Compilar a ejecutable", command=self.compilar_exe, bg="#8839ef",
                  fg="white", bd=0, activebackground="#a35ff5", font=("Segoe UI", 10),
                  padx=12, pady=6).pack(side=tk.LEFT, padx=4, pady=4)

        tk.Button(self.barra, text="🐞 Depurar", command=self.abrir_depurador, bg="#d20f39",
                  fg="white", bd=0, activebackground="#e64553", font=("Segoe UI", 10),
                  padx=12, pady=6).pack(side=tk.LEFT, padx=4, pady=4)

        tk.Button(self.barra, text="🪄 Formatear", command=self.formatear_codigo_actual, bg="#179299",
                  fg="white", bd=0, activebackground="#2ab5bb", font=("Segoe UI", 10),
                  padx=12, pady=6).pack(side=tk.LEFT, padx=4, pady=4)

        tk.Button(self.barra, text="⚙ Configurar", command=self.abrir_configuracion, bg="#df8e1d",
                  fg="white", bd=0, activebackground="#f0a93e", font=("Segoe UI", 10),
                  padx=12, pady=6).pack(side=tk.LEFT, padx=4, pady=4)

        tk.Button(self.barra, text="⌨ Terminal", command=self._alternar_panel_terminal, bg="#6c7086",
                  fg="white", bd=0, activebackground="#7f849c", font=("Segoe UI", 10),
                  padx=12, pady=6).pack(side=tk.LEFT, padx=4, pady=4)

        self._crear_selector_nivel()

    def _crear_selector_nivel(self):
        """Selector de nivel de dificultad (#nivel principiante/facil/medio/dificil/extremo).

        El motor de SiPi (sipi.py) ya tiene este sistema implementado hace
        varias versiones -- restringe que comandos se pueden usar segun el
        nivel elegido, con avisos claros de que nivel desbloquea cada
        comando -- pero no habia ninguna forma de elegirlo desde el editor
        visual sin escribir la directiva '#nivel' a mano en la primera
        linea. Este selector la lee/escribe por vos."""
        colores = self._colores()
        marco = tk.Frame(self.barra, bg=colores["barra"])
        marco.pack(side=tk.LEFT, padx=(16, 4), pady=4)

        tk.Label(marco, text="Nivel:", bg=colores["barra"], fg=colores["texto"],
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 4))

        self.OPCIONES_NIVEL = ["Sin restriccion", "Principiante", "Facil", "Medio", "Dificil", "Extremo"]
        self.nivel_var = tk.StringVar(value="Sin restriccion")
        self.selector_nivel = ttk.Combobox(marco, textvariable=self.nivel_var, values=self.OPCIONES_NIVEL,
                                            state="readonly", width=14, font=("Segoe UI", 10))
        self.selector_nivel.pack(side=tk.LEFT)
        self.selector_nivel.bind("<<ComboboxSelected>>", self._al_cambiar_nivel)

    def _leer_nivel_actual_del_codigo(self):
        """Busca una directiva '#nivel X' entre las primeras lineas no vacias
        del texto actual del editor. Devuelve el nombre capitalizado
        ('Principiante', etc.) o 'Sin restriccion' si no hay ninguna."""
        motor = self._obtener_motor()
        for linea in self.texto.get("1.0", tk.END).split("\n")[:5]:
            m = re.match(r"^#\s*nivel\s+(\w+)\s*$", linea.strip(), re.IGNORECASE)
            if m and motor and m.group(1).lower() in motor.NIVELES_SIPI:
                return m.group(1).lower().capitalize()
        return "Sin restriccion"

    def _actualizar_selector_nivel_desde_codigo(self):
        """Sincroniza el combobox con lo que diga el archivo recien abierto/
        cargado, para no pisar una directiva ya presente con 'Sin restriccion'
        por defecto."""
        if hasattr(self, "nivel_var"):
            self.nivel_var.set(self._leer_nivel_actual_del_codigo())

    def _al_cambiar_nivel(self, evento=None):
        """Reescribe (o quita) la directiva '#nivel' en la primera linea no
        vacia del programa, segun lo elegido en el combobox. No toca el
        resto del codigo."""
        elegido = self.nivel_var.get()
        contenido = self.texto.get("1.0", tk.END)
        lineas = contenido.split("\n")

        # Sacar cualquier directiva '#nivel' preexistente en las primeras lineas
        idx_directiva = None
        for i, linea in enumerate(lineas[:5]):
            if re.match(r"^#\s*nivel\s+\w+\s*$", linea.strip(), re.IGNORECASE):
                idx_directiva = i
                break

        if idx_directiva is not None:
            del lineas[idx_directiva]

        if elegido != "Sin restriccion":
            lineas.insert(0, f"#nivel {elegido.lower()}")

        nuevo_contenido = "\n".join(lineas)
        pos_cursor = self.texto.index(tk.INSERT)
        self.texto.delete("1.0", tk.END)
        self.texto.insert("1.0", nuevo_contenido)
        try:
            self.texto.mark_set(tk.INSERT, pos_cursor)
        except tk.TclError:
            pass
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self._programar_vista_previa()
        if elegido == "Sin restriccion":
            self.estado.config(text="Nivel de dificultad quitado: todos los comandos disponibles, sin restriccion.")
        else:
            self.estado.config(text=f"Nivel de dificultad: {elegido}. Solo se van a poder usar comandos de ese nivel o mas bajo.")

    def _boton_barra(self, texto, comando):
        b = tk.Button(self.barra, text=texto, command=comando, **self.estilo_boton)
        b.pack(side=tk.LEFT, padx=4, pady=4)
        return b

    def _crear_area_principal(self):
        colores = self._colores()
        self._crear_barra_pestanas()
        self.contenedor = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=colores["fondo"],
                                          sashwidth=6, bd=0)
        self.contenedor.pack(fill=tk.BOTH, expand=True)

        # --- Panel explorador de archivos (item 13 del feedback) ---
        self._crear_panel_explorador()

        # --- Panel izquierdo: editor de codigo ---
        panel_codigo = tk.Frame(self.contenedor, bg=colores["fondo"])
        self.numeros = tk.Text(panel_codigo, width=4, bg=colores["barra"], fg="#6c7086",
                                bd=0, font=("Consolas", self.tamano_fuente), state="disabled")
        self.numeros.pack(side=tk.LEFT, fill=tk.Y)

        self.texto = tk.Text(panel_codigo, bg=colores["fondo"], fg=colores["texto"],
                              insertbackground="white", bd=0,
                              font=("Consolas", self.tamano_fuente), undo=True, wrap="none")
        self.texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.contenedor.add(panel_codigo, minsize=300)

        # --- Panel derecho: vista previa en vivo ---
        panel_previa = tk.Frame(self.contenedor, bg=colores["barra"])
        etiqueta_previa = tk.Label(panel_previa, text="Vista previa en vivo (salida de consola)",
                                    bg=colores["barra"], fg=colores["texto"],
                                    font=("Segoe UI", 10, "bold"), anchor="w", padx=8, pady=6)
        etiqueta_previa.pack(side=tk.TOP, fill=tk.X)

        self.salida_previa = tk.Text(panel_previa, bg="#11111b", fg="#cdd6f4", bd=0,
                                      font=("Consolas", 11), state="disabled", wrap="word")
        self.salida_previa.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))
        self.contenedor.add(panel_previa, minsize=250)

        self.texto.tag_configure("clave", foreground=colores["clave"])
        self.texto.tag_configure("cadena", foreground=colores["cadena"])
        self.texto.tag_configure("comentario", foreground=colores["comentario"])
        self.texto.tag_configure("numero", foreground=colores["numero"])

    # ------- Pestañas (item 14 del feedback) -------
    def _crear_barra_pestanas(self):
        colores = self._colores()
        self.barra_pestanas = tk.Frame(self.root, bg=colores["barra"], height=32)
        self.barra_pestanas.pack(side=tk.TOP, fill=tk.X)

    # ------- Explorador de archivos (item 13 del feedback) -------
    def _crear_panel_explorador(self):
        """Arbol de carpetas simple (no un file manager completo: solo
        navegar y abrir), con carga perezosa -- una carpeta con miles de
        archivos no tarda nada en mostrarse porque solo se leen sus hijos
        cuando el usuario la despliega, no todo el arbol de una."""
        colores = self._colores()
        panel = tk.Frame(self.contenedor, bg=colores["barra"])
        self.contenedor.add(panel, minsize=180, width=220)

        encabezado = tk.Frame(panel, bg=colores["barra"])
        encabezado.pack(side=tk.TOP, fill=tk.X)
        tk.Label(encabezado, text="EXPLORADOR", bg=colores["barra"], fg="#a6adc8",
                 font=("Segoe UI", 8, "bold"), anchor="w", padx=8, pady=4).pack(side=tk.LEFT)
        boton_refrescar = tk.Label(encabezado, text="⟳", bg=colores["barra"], fg="#a6adc8",
                                    cursor="hand2", font=("Segoe UI", 10), padx=6)
        boton_refrescar.pack(side=tk.RIGHT)
        boton_refrescar.bind("<Button-1>", lambda e: self._refrescar_explorador())
        boton_carpeta = tk.Label(encabezado, text="📁", bg=colores["barra"], fg="#a6adc8",
                                  cursor="hand2", font=("Segoe UI", 10), padx=6)
        boton_carpeta.pack(side=tk.RIGHT)
        boton_carpeta.bind("<Button-1>", lambda e: self._elegir_carpeta_proyecto())

        estilo = ttk.Style()
        try:
            estilo.theme_use(estilo.theme_use())  # no-op, solo confirma que hay un tema activo
        except Exception:
            pass
        estilo.configure("Explorador.Treeview", background=colores["fondo"], fieldbackground=colores["fondo"],
                          foreground=colores["texto"], borderwidth=0)
        self.arbol_explorador = ttk.Treeview(panel, show="tree", style="Explorador.Treeview", selectmode="browse")
        self.arbol_explorador.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.arbol_explorador.bind("<<TreeviewOpen>>", self._al_desplegar_nodo_explorador)
        self.arbol_explorador.bind("<Double-1>", self._al_doble_clic_explorador)

        # La carpeta raiz por defecto es la del propio SiPi (mismo lugar
        # de siempre, predecible); "elegir carpeta" la cambia a la del
        # proyecto del usuario en el momento que la necesite.
        self.carpeta_proyecto = os.path.dirname(os.path.abspath(__file__))
        self._refrescar_explorador()

    def _elegir_carpeta_proyecto(self):
        carpeta = filedialog.askdirectory(title="Elegir carpeta del proyecto")
        if carpeta:
            self.carpeta_proyecto = carpeta
            self._refrescar_explorador()

    def _refrescar_explorador(self):
        self.arbol_explorador.delete(*self.arbol_explorador.get_children(""))
        nodo_raiz = self.arbol_explorador.insert(
            "", "end", text=f"📂 {os.path.basename(self.carpeta_proyecto) or self.carpeta_proyecto}",
            values=(self.carpeta_proyecto, "carpeta"), open=True)
        self._poblar_hijos_explorador(nodo_raiz, self.carpeta_proyecto)

    def _listar_entradas_carpeta(self, carpeta):
        """Lista una carpeta salteando ruido tipico (ocultos, __pycache__,
        node_modules, .git) y ordenando carpetas primero -- exactamente
        el mismo criterio que ya usa '_buscar_archivos_cache' en
        sipi_cli.py para no tardar de mas en proyectos grandes."""
        try:
            entradas = os.listdir(carpeta)
        except OSError:
            return []
        ocultar = {"__pycache__", "node_modules", ".git", ".sipi"}
        visibles = [e for e in entradas if not e.startswith(".") and e not in ocultar]
        carpetas = sorted(e for e in visibles if os.path.isdir(os.path.join(carpeta, e)))
        archivos = sorted(e for e in visibles if not os.path.isdir(os.path.join(carpeta, e)))
        return [(e, "carpeta") for e in carpetas] + [(e, "archivo") for e in archivos]

    def _poblar_hijos_explorador(self, nodo_padre, carpeta):
        for nombre, tipo in self._listar_entradas_carpeta(carpeta):
            ruta = os.path.join(carpeta, nombre)
            if tipo == "carpeta":
                nodo = self.arbol_explorador.insert(
                    nodo_padre, "end", text=f"📁 {nombre}", values=(ruta, "carpeta"))
                # Nodo "placeholder" para que la flechita de despliegue
                # aparezca sin tener que leer esta subcarpeta todavia --
                # recien se lee de verdad en '_al_desplegar_nodo_explorador'.
                if self._listar_entradas_carpeta(ruta):
                    self.arbol_explorador.insert(nodo, "end", text="")
            else:
                icono = "📄" if nombre.endswith(".sipi") else "  "
                self.arbol_explorador.insert(nodo_padre, "end", text=f"{icono} {nombre}", values=(ruta, "archivo"))

    def _al_desplegar_nodo_explorador(self, evento=None):
        nodo = self.arbol_explorador.focus()
        hijos = self.arbol_explorador.get_children(nodo)
        # Si el unico hijo es el placeholder vacio de arriba, se borra y
        # se cargan los hijos reales recien ahora (carga perezosa).
        if len(hijos) == 1 and not self.arbol_explorador.item(hijos[0], "text").strip():
            self.arbol_explorador.delete(hijos[0])
            valores = self.arbol_explorador.item(nodo, "values")
            if valores:
                self._poblar_hijos_explorador(nodo, valores[0])

    def _al_doble_clic_explorador(self, evento=None):
        nodo = self.arbol_explorador.focus()
        valores = self.arbol_explorador.item(nodo, "values")
        if not valores or valores[1] != "archivo":
            return
        self._abrir_ruta(valores[0])

    def _texto_pestana(self, pestana):
        nombre = os.path.basename(pestana["archivo"]) if pestana["archivo"] else "Sin titulo"
        return f"{nombre} *" if pestana["modificado"] else nombre

    def _redibujar_barra_pestanas(self):
        colores = self._colores()
        for hijo in self.barra_pestanas.winfo_children():
            hijo.destroy()
        for idx, pestana in enumerate(self.pestanas):
            activa = idx == self.indice_pestana_actual
            marco = tk.Frame(self.barra_pestanas, bg=colores["fondo"] if activa else colores["barra"])
            marco.pack(side=tk.LEFT, padx=(2, 0), pady=2)
            etiqueta = tk.Label(
                marco, text=self._texto_pestana(pestana),
                bg=colores["fondo"] if activa else colores["barra"],
                fg=colores["texto"] if activa else "#a6adc8",
                font=("Segoe UI", 9, "bold" if activa else "normal"), padx=10, pady=4, cursor="hand2",
            )
            etiqueta.pack(side=tk.LEFT)
            etiqueta.bind("<Button-1>", lambda e, i=idx: self._cambiar_a_pestana(i))
            boton_cerrar = tk.Label(
                marco, text="✕", bg=colores["fondo"] if activa else colores["barra"],
                fg="#a6adc8", font=("Segoe UI", 9), padx=4, pady=4, cursor="hand2",
            )
            boton_cerrar.pack(side=tk.LEFT)
            boton_cerrar.bind("<Button-1>", lambda e, i=idx: self._cerrar_pestana(i))
        boton_nueva = tk.Label(
            self.barra_pestanas, text="+", bg=colores["barra"], fg=colores["texto"],
            font=("Segoe UI", 11, "bold"), padx=10, pady=4, cursor="hand2",
        )
        boton_nueva.pack(side=tk.LEFT, padx=(4, 0))
        boton_nueva.bind("<Button-1>", lambda e: self.nueva_pestana())

    def _guardar_estado_pestana_actual(self):
        """Vuelca el contenido y estado actuales de 'self.texto' de vuelta
        a 'self.pestanas[indice_actual]', para no perderlo al cambiar de
        pestaña (el widget de texto es UNO SOLO, compartido por todas las
        pestañas -- no se clona un Text por pestaña, mas liviano)."""
        if not self.pestanas:
            return
        pestana = self.pestanas[self.indice_pestana_actual]
        pestana["contenido"] = self.texto.get("1.0", "end-1c")
        pestana["archivo"] = self.archivo_actual
        pestana["modificado"] = self.modificado

    def _cambiar_a_pestana(self, indice):
        if indice == self.indice_pestana_actual or not (0 <= indice < len(self.pestanas)):
            return
        self._guardar_estado_pestana_actual()
        self.indice_pestana_actual = indice
        pestana = self.pestanas[indice]
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", pestana["contenido"])
        self.archivo_actual = pestana["archivo"]
        self.modificado = pestana["modificado"]
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self._actualizar_titulo()
        self._redibujar_barra_pestanas()
        self._programar_vista_previa()
        self._actualizar_selector_nivel_desde_codigo()
        self.estado.config(text=f"Pestaña: {self._texto_pestana(pestana)}")

    def nueva_pestana(self):
        self._guardar_estado_pestana_actual()
        self.pestanas.append({"archivo": None, "contenido": "", "modificado": False})
        self.indice_pestana_actual = len(self.pestanas) - 1
        self.texto.delete("1.0", "end")
        self.archivo_actual = None
        self.modificado = False
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self._actualizar_titulo()
        self._redibujar_barra_pestanas()
        self._programar_vista_previa()
        self._actualizar_selector_nivel_desde_codigo()

    def _indice_pestana_para_archivo(self, ruta):
        """Si 'ruta' ya esta abierta en alguna pestaña, devuelve su
        indice -- evita abrir el mismo archivo dos veces en pestañas
        distintas, que llevaria a confusion sobre cual version es la
        real al guardar."""
        for idx, pestana in enumerate(self.pestanas):
            if pestana["archivo"] and os.path.abspath(pestana["archivo"]) == os.path.abspath(ruta):
                return idx
        return None

    def _cerrar_pestana(self, indice):
        if not (0 <= indice < len(self.pestanas)):
            return
        # Si se cierra la pestaña activa, primero se sincroniza su estado
        # real (por si el usuario tenia cambios sin guardar justo antes
        # de tocar la 'x') para poder preguntar con informacion correcta.
        if indice == self.indice_pestana_actual:
            self._guardar_estado_pestana_actual()
        pestana = self.pestanas[indice]
        if pestana["modificado"]:
            nombre = self._texto_pestana(pestana)
            respuesta = messagebox.askyesnocancel(
                "SiPi", f"'{nombre}' tiene cambios sin guardar. ¿Queres guardarlos antes de cerrar la pestaña?"
            )
            if respuesta is None:
                return
            if respuesta:
                archivo_previo, indice_previo = self.archivo_actual, self.indice_pestana_actual
                self.archivo_actual, self.indice_pestana_actual = pestana["archivo"], indice
                contenido_previo_widget = self.texto.get("1.0", "end-1c")
                self.texto.delete("1.0", "end")
                self.texto.insert("1.0", pestana["contenido"])
                self.modificado = True
                self.guardar_si_hace_falta()
                guardado_ok = not self.modificado
                pestana["archivo"] = self.archivo_actual
                self.texto.delete("1.0", "end")
                self.texto.insert("1.0", contenido_previo_widget)
                self.archivo_actual, self.indice_pestana_actual = archivo_previo, indice_previo
                if not guardado_ok:
                    return  # se cancelo el "Guardar como"
        del self.pestanas[indice]
        if not self.pestanas:
            self.pestanas = [{"archivo": None, "contenido": "", "modificado": False}]
        if self.indice_pestana_actual >= len(self.pestanas):
            self.indice_pestana_actual = len(self.pestanas) - 1
        elif indice < self.indice_pestana_actual:
            self.indice_pestana_actual -= 1
        pestana_activa = self.pestanas[self.indice_pestana_actual]
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", pestana_activa["contenido"])
        self.archivo_actual = pestana_activa["archivo"]
        self.modificado = pestana_activa["modificado"]
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self._actualizar_titulo()
        self._redibujar_barra_pestanas()
        self._programar_vista_previa()

    def _crear_barra_estado(self):
        colores = self._colores()
        self.estado = tk.Label(self.root, text="Listo.", bg=colores["barra"], fg="#a6adc8",
                                anchor="w", font=("Segoe UI", 9), padx=8, pady=4)
        self.estado.pack(side=tk.BOTTOM, fill=tk.X)

    # ------- Terminal integrada (item 12 del feedback) -------
    def _crear_panel_terminal(self):
        """Terminal simple y honesta: cada linea que el usuario escribe se
        corre como UN comando independiente (no una sesion de shell
        interactiva persistente ni un pseudo-terminal) -- misma idea que
        la terminal integrada de cualquier editor de codigo: comandos que
        el USUARIO elige y escribe a mano, con sus propios permisos, en
        su propia carpeta de proyecto. No es mas riesgo que abrir una
        terminal aparte (que el usuario ya puede hacer en cualquier
        momento); la unica diferencia es la comodidad de no salir del
        editor. 'cd' se maneja aparte porque cada comando corre en un
        proceso nuevo, asi que un 'cd' normal no persistiria entre
        comandos si no se guardara la carpeta actual aca."""
        colores = self._colores()
        self.panel_terminal = tk.Frame(self.root, bg=colores["fondo"], height=220)
        # No se empaqueta todavia -- arranca oculta, _alternar_panel_terminal
        # la muestra/oculta.

        encabezado = tk.Frame(self.panel_terminal, bg=colores["barra"])
        encabezado.pack(side=tk.TOP, fill=tk.X)
        tk.Label(encabezado, text="TERMINAL", bg=colores["barra"], fg="#a6adc8",
                 font=("Segoe UI", 8, "bold"), anchor="w", padx=8, pady=4).pack(side=tk.LEFT)
        self.etiqueta_cwd_terminal = tk.Label(encabezado, text="", bg=colores["barra"], fg="#6c7086",
                                               font=("Consolas", 8), anchor="w")
        self.etiqueta_cwd_terminal.pack(side=tk.LEFT, padx=8)
        boton_cerrar_term = tk.Label(encabezado, text="✕", bg=colores["barra"], fg="#a6adc8",
                                      cursor="hand2", font=("Segoe UI", 9), padx=8)
        boton_cerrar_term.pack(side=tk.RIGHT)
        boton_cerrar_term.bind("<Button-1>", lambda e: self._alternar_panel_terminal())

        self.salida_terminal = tk.Text(self.panel_terminal, bg="#11111b", fg="#cdd6f4", bd=0,
                                        font=("Consolas", 9), state="disabled", height=10, wrap="word")
        self.salida_terminal.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        marco_entrada = tk.Frame(self.panel_terminal, bg=colores["fondo"])
        marco_entrada.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(marco_entrada, text="$", bg=colores["fondo"], fg="#a6e3a1",
                 font=("Consolas", 10, "bold"), padx=6).pack(side=tk.LEFT)
        self.entrada_terminal = tk.Entry(marco_entrada, bg="#11111b", fg="#cdd6f4",
                                          insertbackground="white", bd=0, font=("Consolas", 10))
        self.entrada_terminal.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), pady=4)
        self.entrada_terminal.bind("<Return>", self._al_enviar_comando_terminal)

        self.terminal_visible = False
        self.terminal_cwd = self.carpeta_proyecto if hasattr(self, "carpeta_proyecto") else os.getcwd()
        self.historial_terminal = []
        self.indice_historial_terminal = 0

    def _alternar_panel_terminal(self):
        if self.terminal_visible:
            self.panel_terminal.pack_forget()
            self.terminal_visible = False
        else:
            self.panel_terminal.pack(side=tk.BOTTOM, fill=tk.X)
            self.terminal_visible = True
            self._actualizar_etiqueta_cwd_terminal()
            self.entrada_terminal.focus_set()

    def _actualizar_etiqueta_cwd_terminal(self):
        self.etiqueta_cwd_terminal.config(text=self.terminal_cwd)

    def _escribir_en_terminal(self, texto):
        self.salida_terminal.config(state="normal")
        self.salida_terminal.insert("end", texto)
        self.salida_terminal.see("end")
        self.salida_terminal.config(state="disabled")

    def _al_enviar_comando_terminal(self, evento=None):
        comando = self.entrada_terminal.get().strip()
        self.entrada_terminal.delete(0, "end")
        if not comando:
            return
        self.historial_terminal.append(comando)
        self.indice_historial_terminal = len(self.historial_terminal)
        self._escribir_en_terminal(f"$ {comando}\n")

        # 'cd' se maneja localmente (sin lanzar un proceso) porque cada
        # comando de aca en mas corre en un subprocess.Popen nuevo -- un
        # 'cd' real solo cambiaria el directorio de ESE proceso hijo, que
        # muere apenas termina el comando, y el siguiente comando
        # arrancaria de nuevo en la carpeta vieja. Guardando el cwd
        # nosotros mismos, el 'cd' persiste entre comandos como se espera.
        if comando == "cd" or comando.startswith("cd "):
            destino = comando[2:].strip() or os.path.expanduser("~")
            nueva_ruta = destino if os.path.isabs(destino) else os.path.join(self.terminal_cwd, destino)
            nueva_ruta = os.path.normpath(nueva_ruta)
            if os.path.isdir(nueva_ruta):
                self.terminal_cwd = nueva_ruta
                self._actualizar_etiqueta_cwd_terminal()
            else:
                self._escribir_en_terminal(f"cd: no existe la carpeta: {nueva_ruta}\n")
            return

        if comando in ("cls", "clear"):
            self.salida_terminal.config(state="normal")
            self.salida_terminal.delete("1.0", "end")
            self.salida_terminal.config(state="disabled")
            return

        hilo = threading.Thread(target=self._correr_comando_terminal, args=(comando,), daemon=True)
        hilo.start()

    def _correr_comando_terminal(self, comando):
        """Corre en un hilo aparte para no congelar la interfaz mientras
        el comando tarda; el resultado se vuelca al panel via
        'root.after', que es la unica forma segura de tocar widgets de
        Tk desde un hilo que no es el principal."""
        try:
            resultado = subprocess.run(
                comando, shell=True, cwd=self.terminal_cwd,
                capture_output=True, text=True, timeout=120,
                encoding="utf-8", errors="replace",
            )
            salida = (resultado.stdout or "") + (resultado.stderr or "")
        except subprocess.TimeoutExpired:
            salida = "[SiPi] El comando tardo mas de 120 segundos, se corto.\n"
        except OSError as error:
            salida = f"[SiPi] No se pudo correr el comando: {error}\n"
        salida_final = salida if salida.endswith("\n") or not salida else salida + "\n"
        try:
            self.root.after(0, lambda: self._escribir_en_terminal(salida_final))
        except RuntimeError:
            pass  # la ventana ya se cerro mientras el comando corria; no hay donde mostrarlo

    def _aplicar_tema(self):
        colores = self._colores()
        self.root.configure(bg=colores["fondo"])
        self.barra.configure(bg=colores["barra"])
        self.numeros.configure(bg=colores["barra"], font=("Consolas", self.tamano_fuente))
        self.texto.configure(bg=colores["fondo"], fg=colores["texto"], font=("Consolas", self.tamano_fuente))
        self.estado.configure(bg=colores["barra"])
        self.texto.tag_configure("clave", foreground=colores["clave"])
        self.texto.tag_configure("cadena", foreground=colores["cadena"])
        self.texto.tag_configure("comentario", foreground=colores["comentario"])
        self.texto.tag_configure("numero", foreground=colores["numero"])
        self._guardar_config()

    # ------- Resaltado de sintaxis real -------
    def _al_escribir(self, evento=None):
        self._marcar_modificado()
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self._programar_vista_previa()
        # No mostramos/actualizamos autocompletado en teclas de control o
        # de navegacion (evita que se abra o cierre erraticamente).
        if evento is not None and evento.keysym in (
            "Tab", "Return", "Escape", "Up", "Down", "Left", "Right",
            "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
        ):
            return
        self._actualizar_autocompletado()

    # ------- Autocompletado real: comandos, variables y funciones -------
    def _palabra_actual(self):
        """Devuelve (inicio, fin, texto) de la palabra que se esta escribiendo
        justo antes del cursor."""
        indice_cursor = self.texto.index("insert")
        inicio_linea = self.texto.index(f"{indice_cursor} linestart")
        texto_linea = self.texto.get(inicio_linea, indice_cursor)
        m = re.search(r"[A-Za-z_][A-Za-z0-9_]*$", texto_linea)
        if not m:
            return None, None, ""
        columna_inicio = m.start()
        fila = indice_cursor.split(".")[0]
        return f"{fila}.{columna_inicio}", indice_cursor, m.group(0)

    def _obtener_motor(self):
        """Carga el motor de SiPi UNA sola vez y lo cachea (no en cada
        tecla presionada), para poder reusar sus mismas listas de palabras
        de apertura de bloque (PALABRAS_APERTURA_BLOQUE/PALABRAS_MISMO_NIVEL)
        en el autocompletado contextual, en vez de mantener una copia
        separada que se desincronice del lenguaje real."""
        if self._motor_sipi_cache is None:
            try:
                aqui = os.path.dirname(os.path.abspath(__file__))
                self._motor_sipi_cache = _cargar_motor_sipi(aqui)
            except Exception:
                self._motor_sipi_cache = False
        return self._motor_sipi_cache or None

    def _bloque_actual_en_cursor(self):
        """Item 5 de tu feedback (autocompletado 'con intencion'): escanea
        desde el principio del archivo hasta la linea del cursor, con el
        mismo criterio de apertura/cierre de bloques que usa
        formatear_codigo_actual, para saber en que tipo de bloque
        (si/mientras/repetir/para_cada/funcion/etc.) esta parado el cursor
        ahora mismo. Devuelve la palabra del bloque mas interno abierto en
        ese punto, o None si esta en el nivel superior del archivo."""
        motor = self._obtener_motor()
        if motor is None:
            return None
        indice_cursor = self.texto.index("insert")
        fila_cursor = int(indice_cursor.split(".")[0])
        contenido_previo = self.texto.get("1.0", f"{fila_cursor}.0 lineend")
        pila = []
        for linea_cruda in contenido_previo.split("\n"):
            limpia = re.sub(r"//.*$", "", linea_cruda).strip()
            if limpia == "":
                continue
            palabra = limpia.split(" ")[0]
            resto_linea = limpia[len(palabra):].strip()
            es_asignacion = resto_linea.startswith("=") and not resto_linea.startswith("==")
            if palabra == "fin":
                if pila:
                    pila.pop()
            elif palabra in motor.PALABRAS_MISMO_NIVEL:
                continue
            elif palabra in motor.PALABRAS_APERTURA_BLOQUE and not es_asignacion:
                pila.append(palabra)
        return pila[-1] if pila else None

    def _candidatos_contextuales(self):
        """Sugerencias que dependen de DONDE esta parado el cursor, no de
        que letras ya escribio: dentro de un bucle, prioriza 'romper' y
        'continuar'; escribiendo una condicion, prioriza 'y'/'o'/'no'."""
        candidatos = []
        indice_cursor = self.texto.index("insert")
        inicio_linea = self.texto.index(f"{indice_cursor} linestart")
        texto_linea_hasta_cursor = self.texto.get(inicio_linea, indice_cursor)
        if re.match(r"^\s*(si|sino_si|mientras)\s+\S", texto_linea_hasta_cursor):
            candidatos += ["y", "o", "no"]
        bloque = self._bloque_actual_en_cursor()
        if bloque in ("mientras", "repetir", "para_cada", "cada"):
            candidatos += ["romper", "continuar"]
        return candidatos

    def _candidatos_autocompletado(self, prefijo):
        """Junta comandos del lenguaje + variables + funciones definidas en
        el programa actual que empiecen con el prefijo que se esta
        escribiendo, con las sugerencias contextuales (ver
        _candidatos_contextuales) siempre primero en la lista."""
        contenido = self.texto.get("1.0", "end-1c")
        variables = set(re.findall(r"\b(?:variable|var|const)\s+([A-Za-z_]\w*)", contenido))
        funciones = set(re.findall(r"\bfuncion\s+([A-Za-z_]\w*)", contenido))
        candidatos = set(PALABRAS_CLAVE) | variables | funciones
        coincidencias = sorted(c for c in candidatos if c.startswith(prefijo) and c != prefijo)

        contextuales = [c for c in self._candidatos_contextuales() if c.startswith(prefijo) and c != prefijo]
        resto = [c for c in coincidencias if c not in contextuales]
        return (contextuales + resto)[:8]

    def _actualizar_autocompletado(self):
        inicio, fin, palabra = self._palabra_actual()
        if len(palabra) < 2:
            # Con menos de 2 letras normalmente no mostramos nada (seria
            # demasiado ruido), PERO si el cursor esta en un contexto
            # reconocido (recien escribio un espacio dentro de un bucle, o
            # esta armando una condicion) SI mostramos las sugerencias
            # contextuales aunque no haya ninguna letra escrita todavia --
            # es la esencia del item 5: sugerir por intencion, no solo por
            # texto ya tipeado.
            if palabra == "" and self._candidatos_contextuales():
                inicio = fin = self.texto.index("insert")
            else:
                self._cerrar_autocompletado()
                return
        candidatos = self._candidatos_autocompletado(palabra)
        if not candidatos:
            self._cerrar_autocompletado()
            return
        self._mostrar_autocompletado(candidatos, inicio, fin)

    def _mostrar_autocompletado(self, candidatos, inicio, fin):
        self._rango_autocompletado = (inicio, fin)
        colores = self._colores()
        if self.popup_autocompletar is None:
            self.popup_autocompletar = tk.Toplevel(self.root)
            self.popup_autocompletar.overrideredirect(True)
            self.popup_autocompletar.attributes("-topmost", True)
            self.lista_autocompletar = tk.Listbox(
                self.popup_autocompletar, bg=colores["barra"], fg=colores["texto"],
                selectbackground=colores["acento"], selectforeground=colores["fondo"],
                font=("Consolas", max(self.tamano_fuente - 1, 9)), height=min(8, len(candidatos)),
                bd=0, highlightthickness=1, highlightbackground=colores["acento"],
            )
            self.lista_autocompletar.pack(fill=tk.BOTH, expand=True)
            self.lista_autocompletar.bind("<ButtonRelease-1>", lambda e: self._aceptar_autocompletado())
        else:
            self.lista_autocompletar.delete(0, tk.END)
            self.lista_autocompletar.config(height=min(8, len(candidatos)))
        for c in candidatos:
            self.lista_autocompletar.insert(tk.END, c)
        self.lista_autocompletar.selection_clear(0, tk.END)
        self.lista_autocompletar.selection_set(0)
        try:
            bbox = self.texto.bbox(fin)
        except tk.TclError:
            bbox = None
        if bbox:
            x, y, _, alto = bbox
            x_abs = self.texto.winfo_rootx() + x
            y_abs = self.texto.winfo_rooty() + y + alto
            self.popup_autocompletar.geometry(f"+{x_abs}+{y_abs}")

    def _cerrar_autocompletado(self, evento=None):
        if self.popup_autocompletar is not None:
            self.popup_autocompletar.destroy()
            self.popup_autocompletar = None
            self.lista_autocompletar = None

    def _mover_autocompletado(self, evento):
        if self.popup_autocompletar is None:
            return  # deja que Up/Down se comporten normal si no hay popup abierto
        seleccion = self.lista_autocompletar.curselection()
        idx = seleccion[0] if seleccion else 0
        total = self.lista_autocompletar.size()
        if evento.keysym == "Down":
            idx = min(idx + 1, total - 1)
        else:
            idx = max(idx - 1, 0)
        self.lista_autocompletar.selection_clear(0, tk.END)
        self.lista_autocompletar.selection_set(idx)
        self.lista_autocompletar.see(idx)
        return "break"

    def _aceptar_autocompletado(self, evento=None):
        if self.popup_autocompletar is None:
            return  # deja que Tab se comporte normal (indentar) si no hay popup abierto
        seleccion = self.lista_autocompletar.curselection()
        idx = seleccion[0] if seleccion else 0
        palabra = self.lista_autocompletar.get(idx)
        inicio, fin = self._rango_autocompletado
        self.texto.delete(inicio, fin)
        self.texto.insert(inicio, palabra)
        self._cerrar_autocompletado()
        self._resaltar_sintaxis()
        return "break"

    def _al_presionar_enter(self, evento=None):
        if self.popup_autocompletar is not None:
            return self._aceptar_autocompletado()
        return None  # Enter normal (nueva linea) si no hay popup abierto

    def _resaltar_sintaxis(self):
        contenido = self.texto.get("1.0", "end-1c")
        for tag in ("clave", "cadena", "comentario", "numero"):
            self.texto.tag_remove(tag, "1.0", "end")

        for i, linea in enumerate(contenido.split("\n"), start=1):
            for m in re.finditer(r"//.*$", linea):
                self.texto.tag_add("comentario", f"{i}.{m.start()}", f"{i}.{m.end()}")
            for m in re.finditer(r'"[^"]*"', linea):
                self.texto.tag_add("cadena", f"{i}.{m.start()}", f"{i}.{m.end()}")
            for m in re.finditer(r"\b\d+(\.\d+)?\b", linea):
                self.texto.tag_add("numero", f"{i}.{m.start()}", f"{i}.{m.end()}")
            for palabra in PALABRAS_CLAVE:
                for m in re.finditer(rf"\b{re.escape(palabra)}\b", linea):
                    self.texto.tag_add("clave", f"{i}.{m.start()}", f"{i}.{m.end()}")

    def _actualizar_numeros_linea(self):
        total_lineas = int(self.texto.index("end-1c").split(".")[0])
        self.numeros.config(state="normal")
        self.numeros.delete("1.0", "end")
        self.numeros.insert("1.0", "\n".join(str(n) for n in range(1, total_lineas + 1)))
        self.numeros.config(state="disabled")

    # ------- Vista previa en vivo -------
    def _programar_vista_previa(self):
        if not self.vista_previa_activa:
            return
        if self.tarea_pendiente:
            self.root.after_cancel(self.tarea_pendiente)
        self.tarea_pendiente = self.root.after(900, self._actualizar_vista_previa)

    def _ruta_motor_sipi(self, aqui):
        """Devuelve la ruta al motor de SiPi que hay que usar: si estamos en
        una carpeta de publicacion (donde solo existe 'sipi_protegido.py'),
        lo usa a el; si estamos en la carpeta de desarrollo (donde existe
        'sipi.py'), usa ese. Antes esto estaba fijo a 'sipi.py', lo que
        rompia 'editor_protegido.py' generado por proteger_codigo.py: al
        distribuirse sin 'sipi.py' (solo con 'sipi_protegido.py'), el boton
        de Ejecutar/vista previa fallaba porque buscaba un archivo que ya
        no estaba en esa carpeta.
        """
        protegido = os.path.join(aqui, "sipi_protegido.py")
        normal = os.path.join(aqui, "sipi.py")
        if os.path.exists(normal):
            return normal
        if os.path.exists(protegido):
            return protegido
        return normal  # ninguno existe: dejamos que falle con un error claro mas abajo

    def _ruta_generar_exe(self, aqui):
        """Igual que _ruta_motor_sipi pero para el compilador a .exe."""
        protegido = os.path.join(aqui, "generar_exe_protegido.py")
        normal = os.path.join(aqui, "generar_exe.py")
        if os.path.exists(normal):
            return normal
        if os.path.exists(protegido):
            return protegido
        return normal

    def _actualizar_vista_previa(self):
        codigo = self.texto.get("1.0", "end-1c")
        aqui = os.path.dirname(os.path.abspath(__file__))
        sipi_py = self._ruta_motor_sipi(aqui)

        # No corremos ventanas/juegos en la vista previa (abrirían ventanas reales
        # cada vez que escribis); avisamos y solo mostramos que se detecto ese tipo.
        if re.search(r"\bventana\b|\bcrear_juego\b", codigo):
            self._mostrar_previa(
                "[Vista previa] Este programa abre una ventana o un juego real.\n"
                "Presiona '▶ Ejecutar' para verlo funcionando en su propia ventana."
            )
            return

        try:
            import tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".sipi", delete=False, encoding="utf-8") as f:
                f.write(codigo)
                ruta_temporal = f.name
            resultado = subprocess.run(
                [sys.executable, sipi_py, ruta_temporal],
                capture_output=True, text=True, timeout=5, cwd=aqui,
                encoding="utf-8", errors="replace",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            salida = resultado.stdout
            if resultado.stderr:
                salida += "\n" + resultado.stderr
            os.remove(ruta_temporal)
            self._mostrar_previa(salida if salida.strip() else "(sin salida todavia)")
        except subprocess.TimeoutExpired:
            self._mostrar_previa("[Vista previa] El programa tarda demasiado o espera datos (preguntar/bucles).")
        except Exception as e:
            self._mostrar_previa(f"[Vista previa] Error: {e}")

    def _mostrar_previa(self, texto):
        self.salida_previa.config(state="normal")
        self.salida_previa.delete("1.0", "end")
        self.salida_previa.insert("1.0", texto)
        self.salida_previa.config(state="disabled")

    # ------- Ventana de configuracion -------
    def abrir_configuracion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Configurar SiPi Editor")
        ventana.geometry("380x420")
        colores = self._colores()
        ventana.configure(bg=colores["barra"])

        tk.Label(ventana, text="Tema de colores", bg=colores["barra"], fg=colores["texto"],
                 font=("Segoe UI", 11, "bold")).pack(pady=(16, 6))

        var_tema = tk.StringVar(value=self.tema_actual)
        for nombre_tema in TEMAS:
            tk.Radiobutton(
                ventana, text=nombre_tema, variable=var_tema, value=nombre_tema,
                bg=colores["barra"], fg=colores["texto"], selectcolor=colores["fondo"],
                activebackground=colores["barra"], activeforeground=colores["texto"],
                font=("Segoe UI", 10),
                command=lambda v=var_tema: self._cambiar_tema(v.get())
            ).pack(anchor="w", padx=30)

        tk.Label(ventana, text="Tamaño de letra", bg=colores["barra"], fg=colores["texto"],
                 font=("Segoe UI", 11, "bold")).pack(pady=(20, 6))

        escala = tk.Scale(
            ventana, from_=9, to=24, orient=tk.HORIZONTAL, bg=colores["barra"],
            fg=colores["texto"], highlightthickness=0, troughcolor=colores["fondo"],
            command=lambda v: self._cambiar_tamano_fuente(int(v))
        )
        escala.set(self.tamano_fuente)
        escala.pack(fill=tk.X, padx=30)

        tk.Label(ventana, text="Vista previa en vivo", bg=colores["barra"], fg=colores["texto"],
                 font=("Segoe UI", 11, "bold")).pack(pady=(20, 6))

        var_previa = tk.BooleanVar(value=self.vista_previa_activa)
        tk.Checkbutton(
            ventana, text="Actualizar la vista previa mientras escribo", variable=var_previa,
            bg=colores["barra"], fg=colores["texto"], selectcolor=colores["fondo"],
            activebackground=colores["barra"], activeforeground=colores["texto"],
            font=("Segoe UI", 10),
            command=lambda: self._cambiar_vista_previa(var_previa.get())
        ).pack(anchor="w", padx=30)

        tk.Label(ventana, text="Color personalizado del texto", bg=colores["barra"],
                 fg=colores["texto"], font=("Segoe UI", 11, "bold")).pack(pady=(20, 6))
        tk.Button(ventana, text="Elegir color de texto...", command=self._elegir_color_texto,
                  bg="#313244", fg=colores["texto"], bd=0, padx=10, pady=6).pack()

        tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg="#40a02b", fg="white",
                  bd=0, padx=16, pady=8, font=("Segoe UI", 10, "bold")).pack(pady=24)

    def _cambiar_tema(self, nombre_tema):
        self.tema_actual = nombre_tema
        self._aplicar_tema()
        self._resaltar_sintaxis()

    def _cambiar_tamano_fuente(self, tamano):
        self.tamano_fuente = tamano
        self.texto.configure(font=("Consolas", tamano))
        self.numeros.configure(font=("Consolas", tamano))
        self._guardar_config()

    def _cambiar_vista_previa(self, activa):
        self.vista_previa_activa = activa
        self._guardar_config()
        if activa:
            self._programar_vista_previa()
        else:
            self._mostrar_previa("(vista previa desactivada)")

    def _elegir_color_texto(self):
        color = colorchooser.askcolor(title="Elegi el color del texto")[1]
        if color:
            colores_tema = dict(self._colores())
            colores_tema["texto"] = color
            TEMAS[self.tema_actual] = colores_tema
            self._aplicar_tema()

    # ------- Atajos de teclado, titulo, indicador de cambios (items 8, 10, F11) -------
    def _configurar_atajos_teclado(self):
        """Item 10 del feedback: atajos claros y sin conflictos entre si.

        Ctrl+S        Guardar
        Ctrl+Shift+S  Guardar como
        Ctrl+Enter/F5 Ejecutar
        F11           Pantalla completa
        Ctrl+Z/Ctrl+Y Deshacer/Rehacer (Tk ya trae Ctrl+Z; Ctrl+Y se agrega
                      explicitamente porque en Windows/Linux Tk no lo
                      mapea a 'redo' por defecto)
        Ctrl+F        Buscar
        Ctrl+H        Reemplazar
        """
        self.root.bind_all("<Control-s>", lambda e: (self.guardar(), "break")[1])
        self.root.bind_all("<Control-S>", lambda e: (self.guardar(), "break")[1])
        self.root.bind_all("<Control-Shift-S>", lambda e: (self.guardar_como(), "break")[1])
        self.root.bind_all("<Control-Return>", lambda e: (self.ejecutar(), "break")[1])
        self.root.bind_all("<F5>", lambda e: (self.ejecutar(), "break")[1])
        self.root.bind_all("<F11>", self._alternar_pantalla_completa)
        self.root.bind_all("<Escape>", self._salir_pantalla_completa)
        self.texto.bind("<Control-y>", lambda e: (self.texto.edit_redo(), "break")[1])
        self.texto.bind("<Control-Y>", lambda e: (self.texto.edit_redo(), "break")[1])
        self.root.bind_all("<Control-f>", lambda e: (self.abrir_buscar(), "break")[1])
        self.root.bind_all("<Control-h>", lambda e: (self.abrir_reemplazar(), "break")[1])
        self.root.bind_all("<Control-t>", lambda e: (self.nueva_pestana(), "break")[1])
        self.root.bind_all("<Control-w>", lambda e: (self._cerrar_pestana(self.indice_pestana_actual), "break")[1])
        self.root.bind_all("<Control-grave>", lambda e: (self._alternar_panel_terminal(), "break")[1])
        self.root.bind_all("<Control-g>", lambda e: (self.abrir_ir_a_linea(), "break")[1])
        self.texto.bind("<KeyRelease>", self._resaltar_bracket_pareja, add="+")
        self.texto.bind("<ButtonRelease-1>", self._resaltar_bracket_pareja, add="+")
        self._pantalla_completa = False

    def _alternar_pantalla_completa(self, evento=None):
        """Bug #5 del feedback: F11 no hacia nada porque no habia ningun
        binding para esa tecla en todo el editor (se confirmo grepeando
        el archivo entero: cero resultados para 'F11'/'fullscreen' antes
        de este cambio). 'attributes(-fullscreen', ...)' es la forma
        correcta en Tk multiplataforma (Windows/Linux/Mac), a diferencia
        de maximizar la ventana con 'state(zoomed)' que en Windows dejaria
        la barra de titulo visible."""
        self._pantalla_completa = not self._pantalla_completa
        self.root.attributes("-fullscreen", self._pantalla_completa)
        return "break"

    def _salir_pantalla_completa(self, evento=None):
        if getattr(self, "_pantalla_completa", False):
            self._pantalla_completa = False
            self.root.attributes("-fullscreen", False)
        return "break"

    # ------- Ir a linea (item 19) -------
    def abrir_ir_a_linea(self):
        colores = self._colores()
        ventana = tk.Toplevel(self.root)
        ventana.title("Ir a linea")
        ventana.configure(bg=colores["barra"])
        ventana.transient(self.root)
        total_lineas = int(self.texto.index("end-1c").split(".")[0])
        tk.Label(ventana, text=f"Numero de linea (1-{total_lineas}):",
                 bg=colores["barra"], fg=colores["texto"]).pack(padx=10, pady=(10, 4))
        entrada = tk.Entry(ventana, width=10)
        entrada.pack(padx=10, pady=4)
        entrada.focus_set()

        def _ir():
            texto = entrada.get().strip()
            if not texto.isdigit():
                return
            numero = max(1, min(int(texto), total_lineas))
            self.texto.mark_set("insert", f"{numero}.0")
            self.texto.see(f"{numero}.0")
            self.texto.tag_remove("sel", "1.0", "end")
            self.texto.tag_add("sel", f"{numero}.0", f"{numero}.end")
            self.texto.focus_set()
            ventana.destroy()

        entrada.bind("<Return>", lambda e: _ir())
        tk.Button(ventana, text="Ir", command=_ir).pack(padx=10, pady=(4, 10))

    # ------- Bracket matching (item 22) -------
    _PARES_BRACKETS = {"(": ")", "[": "]", "{": "}"}
    _PARES_BRACKETS_INVERSO = {")": "(", "]": "[", "}": "{"}

    def _resaltar_bracket_pareja(self, evento=None):
        """Cuando el cursor esta pegado a un parentesis/corchete/llave,
        busca su pareja (respetando anidamiento -- un '(' de mas adentro
        no hace match con el primer ')' que aparezca, cuenta niveles) y
        resalta ambos. Se limpia el resaltado si el cursor no esta al
        lado de ninguno."""
        self.texto.tag_remove("bracket_pareja", "1.0", "end")
        pos_cursor = self.texto.index("insert")
        candidatos = [pos_cursor]
        # También revisa el caracter inmediatamente ANTES del cursor (caso
        # tipico: usuario acaba de escribir ')' y el cursor quedo despues).
        candidatos.append(self.texto.index(f"{pos_cursor}-1c"))
        for pos in candidatos:
            caracter = self.texto.get(pos)
            if caracter in self._PARES_BRACKETS or caracter in self._PARES_BRACKETS_INVERSO:
                pareja = self._buscar_bracket_pareja(pos, caracter)
                if pareja:
                    self.texto.tag_add("bracket_pareja", pos, f"{pos}+1c")
                    self.texto.tag_add("bracket_pareja", pareja, f"{pareja}+1c")
                    self.texto.tag_configure("bracket_pareja", background="#585b70", foreground="#f9e2af")
                return

    def _buscar_bracket_pareja(self, pos, caracter):
        contenido = self.texto.get("1.0", "end-1c")
        indice_plano = len(self.texto.get("1.0", pos))
        if caracter in self._PARES_BRACKETS:
            objetivo, cierre, direccion = self._PARES_BRACKETS[caracter], caracter, 1
            nivel = 1
            i = indice_plano + 1
            while i < len(contenido):
                if contenido[i] == caracter:
                    nivel += 1
                elif contenido[i] == objetivo:
                    nivel -= 1
                    if nivel == 0:
                        return self.texto.index(f"1.0+{i}c")
                i += 1
        else:
            objetivo = self._PARES_BRACKETS_INVERSO[caracter]
            nivel = 1
            i = indice_plano - 1
            while i >= 0:
                if contenido[i] == caracter:
                    nivel += 1
                elif contenido[i] == objetivo:
                    nivel -= 1
                    if nivel == 0:
                        return self.texto.index(f"1.0+{i}c")
                i -= 1
        return None

    def _marcar_modificado(self):
        if not self.modificado:
            self.modificado = True
            self._actualizar_titulo()
            if self.pestanas:
                self.pestanas[self.indice_pestana_actual]["modificado"] = True
                self._redibujar_barra_pestanas()
        self._programar_autoguardado_recuperacion()

    def _programar_autoguardado_recuperacion(self):
        """Item 9: guarda un snapshot de recuperacion 2 segundos despues
        de la ultima tecla (debounced, igual que la vista previa, para no
        escribir a disco en cada tecla), no el archivo real del usuario
        -- si SiPi se cierra de golpe (falla electrica, cierre por error,
        crash), este snapshot es lo que se ofrece recuperar al reabrir."""
        if getattr(self, "_tarea_autoguardado", None):
            self.root.after_cancel(self._tarea_autoguardado)
        self._tarea_autoguardado = self.root.after(2000, self._guardar_snapshot_recuperacion)

    def _guardar_snapshot_recuperacion(self):
        import time
        datos = {
            "ruta": self.archivo_actual,
            "contenido": self.texto.get("1.0", "end-1c"),
            "fecha": time.time(),
        }
        try:
            with open(ARCHIVO_RECUPERACION, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False)
        except OSError:
            pass  # la recuperacion es un extra, nunca debe interrumpir al usuario

    def _borrar_snapshot_recuperacion(self):
        try:
            os.remove(ARCHIVO_RECUPERACION)
        except OSError:
            pass

    def _ofrecer_recuperacion_si_corresponde(self):
        """Se llama una sola vez, apenas arranca el editor. Si hay un
        snapshot de una sesion anterior que nunca se borro (es decir, esa
        sesion nunca cerro limpio), se le pregunta al usuario si lo quiere
        recuperar -- y se le muestra que archivo era y cuando, para que
        decida con contexto."""
        if not os.path.exists(ARCHIVO_RECUPERACION):
            return
        try:
            with open(ARCHIVO_RECUPERACION, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (OSError, json.JSONDecodeError):
            self._borrar_snapshot_recuperacion()
            return
        import time
        antiguedad_min = (time.time() - datos.get("fecha", 0)) / 60
        nombre = datos.get("ruta") or "(sin guardar)"
        quiere = messagebox.askyesno(
            "SiPi",
            f"Se encontro trabajo sin guardar de una sesion anterior que se cerro "
            f"sin guardar (hace {antiguedad_min:.0f} minuto(s)):\n\n{nombre}\n\n"
            f"¿Deseas recuperar ese trabajo?"
        )
        if quiere:
            self.texto.delete("1.0", "end")
            self.texto.insert("1.0", datos.get("contenido", ""))
            if datos.get("ruta") and os.path.exists(datos["ruta"]):
                self.archivo_actual = datos["ruta"]
            self.modificado = True
            self._actualizar_titulo()
            self._resaltar_sintaxis()
            self._actualizar_numeros_linea()
            self._programar_vista_previa()
            self._actualizar_selector_nivel_desde_codigo()
            self.estado.config(text="Trabajo recuperado de la sesion anterior.")
        self._borrar_snapshot_recuperacion()

    def _actualizar_titulo(self):
        """Item 8: 'main.sipi *' en la barra de titulo cuando hay cambios
        sin guardar, igual que cualquier IDE."""
        nombre = os.path.basename(self.archivo_actual) if self.archivo_actual else "Sin titulo"
        marca = " *" if self.modificado else ""
        self.root.title(f"SiPi - Editor Visual - {nombre}{marca}")

    def _limpiar_carpeta_temporal(self):
        shutil.rmtree(self.carpeta_temporal_ejecucion, ignore_errors=True)

    def _al_cerrar_ventana(self):
        # Item 14: al cerrar el editor entero, hay que revisar TODAS las
        # pestañas por cambios sin guardar, no solo la que esta activa en
        # este momento -- si no, cerrar con una pestaña de fondo
        # modificada perderia ese trabajo en silencio.
        self._guardar_estado_pestana_actual()
        for idx, pestana in enumerate(self.pestanas):
            if not pestana["modificado"]:
                continue
            nombre = self._texto_pestana(pestana)
            respuesta = messagebox.askyesnocancel(
                "SiPi", f"'{nombre}' tiene cambios sin guardar. ¿Queres guardarlos antes de salir?"
            )
            if respuesta is None:
                return
            if respuesta:
                archivo_previo, indice_previo = self.archivo_actual, self.indice_pestana_actual
                contenido_previo = self.texto.get("1.0", "end-1c")
                self.texto.delete("1.0", "end")
                self.texto.insert("1.0", pestana["contenido"])
                self.archivo_actual, self.indice_pestana_actual, self.modificado = pestana["archivo"], idx, True
                self.guardar_si_hace_falta()
                if self.modificado:
                    # Se cancelo el "Guardar como" de esta pestaña: se
                    # restaura la vista y se aborta el cierre entero.
                    self.texto.delete("1.0", "end")
                    self.texto.insert("1.0", contenido_previo)
                    self.archivo_actual, self.indice_pestana_actual = archivo_previo, indice_previo
                    return
                self.texto.delete("1.0", "end")
                self.texto.insert("1.0", contenido_previo)
                self.archivo_actual, self.indice_pestana_actual = archivo_previo, indice_previo
        # Cierre limpio (el usuario dijo explicitamente que no quiere
        # guardar, o ya no habia cambios pendientes): no tiene sentido
        # ofrecer "recuperar" este mismo contenido la proxima vez.
        self._borrar_snapshot_recuperacion()
        self._limpiar_carpeta_temporal()
        # Cancela callbacks 'after' pendientes (autoguardado, oferta de
        # recuperacion) antes de destruir la ventana -- si no, Tk imprime
        # un error benigno pero confuso a stderr cuando el callback
        # intenta dispararse contra un widget que ya no existe.
        for id_pendiente in (getattr(self, "_tarea_autoguardado", None),
                              getattr(self, "_id_recuperacion_pendiente", None),
                              self.tarea_pendiente):
            if id_pendiente:
                try:
                    self.root.after_cancel(id_pendiente)
                except Exception:
                    pass
        self.root.destroy()

    # ------- Archivo -------
    def nuevo(self):
        # Con pestañas, "Nuevo" abre una pestaña nueva en vez de
        # reemplazar el contenido de la actual (evita perder trabajo por
        # error si el usuario tenia algo sin guardar en la pestaña
        # activa).
        self.nueva_pestana()
        self.estado.config(text="Nuevo archivo.")

    def abrir(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos SiPi", "*.sipi"), ("Todos", "*.*")])
        if ruta:
            self._abrir_ruta(ruta)

    def _abrir_ruta(self, ruta):
        """Logica real de abrir un archivo en una pestaña, separada de
        'abrir()' (que solo se encarga del dialogo de seleccion) para que
        el explorador de archivos (item 13 del feedback) pueda abrir un
        archivo con un doble clic sin pasar por un filedialog."""
        indice_existente = self._indice_pestana_para_archivo(ruta)
        if indice_existente is not None:
            self._cambiar_a_pestana(indice_existente)
            self.estado.config(text=f"Ya estaba abierto: {ruta}")
            return
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        pestana_actual = self.pestanas[self.indice_pestana_actual]
        # Si la pestaña activa esta vacia y sin usar (recien creada, sin
        # archivo ni cambios), se reutiliza en vez de abrir una pestaña
        # de mas -- asi "Abrir" en un editor recien iniciado no deja una
        # pestaña "Sin titulo" vacia dando vueltas sin motivo.
        if pestana_actual["archivo"] is None and not pestana_actual["modificado"] and \
                self.texto.get("1.0", "end-1c") == "":
            self.texto.delete("1.0", "end")
            self.texto.insert("1.0", contenido)
            self.archivo_actual = ruta
            self.modificado = False
        else:
            self._guardar_estado_pestana_actual()
            self.pestanas.append({"archivo": ruta, "contenido": contenido, "modificado": False})
            self.indice_pestana_actual = len(self.pestanas) - 1
            self.texto.delete("1.0", "end")
            self.texto.insert("1.0", contenido)
            self.archivo_actual = ruta
            self.modificado = False
        self._actualizar_titulo()
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self._redibujar_barra_pestanas()
        self._programar_vista_previa()
        self._actualizar_selector_nivel_desde_codigo()
        self.estado.config(text=f"Abierto: {ruta}")

    def guardar(self):
        if not self.archivo_actual:
            return self.guardar_como()
        with open(self.archivo_actual, "w", encoding="utf-8") as f:
            f.write(self.texto.get("1.0", "end-1c"))
        self.modificado = False
        self._actualizar_titulo()
        self._borrar_snapshot_recuperacion()
        if self.pestanas:
            pestana = self.pestanas[self.indice_pestana_actual]
            pestana["archivo"] = self.archivo_actual
            pestana["modificado"] = False
            self._redibujar_barra_pestanas()
        self.estado.config(text=f"Guardado: {self.archivo_actual}")

    def guardar_como(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".sipi",
                                             filetypes=[("Archivos SiPi", "*.sipi")])
        if ruta:
            self.archivo_actual = ruta
            self.guardar()

    def guardar_si_hace_falta(self):
        if self.archivo_actual:
            self.guardar()
        else:
            self.guardar_como()

    # ------- Ejecucion y compilacion reales -------
    def _ruta_para_ejecutar_contenido_actual(self):
        """Items 6/7 del feedback ("ejecutar sin guardar"): antes, Ejecutar
        exigia 'guardar_si_hace_falta()' y si el usuario cancelaba el
        dialogo de 'Guardar como', mostraba una advertencia y no corria
        nada. Ahora: si el archivo ya esta guardado y sin cambios, se usa
        esa ruta real tal cual (asi el codigo puede hacer cosas como
        leer archivos relativos a su propia carpeta). Si no -- sin
        guardar todavia, o con cambios pendientes -- se escribe el
        contenido actual del editor a un archivo dentro de
        'carpeta_temporal_ejecucion' (creada una sola vez en __init__ y
        NO borrada hasta cerrar el editor), preservando el nombre
        original si existe. El usuario ni se entera: escribe y ejecuta,
        sin que 'Guardar' sea un paso obligatorio en el medio."""
        if self.archivo_actual and not self.modificado and os.path.exists(self.archivo_actual):
            return self.archivo_actual, False
        nombre_base = os.path.basename(self.archivo_actual) if self.archivo_actual else "sin_titulo.sipi"
        ruta_temporal = os.path.join(self.carpeta_temporal_ejecucion, nombre_base)
        with open(ruta_temporal, "w", encoding="utf-8") as f:
            f.write(self.texto.get("1.0", "end-1c"))
        self._ruta_temporal_actual = ruta_temporal
        return ruta_temporal, True

    def ejecutar(self):
        ruta_a_ejecutar, es_temporal = self._ruta_para_ejecutar_contenido_actual()
        aqui = os.path.dirname(os.path.abspath(__file__))
        try:
            sipi_py = self._ruta_motor_sipi(aqui)
        except ImportError as error:
            self._mostrar_error_motor_no_encontrado(aqui, error)
            return
        aviso_temporal = " (sin guardar todavia -- corriendo desde una copia temporal)" if es_temporal else ""
        self.estado.config(text=f"Ejecutando{aviso_temporal} (juegos y ventanas se abren en su propia ventana real)...")
        if os.name == "nt":
            # 'chcp 65001' fuerza la consola nueva a UTF-8 antes de correr
            # el programa -- sin esto, tildes/emojis salian como
            # caracteres raros aunque sipi.py ya reconfigura su propio
            # stdout a UTF-8 (la consola de Windows seguia leyendolo con
            # su codepage viejo, cp850/cp1252, por defecto).
            subprocess.Popen(f'start cmd /k chcp 65001 >nul && python "{sipi_py}" "{ruta_a_ejecutar}"', shell=True)
        else:
            subprocess.Popen([sys.executable, sipi_py, ruta_a_ejecutar])
        self.estado.config(text=f"Ejecutado: {ruta_a_ejecutar}{aviso_temporal}")

    def _mostrar_error_motor_no_encontrado(self, aqui, error):
        """Item 4 del feedback ("manejo de errores"): en vez de dejar
        pasar un '[Errno 2] No such file or directory' crudo de Python
        (el mensaje real que vio el tester en Windows), se explica que se
        busco, donde, y la causa mas probable (carpeta ejecutandose desde
        un ZIP sin extraer, o un antivirus/limpiador de temporales que
        borro el archivo)."""
        mensaje = (
            "[SiPi] No se encontro 'sipi.py' ni 'sipi_protegido.py'.\n\n"
            f"Carpeta donde se busco:\n{aqui}\n\n"
            "Causas mas probables:\n"
            " - Estas ejecutando SiPi directamente desde adentro de un archivo\n"
            "   .zip descargado (por ejemplo, haciendo doble clic sin extraer\n"
            "   primero). Extrae el .zip completo a una carpeta normal del\n"
            "   disco (no dentro de Temp) y volve a intentar.\n"
            " - Un antivirus o limpiador de temporales borro el archivo\n"
            "   despues de que se extrajo.\n\n"
            f"Detalle tecnico: {error}"
        )
        messagebox.showerror("SiPi", mensaje)
        self.estado.config(text="Error: no se encontro el motor de SiPi.")

    # ------- Buscar y reemplazar (item 15) -------
    def abrir_buscar(self):
        self._abrir_dialogo_busqueda(con_reemplazo=False)

    def abrir_reemplazar(self):
        self._abrir_dialogo_busqueda(con_reemplazo=True)

    def _abrir_dialogo_busqueda(self, con_reemplazo):
        colores = self._colores()
        ventana = tk.Toplevel(self.root)
        ventana.title("Reemplazar" if con_reemplazo else "Buscar")
        ventana.configure(bg=colores["barra"])
        ventana.transient(self.root)

        tk.Label(ventana, text="Buscar:", bg=colores["barra"], fg=colores["texto"]).grid(
            row=0, column=0, padx=6, pady=6, sticky="e")
        entrada_buscar = tk.Entry(ventana, width=30)
        entrada_buscar.grid(row=0, column=1, padx=6, pady=6)
        entrada_buscar.focus_set()

        entrada_reemplazo = None
        if con_reemplazo:
            tk.Label(ventana, text="Reemplazar por:", bg=colores["barra"], fg=colores["texto"]).grid(
                row=1, column=0, padx=6, pady=6, sticky="e")
            entrada_reemplazo = tk.Entry(ventana, width=30)
            entrada_reemplazo.grid(row=1, column=1, padx=6, pady=6)

        etiqueta_resultado = tk.Label(ventana, text="", bg=colores["barra"], fg="#a6adc8")
        etiqueta_resultado.grid(row=2, column=0, columnspan=2)

        def _limpiar_resaltado():
            self.texto.tag_remove("busqueda", "1.0", "end")

        def _buscar_todas(mostrar_resultado=True):
            _limpiar_resaltado()
            self.texto.tag_configure("busqueda", background="#f9c74f", foreground="#1e1e2e")
            objetivo = entrada_buscar.get()
            if not objetivo:
                return 0
            cantidad = 0
            inicio = "1.0"
            while True:
                pos = self.texto.search(objetivo, inicio, stopindex="end")
                if not pos:
                    break
                fin = f"{pos}+{len(objetivo)}c"
                self.texto.tag_add("busqueda", pos, fin)
                inicio = fin
                cantidad += 1
            if mostrar_resultado:
                etiqueta_resultado.config(
                    text=f"{cantidad} coincidencia(s)." if cantidad else "Sin coincidencias.")
            return cantidad

        def _reemplazar_todas():
            objetivo = entrada_buscar.get()
            nuevo = entrada_reemplazo.get() if entrada_reemplazo else ""
            if not objetivo:
                return
            contenido = self.texto.get("1.0", "end-1c")
            cantidad = contenido.count(objetivo)
            contenido = contenido.replace(objetivo, nuevo)
            self.texto.delete("1.0", "end")
            self.texto.insert("1.0", contenido)
            self._marcar_modificado()
            self._resaltar_sintaxis()
            self._actualizar_numeros_linea()
            etiqueta_resultado.config(text=f"{cantidad} reemplazo(s) hecho(s).")

        botones = tk.Frame(ventana, bg=colores["barra"])
        botones.grid(row=3, column=0, columnspan=2, pady=(0, 8))
        tk.Button(botones, text="Buscar", command=_buscar_todas).pack(side=tk.LEFT, padx=4)
        if con_reemplazo:
            tk.Button(botones, text="Reemplazar todas", command=_reemplazar_todas).pack(side=tk.LEFT, padx=4)
        entrada_buscar.bind("<Return>", lambda e: _buscar_todas())

        def _al_cerrar():
            _limpiar_resaltado()
            ventana.destroy()
        ventana.protocol("WM_DELETE_WINDOW", _al_cerrar)

    def compilar_exe(self):
        # A diferencia de Ejecutar, compilar a .exe si necesita un archivo
        # real y permanente (PyInstaller lee del disco, no de un stdin ni
        # de un temporal que podria desaparecer a mitad de la compilacion,
        # que puede tardar bastante mas que una ejecucion normal).
        self.guardar_si_hace_falta()
        if not self.archivo_actual:
            messagebox.showwarning("SiPi", "Guarda el archivo antes de compilarlo.")
            return
        aqui = os.path.dirname(os.path.abspath(__file__))
        try:
            generar_exe = self._ruta_generar_exe(aqui)
        except ImportError as error:
            self._mostrar_error_motor_no_encontrado(aqui, error)
            return
        self.estado.config(text="Compilando a ejecutable, mira la consola...")
        if os.name == "nt":
            subprocess.Popen(f'start cmd /k python "{generar_exe}" "{self.archivo_actual}"', shell=True)
        else:
            subprocess.Popen([sys.executable, generar_exe, self.archivo_actual])

    # ------- Depurador visual paso a paso -------
    def abrir_depurador(self):
        self.guardar_si_hace_falta()
        if not self.archivo_actual:
            messagebox.showwarning("SiPi", "Guarda el archivo antes de depurarlo.")
            return
        if re.search(r"\bventana\b|\bcrear_juego\b", self.texto.get("1.0", "end-1c")):
            messagebox.showinfo(
                "SiPi",
                "El depurador visual esta pensado para programas de consola.\n"
                "Los programas con 'ventana' o 'crear_juego' abren su propia ventana real; "
                "usa el boton ▶ Ejecutar para esos casos."
            )
            return
        VentanaDepurador(self.root, self.archivo_actual, self._colores())

    def formatear_codigo_actual(self):
        aqui = os.path.dirname(os.path.abspath(__file__))
        motor_sipi = _cargar_motor_sipi(aqui)

        contenido_actual = self.texto.get("1.0", "end-1c")
        lineas_originales = contenido_actual.split("\n")

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
            elif palabra in motor_sipi.PALABRAS_MISMO_NIVEL:
                resultado.append("    " * max(0, nivel - 1) + limpia)
            else:
                resultado.append("    " * nivel + limpia)
                if palabra in motor_sipi.PALABRAS_APERTURA_BLOQUE:
                    nivel += 1

        texto_formateado = "\n".join(resultado)
        if texto_formateado == contenido_actual.rstrip("\n"):
            self.estado.config(text="El codigo ya estaba formateado correctamente.")
            return
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", texto_formateado)
        self._resaltar_sintaxis()
        self._actualizar_numeros_linea()
        self.estado.config(text="Codigo formateado (reindentado con 4 espacios por nivel).")


class VentanaDepurador:
    """Depurador visual real: ejecuta el programa paso a paso en un hilo
    aparte, mostrando en vivo el valor de las variables, listas y
    diccionarios, con soporte de breakpoints (clic en el numero de linea)."""

    def __init__(self, root_padre, archivo, colores):
        aqui = os.path.dirname(os.path.abspath(__file__))
        motor_sipi = _cargar_motor_sipi(aqui)
        self.motor_sipi = motor_sipi

        self.archivo = archivo
        self.colores = colores
        self.breakpoints = set()
        self.evento_continuar = threading.Event()
        self.modo_paso = True
        self.detener = False
        self.hilo = None
        self.interprete = None

        # Item 8 de tu feedback: "viaje en el tiempo". Guardamos una foto de
        # las variables en CADA paso ejecutado, para poder navegar hacia
        # atras y ver como estaban las cosas antes -- sin re-ejecutar nada
        # (el programa real no se puede "deshacer" si ya imprimio algo o
        # escribio un archivo), es un historial de solo lectura para mirar
        # atras y entender en que paso una variable tomo el valor que no
        # esperabas.
        self.historial = []  # lista de {"linea": int, "variables": dict, "locales": dict}
        self.indice_historial = None  # None = viendo el paso en vivo

        self.ventana = tk.Toplevel(root_padre)
        self.ventana.title(f"SiPi - Depurador: {os.path.basename(archivo)}")
        self.ventana.geometry("900x600")
        self.ventana.configure(bg=colores["barra"])

        self._crear_interfaz()
        self._cargar_codigo_fuente()
        self._iniciar_sesion()

    def _crear_interfaz(self):
        colores = self.colores
        barra = tk.Frame(self.ventana, bg=colores["barra"])
        barra.pack(side=tk.TOP, fill=tk.X)

        estilo = {"bg": "#313244", "fg": "white", "bd": 0, "padx": 12, "pady": 6, "font": ("Segoe UI", 10)}
        tk.Button(barra, text="⏪ Retroceder", command=self.retroceder, **estilo).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(barra, text="⏩ Adelante", command=self.avanzar, **estilo).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(barra, text="⏭ Paso", command=self.paso, **estilo).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(barra, text="▶ Continuar", command=self.continuar, **estilo).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(barra, text="⏹ Detener", command=self.detener_sesion, bg="#d20f39",
                  fg="white", bd=0, padx=12, pady=6, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Label(barra, text="  Clic en el numero de linea para poner/quitar un breakpoint",
                 bg=colores["barra"], fg="#a6adc8", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10)

        contenedor = tk.PanedWindow(self.ventana, orient=tk.HORIZONTAL, bg=colores["fondo"], sashwidth=6, bd=0)
        contenedor.pack(fill=tk.BOTH, expand=True)

        panel_codigo = tk.Frame(contenedor, bg=colores["fondo"])
        self.numeros = tk.Text(panel_codigo, width=4, bg=colores["barra"], fg="#6c7086",
                                bd=0, font=("Consolas", 11))
        self.numeros.pack(side=tk.LEFT, fill=tk.Y)
        self.numeros.bind("<Button-1>", self._al_clic_numero)

        self.codigo = tk.Text(panel_codigo, bg=colores["fondo"], fg=colores["texto"], bd=0,
                               font=("Consolas", 11), wrap="none", state="disabled")
        self.codigo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.codigo.tag_configure("linea_actual", background="#45475a")
        self.numeros.tag_configure("con_breakpoint", background="#d20f39", foreground="white")
        contenedor.add(panel_codigo, minsize=350)

        panel_variables = tk.Frame(contenedor, bg=colores["barra"])
        tk.Label(panel_variables, text="Variables en vivo", bg=colores["barra"], fg=colores["texto"],
                 font=("Segoe UI", 11, "bold"), anchor="w", padx=8, pady=6).pack(side=tk.TOP, fill=tk.X)
        self.panel_vars = tk.Text(panel_variables, bg="#11111b", fg="#cdd6f4", bd=0,
                                   font=("Consolas", 10), state="disabled", wrap="word")
        self.panel_vars.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))
        contenedor.add(panel_variables, minsize=250)

        self.estado = tk.Label(self.ventana, text="Preparando sesion de depuracion...",
                                bg=colores["barra"], fg="#a6adc8", anchor="w",
                                font=("Segoe UI", 9), padx=8, pady=4)
        self.estado.pack(side=tk.BOTTOM, fill=tk.X)

    def _cargar_codigo_fuente(self):
        with open(self.archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        total_lineas = contenido.count("\n") + 1
        self.numeros.delete("1.0", "end")
        self.numeros.insert("1.0", "\n".join(str(n) for n in range(1, total_lineas + 1)))
        self.codigo.config(state="normal")
        self.codigo.delete("1.0", "end")
        self.codigo.insert("1.0", contenido)
        self.codigo.config(state="disabled")

    def _al_clic_numero(self, evento):
        indice = self.numeros.index(f"@{evento.x},{evento.y}")
        num_linea = int(indice.split(".")[0])
        if num_linea in self.breakpoints:
            self.breakpoints.discard(num_linea)
        else:
            self.breakpoints.add(num_linea)
        self._repintar_breakpoints()

    def _repintar_breakpoints(self):
        self.numeros.tag_remove("con_breakpoint", "1.0", "end")
        for num_linea in self.breakpoints:
            self.numeros.tag_add("con_breakpoint", f"{num_linea}.0", f"{num_linea}.end+1c")

    def _iniciar_sesion(self):
        self.interprete = self.motor_sipi.Interprete(self.archivo)
        self.interprete.hook_linea = self._al_llegar_a_linea

        def ejecutar_programa():
            try:
                self.interprete.ejecutar()
                if not self.detener:
                    self.ventana.after(0, lambda: self.estado.config(text="Programa terminado correctamente."))
            except self.motor_sipi.SiPiError as e:
                mensaje = str(e)
                self.ventana.after(0, lambda: self.estado.config(text=f"Error: {mensaje}"))
            except Exception as e:
                mensaje = str(e)
                self.ventana.after(0, lambda: self.estado.config(text=f"Error inesperado: {mensaje}"))

        self.hilo = threading.Thread(target=ejecutar_programa, daemon=True)
        self.hilo.start()

    def _al_llegar_a_linea(self, num, linea):
        """Se ejecuta DESDE EL HILO del programa SiPi antes de cada linea."""
        if self.detener:
            # Antes se usaba RetornoFuncion para cortar la ejecucion, pero si
            # el programa estaba dentro de una llamada a funcion en ese
            # momento, esa misma funcion atrapaba el RetornoFuncion como si
            # fuera un 'devolver' normal, y el programa seguia corriendo en
            # vez de detenerse (el boton "Detener" no detenia nada si el
            # breakpoint caia dentro de una funcion). Ahora se usa una
            # excepcion dedicada que ninguna llamada a funcion atrapa.
            raise self.motor_sipi.DepuracionDetenida()

        snapshot_variables = dict(self.interprete.entorno.variables)
        # Si estamos dentro de una llamada a funcion, tambien mostramos las
        # variables locales de esa llamada (antes solo se mostraban las
        # globales, asi que dentro de una funcion el panel "Variables en
        # vivo" aparecia vacio o incompleto, aunque la funcion si tuviera
        # variables propias).
        pila_local = list(getattr(self.interprete, "pila_scopes", []))
        snapshot_locales = dict(pila_local[-1]) if pila_local else {}
        self.historial.append({"linea": num, "variables": snapshot_variables, "locales": snapshot_locales})
        self.ventana.after(0, lambda: self._actualizar_vista(num, snapshot_variables, snapshot_locales))

        if num in self.breakpoints or self.modo_paso:
            self.evento_continuar.clear()
            self.evento_continuar.wait()

    def _actualizar_vista(self, num_linea, variables, locales=None, viendo_historial=False):
        self.codigo.tag_remove("linea_actual", "1.0", "end")
        self.codigo.tag_add("linea_actual", f"{num_linea}.0", f"{num_linea}.end+1c")
        self.codigo.see(f"{num_linea}.0")
        if viendo_historial:
            total = len(self.historial)
            self.estado.config(
                text=f"Viendo historial (paso {self.indice_historial + 1} de {total}) - "
                     f"solo lectura, linea {num_linea}. Usa 'Adelante' para volver al presente."
            )
        else:
            self.estado.config(text=f"Ejecutando linea {num_linea}...")

        self.panel_vars.config(state="normal")
        self.panel_vars.delete("1.0", "end")
        if locales:
            self.panel_vars.insert("end", "-- Variables locales (funcion actual) --\n")
            for nombre, valor in locales.items():
                self.panel_vars.insert("end", f"{nombre} = {valor!r}\n")
            self.panel_vars.insert("end", "\n-- Variables globales --\n")
        if not variables and not locales:
            self.panel_vars.insert("1.0", "(sin variables todavia)")
        else:
            for nombre, valor in variables.items():
                self.panel_vars.insert("end", f"{nombre} = {valor!r}\n")
        self.panel_vars.config(state="disabled")

    def retroceder(self):
        """Item 8: navega un paso hacia atras en el historial grabado, sin
        tocar la ejecucion real (que sigue pausada donde estaba). Es una
        vista de solo lectura para entender como llegaron las variables a
        su valor actual."""
        if not self.historial:
            return
        if self.indice_historial is None:
            self.indice_historial = len(self.historial) - 1
        if self.indice_historial > 0:
            self.indice_historial -= 1
        paso = self.historial[self.indice_historial]
        self._actualizar_vista(paso["linea"], paso["variables"], paso["locales"], viendo_historial=True)

    def avanzar(self):
        """Complemento de retroceder(): avanza un paso en el historial ya
        grabado. Si llega al ultimo paso grabado, vuelve al modo 'en vivo'
        normal (siguiendo la ejecucion real, no una foto vieja)."""
        if self.indice_historial is None or not self.historial:
            return
        if self.indice_historial >= len(self.historial) - 1:
            self.indice_historial = None
            paso = self.historial[-1]
            self._actualizar_vista(paso["linea"], paso["variables"], paso["locales"], viendo_historial=False)
            return
        self.indice_historial += 1
        paso = self.historial[self.indice_historial]
        viendo_pasado = self.indice_historial < len(self.historial) - 1
        self._actualizar_vista(paso["linea"], paso["variables"], paso["locales"], viendo_historial=viendo_pasado)

    def paso(self):
        # Si el usuario estaba mirando el historial hacia atras, 'Paso'
        # vuelve primero al presente antes de avanzar la ejecucion real --
        # avanzar la ejecucion de verdad solo tiene sentido desde el estado
        # actual, no desde una foto vieja.
        self.indice_historial = None
        self.modo_paso = True
        self.evento_continuar.set()

    def continuar(self):
        self.indice_historial = None
        self.modo_paso = False
        self.evento_continuar.set()

    def detener_sesion(self):
        self.detener = True
        self.evento_continuar.set()
        self.estado.config(text="Sesion de depuracion detenida por el usuario.")


def _advertir_si_carpeta_volatil(aqui):
    """Bug #3/#1 del feedback: el error real que vio el tester en Windows
    ("can't open file ...\\Temp\\...\\SiPi-main\\sipi_protegido.py") pasa
    cuando SiPi entero se esta ejecutando desde ADENTRO de la carpeta
    temporal de Windows -- tipicamente porque se abrio el .zip descargado
    con doble clic y se corrio un .bat desde ahi sin extraerlo primero a
    una carpeta normal del disco. Windows (y algunos antivirus) limpian
    esa carpeta temporal en cualquier momento, incluso a mitad de la
    ejecucion, asi que un archivo que existia hace un segundo desaparece
    sin aviso. Se detecta comparando la carpeta real del editor contra la
    carpeta temporal del sistema, y se avisa ANTES de que se rompa nada,
    en vez de dejar que aparezca un traceback confuso mas tarde."""
    try:
        temporal = os.path.normcase(os.path.abspath(tempfile.gettempdir()))
        actual = os.path.normcase(os.path.abspath(aqui))
        if actual.startswith(temporal):
            print("=" * 70)
            print("[SiPi] Aviso: parece que estas ejecutando SiPi desde una carpeta")
            print("       temporal del sistema:")
            print(f"       {aqui}")
            print()
            print("       Esto normalmente pasa cuando se abre el .zip descargado")
            print("       haciendo doble clic y se corre un archivo desde ADENTRO")
            print("       del .zip, sin extraerlo primero. Windows puede borrar esa")
            print("       carpeta temporal en cualquier momento (incluso mientras")
            print("       SiPi esta corriendo), lo que causa errores como")
            print("       '[Errno 2] No such file or directory'.")
            print()
            print("       Recomendado: extrae el .zip completo a una carpeta normal")
            print("       (por ejemplo, tu Escritorio o Documentos) y volve a correr")
            print("       SiPi desde ahi.")
            print("=" * 70)
            return True
    except OSError:
        pass
    return False


def main():
    aqui = os.path.dirname(os.path.abspath(__file__))
    _advertir_si_carpeta_volatil(aqui)
    root = tk.Tk()
    EditorSiPi(root)
    root.mainloop()


if __name__ == "__main__":
    main()
