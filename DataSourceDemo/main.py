from MyServer import opc_ua_server
import asyncio

def main():
    server = opc_ua_server.OpcUaTestServer()
    print(server.alive_status())
    try:
        asyncio.run(server.start())

        while True:
            print(server.alive_status())
            asyncio.run(asyncio.sleep(5))


    except KeyboardInterrupt:
        print("Before halt: " + server.alive_status())
        print("Halting...")
        asyncio.run(server.stop())
        print(server.alive_status())
        del server

if __name__ == '__main__':
    main()
