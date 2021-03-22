import fire

def add(a: int):
    return a


if __name__ == "__main__":
    fire.Fire({
        "sum": add
    })