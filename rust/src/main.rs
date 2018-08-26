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

    let result = expr(&mut cur);
    println!("Result: {}", result);
}


fn get_next_token(cur: &mut Cursor) -> Token {
    if cur.pos <= (cur.text.trim().len() - 1) as u32 {
        let current_char = cur.text.chars()
            .nth(cur.pos as usize)
            .expect("EOF reached for provided expression");

        if current_char.is_numeric() {
            let token = Token {typ: String::from("INTEGER"), val: current_char};
            cur.pos += 1;
            return token;
        } else if current_char == '+' {
            let token = Token {typ: String::from("PLUS"), val: current_char};
            cur.pos += 1;
            return token;
        }
    }
    Token {typ: String::from("EOF"), val: ' '}
}

fn expr(cur: &mut Cursor) -> u32 {
    let left = get_next_token(cur);
    if left.typ == "INTEGER" {
        let op = get_next_token(cur);
        if op.typ == "PLUS" {
            let right = get_next_token(cur);
            if right.typ == "INTEGER" {
                let lt: u32 = left.val.to_digit(10)
                    .expect("Integer parsing failed");

                let rt: u32 = right.val.to_digit(10)
                    .expect("Integer parsing failed");
                
                return lt + rt;
            }
        }
    }
    0
}