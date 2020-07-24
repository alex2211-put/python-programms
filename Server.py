import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()

    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


class ClientServerProtocol(asyncio.Protocol):
    everything = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = data.decode().split()
        answer = 'ok\n\n'

        if 2 < len(resp) < 4:
            answer = 'error\nwrong command\n\n'
            self.transport.write(answer.encode())
            return
        elif len(resp) < 2:
            answer = 'error\nwrong command\n\n'
            self.transport.write(answer.encode())
            return

        if resp[0] == 'put':
            if len(resp) != 4:
                answer = 'error\nwrong command\n\n'
                self.transport.write(answer.encode())
                return
            try:
                f = float(resp[2])
                i = int(resp[3])
                if resp[1] not in self.everything:
                    self.everything[resp[1]] = []
                f = False
                k = 0
                for i in range(len(self.everything[resp[1]])):
                    if self.everything[resp[1]][i][1] == resp[3]:
                        f = True
                        k = i
                if not f:
                    self.everything[resp[1]].append((resp[2], resp[3]))
                else:
                    s = self.everything[resp[1]].pop(k)
                    self.everything[resp[1]].append((resp[2], resp[3]))

            except:
                answer = 'error\nwrong command\n\n'

        elif resp[0] == 'get':
            if len(resp) != 2:
                answer = 'error\nwrong command\n\n'
                self.transport.write(answer.encode())
                return

            else:
                if resp[1] == '*':
                    answer = 'ok'
                    for key in self.everything:
                        for i in range(len(self.everything[key])):
                            answer += '\n' + str(key) + ' ' + str(float(self.everything[key][i][0]))\
                                      + ' ' + str(self.everything[key][i][1])
                    answer += '\n\n'
                
                else:
                    if not resp[1] in self.everything:
                        answer = 'ok'
                    else:
                        answer = 'ok'
                        for i in range(len(self.everything[resp[1]])):
                            answer += '\n' + str(resp[1]) + ' ' + str(float(self.everything[resp[1]][i][0]))\
                                      + ' ' + str(self.everything[resp[1]][i][1])
                    answer += '\n\n'


        else:
            answer = 'error\nwrong command\n\n'

        self.transport.write(answer.encode())
