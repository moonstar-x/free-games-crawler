# Free Games Crawler

This is a crawler that extracts information about free games from multiple storefronts.

Currently supported storefronts:

* Epic Games
* Steam

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
