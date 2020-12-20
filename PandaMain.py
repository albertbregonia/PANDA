from discord.ext import commands as cmd
import util.Modular as mod
import glob as match
import discord
import os

print('\n'*5)
panda = cmd.Bot(command_prefix=';')

#Load cogs from 'cogs' directory
for cog in match.glob('cogs/*.py'):
    panda.load_extension(f'cogs.{cog[5:-3]}')

@panda.event
async def on_ready():
    await panda.change_presence(activity=discord.Game('with your code - Use: ;'))

@panda.command(help='Reset Panda™ to default settings')
async def reset(bot):
    if os.path.exists(f'servers/{bot.guild.name}/settings.txt'):
        #delete custom command character
        os.remove(f'servers/{bot.guild.name}/settings.txt')
        #unload and delete custom cogs and macros
        for ccog in os.listdir(f'servers/{bot.guild.name}/ccogs'):
            if ccog.endswith('.py'):
                panda.unload_extension(f'servers.{bot.guild.name}.cogs.{ccog[:-3]}')
                os.remove(f'servers/{bot.guild.name}/ccogs/{ccog}')
        for script in os.listdir(f'servers/{bot.guild.name}/ccdir'):
            if script.endswith('.py'):
                os.remove(f'servers/{bot.guild.name}/ccdir/{script}')
        #Check for success
        if not os.path.exists(f'servers/{bot.guild.name}/settings.txt') and len(os.listdir(f'servers/{bot.guild.name}/ccdir'))==0:
            await bot.channel.send('@everyone - I have successfully been reset to factory default settings. Please run `;setup` or notify an administrator')
        else:
            await bot.channel.send('@everyone - Reset has **failed**. Please try again or notify an administrator.')
    else:
        await bot.channel.send('I am already at default settings. Please run `;setup` or notify an administrator')

@panda.command(help='Append your already defined functions to Panda™')
async def botload(bot):
    for name in os.listdir(f'servers/{bot.guild.name}/ccogs'):
        if name.endswith('.py'):
            try:
                name = name[:-3] #remove the .py
                await bot.channel.send(f'Attempting to append `{name}` to my system...')
                panda.load_extension(f'servers.{bot.guild.name}.ccogs.{name}')
                await bot.channel.send(f'`{name}` has been successfully initialized.')
            except Exception as err:
                header = 'Error Output'
                await bot.channel.send(f'Failed to append `{name}` to my system! \n{mod.border(header)}\n{err}')
    await bot.channel.send('Loading Complete. Please check if your code has successfully been implemented.')

@panda.command(help='Append your own new functions to Panda™')
async def botadd(bot, name, *, code):
    if not os.path.exists(f'servers/{bot.guild.name}/ccogs/{name}.py'):
        try:
            ccog = mod.readfile(open(f'util/CogTemplate.py', 'r'), False)
            with open(f'servers/{bot.guild.name}/ccogs/{name}.py', 'w') as newcog:
                newcog.write(ccog.replace('CogTemplate', name).replace('###', str(code.encode('utf-8').strip())[2:-1])) #remove 'b' and "" from string
            panda.load_extension(f'servers.{bot.guild.name}.ccogs.{name}')
            await bot.channel.send(f'Successfully appended `{name}` to my system! Thank you!')
        except Exception as err:
            header = 'Error Output'
            os.remove(f'servers/{bot.guild.name}/ccogs/{name}.py') #delete unsuccessful file
            await bot.channel.send(f'I was unable to append `{name}` to my system. Please check your code! \n\n{mod.authorheader(bot)}{mod.codeblock(mod.readcode(code))}{mod.border(header)}\n{err}')
    else:
        await bot.channel.send(f'I was unable to append `{name}` to my system. {name} has already been defined. Please perform either `;botload` or `;botrmv {name}`.')

@panda.command(help='Uninstall your functions from Panda™')
async def botrmv(bot, name):
    if os.path.exists(f'servers/{bot.guild.name}/ccogs/{name}.py'):
        try:
            panda.unload_extension(f'servers.{bot.guild.name}.ccogs.{name}')
            os.remove(f'servers/{bot.guild.name}/ccogs/{name}.py')
            if name not in panda.extensions:
                await bot.channel.send(f'`{name}` was successfully uninstalled my system.')
        except Exception as err:
            await bot.channel.send(f'Failed to uninstall `{name}` from my system.')
    else:
        await bot.channel.send(f'I was unable to remove `{name}` from my system. `{name}` was not found.')

panda.run('<BOT-KEY>')