import os
from collections import defaultdict

import PySimpleGUI as sg

from consts import LANGAUGES

from utils import create_price_proposal, send_whatsapp, parse_amadeus_code

TIMES = [f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(24) for m in range(0, 60,10)]
TRAVELERS = ['Child', 'Adult']
COMPARTEMENTS = ['1st Class', 'Business', 'Economy']


def get_travelers_rows(n, default_dict):
    """User input for travelers and contact information"""
    row = []
    for i in range(n):
        adult_default = not default_dict[f"child{i}"]
        row += [sg.Frame(f"Traveler {i + 1}", [
                                           [sg.InputText(key=f"traveler_name{i}", size=(W2, 1), default_text=default_dict[f"traveler_name{i}"],)],
                                           [sg.Radio(f"Adult", f"traveler_age{i}", key=f"adult{i}", default=adult_default)],
                                           [sg.Radio(f"Child", f"traveler_age{i}", key=f"child{i}", default=default_dict[f"child{i}"])]
                                          ])
                ]
    row += [sg.Button('+', key="+traveler", size=(2, 1))]
    phone_row = [sg.Text('Contact WhatsApp', size=(W1, 1)),
                 sg.Input(key="phone_number", size=(W1 - 1, 1), default_text=default_dict["phone_number"])]
    return [phone_row, row]


def get_flight_rows_3(n, default_dict):
    """Arange a frame of dynamic number of flight frames"""
    # add an amadeus parser above the columns
    amadeus_row = [sg.Multiline(enter_submits=False, autoscroll=True, visible=True, do_not_clear=True,
                                key="amadeus_code", size=(W2*6,4), default_text=default_dict["amadeus_code"]),
                   # sg.Input(key=f"amadeus_code", size=(W2*8,1), default_text=default_dict[f"amadeus_code"]),
                   sg.Button('Insert', key=f"insert", size=(4,4))]
    all_rows = [amadeus_row]

    return all_rows


def get_price_and_restriction_rows(default_dict):
    rows = [[
        sg.Frame('Price', [
            [sg.Text("Price (adult)", size=(W2, 1)), sg.Input(size=(PRICE_BOX_SIZE, 1), key="price_adult", default_text=default_dict["price_adult"])],
            [sg.Text("Price (child)", size=(W2, 1)), sg.Input(size=(PRICE_BOX_SIZE, 1), key="price_child", default_text=default_dict["price_child"])],
            [sg.Text("fee percentage", size=(W2, 1)),
             sg.Input(size=(PRICE_BOX_SIZE, 1), key="price_fee", default_text=default_dict["price_fee"])]
        ]),

        sg.Frame('Restrictions', [
            [sg.Text("Change fee", size=(W2, 1)),
             sg.Input(size=(PRICE_BOX_SIZE, 1), key="change_fee", default_text=default_dict["change_fee"])],
            [sg.Text("Cancel fee", size=(W2, 1)),
             sg.Input(size=(PRICE_BOX_SIZE, 1), key="cancel_fee", default_text=default_dict["cancel_fee"])],
            [sg.Text("No show fee", size=(W2, 1)),
             sg.Input(size=(PRICE_BOX_SIZE, 1), key="no_show_fee", default_text=default_dict["no_show_fee"])],
        ]
                 )
    ]]
    return rows


def get_price_detail_rows(default_dict):
    no_bagage_default = not (default_dict['23_kg'] or default_dict['handbag_only'])
    no_meal_default = not (default_dict['regular_meal'] or default_dict['kosher_meal'])
    rows = [[
        sg.Frame('Baggage', [[sg.Radio('No baggage', 'baggage', key='no_baggage', default=no_bagage_default)],
                             [sg.Radio('Handbag only', 'baggage', key='handbag_only',
                                       default=default_dict['handbag_only']), ],
                             [sg.Radio('23 kg', 'baggage', key='23_kg', default=default_dict['23_kg'])]]),

        sg.Frame('Food', [[sg.Radio('No meal', 'other', key='no_meal', default=no_meal_default)],
                          [sg.Radio('Regular meal', 'other', key='regular_meal',
                                    default=default_dict['regular_meal']), ],
                          [sg.Radio('kosher meal', 'other', key='kosher_meal', default=default_dict['kosher_meal'])]])
    ]]

    return rows


def get_total_layout(n_travelers, n_flights, default_values, preview_msg):
    """Create the buttons and boxes layout of the program"""
    layout = list()
    layout.append([sg.Frame("Contacts", get_travelers_rows(n_travelers, default_values), border_width=10)])

    layout.append([sg.Frame("Amadeus code", get_flight_rows_3(n_flights, default_values), border_width=10)])

    layout.append([sg.Frame("Prices", get_price_and_restriction_rows(default_values)),
                   sg.Frame("Details", get_price_detail_rows(default_values))])

    layout.append([
                   sg.Button('Preview', key='Preview'),
                   sg.Frame('Terminals', [[sg.Button('WhatsApp', key='WhatsApp'), sg.Exit()]]),
                   sg.Frame('Resolution', [[sg.Button('+', key='res+'), sg.Button('-', key='res-')]]),
                   sg.Frame('Language', [[
                       sg.ReadFormButton('', key='en', border_width=0, image_subsample=20,button_color=sg.TRANSPARENT_BUTTON, image_filename=os.path.join('images', 'united-states.png')),
                       sg.ReadFormButton('', key='fr', border_width=0, image_subsample=20,button_color=sg.TRANSPARENT_BUTTON, image_filename=os.path.join('images', 'france.png')),
                       # sg.ReadFormButton('', key='he', border_width=0, image_subsample=20,button_color=sg.TRANSPARENT_BUTTON, image_filename=os.path.join('images', 'israel.png')),
                    sg.Text(LANGAUGES[default_values['lang']])]]),
                   ])

    # Lay the input side by side to an output window
    layout = [[sg.Column(layout), sg.Column([[sg.Multiline(size=(2*W1, 3*fs), default_text=preview_msg, key='output_window')]])]]

    return layout

def main(fs):
    """
    Run the main gui application that constantly seeks for user input and shows a preview on a side window.
    By pressing "Whatsapp" a link to whatsapp message is opened
    """
    sg.theme('DarkTeal6')
    # sg.theme_previewer()

    n_travelers = 1
    n_flights = 0
    default_values = defaultdict(lambda: None)
    default_values['lang'] = 'en'
    while True:
        preview_msg = default_values['output_window'] if default_values['output_window'] else ''

        layout = get_total_layout(n_travelers, n_flights, default_values, preview_msg)

        window = sg.Window('Simple data entry window', layout=layout, font=(f"Arial {fs}"))
        event, values = window.read()
        default_values.update(values)

        # Handle events
        if event == '+traveler':
            n_travelers += 1
        if event == '+flights':
            n_flights += 1
        if event == 'WhatsApp':
            send_whatsapp(default_values['phone_number'], default_values['output_window'])
        if event == 'res+':
            fs = int(fs / 0.8)
        if event == 'res-':
            fs = int(fs * 0.8)
        if event == 'insert':
            new_values = parse_amadeus_code(values[f"amadeus_code"])
            if new_values is not None:
                default_values.update(new_values)
                n_flights = len([k for k in default_values if k.startswith('airline')])
        if event in LANGAUGES:
            default_values['lang'] = event
        if event in ['Exit', sg.WIN_CLOSED]:
            break
        if event == 'Preview':
            default_values['output_window'] = create_price_proposal(default_values)

        window.close()


if __name__ == '__main__':
    W1 = 20
    W2 = 12
    PRICE_BOX_SIZE = 7
    fs = 8
    w, h = sg.Window.get_screen_size()
    main(fs)
