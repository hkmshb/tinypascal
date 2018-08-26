use std::io::{self, Write};


#[derive(Debug)]
struct Token {
    typ: String,
    val: char,
}

struct Cursor {
    text: String,
    pos: u32,
}

fn main() {
    let mut cur = Cursor {
        text: String::new(),
        pos: 0,
    };

    print!("calc> ");
    io::stdout().flush().expect("Print failed");

    io::stdin().read_line(&mut cur.text)
        .expect("Failed to read line");

    let token = get_next_token(cur);
    println!("Current Token: {:?}", token);
}

fn get_next_token(cur: Cursor) -> Token {
    if cur.pos <= (cur.text.trim().len() - 1) as u32 {
        let current_char = cur.text.chars()
            .nth(cur.pos as usize)
            .expect("EOF reached for provided expression");

        if current_char.is_numeric() {
            return Token {typ: String::from("INTEGER"), val: current_char};
        } else if current_char == '+' {
            return Token {typ: String::from("PLUS"), val: current_char};
        }
    }
    Token {typ: String::from("EOF"), val: ' '}
}
