from typing import Callable, Optional, TypeVar

InfBitString = Callable[[int], bool]
Predicate = Callable[[InfBitString], bool]
BitDict = dict[int, bool]


def next_bit_queried(p: Predicate, bits: BitDict) -> tuple[bool, Optional[int]]:
    next_bit = None

    def aux(n: int) -> bool:
        nonlocal next_bit
        b = bits.get(n)
        if b is not None:
            return b

        if next_bit is None:
            next_bit = n
        return False

    res = p(aux)
    return res, next_bit


def from_dict(bits: BitDict) -> InfBitString:
    return lambda n: bits.get(n, False)


def search(p: Predicate) -> Optional[BitDict]:
    def aux(bits: BitDict) -> bool:
        r, b = next_bit_queried(p, bits)
        if r:
            return True

        if b is None:
            return False

        bits[b] = False
        if aux(bits):
            return True

        bits[b] = True
        if aux(bits):
            return True

        del bits[b]
        return False

    bits: BitDict = {}
    if aux(bits):
        return bits
    else:
        return None


def forsome(p: Predicate) -> bool:
    return search(p) is not None


def forevery(p: Predicate) -> bool:
    return not forsome(lambda n: not p(n))


T = TypeVar("T")


def equal(p1: Callable[[InfBitString], T], p2: Callable[[InfBitString], T]) -> bool:
    return forevery(lambda n: p1(n) == p2(n))


def proj(n: int) -> Predicate:
    return lambda b: b(n)


def f(b: InfBitString) -> int:
    return b(7 * b(4) + 4 * b(7) + 4)


def g(b: InfBitString) -> int:
    return b(b(4) + 11 * (b(7)))


def h(b: InfBitString) -> int:
    if b(7):
        if b(4):
            return b(15)
        else:
            return b(8)
    else:
        if b(4):
            return b(11)
        else:
            return b(4)


def f2(b: InfBitString) -> int:
    return b(10 * b(3 ** 80) + 100 * b(4 ** 80) + 1000 * b(5 ** 80))


def g2(b: InfBitString) -> int:
    return b(10 * b(3 ** 80) + 100 * b(4 ** 80) + 1000 * b(6 ** 80))


def h2(b: InfBitString) -> int:
    if b(5 ** 80):
        i = 1000
    else:
        i = 0

    if b(3 ** 80):
        j = 10 + i
    else:
        j = i

    if b(4 ** 80):
        k = 100 + j
    else:
        k = j

    return b(k)


assert not equal(f, g)
assert equal(f, h)
assert not equal(g, h)
assert equal(f, f)
assert equal(g, g)
assert equal(h, h)

assert not equal(proj(2 ** 300), proj(2 ** 400))

assert not equal(f2, g2)
assert equal(f2, h2)
assert not equal(g2, h2)
assert equal(f2, f2)
assert equal(g2, g2)
assert equal(h2, h2)
