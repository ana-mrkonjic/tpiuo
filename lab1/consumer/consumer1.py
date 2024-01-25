import asyncio
import json

from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=vjestinahubstorageacc;AccountKey=yqRKu1CY4bg8Dk4HuGJHz+zofTGFyEBYFJBdRDfiuqPToDjCIPtvjDQo/B7Wxk5ULaqhsYKNemvE+AStUDoJWw==;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME = "offsetcontainer"
EVENT_HUB_NAME = "vjestina-hub"
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://mycluster.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=uarjTpZEEbzNLRHxfIjSq/AxWy7DDFfPI+AEhDy3hZ8="

async def on_event(partition_context, event):
    # Parse and print JSON event data.
    # body = event.body_as_str(encoding="UTF-8")
    # if body:
    #     try:
    #         json_data = json.loads(body)
    #         print("Received JSON data:", json_data)
    #     except json.JSONDecodeError as e:
    #         print(f"Failed to parse JSON: {e}")
    # else:
    #     print("Empty event body received.")

    body = event.body_as_str(encoding="UTF-8")
    
    if body:
        print(body)
        # try:
        #     json_data = json.loads(body)
        #     print("Received JSON data:", json_data)
        # except json.JSONDecodeError as e:
        #     print(f"Failed to parse JSON: {e}")
    else:
        print("Empty event body received.")

    # Update the checkpoint.
    await partition_context.update_checkpoint(event)


async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME
    )

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        EVENT_HUB_CONNECTION_STR,
        consumer_group="$Default",
        eventhub_name=EVENT_HUB_NAME,
        checkpoint_store=checkpoint_store,
    )
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event, starting_position="-1")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())
