import json
import requests
import asyncio
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

# Azure Event Hub connection parameters
EVENT_HUB_NAME = "vjestina-hub"
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://mycluster.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=uarjTpZEEbzNLRHxfIjSq/AxWy7DDFfPI+AEhDy3hZ8="
reddit_url = "https://www.reddit.com/r/dataengineering/top.json?limit=10"


producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
)



# Fetch data from Reddit API
#response = requests.get(reddit_url)
#data = response.json()

        # Extract information and send it to Event Hub
        # for post in data["data"]["children"]:
        #     event_data = EventData(body=str(post).encode("utf-8"))
        #     producer.send(event_data)


async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )
    async with producer:

         # Fetch data from Reddit API
        response = requests.get(reddit_url)
        data = json.loads(response.text)
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(data))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

while True:
    asyncio.run(run())  