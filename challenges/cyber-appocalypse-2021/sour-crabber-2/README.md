# SoulCrabber 2

## Description

Aliens realised that hard-coded values are bad, so added a little bit of entropy.

```rust
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;
use std::fs;
use std::io::Write;
use std::time::SystemTime;

fn get_rng() -> StdRng {
    let seed = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .expect("Time is broken")
        .as_secs();
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

`418a5175c38caf8c1cafa92cde06539d512871605d06b2d01bbc1696f4ff487e9d46ba0b5aaf659807`

## Solution

```rust
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;
use std::time::SystemTime;

fn get_rng() -> StdRng {
    let seed = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .expect("Time is broken")
        .as_secs();
    return StdRng::seed_from_u64(seed);
}

fn is_sub<T: PartialEq>(mut haystack: &[T], needle: &[T]) -> bool {
    if needle.len() == 0 { return true; }
    while !haystack.is_empty() {
        if haystack.starts_with(needle) { return true; }
        haystack = &haystack[1..];
    }
    false
}

fn rand_xor(input : &Vec<u8>, mut rng: StdRng) -> Vec<u8> {
    return input
        .into_iter()
        .map(|c| c  ^ rng.gen::<u8>())
        .collect::<Vec<u8>>();
}

fn main() -> std::io::Result<()> {
    let out: Vec<u8> = vec![65, 138, 81, 117, 195, 140, 175, 140, 28, 175, 169, 44, 222, 6, 83, 157, 81, 40, 113, 96, 93, 6, 178, 208, 27, 188, 22, 150, 244, 255, 72, 126, 157, 70, 186, 11, 90, 175, 101, 152, 7];
    let first_bytes: Vec<u8> = vec![67, 72, 84, 66, 123];

    let mut seed = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .expect("Time is broken")
        .as_secs();

    loop {
        let mut rng = StdRng::seed_from_u64(seed);
        let r = rand_xor(&out, rng);
        if is_sub(&r, &first_bytes) {
            let s = r
            .into_iter()
            .map(|c| format!("{:02x}", c))
            .collect::<Vec<String>>()
            .join("");
            println!("{}", s);
            break;
        }
        seed = seed - 1;
    }


    Ok(())
}
```

and then:

```python
from binascii import unhexlify
unhexlify("434854427b636c34353531635f6368346c6c336e67335f72337772317474336e5f316e5f727535747d")
```