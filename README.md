# Free Games Crawler

This is a crawler that extracts information about free games from multiple storefronts. This is meant to be used as the crawler for [discord-free-games-notifier](https://github.com/moonstar-x/discord-free-games-notifier) but can be used alongside any consumer that can connect to Redis.

Currently supported storefronts:

* Epic Games
* Steam

This service is meant to be used as a trigger for services that can act upon receiving new free game offers. It leverages Redis for storing current offers and Redis PubSub for publishing new offers found to a PubSub channel.

Services that consume this information should connect to the Redis instance and subscribe to the `offers` PubSub channel to receive updates. Message payloads are JSON strings that should be parsed by the consumer.

Consumers can also fetch stored offers in Redis. Since there aren't many free game offers at a given time, you may use [`KEYS`](https://redis.io/docs/latest/commands/keys/) to get all the offers. Offer keys follow the format `offer:STORE_FRONT:GAME_ID`, for example, for the game [Drawful 2](https://store.steampowered.com/app/442070/Drawful_2/) the key would be `offer:Steam:442070`.

Game offers are stored as JSON strings in the following format:

```text
{
  "storefront": string,
  "id": string,
  "url": string,
  "title": string,
  "description": string,
  "type": 'game' | 'dlc' | 'bundle' | 'other',
  "publisher": string | null
  "original_price": number | null,
  "original_price_fmt": string | null,
  "thumbnail": string | null
}
```

For example, for the game [Drawful 2](https://store.steampowered.com/app/442070/Drawful_2/), you can expect the following payload:

```json
{
  "storefront": "Steam",
  "id": "442070",
  "url": "https://store.steampowered.com/app/442070/Drawful_2/?snr=1_7_7_2300_150_1",
  "title": "Drawful 2",
  "description": "For 3-8 players and an audience of thousands! Your phones or tablets are your controllers! The game of terrible drawings and hilariously wrong answers.",
  "type": "game",
  "publisher": "Jackbox Games",
  "original_price": 5.79,
  "original_price_fmt": "$5.79 USD",
  "thumbnail": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/442070/header.jpg?t=1721927113"
}
```

## Usage

In order to use this project you'll need the following:

* [Redis](https://redis.io)
* [Doker](https://docker.com) (Recommended) or [Python](https://python.org)

### With Docker (Recommended)

Create a `docker-compose.yml` file with the following:

```yaml
services:
  crawler:
    image: ghcr.io/moonstar-x/free-games-crawler:latest
    restart: unless-stopped
    depends_on:
      - redis
    environment:
      REDIS_URI: redis://redis:6379

  redis:
    image: redis:7.4-rc2-alpine
    restart: unless-stopped
    ports:
      - 6379:6379
```

> You can also the image `moonstarx/free-games-crawler:latest` if you prefer DockerHub.

And that's it, the crawler container will scrape all the supported storefronts every 30 minutes and save the information acquired data in Redis.

### With Python

Make sure to have at least Python 3.8.

First, clone this repository:

```bash
git clone https://github.com/moonstar-x/free-games-crawler
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

And start the crawler:

```bash
REDIS_URI=redis://localhost:6379 python3 main.py
```

> This assumes you have a Redis instance running on `localhost`.

### Configuration

You can configure the crawler with the following environment variables.

| Name                         | Required | Default | Description                                                                                                                                                |
|------------------------------|----------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| REDIS_URI                    | Yes      |         | The Redis instance URI. (i.e `redis://localhost:6379`)                                                                                                     |
| REDIS_TTL                    | No       | 7200    | The amount of seconds the stored information will last for in Redis.                                                                                       |
| SCHEDULER_EVERY_SECONDS      | No       | 1800    | The amount of seconds the crawler will wait before running again.                                                                                          |
| CRAWLER_HTTP_REQUEST_TIMEOUT | No       | 0       | The amount of seconds the crawler should wait before making an HTTP request.                                                                               |
| CRAWLER_HTTP_MAX_RETRIES     | No       | 10      | The amount of times the crawler can repeat an HTTP request before giving up.                                                                               |
| CRAWLER_HTTP_RETRY_TIMEOUT   | No       | 0.5     | The amount of seconds the crawler should wait before retrying failed HTTP requests.                                                                        |
| THREADING_ENABLED            | No       | true    | Whether crawlers should run in multiple threads or not.                                                                                                    |
| THREADING_MAX_WORKERS        | No       | auto    | The amount of threads that can be used to run each crawler. Set this to a specific positive number or `auto` to let Python decide based on CPU core count. |

## Development

Clone this repository:

```bash
git clone https://github.com/moonstar-x/free-games-crawler
```

Create a new Python environment:

```bash
python3 -m venv ./venv
```

Load the environment:

```bash
source ./venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

And create the development environment:

```bash
cd _dev && docker compose up
```

## Testing

You can run unit tests by using:

```bash
pytest test
```

Or, if you wish to have test watch enabled:

```bash
ptw test
```

## Building

To build this project you should use [Docker](https://docker.com)

To build the image locally, you can run:

```bash
docker build -t test/free-games-crawler .  
```

And to run it:

```bash
docker run -it --rm --network host -e REDIS_URI=redis://localhost:6379 test/free-games-crawler
```
