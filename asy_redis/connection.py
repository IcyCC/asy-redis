import asyncio


class Connection(object):

    def __init__(self, host="localhost", port=6379, timeout=None, loop=None):
        self.host = host
        self.port = port

        self.loop = loop or asyncio.get_event_loop()
        self.info = {"db": 0, "pw": None}
        self._reader = None
        self._writer = None

    async def connect(self):
        if not self._reader and not self._writer:
            try:
                self._reader, self._writer = await asyncio.open_connection(host=self.host,
                                                                           port=self.port,
                                                                           loop=self.loop)
            except asyncio.InvalidStateError as e:
                raise e.message

    def disconnect(self):
        self._writer.close()

    async def write(self, data):
        if not self._writer:
            self.disconnect()
            raise IOError("writer connection error")
        # try:
        self._writer.write(data.encode())
        await self._writer.drain()
        # except Exception:
        #     self.disconnect()
        #     raise IOError("writer failed")

    async def read(self, length=-1):
        try:
            if not self._reader:
                self.disconnect()
                raise ConnectionError("read failed")
            data = await self._reader.readline()
            return data
        except:
            self.disconnect()
            raise IOError("read failed")

    def is_connected(self):
        if self._reader is None and self._writer is None:
            return False
        return True
