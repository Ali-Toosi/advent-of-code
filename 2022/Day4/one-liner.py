# Both parts space separated
print(*list(map(lambda z: sum(z), zip(*[
    (((p1 >= q1 and p2 <= q2) or (q1 >= p1 and q2 <= p2)), ((p1 >= q1 and p1 <= q2) or (q1 >= p1 and q1 <= p2)))
    for (p1, p2), (q1, q2)
    in map(lambda x: map(lambda y: map(int, y.split('-')), x.split(',')), open("input.txt").readlines())
]))))

