from random import randint


def gen_file(n, t):
    with open("ff.txt", "w+") as f:
        for _ in range(n):
            f.write(f"{randint(1, t+1)}\n")
