import asyncio

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print("Connection from {}".format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print("data received: {!r}".format(message))
        print("send: {!r}".format(message))
        self.transport.write(data)
        #print("close the client socket")
        #self.transport.close()

    def eof_received(self):
        print("wouldn't received")
        self.transport.close()

async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(
            lambda: EchoServerProtocol(),
            "localhost", 8888)
    async with server:
        await server.serve_forever()


asyncio.run(main())
