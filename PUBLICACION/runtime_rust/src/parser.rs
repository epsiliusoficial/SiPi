//! parser.rs - Parser recursivo-descendente + evaluador de expresiones,
//! version Rust de ast_sipi.py (misma gramatica, mismas precedencias).
//! Ver la nota grande en lexer.rs para el alcance real de esta fase.

use crate::lexer::{tokenizar, Token, TokenConColumna};
use std::collections::HashMap;
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Valor {
    Numero(f64),
    Texto(String),
    Booleano(bool),
    Nulo,
}

impl fmt::Display for Valor {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Valor::Numero(n) => {
                if n.fract() == 0.0 {
                    write!(f, "{}", *n as i64)
                } else {
                    write!(f, "{}", n)
                }
            }
            Valor::Texto(s) => write!(f, "{}", s),
            Valor::Booleano(b) => write!(f, "{}", if *b { "verdadero" } else { "falso" }),
            Valor::Nulo => write!(f, "nulo"),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum Nodo {
    NumeroLiteral(f64),
    TextoLiteral(String),
    BooleanoLiteral(bool),
    NuloLiteral,
    Variable(String),
    Unario(String, Box<Nodo>),
    Binario(Box<Nodo>, String, Box<Nodo>),
}

#[derive(Debug, Clone, PartialEq)]
pub struct ErrorSintactico {
    pub mensaje: String,
    pub columna: usize,
}

#[derive(Debug, Clone, PartialEq)]
pub struct ErrorEvaluacion {
    pub mensaje: String,
}

struct Parser {
    tokens: Vec<TokenConColumna>,
    pos: usize,
}

impl Parser {
    fn actual(&self) -> Option<&TokenConColumna> {
        self.tokens.get(self.pos)
    }

    fn avanzar(&mut self) -> Option<TokenConColumna> {
        let actual = self.tokens.get(self.pos).cloned();
        if self.pos < self.tokens.len() {
            self.pos += 1;
        }
        actual
    }

    fn coincide_operador(&self, ops: &[&str]) -> bool {
        match self.actual() {
            Some(TokenConColumna { token: Token::Operador(op), .. }) => ops.contains(&op.as_str()),
            _ => false,
        }
    }

    fn parsear_expresion(&mut self) -> Result<Nodo, ErrorSintactico> {
        let nodo = self.logico_or()?;
        if self.actual().is_some() {
            let t = self.actual().unwrap();
            return Err(ErrorSintactico {
                mensaje: format!("Se esperaba el final de la expresion, se encontro {:?}", t.token),
                columna: t.columna,
            });
        }
        Ok(nodo)
    }

    fn logico_or(&mut self) -> Result<Nodo, ErrorSintactico> {
        let mut nodo = self.logico_and()?;
        while self.coincide_operador(&["or"]) {
            self.avanzar();
            let der = self.logico_and()?;
            nodo = Nodo::Binario(Box::new(nodo), "or".to_string(), Box::new(der));
        }
        Ok(nodo)
    }

    fn logico_and(&mut self) -> Result<Nodo, ErrorSintactico> {
        let mut nodo = self.igualdad()?;
        while self.coincide_operador(&["and"]) {
            self.avanzar();
            let der = self.igualdad()?;
            nodo = Nodo::Binario(Box::new(nodo), "and".to_string(), Box::new(der));
        }
        Ok(nodo)
    }

    fn igualdad(&mut self) -> Result<Nodo, ErrorSintactico> {
        let mut nodo = self.comparacion()?;
        while self.coincide_operador(&["==", "!="]) {
            let op = self.avanzar().unwrap();
            let der = self.comparacion()?;
            nodo = Nodo::Binario(Box::new(nodo), op_str(&op.token), Box::new(der));
        }
        Ok(nodo)
    }

    fn comparacion(&mut self) -> Result<Nodo, ErrorSintactico> {
        let mut nodo = self.suma()?;
        while self.coincide_operador(&["<", "<=", ">", ">="]) {
            let op = self.avanzar().unwrap();
            let der = self.suma()?;
            nodo = Nodo::Binario(Box::new(nodo), op_str(&op.token), Box::new(der));
        }
        Ok(nodo)
    }

    fn suma(&mut self) -> Result<Nodo, ErrorSintactico> {
        let mut nodo = self.termino()?;
        while self.coincide_operador(&["+", "-"]) {
            let op = self.avanzar().unwrap();
            let der = self.termino()?;
            nodo = Nodo::Binario(Box::new(nodo), op_str(&op.token), Box::new(der));
        }
        Ok(nodo)
    }

    fn termino(&mut self) -> Result<Nodo, ErrorSintactico> {
        let mut nodo = self.unario()?;
        while self.coincide_operador(&["*", "/", "%"]) {
            let op = self.avanzar().unwrap();
            let der = self.unario()?;
            nodo = Nodo::Binario(Box::new(nodo), op_str(&op.token), Box::new(der));
        }
        Ok(nodo)
    }

    fn unario(&mut self) -> Result<Nodo, ErrorSintactico> {
        if self.coincide_operador(&["not", "-", "+"]) {
            let op = self.avanzar().unwrap();
            let operando = self.unario()?;
            return Ok(Nodo::Unario(op_str(&op.token), Box::new(operando)));
        }
        self.primario()
    }

    fn primario(&mut self) -> Result<Nodo, ErrorSintactico> {
        let actual = self.actual().cloned().ok_or(ErrorSintactico {
            mensaje: "Se esperaba un valor, se encontro el final de la expresion".to_string(),
            columna: 0,
        })?;
        match actual.token {
            Token::Numero(n) => {
                self.avanzar();
                Ok(Nodo::NumeroLiteral(n))
            }
            Token::Texto(s) => {
                self.avanzar();
                Ok(Nodo::TextoLiteral(s))
            }
            Token::Identificador(ref nombre) => {
                self.avanzar();
                match nombre.as_str() {
                    "verdadero" => Ok(Nodo::BooleanoLiteral(true)),
                    "falso" => Ok(Nodo::BooleanoLiteral(false)),
                    "nulo" => Ok(Nodo::NuloLiteral),
                    _ => Ok(Nodo::Variable(nombre.clone())),
                }
            }
            Token::ParentesisAbre => {
                self.avanzar();
                let nodo = self.logico_or()?;
                match self.actual() {
                    Some(TokenConColumna { token: Token::ParentesisCierra, .. }) => {
                        self.avanzar();
                        Ok(nodo)
                    }
                    _ => Err(ErrorSintactico { mensaje: "Falta cerrar ')'".to_string(), columna: actual.columna }),
                }
            }
            _ => Err(ErrorSintactico {
                mensaje: format!("Se esperaba un valor, se encontro {:?}", actual.token),
                columna: actual.columna,
            }),
        }
    }
}

fn op_str(token: &Token) -> String {
    match token {
        Token::Operador(s) => s.clone(),
        _ => String::new(),
    }
}

pub fn parsear(texto: &str) -> Result<Nodo, ErrorSintactico> {
    let tokens = tokenizar(texto).map_err(|e| ErrorSintactico { mensaje: e.mensaje, columna: e.columna })?;
    let mut parser = Parser { tokens, pos: 0 };
    parser.parsear_expresion()
}

/// Alias publico de `parsear`, usado por sentencias.rs. Mismo nombre que
/// se le hubiera dado si esta funcion hubiera nacido pensada para
/// sentencias desde el principio -- se mantiene `parsear` tambien por
/// compatibilidad con el modo demo de main.rs.
pub fn parsear_expresion_str(texto: &str) -> Result<Nodo, ErrorSintactico> {
    parsear(texto)
}

fn es_verdadero(valor: &Valor) -> bool {
    match valor {
        Valor::Booleano(b) => *b,
        Valor::Nulo => false,
        Valor::Numero(n) => *n != 0.0,
        Valor::Texto(s) => !s.is_empty(),
    }
}

pub fn evaluar(nodo: &Nodo, variables: &HashMap<String, Valor>) -> Result<Valor, ErrorEvaluacion> {
    match nodo {
        Nodo::NumeroLiteral(n) => Ok(Valor::Numero(*n)),
        Nodo::TextoLiteral(s) => Ok(Valor::Texto(s.clone())),
        Nodo::BooleanoLiteral(b) => Ok(Valor::Booleano(*b)),
        Nodo::NuloLiteral => Ok(Valor::Nulo),
        Nodo::Variable(nombre) => variables.get(nombre).cloned().ok_or_else(|| ErrorEvaluacion {
            mensaje: format!("Variable no declarada: '{}'", nombre),
        }),
        Nodo::Unario(op, operando) => {
            let valor = evaluar(operando, variables)?;
            match op.as_str() {
                "-" => match valor {
                    Valor::Numero(n) => Ok(Valor::Numero(-n)),
                    _ => Err(ErrorEvaluacion { mensaje: "No se puede negar un valor no numerico".to_string() }),
                },
                "+" => Ok(valor),
                "not" => Ok(Valor::Booleano(!es_verdadero(&valor))),
                _ => Err(ErrorEvaluacion { mensaje: format!("Operador unario desconocido: {}", op) }),
            }
        }
        Nodo::Binario(izq, op, der) => evaluar_binario(izq, op, der, variables),
    }
}

fn evaluar_binario(izq: &Nodo, op: &str, der: &Nodo, variables: &HashMap<String, Valor>) -> Result<Valor, ErrorEvaluacion> {
    if op == "and" {
        let vi = evaluar(izq, variables)?;
        return if !es_verdadero(&vi) { Ok(vi) } else { evaluar(der, variables) };
    }
    if op == "or" {
        let vi = evaluar(izq, variables)?;
        return if es_verdadero(&vi) { Ok(vi) } else { evaluar(der, variables) };
    }

    let vi = evaluar(izq, variables)?;
    let vd = evaluar(der, variables)?;

    match op {
        "+" => {
            if let (Valor::Numero(a), Valor::Numero(b)) = (&vi, &vd) {
                Ok(Valor::Numero(a + b))
            } else {
                Ok(Valor::Texto(format!("{}{}", vi, vd)))
            }
        }
        "-" | "*" | "/" | "%" => {
            let (a, b) = match (&vi, &vd) {
                (Valor::Numero(a), Valor::Numero(b)) => (*a, *b),
                _ => return Err(ErrorEvaluacion { mensaje: format!("'{}' necesita numeros a ambos lados", op) }),
            };
            match op {
                "-" => Ok(Valor::Numero(a - b)),
                "*" => Ok(Valor::Numero(a * b)),
                "/" => {
                    if b == 0.0 {
                        Err(ErrorEvaluacion { mensaje: format!("Division por cero al evaluar la expresion '{} / {}'.", a, b) })
                    } else {
                        Ok(Valor::Numero(a / b))
                    }
                }
                "%" => {
                    if b == 0.0 {
                        Err(ErrorEvaluacion { mensaje: format!("Division por cero al evaluar la expresion '{} % {}'.", a, b) })
                    } else {
                        Ok(Valor::Numero(a % b))
                    }
                }
                _ => unreachable!(),
            }
        }
        "==" => Ok(Valor::Booleano(vi == vd)),
        "!=" => Ok(Valor::Booleano(vi != vd)),
        "<" | "<=" | ">" | ">=" => {
            let (a, b) = match (&vi, &vd) {
                (Valor::Numero(a), Valor::Numero(b)) => (*a, *b),
                _ => return Err(ErrorEvaluacion { mensaje: format!("'{}' necesita numeros a ambos lados", op) }),
            };
            let resultado = match op {
                "<" => a < b,
                "<=" => a <= b,
                ">" => a > b,
                ">=" => a >= b,
                _ => unreachable!(),
            };
            Ok(Valor::Booleano(resultado))
        }
        _ => Err(ErrorEvaluacion { mensaje: format!("Operador desconocido: {}", op) }),
    }
}

pub fn evaluar_texto(texto: &str, variables: &HashMap<String, Valor>) -> Result<Valor, String> {
    let nodo = parsear(texto).map_err(|e| e.mensaje)?;
    evaluar(&nodo, variables).map_err(|e| e.mensaje)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sin_variables() -> HashMap<String, Valor> {
        HashMap::new()
    }

    #[test]
    fn precedencia_multiplicacion_sobre_suma() {
        assert_eq!(evaluar_texto("2 + 3 * 4", &sin_variables()).unwrap(), Valor::Numero(14.0));
    }

    #[test]
    fn parentesis_cambian_precedencia() {
        assert_eq!(evaluar_texto("(2 + 3) * 4", &sin_variables()).unwrap(), Valor::Numero(20.0));
    }

    #[test]
    fn division_por_cero_da_error() {
        assert!(evaluar_texto("5 / 0", &sin_variables()).is_err());
    }

    #[test]
    fn comparaciones() {
        assert_eq!(evaluar_texto("5 > 3", &sin_variables()).unwrap(), Valor::Booleano(true));
        assert_eq!(evaluar_texto("5 == 5", &sin_variables()).unwrap(), Valor::Booleano(true));
    }

    #[test]
    fn variables_reales() {
        let mut vars = HashMap::new();
        vars.insert("x".to_string(), Valor::Numero(10.0));
        vars.insert("b".to_string(), Valor::Numero(5.0));
        assert_eq!(evaluar_texto("x + b", &vars).unwrap(), Valor::Numero(15.0));
    }

    #[test]
    fn concatenacion_de_texto() {
        let mut vars = HashMap::new();
        vars.insert("nombre".to_string(), Valor::Texto("Mateo".to_string()));
        assert_eq!(
            evaluar_texto("\"hola \" + nombre", &vars).unwrap(),
            Valor::Texto("hola Mateo".to_string())
        );
    }

    #[test]
    fn negacion_logica_alias_espanol() {
        assert_eq!(evaluar_texto("no verdadero", &sin_variables()).unwrap(), Valor::Booleano(false));
    }

    #[test]
    fn variable_no_declarada_da_error() {
        assert!(evaluar_texto("no_existe + 1", &sin_variables()).is_err());
    }

    #[test]
    fn unario_encadenado() {
        assert_eq!(evaluar_texto("- - 5", &sin_variables()).unwrap(), Valor::Numero(5.0));
    }

    #[test]
    fn expresion_incompleta_da_error_sintactico() {
        assert!(parsear("2 + ").is_err());
    }

    #[test]
    fn parentesis_sin_cerrar_da_error_sintactico() {
        assert!(parsear("(2 + 3").is_err());
    }
}
