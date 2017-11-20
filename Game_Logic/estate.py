from property import Property
from ef import EF
import opertation


class Estate(Property):
    """
    Class estate
    """

    def __init__(self, name, position, uid, estate_value, status, street_id, house_value):
        """
        Call for superclass construct
        Init _houseNum and _houseValue
        :param house_value: The value of single house
        """
        super().__init__(name, position, uid, estate_value, status)
        self._street_id = street_id
        self._house_num = 0
        self._house_value = house_value
        # self._hotel_num = 0
        # self._hotel_value = 4 * house_value

    @property
    def house_num(self):
        return self._house_num

    @house_num.setter
    def house_num(self, house_num):
        self._house_num = house_num

    @property
    def house_value(self):
        return self._house_value

    # @property
    # def hotel_num(self):
    #     return self._hotel_num

    # @hotel_num.setter
    # def hotel_num(self, hotel_num=1):
    #     if self._hotel_num == 0 and hotel_num == 1:
    #         self._hotel_num += hotel_num

    @property
    def value(self):
        return self._estate_value + (self._house_num * self._house_value)

    @property
    def mortgage_value(self):
        return self.value * self.mortgage_rate

    @property
    def payment(self):
        """
        Calculate the payment of the house
        Return:
            :payment: int
        """
        if self.house_num == 0:
            return self.value * 0.1
        elif self.house_num == 1:
            return self.value * 0.15
        elif self.house_num == 2:
            return self.value * 0.2
        elif self.house_num == 3:
            return self.value * 0.25
        elif self.house_num == 4:
            return self.value * 0.3
        elif self.house_num == 5:
            return self.value * 0.4
        elif self.house_num == 6:
            return self.value * 0.5
        else:
            # Should not be here
            raise ValueError("Ivalid house number")
            return 0

    # TODO: implement the method
    def change_house_value(self, EF):
        """
        Change house value according to EF
        :type EF: float
        :param EF: economy factor
        :return: None
        """
        pass

    def display(self, gamer, data_dict, dice_result):
        """
        Display description
        :type player_dict: dict
        :type gamer: player.Player
        :return:
        """
        player_dict = data_dict['player_dict']
        bank = data_dict['epic_bank']
        if self._status == 1:
            # Some body own it
            owner_id = self.owner()
            owner = player_dict[owner_id]
            if owner_id == gamer.id:
                # Owner pass this estate
                print("%s own %s" % (gamer.name, self.name))
            else:
                # Other pass this estate
                payment = self.payment
                opertation.pay(gamer, owner, payment)
        elif self._status == -1:
            # Nobody own
            while True:
                print("Nobody own %s do you want to buy it?")
                print("1: Buy it")
                print("2: Do not buy it")
                choice = int(
                    input("Please enter the number of your decision:"))
                if choice == 1:
                    price = self.value
                    if price > gamer.cash:
                        print("You do not have enough money")
                        break
                    else:
                        opertation.pay(gamer, bank, price)
                        opertation.trade_property(self, bank, gamer)
                        print("%s buy %s for %d" %
                              (gamer.name, self.name, price))
                        break
                elif choice == 2:
                    break
                else:
                    print("Ivalid operation")
        elif self._status == 0:
            # In mortgage
            print("%s is in mortgaged" % (self.name))
        else:
            raise ValueError("Invalid estate status")
