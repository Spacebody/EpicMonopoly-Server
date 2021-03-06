import asset
import operation
# from ef import EF


class Estate(asset.Asset):
    """
    Class estate
    """

    def __init__(self, name, block_id, position, uid, estate_value, status, street_id, house_value):
        """
        Call for superclass construct
        Init _houseNum and _houseValue
        :param house_value: The value of single house
        """
        super().__init__(name, block_id, position, uid, estate_value, status)
        self._street_id = street_id
        self._house_num = 0
        self._house_value = house_value

    @property
    def house_num(self):
        return self._house_num

    @house_num.setter
    def house_num(self, house_num):
        self._house_num = house_num

    @property
    def house_value(self):
        return self._house_value

    @property
    def value(self):
        return self._estate_value + (self._house_num * self._house_value)

    @property
    def mortgage_value(self):
        return self.value * self.mortgage_rate

    @property
    def street_id(self):
        # getPosition
        return self._street_id

    @property
    def payment(self):
        """
        Calculate the payment of the house
        Return:
            :payment: int
        """
        return self._get_payment(self._house_num)

    def _get_payment(self, house_num):
        if house_num == 0:
            return int(self.value * 0.1)
        elif house_num == 1:
            return int(self.value * 0.15)
        elif house_num == 2:
            return int(self.value * 0.2)
        elif house_num == 3:
            return int(self.value * 0.25)
        elif house_num == 4:
            return int(self.value * 0.3)
        elif house_num == 5:
            return int(self.value * 0.4)
        elif house_num == 6:
            return int(self.value * 0.5)
        else:
            # Should not be here
            raise ValueError("Invalid house number")

    def change_value(self, rate):
        self._house_value = self._house_value * (1 + rate)
        self._estate_value = self._estate_value * (1 + rate)

    def display(self, gamer, data, dice_result):
        """
        Display description
        :param dice_result:
        :return:
        """
        player_dict = data['player_dict']
        epic_bank = data['epic_bank']
        if self._status == 1:
            # Some body own it
            owner_id = self.owner
            owner = player_dict[owner_id]
            if owner_id == gamer.id:
                # Owner pass this estate
                operation.push2all("%s own %s" % (gamer.name, self.name))
            else:
                # Other pass this estate
                operation.push2all("%s own %s" % (owner.name, self.name))
                payment = self.payment
                operation.pay(gamer, owner, payment, data)
        elif self._status == -1:
            # Nobody own
            while True:
                operation.push2all(
                    "Nobody own %s do you want to buy it?" % self.name)
                operation.push2all("Price: %d" % self.value)
                operation.push2all("1: Buy it")
                operation.push2all("2: Do not buy it")
                while True:
                    input_str = operation.wait_choice(
                        "Please enter the number of your decision:")
                    if(True):
                        input_data = data["msg"].get_json_data("input")
                        input_str = input_data[0]["request"]
                    try:
                        choice = int(input_str)
                        break
                    except ValueError:
                        operation.push2all("Please enter a number.")
                operation.push2all()
                if choice == 1:
                    price = self.value
                    cur_cash = gamer.cash
                    if price > cur_cash:
                        operation.push2all("You do not have enough money")
                        break
                    else:
                        operation.pay(gamer, epic_bank, price, data)
                        operation.trade_asset(self, epic_bank, gamer)
                        operation.push2all("%s buy %s for %d" %
                                           (gamer.name, self.name, price))
                        break
                elif choice == 2:
                    break
                else:
                    operation.push2all("Invalid operation")
        elif self._status == 0:
            # In mortgage
            operation.push2all("%s is in mortgaged" % self.name)
        else:
            raise ValueError("Invalid estate status")

    def getJSon(self):
        payment_list = []
        for i in range(1, 7):
            payment_list.append(
                {"house_number": i, "payment": self._get_payment(i)})
        json_data = {
            "name": self._name,
            "block_id": self._block_id,
            "position": self._position,
            "uid": self._uid,
            "estate_value": self._estate_value,
            "status": self._status,
            "street_id": self._street_id,
            "house_value": self._house_value,
            "house_num": self._house_num,
            "mortgage_value": self.mortgage_value,
            "payment": payment_list
        }
        return json_data
