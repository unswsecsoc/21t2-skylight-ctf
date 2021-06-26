with open('qrcode.csv') as f:
    for s in f.readlines():
        s = s.replace('\n', '').replace(',','')
        print(r'\x'+r'\x'.join(hex(int(s[i: i + 8], 2)).replace('0x', '').zfill(2) for i in range(0, len(s), 8)), end=r'\x0A')
