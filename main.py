from poly import Poly

a = Poly.from_str("2x + 5")
b = Poly.from_str("x + 1")
c = Poly.from_str("x + 4")

f = a * b * c

print(f)

print(f // Poly.from_str("x - 5"))
print(f % Poly.from_str("x - 5"))


