import os
from datetime import datetime, timezone
import time
from random import choice, randint
import uuid
import json

# static lists with event types and device types
EVT_TYPES = [
    "click", "view", "purchase", "signup", "logout", 
    "login", "add_to_cart", "remove_from_cart", "search", "filter", 
    "sort", "share", "like", "comment", "rate", "review"
    ]

DEVICE_TYPES = [
    "mobile", "desktop", "tablet", "laptop"
    ]

def generate_event():
    event_type = choice(EVT_TYPES)
    device_type = choice(DEVICE_TYPES)
    event_value = round(randint(100, 10_000) / 100, 2) if event_type == "purchase" else None
    event_time = datetime.now(timezone.utc).isoformat()

    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{randint(1, 10_000)}",
        "event_time": event_time,
        "event_type": event_type,
        "device_type": device_type,
        "event_value": event_value,
    }
    return event;


if __name__ == "__main__":
    os.makedirs("data/inbox", exist_ok=True)

    while True:
        # store events
        json_events = []
        # break into smaller batches (random) when generating the events
        batch_size = randint(10, 15)
        # for the above batch_size, generate events in small files
        for _ in range(batch_size):
            json_events.append(json.dumps(generate_event()))
        # record the creation of the file (time) and save it in inbox
        file_creation_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join("data", "inbox", f"events_{file_creation_time}.json")
        # write file to output location in batches
        with open(output_path, "w") as f:
            f.write("\n".join(json_events))
        print(f"Wrote {len(json_events)} events -> {output_path}")
        # wait until next batch
        time.sleep(randint(3, 5))
    