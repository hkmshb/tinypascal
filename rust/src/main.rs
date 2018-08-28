use std::io::{self, Write};


#[derive(Debug)]
struct Token {
    typ: String,
    val: String,
}


#[derive(Debug)]
struct Cursor {
    pos: usize,
    text: String,
    current_token: Token
}

impl Cursor {
    fn new(text: String) -> Cursor {
        Cursor {
            pos: 0,
            text: text.trim().to_string(),
            current_token: Token {typ: String::from("BOF"), val: "".to_string()}
        }
    }

    fn current(&self) -> char {
        if self.pos <= self.text.len() - 1 {
            return self.text.chars()
                .nth(self.pos)
                .unwrap()
        }
        '?'
    }

    fn next(&mut self) -> char {
        self.pos += 1;
        if self.pos <= self.text.len() - 1 {
            return self.text.chars()
                .nth(self.pos)
                .unwrap()
        }
        '?'
    }

    fn reset(&mut self) {
        self.pos = 0;
        self.current_token = Token {
            typ: "BOF".to_string(),
            val: "".to_string()
        };
    }

    fn skip_whitespace(&mut self) {
        let mut current_char = self.current();
        while current_char != '?' && current_char.is_whitespace() {
            current_char = self.next();
        }
    }
}


fn main() {
    loop {
        let mut text = String::new();
        while text.trim().is_empty() {
            print!("calc> ");
            io::stdout().flush()
                .expect("Print failed!");

            io::stdin().read_line(&mut text)
                .expect("Failed to read line!");
        }

        let result = expr(text);
        println!("  >>> {}\n", result);
    }
}


fn expr(text: String) -> u32 {
    let mut cur = Cursor::new(text);
    cur.current_token = get_next_token(&mut cur);

    let mut result = term(&mut cur);
    while ["PLUS", "MINUS"].contains(&&cur.current_token.typ[..]) {
        if cur.current_token.typ == "PLUS" {
            eat(&mut cur, String::from("PLUS"));
            result += term(&mut cur);
        } else {
            eat(&mut cur, String::from("MINUS"));
            result -= term(&mut cur);
        }
    }
    result
}


fn get_next_token(cur: &mut Cursor) -> Token {
    let mut current_char = cur.current();
    while current_char != '?' {
        if current_char.is_whitespace() {
            cur.skip_whitespace();
            current_char = cur.current();
            continue;
        }

        if current_char.is_numeric() {
            let digits = get_digits(cur);
            return Token {
                typ: String::from("INTEGER"),
                val: digits
            };
        }
        if "+-".contains(current_char) {
            cur.next();

            if current_char == '+' {
                return Token {
                    typ: String::from("PLUS"),
                    val: current_char.to_string()
                };
            }
            return Token {
                typ: String::from("MINUS"),
                val: current_char.to_string()
            };
        }
    }
    Token {typ:String::from("EOF"), val: "".to_string()}
}


fn get_digits(cur: &mut Cursor) -> String {
    let mut digits = String::new();
    let mut current_char = cur.current();
    while current_char != '?' && current_char.is_numeric() {
        digits.push(current_char);
        current_char = cur.next();
    }

    digits
}


fn eat(cur: &mut Cursor, token_type: String) {
    if cur.current_token.typ == token_type {
        cur.current_token = get_next_token(cur);
    }
}


fn term(cur: &mut Cursor) -> u32 {
    let value = cur.current_token.val.clone();
    eat(cur, String::from("INTEGER"));

    let value: u32 = value.parse()
        .expect("Invalid integer token");

    value
}