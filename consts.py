import pandas as pd

LANGAUGES = {'en': 'English', 'fr': 'Francais', 'he': 'עברית'}

DAYS = {
    'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'fr': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
}

ALLER = {'en':'Outbound flt.', 'fr':'Aller'}

RETOUR = {'en':'Inbound flt.', 'fr':'Retour'}

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

ONE_WAY = {"en": 'O/w', 'fr': 'aller-simple'}

ROUND_TRIP = {'en': 'round-trip', 'fr': 'aller-retor'}

TOGETHER = {'en': 'together with', 'fr': 'avec'}

ITINERARY = {'en': 'Itinerary', 'fr': 'itinéraire'}

FLIGHT_DESC = {'en': f"As per your request you'll find below\n"
                     f"my proposal for your upcoming fligh",
               'fr': f"Suite à ta demande,tu trouveras ci-dessus\n"
                     f"ma proposition pour le voyage"
               }

FLIGHT = {'en': 'Flight', 'fr': 'Vol'}
SEAT = {'en': 'Seat', 'fr': 'Siege'}
MEAL = {'en': 'Meal', 'fr': 'Repa'}

PLEASE_PAY_MSG_EN = {'en': f"Kindly reply to the content of this whatsapp message\n" 
                           f"with your Immediate ticketing approval accordingly.",
                     'fr': f"Merci SVP d’y répondre avec votre accord sur le contenu en\n"
                           f"validant à l’immédiat l’émission de vos billets d’avions conformémen."
                     }

PLEASE_PAY_AGAIN_MSG_EN = {'en': f"Thanks for replying to this whatsapp\n"
                                 f"proposal with your immediate\n"
                                 f"confirmation.",
                           'fr': f"Merci de repondre en validant a l'immediat\n"
                                 f"l'emission du billet aux conditions mentionnées"
                           }

PRICE_MAY_CHANGE = {'en': f"*Attention*\n"
                          f"Price may change\n"
                          f"unless tickets were issued!",
                    'fr': f"*Attention*\n"
                          f"Tarifs non garantis\n"
                          f" tant que billet non emist!"
                    }

FAREWELL = {'en': f"Thanks,\nGad",
            'fr': f"Merci',\nGad"
            }

class KeyReturningDefaultdict:
    def __init__(self, dict):
        self.dict = dict
    def __getitem__(self, key):
        return self.dict[key] if key in self.dict else key

airports_file = 'airport_filtered.csv'
aiports_df = pd.read_csv(airports_file)
AIRPORTS = KeyReturningDefaultdict(dict(zip(aiports_df['iata_code'], aiports_df['municipality'])))
airlines_file = 'airlines.csv'
airlines_df = pd.read_csv(airlines_file)
AIRLINES = KeyReturningDefaultdict(dict(zip(airlines_df['iata'], airlines_df['name'])))

