import pandas


df = pandas.read_csv("hotels.csv", dtype={"id": str})
cards = pandas.read_csv('cards.csv', dtype=str).to_dict(orient="records")
df_security_info = pandas.read_csv('card-security.csv', dtype="str")


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        #df.to_csv("hotels.csv", index=False)

    def available(self):
        """check if the hotel is available """
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    @property
    def costume_name(self):
        name = self.name.strip()
        name = name.title
        return name

    def __eq__(self, other):
        if self.hotel_id == other.hotel_id:
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, costumer_name, reserved_room):
        self.costumer_name = costumer_name
        self.reserved_room = reserved_room

    def generate(self):
        ticket = f"name: {self.costumer_name}\n" \
                 f"the hotel: {self.reserved_room.name}"
        return ticket


class Reserve(ReservationTicket):
    def generate(self):
        ticket = f"the room 302 at {self.reserved_room.name} \n in the name of {self.costumer_name}"
        return ticket


class Spa:
    def __init__(self, username, hotel_object):
        self.name = username
        self.object = hotel_object

    def book(self):
        ticket = f"""
        thank you for choosing us
        the {self.object.name} is booked
        in the name of {self.costume_name2}"""
        return ticket

    @property
    def costume_name2(self):
        name2 = self.name.strip()
        name2 = name2.title()
        return name2


class Pay:
    def __init__(self, card):
        self.card = card

    def validate(self, expiration, cvv, holder1):
        card_data = {"number": self.card, "expiration": expiration,
                     "cvc": cvv, "holder": holder1}
        if card_data in cards:
            return True


class SecureCreditCard(Pay):
    def checkpass(self, given_password):
        password1 = df_security_info.loc[df_security_info["number"] == self.card, "password"].squeeze()
        print(password1)
        if given_password == password1:
            return True


print(df)
room_id = input("enter id of the hotel:")
hotel = Hotel(room_id)
if hotel.available():
    pay = SecureCreditCard(card='1234567890123456')
    if pay.validate(expiration="12/26", cvv='123', holder1="JOHN SMITH"):
        if pay.checkpass(given_password="mypass"):
            hotel.book()
            name = input("and your name?")
            reservation = ReservationTicket(name, hotel)
            rg = Reserve(name, hotel)
            rg = rg.costumer_name
            print(rg.generate())
            spa = input("do you want spa package?")
            if spa == "yes":
                package = Spa(name, hotel)
                package = package.costume_name2
                rs = package.book()
                print(rs)
        else:
            print("your credit card info are not valid")
    else:
        print("somthing is wrong with your payment")
else:
    print("room is not available")
