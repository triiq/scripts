#!/bin/bash

#cd /home/triiq/docker/immich

#docker compose pull

#docker compose up -d

#if [ $? -eq 0 ]
#then
#  curl -d "immich update sucessfully checked" ntfy.triiq.xyz/immich
#fi

#!/bin/bash

# Define the Docker Compose file
COMPOSE_FILE="/home/triiq/docker/immich/docker-compose.yml"

# Get the current image IDs
BEFORE_IDS=$(docker images --format "{{.ID}}" --filter reference="$(docker compose -f $COMPOSE_FILE config --services)")

# Pull the latest images
docker compose -f $COMPOSE_FILE pull

# Recreate the containers if there are new images
docker compose -f $COMPOSE_FILE up -d

# Get the new image IDs
AFTER_IDS=$(docker images --format "{{.ID}}" --filter reference="$(docker compose -f $COMPOSE_FILE config --services)")

# Check if there were any updates & send push notification
if [ "$BEFORE_IDS" != "$AFTER_IDS" ]; then
    curl -H "Title: Immich Update" -H "Tags: heavy_check_mark" -d "Updates were available and applied." ntfy.triiq.xyz/immich
else
    curl -H "Title: Immich Update" -H "Tags: +1" -d "No updates were available." ntfy.triiq.xyz/immich
fi
