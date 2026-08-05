#!/usr/bin/env python3
"""
generar_docs.py - Item 3 de tu feedback: sistema de "docstrings" y
generacion de documentacion automatica para SiPi.

Permite escribir comentarios especiales dentro de funciones y clases:

    funcion sumar(a, b)
        //! Suma dos numeros y devuelve el resultado.
        //! @param a: primer numero
        //! @param b: segundo numero
        //! @returns: a + b
        devolver a + b
    fin

Y genera un sitio HTML con toda la API documentada:

    python generar_docs.py mi_programa.sipi
    (o, si preferis: sipi doc mi_programa.sipi)

No depende del interprete de SiPi -- lee el archivo fuente en crudo,
asi que funciona incluso sobre codigo con errores de sintaxis (util
para revisar la documentacion de un programa que todavia no corre).
"""
import sys
import os
import re
import html
import datetime


def _extraer_docstring(lineas, idx_siguiente_a_la_firma):
    """Junta las lineas '//!' que vienen inmediatamente despues de la
    firma de una funcion/clase/metodo (saltando lineas en blanco), y las
    separa en: descripcion general, lista de @param, y @returns."""
    descripcion = []
    params = []  # (nombre, descripcion)
    retorno = None
    j = idx_siguiente_a_la_firma
    while j < len(lineas):
        cruda = lineas[j]
        limpia = cruda.strip()
        if limpia == "":
            j += 1
            continue
        if not limpia.startswith("//!"):
            break
        contenido = limpia[3:].strip()
        m_param = re.match(r"@param\s+(\w+)\s*:\s*(.*)$", contenido)
        m_returns = re.match(r"@returns?\s*:\s*(.*)$", contenido)
        if m_param:
            params.append((m_param.group(1), m_param.group(2)))
        elif m_returns:
            retorno = m_returns.group(1)
        else:
            descripcion.append(contenido)
        j += 1
    return {
        "descripcion": " ".join(descripcion).strip(),
        "params": params,
        "retorno": retorno,
    }


def extraer_api(ruta_archivo):
    """Escanea un .sipi en crudo y devuelve la info de documentacion de
    cada funcion, clase e interfaz que tenga un docstring '//!'."""
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        lineas = f.read().split("\n")

    nombre_programa = None
    funciones = []
    clases = []

    for idx, cruda in enumerate(lineas):
        limpia = cruda.strip()
        m_prog = re.match(r'programa\s+"([^"]*)"', limpia)
        if m_prog:
            nombre_programa = m_prog.group(1)
            continue

        m_fn = re.match(r"funcion\s+(\w+)\((.*?)\)(?:\s*->\s*(\w+))?$", limpia)
        if m_fn:
            nombre, params_txt, tipo_retorno = m_fn.groups()
            doc = _extraer_docstring(lineas, idx + 1)
            funciones.append({
                "nombre": nombre,
                "firma": f"{nombre}({params_txt})" + (f" -> {tipo_retorno}" if tipo_retorno else ""),
                "tipo_retorno": tipo_retorno,
                **doc,
            })
            continue

        m_clase = re.match(r"clase\s+(\w+)(?:\s+hereda_de\s+(\w+))?(?:\s+implementa\s+([\w,\s]+))?$", limpia)
        if m_clase:
            nombre, padre, interfaces = m_clase.groups()
            doc = _extraer_docstring(lineas, idx + 1)
            metodos = []
            # Buscamos los metodos dentro de esta clase (hasta el 'fin'
            # que le corresponde, aproximado por indentacion/anidado simple).
            profundidad = 1
            j = idx + 1
            while j < len(lineas) and profundidad > 0:
                l2 = lineas[j].strip()
                palabra = l2.split(" ", 1)[0] if l2 else ""
                if palabra in ("si", "mientras", "repetir", "para_cada", "funcion",
                               "metodo", "intentar", "clase", "interfaz", "cada"):
                    profundidad += 1
                elif palabra == "fin":
                    profundidad -= 1
                m_metodo = re.match(r"metodo\s+(\w+)\((.*?)\)$", l2)
                if m_metodo and profundidad == 2:
                    doc_m = _extraer_docstring(lineas, j + 1)
                    metodos.append({
                        "nombre": m_metodo.group(1),
                        "firma": f"{m_metodo.group(1)}({m_metodo.group(2)})",
                        **doc_m,
                    })
                j += 1
            clases.append({
                "nombre": nombre, "padre": padre,
                "interfaces": [i.strip() for i in interfaces.split(",")] if interfaces else [],
                "metodos": metodos, **doc,
            })

    return {"nombre_programa": nombre_programa, "funciones": funciones, "clases": clases}


def _render_docstring_html(doc):
    partes = []
    if doc.get("descripcion"):
        partes.append(f'<p class="desc">{html.escape(doc["descripcion"])}</p>')
    if doc.get("params"):
        partes.append('<p class="tag-title">Parametros:</p><ul class="params">')
        for nombre, desc in doc["params"]:
            partes.append(f'<li><code>{html.escape(nombre)}</code> — {html.escape(desc)}</li>')
        partes.append("</ul>")
    if doc.get("retorno"):
        partes.append(f'<p class="tag-title">Devuelve:</p><p class="returns">{html.escape(doc["retorno"])}</p>')
    if not partes:
        partes.append('<p class="desc sin-doc">(sin documentacion todavia -- agrega un comentario //! arriba del devolver)</p>')
    return "\n".join(partes)


def generar_html(api, nombre_archivo):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    titulo = api["nombre_programa"] or nombre_archivo

    secciones = []
    if api["funciones"]:
        bloques = []
        for fn in api["funciones"]:
            bloques.append(f'''
            <div class="item" id="fn-{html.escape(fn["nombre"])}">
                <h3><code>funcion {html.escape(fn["firma"])}</code></h3>
                {_render_docstring_html(fn)}
            </div>''')
        secciones.append(f'<h2>Funciones</h2>{"".join(bloques)}')

    if api["clases"]:
        bloques = []
        for cl in api["clases"]:
            extra = ""
            if cl["padre"]:
                extra += f' hereda de <code>{html.escape(cl["padre"])}</code>'
            if cl["interfaces"]:
                extra += f' implementa <code>{html.escape(", ".join(cl["interfaces"]))}</code>'
            metodos_html = "".join(
                f'''<div class="metodo">
                    <h4><code>metodo {html.escape(m["firma"])}</code></h4>
                    {_render_docstring_html(m)}
                </div>''' for m in cl["metodos"]
            )
            bloques.append(f'''
            <div class="item" id="clase-{html.escape(cl["nombre"])}">
                <h3><code>clase {html.escape(cl["nombre"])}</code>{extra}</h3>
                {_render_docstring_html(cl)}
                {metodos_html}
            </div>''')
        secciones.append(f'<h2>Clases</h2>{"".join(bloques)}')

    if not secciones:
        secciones.append('<p class="sin-doc">No se encontraron funciones ni clases documentadas en este archivo.</p>')

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Documentacion de {html.escape(titulo)}</title>
<style>
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; max-width: 900px; margin: 0 auto;
            padding: 40px 20px; background: #1e1e2e; color: #cdd6f4; line-height: 1.6; }}
    h1 {{ color: #89b4fa; border-bottom: 2px solid #313244; padding-bottom: 12px; }}
    h2 {{ color: #a6e3a1; margin-top: 40px; }}
    h3 {{ color: #f9e2af; margin-bottom: 4px; }}
    h4 {{ color: #fab387; margin-bottom: 4px; }}
    code {{ background: #313244; padding: 2px 8px; border-radius: 4px; font-family: 'Cascadia Code', monospace; }}
    .item {{ background: #232336; border-radius: 10px; padding: 20px; margin: 16px 0; border: 1px solid #313244; }}
    .metodo {{ margin-left: 20px; padding: 12px; border-left: 3px solid #45475a; margin-top: 12px; }}
    .desc {{ color: #cdd6f4; }}
    .sin-doc {{ color: #7f849c; font-style: italic; }}
    .tag-title {{ color: #94e2d5; font-weight: bold; margin-bottom: 4px; }}
    .params li {{ margin: 4px 0; }}
    footer {{ margin-top: 60px; color: #7f849c; font-size: 0.85em; }}
</style>
</head>
<body>
<h1>{html.escape(titulo)}</h1>
<p>Documentacion generada automaticamente desde <code>{html.escape(nombre_archivo)}</code></p>
{"".join(secciones)}
<footer>Generado por SiPi (generar_docs.py) el {fecha}.</footer>
</body>
</html>
'''


def main():
    if len(sys.argv) < 2:
        print("Uso: python generar_docs.py mi_programa.sipi")
        sys.exit(1)
    ruta = sys.argv[1]
    if not os.path.exists(ruta):
        print(f"[SiPi] No se encontro el archivo: {ruta}")
        sys.exit(1)

    api = extraer_api(ruta)
    html_generado = generar_html(api, os.path.basename(ruta))
    salida = os.path.splitext(ruta)[0] + "_docs.html"
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html_generado)

    total = len(api["funciones"]) + len(api["clases"])
    print(f"[SiPi] Documentacion generada: {salida}")
    print(f"[SiPi] {len(api['funciones'])} funcion(es) y {len(api['clases'])} clase(s) encontradas.")
    if total == 0:
        print("[SiPi] Aviso: no se encontro ninguna funcion ni clase en este archivo.")


if __name__ == "__main__":
    main()
