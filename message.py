from consts import *


class Traveler:
    def __init__(self, name, is_child):
        self.name = name
        self.is_child = is_child


class FlightInfo:
    def __init__(self, airport_depart, airport_destination,
                 airline, flight_code, time_departure, time_destination,
                 seat):
        self.airport_depart = airport_depart
        self.airport_destination = airport_destination
        self.flight_code = flight_code
        self.airline = airline
        self.time_departure = time_departure
        self.time_destination = time_destination
        self.seat = seat

    def get_flight_desc(self, lang):
        return f"{FLIGHT[lang]}:  {self.airline}-{self.flight_code}\n" \
               f"\tDeparture:  ({self.airport_depart}) {self.time_departure}\n" \
               f"\tDestination: ({self.airport_destination}) {self.time_destination}\n" \
               f"\t{SEAT[lang]}: {self.seat}"


class PriceMessage:
    def __init__(self, flights, costumers, price_adult, price_child, restrictions,
                 baggage, meal, compartment, language='en'):
        self.travelers = costumers
        self.flights = flights
        self.price_adult = price_adult
        self.price_child = price_child if price_child else price_adult
        self.restrictions = restrictions
        self.baggage = baggage
        self.meal = meal
        self.compartment = compartment
        self.lang = language

    def deal_summary(self):
        """A short text describing the trip by airports"""
        if len(self.flights) == 1:
            dest_str = ONE_WAY[self.lang]
        else:
            dest_str = f"-> {self.flights[-1].airport_destination} "
        msg = f"{FLIGHT_DESC[self.lang]} {ROUND_TRIP[self.lang]}\n" \
              f"{' -> '.join([x.airport_depart for x in self.flights])} {dest_str}\n"
        if len(self.travelers) > 1:
            msg += f"{TOGETHER[self.lang]} {','.join([x.name for x in self.travelers[1:]])}"

        return msg

    def pricing_summary(self):
        # msg += f"Airlines\n{[x.airline for x in self.flights]}\n\n"

        msg = "*Prices*:\n"
        num_adults = len([x for x in self.travelers if not x.is_child])
        num_childs = len([x for x in self.travelers if x.is_child])
        msg += f"\t{num_adults} $ x {self.price_adult} adults\n"
        msg += f"\t{num_childs} $ x {self.price_child} children\n"
        msg += f"\ttotal: {float(num_adults) * float(self.price_adult) + float(num_childs) * float(self.price_child)} $\n\n"

        msg += "*Restrictions*:"
        for k, v in self.restrictions.items():
            msg += f"\n\t{k}: {v}"

        return msg

    def details_summary(self):
        msg = f"*Details*:\n"
        msg += f"\t-Compartment: {self.compartment}\n"
        msg += f"\t-Baggage: {self.baggage}\n"
        msg += f"\t-Meal: {self.meal}\n"

        return msg

    def construct_msg(self):
        msg = f"{self.travelers[0].name}, Shalom!\n\n"
        msg += f"{self.deal_summary()}\n\n"
        msg += f"{PLEASE_PAY_MSG_EN[self.lang]}\n\n"
        msg += f"*---------- {ITINERARY[self.lang]} -----------*\n"

        for flight in self.flights:
            msg += f"{flight.get_flight_desc(self.lang)}\n"
        msg += "*--------------------------------*\n\n"

        msg += f"{self.pricing_summary()}\n\n"

        msg += f"{self.details_summary()}\n\n"

        msg += f"{PRICE_MAY_CHANGE[self.lang]}\n\n"

        msg += f"{PLEASE_PAY_AGAIN_MSG_EN[self.lang]}\n\n"

        msg += f"{FAREWELL[self.lang]}\n\n"

        return msg

