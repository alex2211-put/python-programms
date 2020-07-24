import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = str(host)
        self.port = int(port)
        self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def put(self, metric, data, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())
        s = ('put ' + str(metric) + ' ' + str(data) + ' ' + str(timestamp) + '\n').encode()
        self.sock.sendall(s)
        data = self.sock.recv(1024).decode('utf-8')
        print('server returned:{}'.format(data))
        if not data == "ok\n\n":
            raise ClientError

    def get(self, metric):
        diction = {}
        s = ('get ' + str(metric) + '\n').encode()
        self.sock.sendall(s)

        data_all = self.sock.recv(1024).decode('utf-8')
        print('server returned:{}'.format(data_all))

        if data_all == 'ok\n\n':
            return diction

        d = data_all.split('\n')

        if not d[0] == 'ok':
            raise ClientError

        if len(d[1].split()) < 3:
            raise ClientError

        data = []
        for i in range(1, len(d) - 2):
            data.append(d[i])
        if len(data) > 0:
            for i in data:
                s = i.split()
                if not s[0] in diction:
                    diction[s[0]] = []
                diction[s[0]].append((int(s[2]), float(s[1])))
                diction[s[0]].sort(key=lambda st: st[0])
        return diction

