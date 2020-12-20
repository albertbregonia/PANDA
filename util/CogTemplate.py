from discord.ext import commands as cmd

class CogTemplate(cmd.Cog):

    def __init__(self, panda):
        self.panda = panda
    
    ###

def setup(panda):
    panda.add_cog(CogTemplate(panda))
