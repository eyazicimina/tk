
import math
class Nokta:
    x = 0
    y = 0

    def __str__(self):
        return f"POINT({self.x} {self.y})"

    def distance(self, other):
        return math.sqrt(
            math.pow(self.x - other.x, 2) +
            math.pow(self.y - other.y, 2)
        )


    def distance(p1, p2):
        return math.sqrt(
            math.pow(p1.x - p2.x, 2) +
            math.pow(p1.y - p2.y, 2)
        )


def distance(p1, p2):
    return math.sqrt(
        math.pow(p1.x - p2.x, 2) +
        math.pow(p1.y - p2.y, 2)
    )

n1 = Nokta()
n2 = Nokta()

n1.x = 10
n1.y = 20

n2.x = 15
n2.y = 15


print(n1, n2)

print(n1.distance(n2))
print(n2.distance(n1))
print(Nokta.distance(n1,n2))
print(distance(n1,n2))