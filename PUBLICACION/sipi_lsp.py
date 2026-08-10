#!/usr/bin/env python3
"""
sipi_lsp.py - Item 2 de tu feedback: Servidor de Lenguaje (LSP) para
VS Code / Neovim / cualquier editor que hable el protocolo LSP estandar.

Implementa el protocolo JSON-RPC sobre stdio que usa LSP (el mismo que
usan pyright, rust-analyzer, etc.), sin depender de ninguna libreria
externa -- solo la biblioteca estandar de Python.

Que ofrece HOY (alcance real, sin exagerar):
- Diagnosticos en tiempo real: bloques 'si'/'mientras'/'funcion'/etc. sin
  su 'fin' correspondiente, usando el mismo parser que usa el interprete
  real (Interprete._preprocesar_contenido), asi que el diagnostico es
  exactamente el mismo error que veria el usuario al ejecutar.
- Autocompletado: los ~190 comandos del lenguaje, tomados directo de
  COMANDOS_CONOCIDOS (no una lista separada que se desactualice).

Que NO hace todavia (para ser honesto sobre el alcance): no valida la
sintaxis especifica de cada comando (esto necesitaria ejecutar el
programa, lo cual es inseguro para diagnosticos en vivo mientras el
usuario escribe -- un programa a medio escribir podria abrir una
ventana, tardar para siempre en un bucle, etc.), ni ofrece "goto
definition" o "hover" todavia. Es una base real y funcional, no un LSP
completo de nivel productivo.

Uso (configuracion de ejemplo para un cliente LSP generico):
    python sipi_lsp.py
(el servidor lee/escribe JSON-RPC enmarcado con Content-Length por
stdin/stdout, como cualquier servidor LSP estandar)
"""
import sys
import os
import re
import json
import importlib.util


def _cargar_motor_sipi():
    aqui = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(aqui, "sipi.py")
    spec = importlib.util.spec_from_file_location("motor_sipi_lsp", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class ServidorLSP:
    def __init__(self, entrada=None, salida=None):
        self.entrada = entrada if entrada is not None else sys.stdin.buffer
        self.salida = salida if salida is not None else sys.stdout.buffer
        self.documentos = {}  # uri -> texto
        self.motor = _cargar_motor_sipi()
        self.detener = False

    # ---------- Framing JSON-RPC (Content-Length) ----------
    def _leer_mensaje(self):
        headers = {}
        while True:
            linea = self.entrada.readline()
            if not linea:
                return None  # EOF: el cliente cerro la conexion
            linea = linea.decode("utf-8", errors="replace").strip()
            if linea == "":
                break
            if ":" in linea:
                clave, _, valor = linea.partition(":")
                headers[clave.strip().lower()] = valor.strip()
        largo = int(headers.get("content-length", 0))
        if largo == 0:
            return None
        cuerpo = self.entrada.read(largo)
        return json.loads(cuerpo.decode("utf-8"))

    def _escribir_mensaje(self, mensaje):
        cuerpo = json.dumps(mensaje).encode("utf-8")
        encabezado = f"Content-Length: {len(cuerpo)}\r\n\r\n".encode("utf-8")
        self.salida.write(encabezado + cuerpo)
        self.salida.flush()

    def _responder(self, id_peticion, resultado):
        self._escribir_mensaje({"jsonrpc": "2.0", "id": id_peticion, "result": resultado})

    def _notificar(self, metodo, params):
        self._escribir_mensaje({"jsonrpc": "2.0", "method": metodo, "params": params})

    # ---------- Diagnosticos ----------
    def _calcular_diagnosticos(self, texto):
        """Corre el mismo parser que usa el interprete real (sin
        ejecutar ninguna linea del programa) para detectar bloques sin
        'fin'. Devuelve una lista de diagnosticos en formato LSP."""
        diagnosticos = []
        try:
            interprete = self.motor.Interprete.__new__(self.motor.Interprete)
            interprete.lineas = interprete._preprocesar_contenido(texto)
            interprete._cache_fin_bloque = {}
            # Verificamos que cada bloque abierto tenga su 'fin', recorriendo
            # con el mismo _encontrar_fin real que usa la ejecucion. Si algo
            # quedo sin cerrar en TODO el archivo, _preprocesar_contenido ya
            # lo habria intentado cerrar por indentacion; si aun asi falta,
            # dispara el mismo SiPiError que veria el usuario al ejecutar.
            i = 0
            n = len(interprete.lineas)
            while i < n:
                _, linea = interprete.lineas[i]
                if not linea:
                    i += 1
                    continue
                palabra = linea.split(" ", 1)[0]
                resto = linea[len(palabra):].strip()
                es_asignacion = resto.startswith("=") and not resto.startswith("==")
                if palabra in self.motor.BLOQUES_QUE_ABREN and not es_asignacion:
                    interprete._encontrar_fin(i, self.motor.BLOQUES_QUE_ABREN)
                i += 1
        except self.motor.SiPiError as e:
            mensaje = str(e)
            m_linea = re.search(r"\blinea (\d+)", mensaje)
            fila = (int(m_linea.group(1)) - 1) if m_linea else 0
            diagnosticos.append({
                "range": {
                    "start": {"line": max(fila, 0), "character": 0},
                    "end": {"line": max(fila, 0), "character": 200},
                },
                "severity": 1,  # Error
                "source": "sipi-lsp",
                "message": mensaje,
            })
        except Exception:
            # Cualquier otro problema de parseo no debe tumbar el servidor
            # LSP entero -- simplemente no hay diagnostico esta vez.
            pass
        return diagnosticos

    def _publicar_diagnosticos(self, uri, texto):
        diagnosticos = self._calcular_diagnosticos(texto)
        self._notificar("textDocument/publishDiagnostics", {"uri": uri, "diagnostics": diagnosticos})

    # ---------- Autocompletado ----------
    def _items_autocompletado(self):
        items = []
        ayuda = getattr(self.motor, "AYUDA_COMANDOS", {})
        for cmd in sorted(set(self.motor.COMANDOS_CONOCIDOS)):
            detalle = ayuda.get(cmd)
            item = {"label": cmd, "kind": 14}  # 14 = Keyword en la especificacion LSP
            if detalle:
                item["documentation"] = detalle[0]
            items.append(item)
        return items

    # ---------- Manejo de peticiones ----------
    def _manejar(self, msg):
        metodo = msg.get("method")
        id_peticion = msg.get("id")
        params = msg.get("params", {}) or {}

        if metodo == "initialize":
            self._responder(id_peticion, {
                "capabilities": {
                    "textDocumentSync": 1,  # 1 = Full (se manda el documento entero en cada cambio)
                    "completionProvider": {"triggerCharacters": ["_"]},
                    "diagnosticProvider": False,
                }
            })
        elif metodo == "initialized":
            pass
        elif metodo == "textDocument/didOpen":
            doc = params.get("textDocument", {})
            uri, texto = doc.get("uri"), doc.get("text", "")
            self.documentos[uri] = texto
            self._publicar_diagnosticos(uri, texto)
        elif metodo == "textDocument/didChange":
            doc = params.get("textDocument", {})
            uri = doc.get("uri")
            cambios = params.get("contentChanges", [])
            if cambios:
                texto = cambios[-1].get("text", "")
                self.documentos[uri] = texto
                self._publicar_diagnosticos(uri, texto)
        elif metodo == "textDocument/didClose":
            doc = params.get("textDocument", {})
            self.documentos.pop(doc.get("uri"), None)
        elif metodo == "textDocument/completion":
            if id_peticion is not None:
                self._responder(id_peticion, self._items_autocompletado())
        elif metodo == "shutdown":
            self._responder(id_peticion, None)
        elif metodo == "exit":
            self.detener = True
        else:
            if id_peticion is not None:
                self._responder(id_peticion, None)

    def ejecutar(self):
        while not self.detener:
            msg = self._leer_mensaje()
            if msg is None:
                break
            try:
                self._manejar(msg)
            except Exception as e:
                sys.stderr.write(f"[sipi-lsp] Error manejando mensaje: {e}\n")


def main():
    ServidorLSP().ejecutar()


if __name__ == "__main__":
    main()
