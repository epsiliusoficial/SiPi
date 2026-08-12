//! main.rs - Demo minima del prototipo de runtime Rust (item #70).
//! Dos modos:
//!  - Un solo argumento SIN salto de linea y que parece una expresion
//!    suelta -> se evalua como expresion (fase 1, compatibilidad con
//!    versiones anteriores del binario).
//!  - Un archivo .sipi (ruta como argumento) o texto con varias lineas
//!    -> se parsea y ejecuta como programa con `variable`/`decir`/`si`
//!    (fase 2, ver sentencias.rs).
//! No es un runtime completo -- ver la nota grande en lexer.rs para el
//! alcance real de esta fase.

mod lexer;
mod parser;
mod sentencias;

use std::collections::HashMap;
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        println!("Prototipo de runtime SiPi en Rust (item #70 del feedback, fase 2: expresiones + variable/decir/si).");
        println!("Uso:");
        println!("  sipi_runtime_rust \"2 + 3 * 4\"          (evalua una expresion suelta)");
        println!("  sipi_runtime_rust programa.sipi          (ejecuta un archivo)");
        return;
    }

    // Si el argumento es una ruta a un archivo existente, lo leemos como
    // programa. Si no, tratamos todos los argumentos juntos como texto:
    // programa multilinea si contiene '\n', expresion suelta si no.
    let texto = if args.len() == 1 && fs::metadata(&args[0]).is_ok() {
        match fs::read_to_string(&args[0]) {
            Ok(contenido) => contenido,
            Err(err) => {
                eprintln!("[SiPi/Rust] No se pudo leer '{}': {}", args[0], err);
                std::process::exit(1);
            }
        }
    } else {
        args.join(" ")
    };

    if texto.contains('\n') {
        match sentencias::ejecutar_programa(&texto) {
            Ok(salida) => {
                for linea in salida {
                    println!("{}", linea);
                }
            }
            Err(mensaje) => {
                eprintln!("[SiPi/Rust] Error: {}", mensaje);
                std::process::exit(1);
            }
        }
    } else {
        match parser::evaluar_texto(&texto, &HashMap::new()) {
            Ok(valor) => println!("{}", valor),
            Err(mensaje) => {
                eprintln!("[SiPi/Rust] Error: {}", mensaje);
                std::process::exit(1);
            }
        }
    }
}
