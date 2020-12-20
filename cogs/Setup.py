from discord.ext import commands as cmd
import os
import util.Modular as mod

class Setup(cmd.Cog):
    
    def __init__(self, panda):
        self.panda = panda
    
    @cmd.Cog.listener()
    async def on_ready(self):
        print('Successfuly initalized Panda™'+'\n'*5)
        
    @cmd.command(help='Basic information on how to get started with Panda™')
    async def setup(self, bot):
        if not os.path.exists(f'servers/{bot.guild.name}/settings.txt'):
            if bot.channel.name == 'console':
                #generate folders for current server
                directory = ['servers', f'servers/{bot.guild.name}', f'servers/{bot.guild.name}/ccdir', f'servers/{bot.guild.name}/ccogs']
                for folder in directory:
                    if not os.path.exists(folder):
                        os.mkdir(folder)
                #display bio
                await bot.channel.send(f'Hello {bot.author.mention}, I\'m {self.panda.user.mention} !\nIn short, I am a programmer\'s ideal partner!\nI was designed to create `man-db` integration and instant `macro/script creation` into a Discord server to allow for faster software development\nPlease run `;su <character>` to assign a custom command character and finish setup')
            else:
                await bot.channel.send(f'{bot.author.mention}, please use a `#console` text channel to interact with this feature.')
        else:
            await bot.channel.send(f'Sorry {bot.author.mention}, the setup has already been completed. Please run `;reset` then run `;setup` to run the setup again or notify an administrator.')
    
    @cmd.command(help='Define this server\'s prefix for custom commands')
    async def su(self, bot, prefix):
        if not os.path.exists(f'servers/{bot.guild.name}/settings.txt'):
            if len(prefix)==1:
                with open(f'servers/{bot.guild.name}/settings.txt', 'w') as file:
                    file.write(prefix + '\n')
                await bot.channel.send(f'Thank you {bot.author.mention}, the first time setup is now complete. Please use `;new <name> <code>` and `;rmv <name>` to create and delete commands.\nYou can also use `;run <code>` or simply DM me to use my integrated **Python Interpreter**!')
            else:
                await bot.channel.send(f'Invalid input {bot.author.mention}! Please re-run `;su <character>` to assign a custom command character and finish setup')
        else:
            await bot.channel.send(f'Sorry {bot.author.mention}, the setup has already been completed. Please run `;reset` and then `;setup` to run the setup again or notify an administrator.')
        
def setup(panda):
    panda.add_cog(Setup(panda))
