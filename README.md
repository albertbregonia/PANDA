# PANDA™
## Your Discord Server's <ins>P</ins>ersonal <ins>A</ins>daptive <ins>N</ins>etwork-<ins>D</ins>riven <ins>A</ins>ssistant
 In short, Panda™ is a simple Discord bot with many features. It was designed to allow for `man-db` integration as well as instant `macro/script` creation within a Discord server. It promotes faster software development as well as collaboration between programmers. 

Subsequently, Panda™ is a great integrated tool to allow for regular people to learn Python programming. As only one person is required to have an installation of Python to run the bot, it is easy for anyone or any group to get started.

# Main Features:
- Integrated Python Interpreter
  - Accessible in both in a `#console` channel or in a direct message
  - In a `#console` channel, `;run <code>` is the command to run Python code
  - In a direct message channel, **all messages are assumed to be code**
  - Upon completion, the output of given code is sent as a regular Discord message
  <p align="center">
  <img title="Selection Sort" src=https://github.com/albertbregonia/PANDA/blob/main/img/selsort.png></img>
  </p>
- Support for `pip install <package>`
  - All users are able to remotely add any package of their desire to Panda™'s system
  <br>
- Macro/Script Creation
  - Code is allowed to be remotely saved to script files and assigned a name
  - After saving a script, it can be re-ran using the user-defined command key followed by the script name. (**Ex:** `?script`, *where `?` is the user-defined command key*)
  - Using `;sc <script-name>`, users can display the source code for any saved script 
  <br>
- Modularity
  - A [`CogTemplate.py`](https://github.com/albertbregonia/PANDA/blob/main/util/CogTemplate.py) file is included in [`util`](https://github.com/albertbregonia/PANDA/tree/main/util) to allow any user to easily create their own custom cog for Panda™ and append it seamlessly to the system
  - The only requirement being that `;botload` needs to be ran every time the bot is restarted in order to load custom cogs
  <br>
- Man-db Integration
  - Using the `;man <search-term>` command, users have easy access to the search of functions and commands within the online manual database found on Linux systems
  <br>
- Discord Tools
  - Using `;wipe` and `;cleanup`, users can easily mass-delete messages from a channel
  - Using `;reset`, users can easily reset to delete all scripts and settings
  <br>
- YouTube Music Player
  - Audio can be played with `;play <link>` and stopped with `;stop`
  - Note: This feature isn't too well developed. It was not a focus but **is** fully functional.

# Installation and Requirements:
- To install, simply clone this repository and run `pip install -r requirements.txt`.
- To start the bot, run [`PandaMain.py`](https://github.com/albertbregonia/PANDA/blob/main/PandaMain.py).
- To get started, create a `#console` channel, run the `;setup` command and follow the instructions.
- Use `;help` to see quick descriptions of all pre-defined commands.
  <br>
  <p align="center">
  <img title="Help" src=https://github.com/albertbregonia/PANDA/blob/main/img/help.png></img>
  </p>
 - Note: If you do not have `FFmpeg` installed in your system's `PATH`, you can obtain a copy of `FFmpeg` for your system at the link below.

# Dependencies:
- [Discord.py](https://github.com/Rapptz/discord.py "Discord.py by Rapptz")
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/ "BS4 HTML Parser")
- [YouTube-DL](https://github.com/ytdl-org/youtube-dl "Youtube-dl by YTDL-org")
- [FFmpeg](https://ffmpeg.org/ "Audio conversion resource using in conjuction with Youtube-dl")
