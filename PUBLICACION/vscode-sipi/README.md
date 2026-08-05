# SiPi para Visual Studio Code

Resaltado de sintaxis, snippets y configuracion de indentacion/plegado
para archivos `.sipi`.

## Que incluye
- **Resaltado de sintaxis** para los ~190 comandos de SiPi, palabras
  clave (`si`, `mientras`, `funcion`, `clase`, `interfaz`, etc.), tipos
  opcionales (`entero`, `decimal`, `texto`, `lista`, `diccionario`),
  strings con interpolacion (`"Hola {nombre}"`), numeros y comentarios
  (`//` y `/* */`).
- **15 snippets** listos para usar: `programa`, `si`, `mientras`,
  `repetir`, `para_cada`, `funcion`, `funcion_tipada`, `variable_tipada`,
  `clase`, `interfaz`, `intentar`, `crear_juego`, `escena_3d`,
  `lista_tipada`, `diccionario_tipado`.
- **Plegado de codigo** (code folding) y **auto-indentacion** basados en
  los bloques que abren SiPi (`si`/`mientras`/`funcion`/`clase`/etc.) y
  cierran con `fin`.
- Autocompletado de parentesis, corchetes y comillas.

## Como instalarlo (sin publicar en el Marketplace)

**Opcion 1 - carpeta de extensiones de VS Code:**
1. Copia toda la carpeta `vscode-sipi` a tu carpeta de extensiones:
   - Windows: `%USERPROFILE%\.vscode\extensions\sipi-lang-0.1.0`
   - Linux/Mac: `~/.vscode/extensions/sipi-lang-0.1.0`
2. Reinicia VS Code. Abre cualquier archivo `.sipi` y deberia verse con
   colores.

**Opcion 2 - empaquetar como .vsix (para compartir o instalar en otra maquina):**
```bash
npm install -g @vscode/vsce
cd vscode-sipi
vsce package
code --install-extension sipi-lang-0.1.0.vsix
```

## Verificado
La gramatica (`syntaxes/sipi.tmLanguage.json`) fue probada con el motor
real que usa VS Code (`vscode-textmate` + `vscode-oniguruma`), tokenizando
un programa de ejemplo con comandos, palabras clave, tipos, strings con
interpolacion, numeros y comentarios -- todas las categorias se
reconocieron correctamente antes de entregar esta extension.
