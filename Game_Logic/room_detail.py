import multiprocessing
import threading
# import messager
import game_entrance


class Room_detail:
    """
    Class Room_detail

    """

    def __init__(self, roomid, create_room_dict, init_client):
        self.roomid = roomid
        self.clients = dict()
        self.game_log = []
        self.global_choice = Choice()
        self.create_room_dict = create_room_dict
        # print("+",create_room_dict)

        for it in init_client:
            self.add_clients(it, init_client[it])

        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        # self.mess_hand = messager.Messager(self.roomid, self.child_conn)
        self.p = multiprocessing.Process(
            target=game_entrance.start_game, args=(self.create_room_dict, self.child_conn,))
        self.p.start()
        self.hear = threading.Thread(target=self.listener)
        self.hear.start()

    def sender(self, line):
        """
        sender

        """
        self.parent_conn.send((self.roomid, line))

    def listener(self):
        """
        listener

        """
        while True:
            iroomid, line, ranges = self.parent_conn.recv()
            if ranges == "ALL":
                self.add_log("NPC", line)
                assert(iroomid == self.roomid)
                for key in self.clients.keys():
                    self.get_client(key).write_message(line)
                    print("RD:Write to Room %s client %s: %s" %
                          (iroomid, key, line))
            else:
                self.add_log(ranges, line)
                assert(iroomid == self.roomid)
                self.get_client(ranges).write_message(line)
                print("RD:Write to Room %s client %s: %s" %
                      (iroomid, ranges, line))

    def add_clients(self, id, client):
        self.clients[id] = {"id": id, "object": client}
        print("a1", self.clients)

    def add_log(self, id, message):
        self.game_log.append((id, message))

    def rm_clients(self, id):
        del self.clients[id]

    def get_client(self, id):
        return self.clients[id]["object"]

    def empty(self):
        if self.clients:
            return False
        else:
            return True


class Choice(object):
    def __init__(self):
        self.choice = -2
        # -2 初始化值
        self.isvalid = False

    def set_choice(self, choice):
        self.choice = choice
        self.isvalid = True

    def get_choice(self):
        if not self.isvalid:
            # -1无效值
            return -1
        else:
            self.isvalid = False
            return self.choice
