# Ratio-as-a-Service

Ratio-as-a-service is a simple service to generate Twitter-like ratios in French.

## Quickstart
The service is available as a Docker image.

First, you need to create a discord bot and add it to your server. You can find a guide on how to do that [here](https://discordpy.readthedocs.io/en/latest/discord.html).

Add the bot token to the `compose.yml'  file.
Then run the following command to start the service:

```bash
docker-compose up -d
```

The app is made with NLP library spaCy and is available in french only.

## Usage
Example of trigger (in a discord channel):

```
Input: Je veux manger un sandwich
Output: Et ce ratio il veut manger un sandwich ???
```

```
Input: Aujourd'hui je suis absent.
Output: Et ce ratio il est absent ???
```

## Development

App is available in VS (with requirements.txt) or in python venv with requirements-tux.txt).

