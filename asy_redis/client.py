import asyncio
from .connection import Connection


class CmdLine(object):
    def __init__(self, cmd, key, value = None):
        self.cmd = cmd
        self.key = key
        self.value = value

    def __repr__(self):
        if self.value is None:
            return "{} {}".format(self.cmd, self.key)
        else:
            return "{} {} {}".format(self.cmd, self.key, self.value)


class Client(object):
    def __init__(self, host="127.0.0.1", port=6379, pwd=None, db=None, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.password = pwd
        self.db = db or 0
        self.connection = Connection(host=host, port=port, loop=loop)

    def __del__(self):
        self.connection.disconnect()

    async def connect(self):
        if not self.connection.is_connected():
            await self.connection.connect()

    async def disconnet(self):
        if self.connection.is_connected():
            await self.connection.disconnect()

    def format_command(self, *tokens, **kwargs):
        cmds = []
        for t in tokens:
            e_t = str(t)
            cmds.append("$%s\r\n%s\r\n" % (len(e_t), e_t))
        return "*%s\r\n%s" % (len(tokens), "".join(cmds))

    def format_reply(self, cmd_line, data):
        cmd = cmd_line.cmd
        if cmd == "AUTH":
            return bool(data)
        elif cmd == "SELECT":
            return data == "OK"
        elif cmd == "SET":
            return data == "OK"
        else:
            return data

    async def execute(self, cmd, *args, **kwargs):
        result = None
        cmd_line = CmdLine(cmd, *args, **kwargs)
        tries = 2
        if cmd == 'SET':
            while tries > 0:
                tries = tries - 1

                if not self.connection.is_connected():
                    self.connection.connect()

                command = repr(cmd_line)
                try:
                    await self.connection.write(command)
                    data = await self.connection.read()
                    if not data:
                        if not tries:
                            raise ConnectionError("no data received")
                    else:
                        return data
                except Exception as e:
                    if not tries:
                        raise e
                    else:
                        continue

    async def set(self, _key, _value):
        await self.execute("SET", _key, _value)

    async def get(self, _key):
        resp = await self.execute("GET",_key)
        return resp
