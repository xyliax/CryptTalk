mod security;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let s = security::from_python();
    println!("{}", s);
    Ok(())
}
