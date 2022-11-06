
import random
for _ in range(100):
    id = random.randint(1, 100000)
    alan = random.random() * 1000
    no = random.randint(1, 100)
    ilid = random.randint(1, 81)
    print(f"INSERT INTO parsel(id, alan, no, ilid) VALUES ({id}, {alan}, {no}, {ilid});")
