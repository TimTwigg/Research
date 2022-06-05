# updated 4 June 2022
# generate c++ map<char, int> items for letter and symbol hex codes

letters = "abcdefghijklmnopqrstuvwxyz"
symbols = "\\/{}[],;:'\"!@~.+=-_ 1234567890"
d = {}

for l in letters.upper():
    d[l] = hex(ord(l))

for l in letters:
    d[l] = hex(ord(l))

for s in symbols:
    d[s] = hex(ord(s))

out = []
for k,v in d.items():
    out.append(f"{{'{k}', {v}}}")

print(",\n".join(out))