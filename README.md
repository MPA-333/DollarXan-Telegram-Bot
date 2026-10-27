# Telegram Bot – DollarXan

## My Motivation

For a while, I had been using a Telegram bot called "MeowieQBot"—or rather, a Telegram mini-app designed for gaming. In our own group, we refer to it as the "Meow-Meow" game. One day, the idea came up in our group to build a bot similar to Meow-Meow—a challenge to see if we could actually pull it off.

That became my motivation to create the "DollarKhan" Telegram bot. It’s not quite on the same level as Meow-Meow—nor was it intended to be—but it’s good enough to satisfy me! :)

## What is DollarXan?

DollarKhan is a Telegram gaming bot, modeled after the MeowieQBot mini-app. Once added to a group, members can use the bot to generate dollars and then use those virtual dollars to play games with one another. For instance, if a user types the word "dollar" in the group, the bot grants them a certain amount of virtual currency. These dollars are entirely virtual and hold no value outside of this digital environment. Users can then initiate a game by typing "dollar game", which requires a stake to participate. For example, members might send a "dice" sticker; whoever rolls the highest number wins the entire pot.

## Using the Code

Currently, this bot isn't running on a dedicated server; it was only active for a few days for testing and entertainment purposes. If you’d like to use or test this code (though I make no claims regarding its optimization), please note the following:

- It uses MongoDB as the database.

- The entire bot is based on the \`python-telegram-bot\` framework.

- You need to create a file named exactly \`secret\_key.py\` right next to the \`master.py\` file, and include the following two lines inside it:

Code : secret\_key.py

| \`\`\` BOT\_TOKEN = "your bot token"  ADMIN\_ID = 1111111111

```
| - |
```

translate by:  google translate
