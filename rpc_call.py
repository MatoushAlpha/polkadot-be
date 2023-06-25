import asyncio
import websockets
import json
from jsonrpcclient import request

connected = set()

async def relay_events(ws, path):
    connected.add(ws)
    try:
        while True:
            event = await events_queue.get()
            await asyncio.wait([ws.send(event) for ws in connected])
    finally:
        connected.remove(ws)

async def listen_to_polkadot_node():
    async with websockets.connect('ws://localhost:9946') as client:
        msg = request("chain_subscribeNewHeads")
        await client.send(json.dumps(msg))

        while True:
            response = await client.recv()
            data = json.loads(response)
            print(f"Response data: {data}") # debugging

            # ensure data['result'] exists and is a dictionary
            if isinstance(data.get('result'), dict):
                block_hash = data["result"]["hash"]
                print(f"Block hash: {block_hash}")

                # Get the block data
                msg = request("chain_getBlock", [block_hash])
                await client.send(json.dumps(msg))
                response = await client.recv()
                data = json.loads(response)
                # ensure data['result'] exists and is a dictionary
                if isinstance(data.get('result'), dict):
                    # Extract extrinsics
                    extrinsics = data['result']['block']['extrinsics']
                    for extrinsic in extrinsics:
                        print(f"Extrinsic data: {extrinsic}")
                        # TODO: Decode the extrinsic to get meaningful data
                        await events_queue.put(json.dumps(extrinsic)) # add to queue for relaying

events_queue = asyncio.Queue()

server = websockets.serve(relay_events, 'localhost', 8765)
loop = asyncio.get_event_loop()
loop.run_until_complete(server)
loop.run_until_complete(listen_to_polkadot_node())
loop.run_forever()
