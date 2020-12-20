import discord
from discord.ext import commands as cmd
import util.Modular as mod
import os

class Macro(cmd.Cog): #macro based tools
    
    #Setup
    def __init__(self, panda):
        self.panda=panda
        self.blacklisted = ['sys.exit()','quit()','exit()','os._exit']
        self.key=';'

    @cmd.Cog.listener()
    async def on_ready(self):
        print('Macro functions and Python Interpreter have been initialized')

    #DM Channel Functions and Custom Commands
    @cmd.Cog.listener()
    async def on_message(self, msg):

        if not msg.author.bot:
            if isinstance(msg.channel, discord.channel.DMChannel):

                #--------------DM Help Menu--------------
                if msg.content.startswith(';help'):
                    await msg.author.send(mod.border('Valid DM Commands')+mod.codeblock('\n;pip install\n;blacklist\n*By default, all messages sent here are assumed to be code. Thus \';run <code>\' is not required.'))

                #-----'pip install <package>' for DM-----
                elif msg.content.startswith(';pip install '):
                    os.system(f'cmd /c "pip install {msg.content[13:]}"')
                    if msg.content[13:] in os.listdir(os.getcwd()+'/venv/Lib/site-packages'):
                        await msg.author.send(f'`{msg.content[13:]}` was successfully installed or already exists')
                    else:
                        await msg.author.send(f'`{msg.content[13:]}` failed to install.')

                #---------Show Blacklisted Code----------
                elif msg.content.startswith(';blacklist'): 
                    await msg.author.send(mod.border('List of Blacklisted Code'))
                    await msg.author.send(mod.codeblock('\n'.join(self.blacklisted)))

                #----------Interpret DMs as Code---------
                else:
                    if not self.hasBlacklisted(msg.content):
                        await msg.author.send(mod.DMresult(msg))
                    else:
                        await msg.author.send('Sorry, but your code contains a blacklisted statement.\nPlease use `;blacklist` to see a list of restricted code.')

            #Only run custom commands in console channel
            elif os.path.exists(f'servers/{msg.guild.name}/settings.txt'):
                with open(f'servers/{msg.guild.name}/settings.txt', 'r') as settings:
                    self.key = settings.readline(1)[0]
                if msg.content.startswith(self.key):
                    try:
                        mod.run(str(msg.author), mod.readfile(open(f'servers/{msg.guild.name}/ccdir/{msg.content[1:]}.py', 'r'), False))
                        await msg.channel.send(mod.outputblock(mod.readfile(open(str(msg.author)+'.txt', 'r'), True)))
                    except Exception as error:
                        if isinstance(error, FileNotFoundError):
                            await msg.channel.send(f'`{msg.content}` is not a valid command.')
                        else:
                            await msg.channel.send(f'An unforeseen error occurred. Please try again.')

        elif msg.content.startswith(';'): #Process valid commands if applicable
            await self.panda.process_commands(msg)

    @cmd.command(help='Display a list of custom defined commands')
    async def ls(self, bot):
        await bot.channel.send(mod.border('Custom Defined Commands')+'\n'+mod.codeblock(self.key+('\n'+self.key).join(os.listdir(f'servers/{bot.guild.name}/ccdir')).replace('.py', '')))
        
    @cmd.command(help='Display the list of blacklisted code')
    async def blacklist(self, bot):
        if os.path.exists(f'servers/{bot.guild.name}/settings.txt'):
            await bot.channel.send(mod.border('List of Blacklisted Code'))
            for line in self.blacklisted:
                await bot.channel.send(f'`{line}`')
        else:
            await bot.channel.send(f'{bot.author.mention}, please run `;setup` and `;su` before trying to perform commands.')
        
    @cmd.command(help='Create a custom command')
    async def new(self, bot, name, *, code):
        if os.path.exists(f'servers/{bot.guild.name}/settings.txt'):
            if not os.path.exists(f'servers/{bot.guild.name}/ccdir/{name}.py'): #Check if command already exists
                if not self.hasBlacklisted(code):
                    with open(f'servers/{bot.guild.name}/ccdir/{name}.py', 'w') as macro: #Create script for command
                        macro.write(code)
                    await bot.channel.send(mod.result(bot, code)) #run newly created script
                else:
                    await bot.channel.send(f'Sorry {bot.author.mention}, but your code contains a blacklisted statement.\nPlease use `;blacklisted` to see a list of restricted code.')
            else:
                await bot.channel.send(f'Sorry {bot.author.mention}, but `{name}` already exists.\nPlease use `;rmv {name}` to delete a command.')
        else:
            await bot.channel.send(f'{bot.author.mention}, please run `;setup` and `;su` before trying to perform commands.')
        
    @cmd.command(help='Delete a custom command')
    async def rmv(self, bot, command):
        if os.path.exists(f'servers/{bot.guild.name}/settings.txt'): 
            if bot.channel.name=='console':
                if os.path.exists(f'servers/{bot.guild.name}/ccdir/{command}.py'): #Delete script if it exists
                    os.remove(f'servers/{bot.guild.name}/ccdir/{command}.py')
                    if not os.path.exists(f'servers/{bot.guild.name}/ccdir/{command}.py'): #Check for successful deletion
                        await bot.channel.send(f'`{command}` was deleted.')
                    else:
                        await bot.channel.send(f'`{command}` failed to delete.')
                else:
                    await bot.channel.send(f'`{command}` is not a valid command.')
            else:
                await bot.channel.send(bot.author.mention+', please use a `#console` text channel to interact with this feature.')
        else:
            await bot.channel.send(bot.author.mention+', please run `;setup` and `;su` before trying to perform commands.')
            
    @cmd.command(help='Show the source code for a custom command')
    async def sc(self, bot, command):
        if os.path.exists(f'servers/{bot.guild.name}/ccdir/{command}.py'):
            await bot.channel.send(mod.border(f'Source Code for: `{command}``')+mod.codeblock(mod.readfile(open(f'servers/{bot.guild.name}/ccdir/{command}.py', 'r'), False)))
        else:
            await bot.channel.send(f'`{command}`' + ' is not a valid command.')

    @cmd.command(help='Installs packages found in the Python Package Index', usage='install <package>')
    async def pip(self, bot, install, package): #I really did want it to be 'pip install'
        if os.path.exists(f'servers/{bot.guild.name}/settings.txt'):
            if bot.channel.name=='console':
                await bot.channel.send(f'Attempting to install `{package}`...')
                os.system(f'cmd /c "pip install {package}"') #run 'pip install' in terminal with the specified package
                if package in os.listdir(os.getcwd()+'/venv/Lib/site-packages'):
                    await bot.channel.send(f'`{package}` was successfully installed or already exists')
                else:
                    await bot.channel.send(f'`{package}` failed to install.')
            else:
                await bot.channel.send(f'{bot.author.mention}, please use a `#console` text channel to interact with this feature.')
        else:
            await bot.channel.send(f'{bot.author.mention}, please run `;setup` and `;su` before trying to perform commands.')
            
    @cmd.command(help='Python interpreter that runs code') 
    async def run(self, bot, *, code):
        if os.path.exists(f'servers/{bot.guild.name}/settings.txt'):
            if not self.hasBlacklisted(code):
                await bot.channel.send(mod.result(bot, code))
            else:
                await bot.channel.send(f'Sorry {bot.author.mention}, but your code contains a blacklisted statement.\nPlease use `;blacklisted` to see a list of restricted code.')
            
        else:
            await bot.channel.send(f'{bot.author.mention}, please run `;setup` and `;su` before trying to perform commands.')
    
    def hasBlacklisted(self, code):
        for line in self.blacklisted:
                if line in code:
                    return True
        return False

def setup(panda):
    panda.add_cog(Macro(panda))