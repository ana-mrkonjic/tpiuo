import asyncio
import requests
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

# Azure Event Hub connection parameters
EVENT_HUB_NAME = "vjestina-hub"
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://mycluster.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=uarjTpZEEbzNLRHxfIjSq/AxWy7DDFfPI+AEhDy3hZ8="
REDDIT_URL = "https://www.reddit.com/r/dataengineering/top.json?limit=10"

async def fetch_initial_posts(retries=5, backoff=1, timeout=5):
    """
    Fetch initial posts from Reddit.

    Parameters:
        retries (int): Number of retries in case of failure.
        backoff (int): Initial backoff time.
        timeout (int): Timeout for the HTTP request.

    Returns:
        list: List of initial posts.
    """
    for _ in range(retries):
        try:
            response = requests.get(REDDIT_URL, timeout=timeout)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"Rate limited. Retrying in {backoff} seconds.")
                await asyncio.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"Failed to fetch posts. Status code: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return []
    print("Exceeded retries. Aborting.")
    return []

async def send_to_event_hub(posts):
    """
    Send posts to Azure Event Hub.

    Parameters:
        posts (list): List of posts to send.
    """
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        event_data_batch = await producer.create_batch()

        for post in posts:
            event_data_batch.add(EventData(str(post)))
        # print(str(posts))
        event_data_batch.add(EventData(str(posts)))
        await producer.send_batch(event_data_batch)
        print("Initial posts sent to Event Hub")
        print("Success")     

async def main():
    """
    Main function to run the program.
    """
    initial_posts = await fetch_initial_posts()
    if initial_posts:
        await send_to_event_hub(initial_posts)

    while True:
        # Keep the loop running to maintain the process
        await asyncio.sleep(60)

# Run the main function within an event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
