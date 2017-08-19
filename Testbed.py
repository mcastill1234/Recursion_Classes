import string

shift_dict = {}
dkeysl = string.ascii_lowercase
dkeysu = string.ascii_uppercase

shift = 4

for char in dkeysl:
    if dkeysl.index(char) + shift < 26:
        shift_dict[char] = dkeysl[dkeysl.index(char)+shift]
    elif dkeysl.index(char) + shift >= 26:
        shift_dict[char] = dkeysl[dkeysl.index(char)+shift-26]

for char in dkeysu:
    if dkeysu.index(char) + shift < 26:
        shift_dict[char] = dkeysu[dkeysu.index(char)+shift]
    elif dkeysu.index(char) + shift >= 26:
        shift_dict[char] = dkeysu[dkeysu.index(char)+shift-26]

print(shift_dict.keys())
print(shift_dict.values())
