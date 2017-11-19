import role
import bank


class Player(role.Role):
    """
    subclass(Role): Player
    """

    def __init__(self, uid, name, cash, alliance):
        """
        Constructor
        :param uid: int
        :param name: string
        :param cash: int
        :param alliance: string
        """
        super().__init__(uid, name, cash)
        self._alliance = alliance
        self._position = 0
        self._bail_card_num = 0
        self._cur_status = 1
        self._utility_num = 0
        self._station_num = 0

    @property  # getAlliance
    def alliance(self):
        return self._alliance

    @property
    def position(self):
        return self._position

    # @position.setter
    # def position(self, position):
    #     self._position = position

    @property
    def bail_card_num(self):
        return self._bail_card_num

    @bail_card_num.setter  # changeBailCard
    def bail_card_num(self, bail_card_num):
        self._bail_card_num = bail_card_num

    @property  # get currentStatus
    def cur_status(self):
        return self._cur_status

    @cur_status.setter  # changeStatus
    def cur_status(self, cur_status):
        self._cur_status = cur_status

    @property  # changeUtilityNum
    def utility_num(self):
        return self._utility_num

    # @utility_num.setter
    # def utility_num(self, utility_num):
    #     self._utility_num = utility_num

    @property
    def station_num(self):
        return self._station_num

    # @station_num.setter
    # def station_num(self, station_num):
    #     self._station_num = station_num

    @role.Role.cash.setter
    def cash(self, amount):
        self._cash += amount

    def move(self, steps, position=None):
        """
        Move players
        :type steps: int
        :type position: int
        :param steps: steps to move
        :param position: position to arrive(actually go into jail or something else)
        position: None if normally move on map otherwise set the position
        """
        if not position:
            self._position += steps
        else:
            self._position = position

    def trade_property(self, properties, from_role, to_role):
        """
        Trade for other players or bank, here is just to sell
        :type properties: set
        :type from_role: Player
        :type to_role: Player or Bank
        :param properties: a set of Property
        :param from_role: Role
        :param to_role: Role
        :return boolean: Trade successfully or not
        """
        from_role.remove_property(properties)
        to_role.add_property(properties)
        return True

    def pay(self, amount, from_role, to_role):
        """
        Trade cash between players or bank
        :type from_role: Player
        :type to_role: Player or Bank
        :param amount: amount of cash to be traded
        :param from_role: Player or Bank
        :param to_role: Player or Bank
        :return boolean: Trade finished or error
        """
        if from_role._cash >= amount:
            from_role._cash(-amount)
            if isinstance(to_role, Player):
                to_role._cash(amount)
                return True
            if isinstance(to_role, bank.Bank):
                return True
        else:
            return False

