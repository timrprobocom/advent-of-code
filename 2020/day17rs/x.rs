use itertools::iproduct;

fn main() {
    let p = iproduct!( -1..1, -1..1, -1..1, -1..1 );
    p
        .filter(|x| *x != (0,0,0,0))
        .for_each(|x| println!("{:?}", x));
}
