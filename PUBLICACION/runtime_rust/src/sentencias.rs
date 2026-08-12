//! sentencias.rs - Sentencias de SiPi para el runtime Rust (item #70 del
//! feedback, fase 2: `variable`, `decir`/`imprimir`, `si`/`sino`,
//! `mientras`, `repetir...veces`, `romper`/`continuar`, `funcion` con
//! parametros y `devolver`, `llamar`/`llamar_valor`).
//!
//! Fase 1 (parser.rs) solo sabia evaluar UNA expresion suelta. Esta fase
//! agrega un parser de PROGRAMAS: varias lineas, con estado mutable
//! (`entorno`) que persiste entre sentencias, exactamente como hace
//! `sipi.py` linea por linea. Misma gramatica que el interprete Python
//! para este subconjunto (ver `sipi.py`, secciones `cmd == "variable"`,
//! `"decir"`, `"si"`, `"mientras"`, `"repetir"`, `"funcion"`, `"llamar"`,
//! `"devolver"`).
//!
//! Simplificacion deliberada frente a sipi.py: las funciones en este
//! runtime tienen scope local PURO (no ven variables globales ni de
//! quien las llama, solo sus parametros) en vez de la pila de scopes
//! real de Python. Para el subconjunto de sentencias soportado hoy
//! (sin listas/diccionarios que pasar por referencia) esto es
//! observacionalmente equivalente para cualquier programa que solo use
//! parametros y `devolver`; se documenta como limitacion conocida, no
//! como bug, por si mas adelante se agregan variables globales de
//! verdad accesibles desde funciones.
//!
//! Deliberadamente NO cubre todavia: `para_cada` (necesita listas, que
//! el runtime Rust no tiene aun), llamadas a funcion DENTRO de una
//! expresion (`decir mi_funcion(2)`, hoy funcion solo se invoca como
//! sentencia con `llamar`/`llamar_valor`, igual que el resto de
//! comandos de sipi.py), listas/diccionarios, `intentar`/`capturar`, ni
//! nada de I/O real. Eso queda para la proxima ronda.

use crate::parser::{evaluar, parsear_expresion_str, ErrorEvaluacion, ErrorSintactico, Nodo, Valor};
use std::collections::HashMap;
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Sentencia {
    Variable { nombre: String, expresion: Nodo },
    Decir { expresion: Nodo },
    Si { condicion: Nodo, entonces: Vec<Sentencia>, sino: Vec<Sentencia> },
    Mientras { condicion: Nodo, cuerpo: Vec<Sentencia> },
    Repetir { veces: Nodo, cuerpo: Vec<Sentencia> },
    Romper,
    Continuar,
    Funcion { nombre: String, parametros: Vec<String>, cuerpo: Vec<Sentencia> },
    Llamar { nombre: String, argumentos: Vec<Nodo> },
    LlamarValor { nombre: String, argumentos: Vec<Nodo>, destino: String },
    Devolver { expresion: Nodo },
}

#[derive(Debug, Clone, PartialEq)]
pub struct ErrorPrograma {
    pub mensaje: String,
    pub linea: usize, // 1-indexado, como los mensajes de error de sipi.py
}

impl fmt::Display for ErrorPrograma {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Linea {}: {}", self.linea, self.mensaje)
    }
}

/// Entorno de ejecucion: variables mutables del programa. Separado de
/// `HashMap<String, Valor>` de parser.rs solo por claridad de nombre;
/// misma representacion, para no duplicar tipos.
pub type Entorno = HashMap<String, Valor>;

/// Quita un comentario de linea completa (`# ...`) o al final (`// ...`).
/// No es tan robusto como `_quitar_comentario_linea` de sipi.py (que
/// respeta comillas), pero cubre el caso comun para este prototipo.
fn limpiar_linea(linea: &str) -> String {
    let sin_comentario_completo = if linea.trim_start().starts_with('#') {
        ""
    } else {
        linea
    };
    match sin_comentario_completo.find("//") {
        Some(pos) => sin_comentario_completo[..pos].to_string(),
        None => sin_comentario_completo.to_string(),
    }
}

/// Separa el primer "token de comando" (palabra) del resto de la linea,
/// igual que hace sipi.py: `linea.split(" ")[0]` + resto.
fn separar_comando(linea: &str) -> (String, String) {
    let recortada = linea.trim();
    match recortada.find(char::is_whitespace) {
        Some(pos) => (recortada[..pos].to_string(), recortada[pos..].trim_start().to_string()),
        None => (recortada.to_string(), String::new()),
    }
}

/// Parsea el texto completo de un programa en una lista de sentencias
/// (recursivo para los bloques de `si`).
pub fn parsear_programa(texto: &str) -> Result<Vec<Sentencia>, ErrorPrograma> {
    let lineas_crudas: Vec<&str> = texto.lines().collect();
    let lineas_limpias: Vec<String> = lineas_crudas.iter().map(|l| limpiar_linea(l)).collect();
    let mut pos = 0usize;
    let sentencias = parsear_bloque(&lineas_limpias, &mut pos, &[])?;
    Ok(sentencias)
}

/// Parsea sentencias hasta encontrar una de las palabras clave de
/// `terminadores` (al mismo nivel de anidamiento) o el final del texto.
/// Devuelve las sentencias del bloque; `pos` queda apuntando a la linea
/// terminadora (sin consumirla), para que el que llamo decida que hacer.
fn parsear_bloque(
    lineas: &[String],
    pos: &mut usize,
    terminadores: &[&str],
) -> Result<Vec<Sentencia>, ErrorPrograma> {
    let mut sentencias = Vec::new();

    while *pos < lineas.len() {
        let numero_linea = *pos + 1;
        let linea = lineas[*pos].trim();

        if linea.is_empty() {
            *pos += 1;
            continue;
        }

        let (comando, resto) = separar_comando(linea);

        if terminadores.contains(&comando.as_str()) {
            return Ok(sentencias);
        }

        match comando.as_str() {
            "variable" | "var" => {
                let (nombre, expr_texto) = separar_variable(&resto).ok_or_else(|| ErrorPrograma {
                    mensaje: format!("Sintaxis invalida en 'variable': {}", resto),
                    linea: numero_linea,
                })?;
                let expresion = parsear_expresion_str(&expr_texto).map_err(|e| convertir_error(e, numero_linea))?;
                sentencias.push(Sentencia::Variable { nombre, expresion });
                *pos += 1;
            }
            "decir" | "imprimir" => {
                if resto.trim().is_empty() {
                    return Err(ErrorPrograma {
                        mensaje: "'decir' necesita algo para mostrar".to_string(),
                        linea: numero_linea,
                    });
                }
                let expresion = parsear_expresion_str(&resto).map_err(|e| convertir_error(e, numero_linea))?;
                sentencias.push(Sentencia::Decir { expresion });
                *pos += 1;
            }
            "si" => {
                if resto.trim().is_empty() {
                    return Err(ErrorPrograma {
                        mensaje: "'si' necesita una condicion".to_string(),
                        linea: numero_linea,
                    });
                }
                let condicion = parsear_expresion_str(&resto).map_err(|e| convertir_error(e, numero_linea))?;
                *pos += 1; // consume la linea 'si ...'

                let entonces = parsear_bloque(lineas, pos, &["sino", "fin"])?;

                let sino = if *pos < lineas.len() {
                    let (cmd_actual, _) = separar_comando(lineas[*pos].trim());
                    if cmd_actual == "sino" {
                        *pos += 1; // consume 'sino'
                        parsear_bloque(lineas, pos, &["fin"])?
                    } else {
                        Vec::new()
                    }
                } else {
                    Vec::new()
                };

                if *pos >= lineas.len() {
                    return Err(ErrorPrograma {
                        mensaje: "Falta 'fin' para cerrar el bloque 'si'".to_string(),
                        linea: numero_linea,
                    });
                }
                *pos += 1; // consume 'fin'

                sentencias.push(Sentencia::Si { condicion, entonces, sino });
            }
            "mientras" => {
                if resto.trim().is_empty() {
                    return Err(ErrorPrograma {
                        mensaje: "'mientras' necesita una condicion".to_string(),
                        linea: numero_linea,
                    });
                }
                let condicion = parsear_expresion_str(&resto).map_err(|e| convertir_error(e, numero_linea))?;
                *pos += 1;
                let cuerpo = parsear_bloque(lineas, pos, &["fin"])?;
                if *pos >= lineas.len() {
                    return Err(ErrorPrograma {
                        mensaje: "Falta 'fin' para cerrar el bloque 'mientras'".to_string(),
                        linea: numero_linea,
                    });
                }
                *pos += 1;
                sentencias.push(Sentencia::Mientras { condicion, cuerpo });
            }
            "repetir" => {
                let resto_trim = resto.trim();
                let expr_veces = resto_trim.strip_suffix("veces").map(|s| s.trim()).ok_or_else(|| ErrorPrograma {
                    mensaje: format!("Sintaxis invalida en 'repetir': se esperaba '<expresion> veces', se encontro '{}'", resto),
                    linea: numero_linea,
                })?;
                let veces = parsear_expresion_str(expr_veces).map_err(|e| convertir_error(e, numero_linea))?;
                *pos += 1;
                let cuerpo = parsear_bloque(lineas, pos, &["fin"])?;
                if *pos >= lineas.len() {
                    return Err(ErrorPrograma {
                        mensaje: "Falta 'fin' para cerrar el bloque 'repetir'".to_string(),
                        linea: numero_linea,
                    });
                }
                *pos += 1;
                sentencias.push(Sentencia::Repetir { veces, cuerpo });
            }
            "romper" => {
                sentencias.push(Sentencia::Romper);
                *pos += 1;
            }
            "continuar" => {
                sentencias.push(Sentencia::Continuar);
                *pos += 1;
            }
            "funcion" => {
                let (nombre, args_texto) = separar_llamada(resto.trim()).ok_or_else(|| ErrorPrograma {
                    mensaje: format!("Sintaxis invalida en 'funcion': se esperaba 'nombre(parametros)', se encontro '{}'", resto),
                    linea: numero_linea,
                })?;
                let parametros = separar_parametros(&args_texto);
                *pos += 1;
                let cuerpo = parsear_bloque(lineas, pos, &["fin"])?;
                if *pos >= lineas.len() {
                    return Err(ErrorPrograma {
                        mensaje: format!("Falta 'fin' para cerrar la funcion '{}'", nombre),
                        linea: numero_linea,
                    });
                }
                *pos += 1;
                sentencias.push(Sentencia::Funcion { nombre, parametros, cuerpo });
            }
            "llamar" => {
                let (nombre, args_texto) = separar_llamada(resto.trim()).ok_or_else(|| ErrorPrograma {
                    mensaje: format!("Sintaxis invalida en 'llamar': se esperaba 'nombre(argumentos)', se encontro '{}'", resto),
                    linea: numero_linea,
                })?;
                let argumentos = parsear_argumentos_como_nodos(&args_texto, numero_linea)?;
                sentencias.push(Sentencia::Llamar { nombre, argumentos });
                *pos += 1;
            }
            "llamar_valor" => {
                let m = resto.trim().rfind("->").ok_or_else(|| ErrorPrograma {
                    mensaje: format!("Sintaxis invalida en 'llamar_valor': falta '-> variable_destino' en '{}'", resto),
                    linea: numero_linea,
                })?;
                let (llamada_texto, destino_texto) = resto.trim().split_at(m);
                let destino = destino_texto[2..].trim().to_string();
                if destino.is_empty() {
                    return Err(ErrorPrograma {
                        mensaje: "'llamar_valor' necesita un nombre de variable destino despues de '->'".to_string(),
                        linea: numero_linea,
                    });
                }
                let (nombre, args_texto) = separar_llamada(llamada_texto.trim()).ok_or_else(|| ErrorPrograma {
                    mensaje: format!("Sintaxis invalida en 'llamar_valor': se esperaba 'nombre(argumentos) -> variable', se encontro '{}'", resto),
                    linea: numero_linea,
                })?;
                let argumentos = parsear_argumentos_como_nodos(&args_texto, numero_linea)?;
                sentencias.push(Sentencia::LlamarValor { nombre, argumentos, destino });
                *pos += 1;
            }
            "devolver" => {
                if resto.trim().is_empty() {
                    return Err(ErrorPrograma {
                        mensaje: "'devolver' necesita un valor (usa 'devolver nulo' si no hay nada que devolver)".to_string(),
                        linea: numero_linea,
                    });
                }
                let expresion = parsear_expresion_str(&resto).map_err(|e| convertir_error(e, numero_linea))?;
                sentencias.push(Sentencia::Devolver { expresion });
                *pos += 1;
            }
            otro => {
                return Err(ErrorPrograma {
                    mensaje: format!("Comando desconocido o todavia no soportado en el runtime Rust: '{}'", otro),
                    linea: numero_linea,
                });
            }
        }
    }

    Ok(sentencias)
}

/// `nombre[: tipo] = expr` -> (nombre, expr). El tipo declarado se ignora
/// por ahora (el runtime Rust todavia no valida tipos, a diferencia de
/// sipi.py) -- se documenta como limitacion, no como bug.
fn separar_variable(resto: &str) -> Option<(String, String)> {
    let pos_igual = resto.find('=')?;
    // evita confundir '==' con el '=' de asignacion
    if resto[pos_igual..].starts_with("==") {
        return None;
    }
    let parte_nombre = resto[..pos_igual].trim();
    let nombre = match parte_nombre.find(':') {
        Some(p) => parte_nombre[..p].trim(),
        None => parte_nombre,
    };
    if nombre.is_empty() || !nombre.chars().next().unwrap().is_alphabetic() && nombre.chars().next() != Some('_') {
        return None;
    }
    let expr = resto[pos_igual + 1..].trim();
    if expr.is_empty() {
        return None;
    }
    Some((nombre.to_string(), expr.to_string()))
}

fn convertir_error(e: ErrorSintactico, linea: usize) -> ErrorPrograma {
    ErrorPrograma { mensaje: e.mensaje, linea }
}

/// Separa `nombre(args)` -> (nombre, texto_args_sin_parentesis).
fn separar_llamada(texto: &str) -> Option<(String, String)> {
    let texto = texto.trim();
    if !texto.ends_with(')') {
        return None;
    }
    let pos_abre = texto.find('(')?;
    let nombre = texto[..pos_abre].trim();
    if nombre.is_empty() {
        return None;
    }
    let args = &texto[pos_abre + 1..texto.len() - 1];
    Some((nombre.to_string(), args.to_string()))
}

/// Separa una lista de argumentos por comas de nivel superior (no dentro
/// de comillas ni de parentesis anidados), igual de espiritu que
/// `_separar_nivel_superior` de sipi.py mismo si mas simple. Ignora
/// argumentos vacios (permite `f()` sin argumentos).
fn separar_argumentos(texto: &str) -> Vec<String> {
    let mut argumentos = Vec::new();
    let mut actual = String::new();
    let mut profundidad = 0i32;
    let mut dentro_de_texto = false;
    let mut chars = texto.chars().peekable();
    while let Some(c) = chars.next() {
        if dentro_de_texto {
            actual.push(c);
            if c == '\\' {
                if let Some(&siguiente) = chars.peek() {
                    actual.push(siguiente);
                    chars.next();
                }
            } else if c == '"' {
                dentro_de_texto = false;
            }
            continue;
        }
        match c {
            '"' => {
                dentro_de_texto = true;
                actual.push(c);
            }
            '(' => {
                profundidad += 1;
                actual.push(c);
            }
            ')' => {
                profundidad -= 1;
                actual.push(c);
            }
            ',' if profundidad == 0 => {
                argumentos.push(actual.trim().to_string());
                actual = String::new();
            }
            _ => actual.push(c),
        }
    }
    if !actual.trim().is_empty() {
        argumentos.push(actual.trim().to_string());
    }
    argumentos
}

fn parsear_argumentos_como_nodos(texto: &str, numero_linea: usize) -> Result<Vec<Nodo>, ErrorPrograma> {
    separar_argumentos(texto)
        .into_iter()
        .map(|a| parsear_expresion_str(&a).map_err(|e| convertir_error(e, numero_linea)))
        .collect()
}

/// Separa una lista de nombres de parametros por comas (declaracion de
/// `funcion nombre(a, b, c)` -- sin valores por default ni tipos por
/// ahora, a diferencia de sipi.py que si los soporta).
fn separar_parametros(texto: &str) -> Vec<String> {
    texto
        .split(',')
        .map(|p| p.trim().to_string())
        .filter(|p| !p.is_empty())
        .collect()
}

fn es_verdadero(valor: &Valor) -> bool {
    match valor {
        Valor::Booleano(b) => *b,
        Valor::Nulo => false,
        Valor::Numero(n) => *n != 0.0,
        Valor::Texto(s) => !s.is_empty(),
    }
}

/// Senal de control que una sentencia puede propagar hacia arriba:
/// romper/continuar de un bucle, o devolver de una funcion. `Normal`
/// significa "seguir ejecutando la siguiente sentencia normalmente".
#[derive(Debug, Clone, PartialEq)]
enum Control {
    Normal,
    Romper,
    Continuar,
    Retornar(Valor),
}

#[derive(Debug, Clone)]
struct DefinicionFuncion {
    parametros: Vec<String>,
    cuerpo: Vec<Sentencia>,
}

/// Contexto de ejecucion compartido entre todas las sentencias de un
/// programa: variables del scope actual + funciones declaradas (siempre
/// globales, igual que en sipi.py -- una funcion declarada dentro de un
/// 'si' sigue siendo invocable despues, ya que 'funcion' se registra al
/// parsear/ejecutar la sentencia, no al entrar al bloque).
struct Contexto {
    funciones: HashMap<String, DefinicionFuncion>,
    profundidad_bucles: u32,
}

/// Ejecuta una lista de sentencias contra un entorno mutable, acumulando
/// todo lo que `decir`/`imprimir` mostrarian (una linea por llamada) para
/// que main.rs y los tests puedan inspeccionar la salida sin depender de
/// stdout.
pub fn ejecutar(sentencias: &[Sentencia], entorno: &mut Entorno) -> Result<Vec<String>, ErrorEvaluacion> {
    let mut salida = Vec::new();
    let mut ctx = Contexto { funciones: HashMap::new(), profundidad_bucles: 0 };
    ejecutar_en(sentencias, entorno, &mut ctx, &mut salida)?;
    Ok(salida)
}

fn ejecutar_en(
    sentencias: &[Sentencia],
    entorno: &mut Entorno,
    ctx: &mut Contexto,
    salida: &mut Vec<String>,
) -> Result<Control, ErrorEvaluacion> {
    for sentencia in sentencias {
        let control = ejecutar_sentencia(sentencia, entorno, ctx, salida)?;
        if control != Control::Normal {
            return Ok(control);
        }
    }
    Ok(Control::Normal)
}

fn ejecutar_sentencia(
    sentencia: &Sentencia,
    entorno: &mut Entorno,
    ctx: &mut Contexto,
    salida: &mut Vec<String>,
) -> Result<Control, ErrorEvaluacion> {
    match sentencia {
        Sentencia::Variable { nombre, expresion } => {
            let valor = evaluar(expresion, entorno)?;
            entorno.insert(nombre.clone(), valor);
            Ok(Control::Normal)
        }
        Sentencia::Decir { expresion } => {
            let valor = evaluar(expresion, entorno)?;
            salida.push(valor.to_string());
            Ok(Control::Normal)
        }
        Sentencia::Si { condicion, entonces, sino } => {
            let valor_condicion = evaluar(condicion, entorno)?;
            if es_verdadero(&valor_condicion) {
                ejecutar_en(entonces, entorno, ctx, salida)
            } else {
                ejecutar_en(sino, entorno, ctx, salida)
            }
        }
        Sentencia::Mientras { condicion, cuerpo } => {
            ctx.profundidad_bucles += 1;
            let mut limite_seguridad = 0u32;
            let resultado = (|| -> Result<Control, ErrorEvaluacion> {
                while es_verdadero(&evaluar(condicion, entorno)?) && limite_seguridad < 1_000_000 {
                    match ejecutar_en(cuerpo, entorno, ctx, salida)? {
                        Control::Romper => break,
                        Control::Continuar | Control::Normal => {}
                        retorno @ Control::Retornar(_) => return Ok(retorno),
                    }
                    limite_seguridad += 1;
                }
                Ok(Control::Normal)
            })();
            ctx.profundidad_bucles -= 1;
            resultado
        }
        Sentencia::Repetir { veces, cuerpo } => {
            let valor_veces = evaluar(veces, entorno)?;
            let n = match valor_veces {
                Valor::Numero(n) => n as i64,
                _ => {
                    return Err(ErrorEvaluacion {
                        mensaje: "'repetir' necesita un numero antes de 'veces'".to_string(),
                    })
                }
            };
            ctx.profundidad_bucles += 1;
            let resultado = (|| -> Result<Control, ErrorEvaluacion> {
                for _ in 0..n.max(0) {
                    match ejecutar_en(cuerpo, entorno, ctx, salida)? {
                        Control::Romper => break,
                        Control::Continuar | Control::Normal => {}
                        retorno @ Control::Retornar(_) => return Ok(retorno),
                    }
                }
                Ok(Control::Normal)
            })();
            ctx.profundidad_bucles -= 1;
            resultado
        }
        Sentencia::Romper => {
            if ctx.profundidad_bucles == 0 {
                return Err(ErrorEvaluacion {
                    mensaje: "Se uso 'romper' fuera de un bucle (mientras/repetir).".to_string(),
                });
            }
            Ok(Control::Romper)
        }
        Sentencia::Continuar => {
            if ctx.profundidad_bucles == 0 {
                return Err(ErrorEvaluacion {
                    mensaje: "Se uso 'continuar' fuera de un bucle (mientras/repetir).".to_string(),
                });
            }
            Ok(Control::Continuar)
        }
        Sentencia::Funcion { nombre, parametros, cuerpo } => {
            ctx.funciones.insert(
                nombre.clone(),
                DefinicionFuncion { parametros: parametros.clone(), cuerpo: cuerpo.clone() },
            );
            Ok(Control::Normal)
        }
        Sentencia::Llamar { nombre, argumentos } => {
            invocar_funcion(nombre, argumentos, entorno, ctx, salida)?;
            Ok(Control::Normal)
        }
        Sentencia::LlamarValor { nombre, argumentos, destino } => {
            let valor = invocar_funcion(nombre, argumentos, entorno, ctx, salida)?;
            entorno.insert(destino.clone(), valor);
            Ok(Control::Normal)
        }
        Sentencia::Devolver { expresion } => {
            let valor = evaluar(expresion, entorno)?;
            Ok(Control::Retornar(valor))
        }
    }
}

/// Invoca una funcion ya declarada: evalua los argumentos en el entorno
/// de quien llama, arma un scope local nuevo solo con los parametros
/// (ver nota de "Simplificacion deliberada" al inicio del archivo) y
/// ejecuta el cuerpo. Sin 'devolver' explicito, el valor es `nulo`.
fn invocar_funcion(
    nombre: &str,
    argumentos: &[Nodo],
    entorno_llamador: &Entorno,
    ctx: &mut Contexto,
    salida: &mut Vec<String>,
) -> Result<Valor, ErrorEvaluacion> {
    let definicion = ctx.funciones.get(nombre).cloned().ok_or_else(|| ErrorEvaluacion {
        mensaje: format!("Funcion no definida: '{}'. Declarala primero con 'funcion {}(...)'.", nombre, nombre),
    })?;

    if argumentos.len() != definicion.parametros.len() {
        return Err(ErrorEvaluacion {
            mensaje: format!(
                "'{}' espera {} argumento(s), se recibieron {}",
                nombre,
                definicion.parametros.len(),
                argumentos.len()
            ),
        });
    }

    let mut valores_argumentos = Vec::with_capacity(argumentos.len());
    for arg in argumentos {
        valores_argumentos.push(evaluar(arg, entorno_llamador)?);
    }

    let mut scope_local = Entorno::new();
    for (parametro, valor) in definicion.parametros.iter().zip(valores_argumentos.into_iter()) {
        scope_local.insert(parametro.clone(), valor);
    }

    let profundidad_bucles_anterior = ctx.profundidad_bucles;
    ctx.profundidad_bucles = 0; // 'romper'/'continuar' no cruzan el limite de una funcion
    let resultado = ejecutar_en(&definicion.cuerpo, &mut scope_local, ctx, salida);
    ctx.profundidad_bucles = profundidad_bucles_anterior;

    match resultado? {
        Control::Retornar(valor) => Ok(valor),
        _ => Ok(Valor::Nulo),
    }
}

/// Conveniencia: parsea y ejecuta un programa completo de una sola vez,
/// devolviendo lo que hubiera impreso `decir`/`imprimir`, linea por
/// linea. Pensado para tests y para el modo demo de main.rs.
pub fn ejecutar_programa(texto: &str) -> Result<Vec<String>, String> {
    let sentencias = parsear_programa(texto).map_err(|e| e.to_string())?;
    let mut entorno = Entorno::new();
    ejecutar(&sentencias, &mut entorno).map_err(|e| e.mensaje)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn variable_y_decir_simple() {
        let programa = "variable x = 5\ndecir x";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["5".to_string()]);
    }

    #[test]
    fn decir_expresion() {
        let programa = "variable x = 5\nvariable b = 3\ndecir x + b";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["8".to_string()]);
    }

    #[test]
    fn reasignacion_de_variable() {
        let programa = "variable x = 1\nvariable x = x + 1\ndecir x";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["2".to_string()]);
    }

    #[test]
    fn si_sin_sino_rama_verdadera() {
        let programa = "variable x = 10\nsi x > 5\ndecir \"mayor\"\nfin";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["mayor".to_string()]);
    }

    #[test]
    fn si_sin_sino_rama_falsa_no_imprime_nada() {
        let programa = "variable x = 1\nsi x > 5\ndecir \"mayor\"\nfin";
        let salida = ejecutar_programa(programa).unwrap();
        assert!(salida.is_empty());
    }

    #[test]
    fn si_con_sino_rama_falsa() {
        let programa = "variable x = 1\nsi x > 5\ndecir \"mayor\"\nsino\ndecir \"menor o igual\"\nfin";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["menor o igual".to_string()]);
    }

    #[test]
    fn si_anidado() {
        let programa = "variable x = 10\nvariable alto = 20\nsi x > 5\nsi alto > 15\ndecir \"ambos\"\nfin\nfin";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["ambos".to_string()]);
    }

    #[test]
    fn comentarios_se_ignoran() {
        let programa = "# esto es un comentario\nvariable x = 5 // otro comentario\ndecir x";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["5".to_string()]);
    }

    #[test]
    fn lineas_vacias_se_ignoran() {
        let programa = "variable x = 5\n\n\ndecir x";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["5".to_string()]);
    }

    #[test]
    fn variable_no_declarada_da_error_de_ejecucion() {
        let programa = "decir no_existe";
        assert!(ejecutar_programa(programa).is_err());
    }

    #[test]
    fn si_sin_fin_da_error_sintactico_con_linea() {
        let programa = "variable x = 1\nsi x > 0\ndecir \"a\"";
        let error = parsear_programa(programa).unwrap_err();
        assert_eq!(error.linea, 2);
    }

    #[test]
    fn variable_sin_igual_da_error_con_linea() {
        let programa = "variable x";
        let error = parsear_programa(programa).unwrap_err();
        assert_eq!(error.linea, 1);
    }

    #[test]
    fn nombre_de_variable_que_choca_con_alias_logico_falla_al_usarse_en_expresion() {
        // 'y'/'o'/'no' son palabras reservadas (alias de and/or/not, ver
        // lexer.rs y el mismo _ALIAS_OPERADOR_LOGICO de lexer_sipi.py).
        // Declarar `variable y = 3` no falla (el nombre no pasa por el
        // lexer de expresiones), pero USARLA en una expresion si falla,
        // porque el lexer la lee como el operador 'and'. Paridad real
        // con el interprete Python, no un bug de esta fase.
        let programa = "variable y = 3\ndecir y";
        assert!(parsear_programa(programa).is_err());
    }

    #[test]
    fn mientras_basico() {
        let programa = "variable x = 0\nmientras x < 5\nvariable x = x + 1\nfin\ndecir x";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["5".to_string()]);
    }

    #[test]
    fn repetir_n_veces() {
        let programa = "variable contador = 0\nrepetir 3 veces\nvariable contador = contador + 1\ndecir contador\nfin";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["1".to_string(), "2".to_string(), "3".to_string()]);
    }

    #[test]
    fn romper_sale_del_bucle() {
        let programa = "variable x = 0\nmientras x < 100\nvariable x = x + 1\nsi x == 3\nromper\nfin\nfin\ndecir x";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["3".to_string()]);
    }

    #[test]
    fn continuar_salta_iteracion() {
        // suma todo menos cuando x vale 2
        let programa = "variable x = 0\nvariable suma = 0\nmientras x < 4\nvariable x = x + 1\nsi x == 2\ncontinuar\nfin\nvariable suma = suma + x\nfin\ndecir suma";
        let salida = ejecutar_programa(programa).unwrap();
        // x recorre 1,2,3,4 -> se salta el '+= x' cuando x=2 -> 1+3+4=8
        assert_eq!(salida, vec!["8".to_string()]);
    }

    #[test]
    fn romper_fuera_de_bucle_da_error() {
        let programa = "romper";
        assert!(ejecutar_programa(programa).is_err());
    }

    #[test]
    fn funcion_simple_con_llamar_valor() {
        let programa = "funcion sumar_dos(a, b)\ndevolver a + b\nfin\nllamar_valor sumar_dos(3, 4) -> resultado\ndecir resultado";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["7".to_string()]);
    }

    #[test]
    fn funcion_sin_devolver_da_nulo() {
        let programa = "funcion saluda(nombre)\ndecir \"hola \" + nombre\nfin\nllamar saluda(\"Mateo\")";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["hola Mateo".to_string()]);
    }

    #[test]
    fn funcion_recursiva() {
        let programa = "funcion factorial(n)\nsi n <= 1\ndevolver 1\nsino\nllamar_valor factorial(n - 1) -> resto\ndevolver n * resto\nfin\nfin\nllamar_valor factorial(5) -> resultado\ndecir resultado";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["120".to_string()]);
    }

    #[test]
    fn funcion_no_ve_variables_globales() {
        // Simplificacion deliberada documentada en el header del modulo:
        // scope local puro, la funcion no deberia ver 'externa'.
        let programa = "variable externa = 99\nfuncion f()\ndecir externa\nfin\nllamar f()";
        assert!(ejecutar_programa(programa).is_err());
    }

    #[test]
    fn funcion_con_numero_incorrecto_de_argumentos_da_error() {
        let programa = "funcion f(a, b)\ndevolver a + b\nfin\nllamar_valor f(1) -> x";
        assert!(ejecutar_programa(programa).is_err());
    }

    #[test]
    fn funcion_no_definida_da_error() {
        let programa = "llamar no_existe(1, 2)";
        assert!(ejecutar_programa(programa).is_err());
    }

    #[test]
    fn devolver_corta_ejecucion_del_resto_de_la_funcion() {
        let programa = "funcion f(x)\nsi x > 0\ndevolver \"positivo\"\nfin\ndevolver \"no positivo\"\nfin\nllamar_valor f(5) -> r\ndecir r";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["positivo".to_string()]);
    }

    #[test]
    fn devolver_dentro_de_bucle_corta_la_funcion_no_solo_el_bucle() {
        let programa = "funcion buscar()\nvariable i = 0\nmientras i < 10\nvariable i = i + 1\nsi i == 3\ndevolver i\nfin\nfin\ndevolver -1\nfin\nllamar_valor buscar() -> r\ndecir r";
        let salida = ejecutar_programa(programa).unwrap();
        assert_eq!(salida, vec!["3".to_string()]);
    }

    #[test]
    fn comando_desconocido_da_error_con_linea() {
        let programa = "variable x = 1\npara_cada item en lista\ndecir item\nfin";
        let error = parsear_programa(programa).unwrap_err();
        assert_eq!(error.mensaje.contains("para_cada"), true);
        assert_eq!(error.linea, 2);
    }
}
