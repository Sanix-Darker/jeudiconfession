# JeudiConfessionBot

LOL LOL LOL, i wanted to do a nice and simple bot to notify me for each new tweet with a specific hashtag on my telegram Chat app.

## Requierements

- python (3.x is recommended)
- Docker

## How to install

You just nee to follow theese steps:

```shell

# Install python requierements
pip install -r requierements.txt

```

## How to launch

You just need to hit theese commands:

```shell

# After getting the container scrapinghub/splash,
# Start the splash_scrapy container
docker run -p 8050:8050 scrapinghub/splash

# open the First CLI to start the main bot script
python ./bot/main.py

# Open the Second CLI to start the job of fetching
python ./bot/job.py

# Open your third CLI to run the twitter_scarpper_module
python ./bot/twitter_tag_scrapper.py

```

## Author

- Sanix-darker