from consts import *


class Time:
    def __init__(self, date, time_in_day):
        self.date = date
        self.time_in_day = time_in_day

    def __str__(self):
        return f"{self.date} {self.time_in_day}"

class Traveler:
    def __init__(self, name, is_child):
        self.name = name
        self.is_child = is_child


class FlightInfo:
    def __init__(self, airport_depart, airport_destination,
                 airline, flight_code, time_departure, time_destination):
        self.airport_depart = airport_depart
        self.airport_destination = airport_destination
        self.flight_code = flight_code
        self.airline = airline
        self.time_departure = time_departure
        self.time_destination = time_destination

    def get_flight_desc(self, lang):
        return f"   {AIRLINES[self.airline]}-({self.airline}{self.flight_code})\n" \
               f"   {AIRPORTS[self.airport_depart]}>{AIRPORTS[self.airport_destination]}\n" \
               f"   {self.time_departure} - {self.time_destination}"


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
            dest_str =" " + ONE_WAY[self.lang]
        else:
            dest_code = self.flights[-1].airport_destination
            dest_str = f">{AIRPORTS[dest_code]} "
        trip_str = [AIRPORTS[x.airport_depart] for x in self.flights]
        msg = f"{FLIGHT_DESC[self.lang]} {ROUND_TRIP[self.lang]}\n" \
              f"{'>'.join(trip_str)}{dest_str}\n"
        if len(self.travelers) > 1:
            msg += f"{TOGETHER[self.lang]} {','.join([x.name for x in self.travelers[1:]])}"

        return msg

    def flights_summary(self):
        print_retour = True
        msg = f"*{ITINERARY[self.lang]}*\n"
        msg += f"{FLIGHT[self.lang]} {ALLER[self.lang]}\n"
        for i, flight in enumerate(self.flights):
            if i > 0:
                if print_retour and flight.time_departure.date != self.flights[i-1].time_destination.date:
                    msg += f"{FLIGHT[self.lang]} {RETOUR[self.lang]}\n"
                    print_retour = False
            msg += f"{flight.get_flight_desc(self.lang)}\n"
        return msg

    def pricing_summary(self):
        # msg += f"Airlines\n{[x.airline for x in self.flights]}\n\n"

        msg = "*Prices*:\n"
        num_adults = len([x for x in self.travelers if not x.is_child])
        num_childs = len([x for x in self.travelers if x.is_child])
        msg += f"   {num_adults} $ x {self.price_adult} adults\n"
        msg += f"   {num_childs} $ x {self.price_child} children\n"
        msg += f"   total: {float(num_adults) * float(self.price_adult) + float(num_childs) * float(self.price_child)} $\n\n"

        msg += "*Restrictions*:"
        for k, v in self.restrictions.items():
            msg += f"\n   {k}: {v}"

        return msg

    def details_summary(self):
        msg = f"*Details*:\n"
        msg += f"  -Compartment: {self.compartment}\n"
        msg += f"  -Baggage: {self.baggage}\n"
        msg += f"  -Meal: {self.meal}\n"

        return msg

    def construct_msg(self):
        if self.flights:
            msg = f"{self.travelers[0].name}, Shalom!\n\n"
            msg += f"{self.deal_summary()}\n\n"
            msg += f"{PLEASE_PAY_MSG_EN[self.lang]}\n\n"

            msg += f"{self.flights_summary()}\n\n"

            msg += f"{self.pricing_summary()}\n\n"

            msg += f"{self.details_summary()}\n\n"

            msg += f"{PRICE_MAY_CHANGE[self.lang]}\n\n"

            msg += f"{PLEASE_PAY_AGAIN_MSG_EN[self.lang]}\n\n"

            msg += f"{FAREWELL[self.lang]}\n\n"

            return msg

