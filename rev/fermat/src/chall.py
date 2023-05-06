flag = b"FLAG{you_need_a_lot_of_time_and_effort_to_solve_reversing_208b47bd66c2cd8}\x00\x00"
flag = [
    0xB0C0B0C0 ^ int.from_bytes(flag[i : i + 4], "little")
    for i in range(0, len(flag), 4)
]
print(flag)
buffer = [0 for _ in range(len(flag) * 4)]
for i, x in enumerate(flag):
    buffer[4 * i + 0] = ((x ^ 0x000000C0) >> 0x00) & 0xFF
    buffer[4 * i + 1] = ((x ^ 0x0000B000) >> 0x08) & 0xFF
    buffer[4 * i + 2] = ((x ^ 0x00C00000) >> 0x10) & 0xFF
    buffer[4 * i + 3] = ((x ^ 0xB0000000) >> 0x18) & 0xFF
    print(bytes(buffer))
