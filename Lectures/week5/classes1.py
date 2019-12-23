
class Flight():
    """docstring for Flight."""

    def __init__(self, origin, destination, duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration


def main():
    #Create flight
    f = Flight(origin="New York", destination="Paris", duration=540)

    f.duration += 10
    print(f.origin)
    print(f.destination)
    print(f.duration)


if __name__ == "__main__":
    main()
    # Esta notacion permite importar la clase Flight sin run el codigo que esta entre las lineas 11 a 18
