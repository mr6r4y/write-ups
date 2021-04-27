# SoulCrabber

## Description

Aliens heard of this cool newer language called Rust, and hoped the safety it offers could be used to improve their stream cipher.

```rust
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;
use std::fs;
use std::io::Write;

fn get_rng() -> StdRng {
    let seed = 13371337;
    return StdRng::seed_from_u64(seed);
}

fn rand_xor(input : String) -> String {
    let mut rng = get_rng();
    return input
        .chars()
        .into_iter()
        .map(|c| format!("{:02x}", (c as u8 ^ rng.gen::<u8>())))
        .collect::<Vec<String>>()
        .join("");
}

fn main() -> std::io::Result<()> {
    let flag = fs::read_to_string("flag.txt")?;
    let xored = rand_xor(flag);
    println!("{}", xored);
    let mut file = fs::File::create("out.txt")?;
    file.write(xored.as_bytes())?;
    Ok(())
}
```

`1b591484db962f7782d1410afa4a388f7930067bcef6df546a57d9f873`

## Solution

Make the `flag.txt` binary by working with `Vec<u8>`:

```rust
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;
use std::fs;
use std::io::Write;

fn get_rng() -> StdRng {
    let seed = 13371337;
    return StdRng::seed_from_u64(seed);
}

fn rand_xor(input: Vec<u8>) -> String {
    let mut rng = get_rng();
    return input
        .into_iter()
        .map(|c| format!("{:02x}", (c as u8 ^ rng.gen::<u8>())))
        .collect::<Vec<String>>()
        .join("");
}

fn main() -> std::io::Result<()> {
    let flag = fs::read("flag.txt")?;
    let xored = rand_xor(flag);
    println!("{}", xored);
    let mut file = fs::File::create("out.txt")?;
    file.write(xored.as_bytes())?;
    Ok(())
}
```

Put the binary result in `flag.txt`:

```python
from binascii import unhexlify
open("flag.txt", "wb").write(unhexlify("1b591484db962f7782d1410afa4a388f7930067bcef6df546a57d9f873"))
```

Compile with `cargo`:

- `cargo new`
- Put code in `main.rs`
- Add deppendency in `Cargo.toml`: `rand = "*"`
- `cargo build`
- Move `flag.txt` where the build is and run executable

Get the flag:

```python
from binascii import unhexlify
unhexlify("434854427b6d656d3072795f733466335f6372797074305f6634316c7d")

```
