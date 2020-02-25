with open("header.txt") as f:
    res = f.readlines()
headers ={}
for r in res:
    headers[r.split(": ")[0]]=r.split(": ")[1].replace("\n","")
print(headers)