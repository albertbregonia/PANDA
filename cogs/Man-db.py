from discord.ext import commands as cmd
import bs4 #beautiful soup
import requests
import util.Modular as mod

class Man_db(cmd.Cog):

    def __init__(self, panda):
        self.panda = panda
    
    @cmd.Cog.listener()
    async def on_ready(self):
        print('Man-db Successfully Integrated')

    @cmd.command(help='Man-db search tool')
    async def man(self, bot, cmd):
        await bot.channel.send(f'{bot.author.mention}, searching for `{cmd}`...')
        #gets the content of the page and prints it
        for i in range(1,8): #search
            source = requests.get(f'https://man7.org/linux/man-pages/dir_section_{i}.html')
            soup = bs4.BeautifulSoup(source.text, features='html.parser')
            if cmd in soup.text:
                source = requests.get(f'https://man7.org/linux/man-pages/man{i}/{cmd}.{i}.html')
                soup = bs4.BeautifulSoup(source.text.replace('<span class="top-link">top</span></a>',''), 'html.parser') #soup object of html with the 'top' link removed
                #remove excess
                content = soup.text[soup.text.find('COLOPHON'):]
                content = content[content.find('NAME'):]
                content = content[:content.rfind('COLOPHON')]
                temp = ''
                for char in content:
                    if (ord(char) < 127 and ord(char) >= 32) or char=='\n' or ord(char)==9: #remove invalid chars
                        temp+=char
                content = temp
                #check if message is 2K+ characters
                if(len(content)<1994): #2K characters - 6 for the code block characters
                    if(len(content)<=len(cmd)):
                        continue
                    else:
                        await bot.channel.send(mod.codeblock(content))
                else:
                    await bot.channel.send(mod.codeblock(content[0:1989]+"..."))
                    await bot.channel.send(f'Read more at: https://man7.org/linux/man-pages/man{i}/{cmd}.{i}.html')
                return
        await bot.channel.send(f'`{cmd}` was not found.')

def setup(panda):
    panda.add_cog(Man_db(panda))