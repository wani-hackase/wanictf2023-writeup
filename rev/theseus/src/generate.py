tar = "FLAG{vKCsq3jl4j_Y0uMade1t}"
ans = "FLAG"
for i in range(4, 26):
    temp = (ord(tar[i])) - (i * 11) % 15

    ans += chr(temp)
print(ans)
