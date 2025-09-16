"""
Requirements:
1) Customers book rides (pickup, dropoff, ride type).
2) Assign first available driver.
3) Three ride types with simple per-mile fares.
4) Show estimated fare + driver name BEFORE confirming (then mark driver occupied).
"""

from abc import ABC, abstractmethod

# Ride types 
class Ride(ABC):
    @abstractmethod
    def calculate_fare(self, distance):
        pass

# all ride types inherit from abstract Parent class ride
class EconomyRide(Ride):
    def calculate_fare(self, distance):
        return distance * 5

class LuxuryRide(Ride):
    def calculate_fare(self, distance):
        return distance * 10

class PoolRide(Ride):
    def calculate_fare(self, distance):
        return distance * 3


# User Types
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

#Customer inherits from User class
class Customer(User):
    def book_ride(self, pickup_location, dropoff_location, distance, ride_type):
        ride = ride_from_string(ride_type)
        return RideRequest(self, pickup_location, dropoff_location, distance, ride)

#Driver inherits from User class
class Driver(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.available = True


# Input for ride request
class RideRequest:
    def __init__(self, customer, pickup_location, dropoff_location, distance, ride):
        self.customer = customer
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.distance = distance
        self.ride = ride


# string to ride_type
def ride_from_string(ride_type):
    key = ride_type.strip().lower()
    if key == "economy":
        return EconomyRide()
    if key == "luxury":
        return LuxuryRide()
    if key == "pool":
        return PoolRide()
    raise ValueError(f"Unknown ride type: {ride_type!r}")


# assign drivers + estimates before confirmation 
class Dispatcher:
    def __init__(self, drivers):
        self.drivers = drivers

    def _first_available_driver(self):
        for d in self.drivers:
            if d.available:
                return d
        return None

    def estimate(self, ride_request):
        driver = self._first_available_driver()
        if not driver:
            return None, None
        fare = ride_request.ride.calculate_fare(ride_request.distance)
        return driver, fare

    def confirm(self, driver):
        #Marks the chosen driver as occupied if unavailable.
        if driver:
            driver.available = False


# Tasks to complete
if __name__ == "__main__":
    # Drivers
    alice = Driver(1, "Alice")
    bob = Driver(2, "Bob")

    # Customers
    john = Customer(101, "John")
    rebecca = Customer(102, "Rebecca")
    mike = Customer(103, "Mike")

    dispatcher = Dispatcher([alice, bob])

    # John, from Airport to Downtown, 15 miles, Economy
    r1 = john.book_ride("Airport", "Downtown", 15, "Economy")
    d1, f1 = dispatcher.estimate(r1)
    if d1 is None:
        print("No drivers available.")
    else:
        print(f"Ride Fare: ${int(f1)}, Driver: {d1.name}")
        dispatcher.confirm(d1)

    # Rebecca, from College to Downtown, 10 miles, Luxury
    r2 = rebecca.book_ride("College", "Downtown", 10, "Luxury")
    d2, f2 = dispatcher.estimate(r2)
    if d2 is None:
        print("No drivers available.")
    else:
        print(f"Ride Fare: ${int(f2)}, Driver: {d2.name}")
        dispatcher.confirm(d2)

    # Mike, from Downtown to Shopping Mall, 5 miles, Pool
    r3 = mike.book_ride("Downtown", "Shopping Mall", 5, "Pool")
    d3, f3 = dispatcher.estimate(r3)
    if d3 is None:
        print("No drivers available.")
    else:
        print(f"Ride Fare: ${int(f3)}, Driver: {d3.name}")
        dispatcher.confirm(d3)