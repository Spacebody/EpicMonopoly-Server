import role


class Player(role.Role):
    """
    subclass(Role): Player
    """

    def __init__(self, uid, name, cash, alliance, avatar):
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
        self._pre_position = 0
        self._in_jail_time = 0
        self._avatar = avatar

    @property  # getAlliance
    def alliance(self):
        return self._alliance

    @property
    def position(self):
        return self._position

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, amount):
        self._cash += amount

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
        """
        count the times of being prisoned
        """
        if self._in_jail < 2:
            self._in_jail = self._in_jail + 1
            return False
        else:
            self._cur_status = 1
            self._in_jail = 0
            return True

    @property
    def station_num(self):
        return self._station_num

    @property
    def assets(self):
        return self._assets

    @property
    def in_jail_time(self):
        return self._in_jail_time

    def add_in_jail_time(self):
        """
        add the times in jail
        """
        self._in_jail_time += 1

    def calculate_asset_value(self):
        """
        calculate the value of asset
        """
        total_asset_value = self._cash
        for a in self._assets:
            total_asset_value = total_asset_value + a.value
        return total_asset_value

    def get_built_list(self):
        """
        get the list of available buildings
        """
        import operation
        import estate
        available_built_list = []
        own_street_list = operation.own_all_block(self)
        for cur_asset in self._assets:
            if isinstance(cur_asset, estate.Estate):
                if (cur_asset.street_id in own_street_list) and (cur_asset.status == 1):
                    available_built_list.append(cur_asset.block_id)
        return available_built_list

    def add_asset(self, new_asset):
        """
        Add asset to player
        """
        import estate
        import station
        import utility
        if isinstance(new_asset, estate.Estate):
            self._assets.add(new_asset)
            new_asset.owner = self.id
            new_asset.status = 1
        elif isinstance(new_asset, station.Station):
            self._assets.add(new_asset)
            new_asset.owner = self.id
            new_asset.status = 1
            self._station_num = self._station_num + 1
        elif isinstance(new_asset, utility.Utility):
            self._assets.add(new_asset)
            new_asset.owner = self.id
            new_asset.status = 1
            self._utility_num = self._utility_num + 1
        else:
            pass

    def remove_asset(self, old_asset):
        """
        remove asset
        """
        import estate
        import station
        import utility
        if isinstance(old_asset, estate.Estate):
            self._assets.remove(old_asset)
            old_asset.owner = -1
            old_asset.status = -1
        elif isinstance(old_asset, station.Station):
            self._assets.remove(old_asset)
            old_asset.owner = -1
            old_asset.status = -1
            self._station_num = self._station_num - 1
        elif isinstance(old_asset, utility.Utility):
            self._assets.remove(old_asset)
            old_asset.owner = -1
            old_asset.status = -1
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
        self._pre_position = self._position
        if not position:
            self._position = (self._position + steps) % 40
        else:
            self._position = position

    def getJSON(self):
        # property_list = []
        # for asset in self.assets:
        #     property_list.append(asset.block_id)
        json_data = {
            "name": self._name,
            "cash": self._cash,
            "id": self.id,
            "position": self._position,
            "alliance": self._alliance,
            "card_num": self._bail_card_num,
            "cur_status": self._cur_status,
            "pre_position": self._pre_position,
            # "property": property_list,
            "avatar": self._avatar,
            "available_built_list": self.get_built_list()
        }
        return json_data
