# GLOSSARY — Terminología internacional

SiPi usa palabras clave en español a propósito (ver "¿Por qué existe SiPi?" en el `README.md`). Pero los *conceptos* detrás de esas palabras son los mismos que en cualquier lenguaje de programación, y tienen nombres estándar en inglés que vas a encontrar en cualquier otro lenguaje, tutorial, o entrevista de trabajo. Esta tabla conecta ambos mundos, para que aprender SiPi no te deje aislado del vocabulario que se usa afuera.

| En SiPi | Concepto | Término internacional (inglés) |
|---|---|---|
| `variable` | Un espacio con nombre que guarda un valor | **variable** |
| `funcion` | Bloque de código reutilizable, con nombre y parámetros | **function** |
| `funcion` que se llama a sí misma | Función que se llama a sí misma para resolver un problema por partes | **recursion** |
| Una función pasada como parámetro a otra (ej. en `lista_mapear numeros con doble`) | Una función usada como valor, pasada a otra función | **callback** / **higher-order function** |
| Una función corta, sin nombre propio, usada al vuelo | Función anónima definida en el lugar donde se usa | **lambda** / **anonymous function** |
| Una función que "recuerda" variables de donde fue creada | Función que retiene acceso a variables de su entorno original, aunque ese entorno ya haya terminado | **closure** |
| `clase` | Plantilla para crear objetos con datos y comportamiento propios | **class** |
| `nuevo Clase()` | Crear un objeto real a partir de una clase | **instantiation** |
| `hereda_de` | Una clase que extiende otra, reutilizando su comportamiento | **inheritance** |
| `implementa` | Obligación de que una clase tenga ciertos métodos, sin heredar la implementación | **interface** |
| Un método sobreescrito en una subclase | Que el mismo nombre de método se comporte distinto según la clase real del objeto | **polymorphism** |
| `este` | Referencia al objeto actual dentro de un método | **self** / **this** |
| `intentar` / `capturar` | Ejecutar código que puede fallar, y manejar el error sin cortar el programa | **try** / **catch** (**exception handling**) |
| `lanzar_error` | Generar un error a propósito | **throw** / **raise** |
| `enum` | Un tipo con un conjunto fijo y nombrado de valores posibles | **enum** (enumeration) |
| `estructura` | Agrupar varios datos relacionados bajo un solo nombre, sin comportamiento | **struct** |
| `seleccionar` / `caso` | Comparar un valor contra varias opciones posibles, de forma más legible que muchos `si`/`sino` encadenados | **pattern matching** / **switch-case** |
| `sipi.py` (el programa que lee y ejecuta tu código) | El programa que ejecuta tu código línea por línea, sin convertirlo antes a código nativo de la máquina | **interpreter** |
| La parte de `sipi.py` que entiende la estructura de tu código antes de ejecutarlo | El proceso de analizar el texto de tu programa y entender su estructura | **parser** / **parsing** |
| El código de máquina/formato intermedio que produciría un compilador | Convertir código fuente a un formato que la máquina ejecuta directamente, antes de correrlo (SiPi no hace esto — ver `LANGUAGE_SPEC.md`) | **compilation** |
| `.sipic` | Una versión precomputada del programa que acelera reejecuciones, sin ser código nativo | **bytecode cache** |
| `importar` / `instalar_modulo` | Traer código de otro archivo/paquete para usarlo en el tuyo | **import** / **module** / **package** |
| `variable x: entero` | Decirle al lenguaje de antemano qué tipo de dato va a tener una variable | **type annotation** |
| Que SiPi permita variables sin anotar tipo, y que ese tipo pueda cambiar | Que el tipo de una variable se determina y puede cambiar en tiempo de ejecución, no antes | **dynamic typing** |
| `-> variable` (patrón de comandos que calculan algo) | Un valor que una operación produce y se guarda | **return value** |
| `romper` / `continuar` | Cortar un bucle antes de tiempo, o saltar a la siguiente vuelta | **break** / **continue** |
| `nulo` | Un valor que representa "sin valor" | **null** / **None** |
| Navegación segura con `?` | Acceder a un campo que podría no existir, sin que el programa se caiga | **optional chaining** / **safe navigation** |
| `\|>` (pipe operator) | Encadenar el resultado de una operación como entrada de la siguiente, de forma legible | **pipe operator** |

## Por qué importa esto

Si en algún momento pasás de SiPi a otro lenguaje (Python, JavaScript, Java, lo que sea), vas a encontrar estos mismos conceptos con estos mismos nombres en inglés — en la documentación oficial de ese lenguaje, en Stack Overflow, en una entrevista de trabajo. Aprender la idea en SiPi ya es aprender el concepto; esta tabla es el puente para que también sepas cómo se llama afuera.
