class Flight():
    """docstring for Flight."""

    def __init__(self, origin, destination, duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration

    def print_info(self):
        print(f"Flight origin: {self.origin}") #Curly braces says "Insert that variable here"
        print(f"Flight destination: {self.destination}")
        print(f"Flight duration: {self.duration}")

    def delay(self, amount):
        self.duration += amount

def main():
    #Create flight
    f1 = Flight(origin="New York", destination="Paris", duration=540)
    f1.delay(10)
    f1.print_info()


if __name__ == "__main__":
    main()
    # Esta notacion permite importar la clase Flight sin run el codigo que esta entre las lineas 11 a 18
