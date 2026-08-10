//! lexer.rs - Tokenizador de SiPi en Rust.
//!
//! Item #70 del feedback ("runtime alternativo... no hacerlo todavia,
//! dejar preparado el diseño"): esto es exactamente eso, el primer paso
//! real y compilable, no solo un diseño en papel. Replica a proposito el
//! MISMO comportamiento que `lexer_sipi.py` (Python, en la carpeta
//! padre) para el mismo subconjunto de SiPi (expresiones), de forma que
//! los tests puedan comparar ambos lado a lado y demostrar paridad real
//! entre los dos lenguajes de implementacion -- no "deberian dar lo
//! mismo", sino "dan lo mismo, verificado".

#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    Numero(f64),
    Texto(String),
    Identificador(String),
    Operador(String),
    ParentesisAbre,
    ParentesisCierra,
    Coma,
}

#[derive(Debug, Clone, PartialEq)]
pub struct TokenConColumna {
    pub token: Token,
    pub columna: usize,
}

#[derive(Debug, Clone, PartialEq)]
pub struct ErrorLexico {
    pub mensaje: String,
    pub columna: usize,
}

fn alias_operador_logico(palabra: &str) -> Option<&'static str> {
    match palabra {
        "y" => Some("and"),
        "o" => Some("or"),
        "no" => Some("not"),
        "and" => Some("and"),
        "or" => Some("or"),
        "not" => Some("not"),
        _ => None,
    }
}

pub fn tokenizar(texto: &str) -> Result<Vec<TokenConColumna>, ErrorLexico> {
    let caracteres: Vec<char> = texto.chars().collect();
    let n = caracteres.len();
    let mut tokens = Vec::new();
    let mut i = 0usize;

    while i < n {
        let c = caracteres[i];

        if c == ' ' || c == '\t' {
            i += 1;
            continue;
        }

        if c == '"' {
            let inicio = i;
            i += 1;
            let mut pieza = String::new();
            while i < n && caracteres[i] != '"' {
                if caracteres[i] == '\\' && i + 1 < n {
                    let siguiente = caracteres[i + 1];
                    let traducido = match siguiente {
                        'n' => '\n',
                        't' => '\t',
                        '"' => '"',
                        '\\' => '\\',
                        '\'' => '\'',
                        otro => otro,
                    };
                    pieza.push(traducido);
                    i += 2;
                } else {
                    pieza.push(caracteres[i]);
                    i += 1;
                }
            }
            if i >= n {
                return Err(ErrorLexico {
                    mensaje: "Cadena de texto sin cerrar (falta la comilla final '\"')".to_string(),
                    columna: inicio,
                });
            }
            i += 1; // consume la comilla de cierre
            tokens.push(TokenConColumna { token: Token::Texto(pieza), columna: inicio });
            continue;
        }

        if c.is_ascii_digit() || (c == '.' && i + 1 < n && caracteres[i + 1].is_ascii_digit()) {
            let inicio = i;
            let mut tiene_punto = false;
            while i < n && (caracteres[i].is_ascii_digit() || (caracteres[i] == '.' && !tiene_punto)) {
                if caracteres[i] == '.' {
                    tiene_punto = true;
                }
                i += 1;
            }
            let crudo: String = caracteres[inicio..i].iter().collect();
            let valor: f64 = crudo.parse().unwrap_or(0.0);
            tokens.push(TokenConColumna { token: Token::Numero(valor), columna: inicio });
            continue;
        }

        if c.is_alphabetic() || c == '_' {
            let inicio = i;
            while i < n && (caracteres[i].is_alphanumeric() || caracteres[i] == '_') {
                i += 1;
            }
            let palabra: String = caracteres[inicio..i].iter().collect();
            if let Some(op) = alias_operador_logico(&palabra) {
                tokens.push(TokenConColumna { token: Token::Operador(op.to_string()), columna: inicio });
            } else {
                tokens.push(TokenConColumna { token: Token::Identificador(palabra), columna: inicio });
            }
            continue;
        }

        // Operadores de dos caracteres ANTES que los de uno, mismo orden
        // que en lexer_sipi.py, por la misma razon: '==' no se puede
        // tokenizar como dos '=' sueltos.
        if i + 1 < n {
            let dos: String = caracteres[i..i + 2].iter().collect();
            if ["==", "!=", "<=", ">="].contains(&dos.as_str()) {
                tokens.push(TokenConColumna { token: Token::Operador(dos), columna: i });
                i += 2;
                continue;
            }
        }

        if "+-*/%<>".contains(c) {
            tokens.push(TokenConColumna { token: Token::Operador(c.to_string()), columna: i });
            i += 1;
            continue;
        }

        if c == '(' {
            tokens.push(TokenConColumna { token: Token::ParentesisAbre, columna: i });
            i += 1;
            continue;
        }
        if c == ')' {
            tokens.push(TokenConColumna { token: Token::ParentesisCierra, columna: i });
            i += 1;
            continue;
        }
        if c == ',' {
            tokens.push(TokenConColumna { token: Token::Coma, columna: i });
            i += 1;
            continue;
        }

        return Err(ErrorLexico { mensaje: format!("Caracter inesperado: '{}'", c), columna: i });
    }

    Ok(tokens)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn numeros_enteros_y_decimales() {
        let tokens = tokenizar("42 3.14").unwrap();
        assert_eq!(tokens[0].token, Token::Numero(42.0));
        assert_eq!(tokens[1].token, Token::Numero(3.14));
    }

    #[test]
    fn texto_con_escapes() {
        let tokens = tokenizar(r#""hola\nmundo""#).unwrap();
        assert_eq!(tokens[0].token, Token::Texto("hola\nmundo".to_string()));
    }

    #[test]
    fn texto_sin_cerrar_da_error_con_columna() {
        let error = tokenizar(r#"decir "sin cerrar"#).unwrap_err();
        assert_eq!(error.columna, 6);
    }

    #[test]
    fn alias_logicos_en_espanol_se_traducen() {
        let tokens = tokenizar("x y verdadero").unwrap();
        assert_eq!(tokens[0].token, Token::Identificador("x".to_string()));
        assert_eq!(tokens[1].token, Token::Operador("and".to_string()));
        assert_eq!(tokens[2].token, Token::Identificador("verdadero".to_string()));
    }

    #[test]
    fn operadores_de_dos_caracteres_no_se_confunden() {
        let tokens = tokenizar("a >= b == c").unwrap();
        let operadores: Vec<&str> = tokens.iter().filter_map(|t| match &t.token {
            Token::Operador(op) => Some(op.as_str()),
            _ => None,
        }).collect();
        assert_eq!(operadores, vec![">=", "=="]);
    }

    #[test]
    fn caracter_desconocido_da_error_con_columna_exacta() {
        let error = tokenizar("5 @ 2").unwrap_err();
        assert_eq!(error.columna, 2);
    }
}
