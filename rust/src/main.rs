use std::io::{self, Write};


fn main() {
    let mut text: String = String::new();

    print!("calc> ");
    io::stdout().flush();

    io::stdin().read_line(&mut text)
        .expect("Failed to read line");

    println!("Entered expression: {}", text);
}
