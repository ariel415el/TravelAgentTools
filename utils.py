from message import Traveler, FlightInfo, PriceMessage
import webbrowser
import urllib.parse
import PySimpleGUI as sg


def parse_amadeus_code(code, flight_number):
    results = dict()
    try:
        words = code.split()
        results[f"airline{flight_number}"] = words[0]
        results[f"code{flight_number}"] = words[1]
        # price_cide = words[2]
        results[f"depart_date{flight_number}"] = words[3]
        # day_code = words[4]

        results[f"depart_airport{flight_number}"] = words[5][:3]
        results[f"dest_airport{flight_number}"] = words[5][3:]
        # code_1 = words[6]
        results[f"depart_time{flight_number}"] = f"{words[7][:2]}:{words[7][2:]}"
        results[f"dest_time{flight_number}"] = f"{words[8][:2]}:{words[8][2:]}"
        results[f"dest_date{flight_number}"] = words[9]

        # code_2 = words[10]
        # PNR = words[11]
    except IndexError as e:
        sg.Popup('Opps!', 'Bad amadeus code format!')

    return results


def parse_user_input(user_input):
    # parse flights
    travelers = []
    flights = []
    num_travelers = sum([x.startswith('traveler') for x in user_input])
    for i in range(num_travelers):
        travelers.append(Traveler(user_input[f"traveler_name{i}"], user_input[f"child{i}"]))

    num_flights = sum([x.startswith('depart_airport') for x in user_input])
    for i in range(num_flights):
        depart_time = user_input[f"depart_date{i}"] + " " + user_input[f"depart_time{i}"],
        dest_time = user_input[f"dest_date{i}"] + " " + user_input[f"dest_time{i}"],
        flights.append(FlightInfo(user_input[f"depart_airport{i}"],
                                  user_input[f"dest_airport{i}"],
                                  user_input[f"airline{i}"],
                                  user_input[f"code{i}"],
                                  depart_time,
                                  dest_time,
                                  user_input[f"seat{i}"])
                       )
    restrictions = {'Change': user_input['change_fee'], 'Cancel': user_input['cancel_fee'], 'No show': user_input['no_show_fee'],}
    baggage = 'no baggage'
    if user_input['handbag_only']:
        baggage = 'Handbag only'
    elif user_input['23_kg']:
        baggage = '23 kg'

    meal = 'no meal'
    if user_input['regular_meal']:
        meal = 'Regular meal'
    elif user_input['kosher_meal']:
        meal = 'Kosher meal'

    return travelers, flights, restrictions, baggage, meal


def send_whatsapp(number, msg):
    msg = urllib.parse.quote(msg)
    url = f"https://wa.me/{number}?text={msg}"
    webbrowser.open_new(url)


def create_price_proposal(values):
    travelers, flights, restrictions, baggage, meal = parse_user_input(values)

    msg = PriceMessage(flights, travelers,
                        price_adult=values["price_adult"] if values["price_adult"] else 0,
                        price_child=values["price_child"] if values["price_child"] else 0,
                        restrictions=restrictions,
                        baggage=baggage,
                        meal=meal,
                        compartment=values['compartment0'],
                        language=values['lang'],
                       ).construct_msg()

    return msg

