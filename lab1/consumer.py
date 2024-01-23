from azure.eventhub import EventHubConsumerClient


EVENT_HUB_NAME = "vjestina-hub"
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://mycluster.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=uarjTpZEEbzNLRHxfIjSq/AxWy7DDFfPI+AEhDy3hZ8="


# Event Hub consumer group
consumer_group = "$Default"

# Define callback function to process received events
def on_event(partition_context, event):
    # Print the received message
    # print("Received event from partition: {}".format(partition_context.partition_id))
    # print("Event body: {}".format(event.body_as_str()))
    # print("Properties: {}".format(event.properties))
    # print("System properties: {}".format(event.system_properties))
    # print("-----------")
    print(
        'Received the event: "{}" from the partition with ID: "{}"'.format(
            event.body_as_str(encoding="UTF-8"), partition_context.partition_id
        )
    )

# Create Event Hub consumer client
consumer_client = EventHubConsumerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STR,
    consumer_group=consumer_group,
    eventhub_name=EVENT_HUB_NAME
)

try:
    # Start receiving events from the Event Hub
    with consumer_client:
        consumer_client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the end of the partition
        )

except KeyboardInterrupt:
    print("Receiving has stopped.")