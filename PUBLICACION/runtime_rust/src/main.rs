//! main.rs - Demo minima del prototipo de runtime Rust (item #70).
//! Evalua expresiones SiPi pasadas como argumentos de linea de comandos,
//! solo para poder probar el binario de punta a punta ademas de los
//! tests automaticos. No es un runtime completo -- ver la nota grande en
//! lexer.rs para el alcance real de esta fase.

mod lexer;
mod parser;

use std::collections::HashMap;
use std::env;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        println!("Prototipo de runtime SiPi en Rust (item #70 del feedback, fase 1: solo expresiones).");
        println!("Uso: sipi_runtime_rust \"2 + 3 * 4\"");
        return;
    }
    let expresion = args.join(" ");
    match parser::evaluar_texto(&expresion, &HashMap::new()) {
        Ok(valor) => println!("{}", valor),
        Err(mensaje) => {
            eprintln!("[SiPi/Rust] Error: {}", mensaje);
            std::process::exit(1);
        }
    }
}
