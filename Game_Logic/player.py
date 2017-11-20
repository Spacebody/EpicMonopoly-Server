import role


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
        self._in_jail = 0

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
    def cur_status(self, change_status):
        self._cur_status = change_status

    @property
    def utility_num(self):
        return self._utility_num

    def count_in_jail(self):
        if self._in_jail < 2:
            self._in_jail = self._in_jail + 1
            return False
        else:
            self._in_jail = 0
            return True

    @property
    def station_num(self):
        return self._station_num

    def pay(self, amount):
        self._cash = self._cash - amount

    def gain(self, amount):
        self._cash = self._cash + amount

    def calculate_asset_value(self):
        total_asset_value = self.cash
        for a in self._assets:
            total_asset_value = total_asset_value + a.value
        return total_asset_value

    def add_asset(self, new_asset):
        """
        Add asset to player
        :type new_asset: estate.Estate, station.Station, utility.Utility
        """
        import estate
        import station
        import utility
        if isinstance(new_asset, estate.Estate):
            self._assets.add(new_asset)
            new_asset.owner(self.id)
            new_asset.status(1)
        elif isinstance(new_asset, station.Station):
            self._assets.add(new_asset)
            new_asset.owner(self.id)
            new_asset.status(1)
            self._station_num = self._station_num + 1
        elif isinstance(new_asset, utility.Utility):
            self._assets.add(new_asset)
            new_asset.owner(self.id)
            new_asset.status(1)
            self._utility_num = self._utility_num + 1
        else:
            pass

    def remove_asset(self, old_asset):
        """
        docstring here
            :param self: 
            :type old_asset: estate.Estate, station.Station, utility.Utility
        """
        import estate
        import station
        import utility
        if isinstance(old_asset, estate.Estate):
            self._assets.remove(old_asset)
            old_asset.owner(self.id)
            old_asset.status(-1)
        elif isinstance(old_asset, station.Station):
            self._assets.remove(old_asset)
            old_asset.owner(self.id)
            old_asset.status(-1)
            self._station_num = self._station_num - 1
        elif isinstance(old_asset, utility.Utility):
            self._assets.remove(old_asset)
            old_asset.owner(self.id)
            old_asset.status(-1)
            self._utility_num = self._utility_num - 1
        else:
            pass

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
            self._position = (self._position + steps)%40
        else:
            self._position = position
