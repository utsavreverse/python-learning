print(f"out side a's display method")


def show():
    import b
    b.display()


def display():
    print(f"in side a's display method")


show()
