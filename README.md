# Hala
A discord bot.

## Command Categories

- Help
- Characters
- Misc.
- Rolling
- Music
- and Moderation

The commands for said categories go as follows.

### Help
-help - Shows this command

### Characters

- register - Registers a character with the given information.
- createfile - Creates utopiumsheet file
- update - Updates a given character
- delete - Deletes a character
- get-character - Returns information about a character.
- list-characters - displays a list of characters for a member.

### Misc.
- set-prefix - Changes the bot's prefix in the current server
- google - Searches for a given query on google.

### Rolling
- roll - Rolls a dice using RPG format
- stats - Rolls basic stat rolls.

### Music

- join - Joins a voice channel
- summon - Summons the bot to a voice channel.
- leave - Will have the bot leave the channel.
- volume - Changes the bot's volume.
- now - Shows the current song.
- pause - Pauses the bot player
- resume - Resumes the song.
- stop - Stops the bot player
- skip - Skips the current song.
- queue - Shows the queue
- shuffle - Shuffles the queue
- remove - Removes a song from the queue
- loop - Loops the currently playing song.
- play - Plays a song with the given title unless a direct URL is provided.

### Moderation
- ban - Bans a given member
- kick - Kicks a given member
- mute - Mutes a member for a given duration
- unmute - Unmutes a given member
- unban - Unbans a given user.
- userinfo - Displays information about a given user.
- avatar - Returns a users avatar.
- purge - Purges a given number of messages
- lock - locks down the current channel.
- unlock - Unlocks a currently locked channel.

More information on each command can be found either using the description attribute of each command, or using {prefix}help <command>.

## Roadmap (v 1.1.0)

- Scheduling
- Better help command
- Help paginator class
- A Music Cog thats actually written by me
- A dise parsing and rolling system actually written by me
- Improved sheet parsing
- Webhook based character roleplay

## Features

- Music
- Moderation
- D&D Die Format Rolling
- Stat Rolling
- Character Creation and Storage

## Contributing

If you wish to contribute you can simply make a pull request or raise an issue.

## Known Issues

- List command returns database values instead of a list of characters that a member owns
- Help command displays Cogs that do not have commands in them
- Register command does not raise an error when improper .utopiumsheet files are passed

## Credits

- Valentin B. for the Music Cog
- The team at Avrae and D&D Beyong for the D20 module
- Akins2229 (me) for literally everything else
