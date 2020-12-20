import os
import sys

def readfile(file, temp): #read code from file
    msg = ''
    for line in file.readlines():
        msg+=line
    file.close()
    if temp:
        os.remove(file.name)
    return msg

def readcode(code): #read code from string
    msg = ''
    i = 0
    for line in code.split('\n'):
        i+=1
        msg += f'{i}. {line}\n'
    return msg

def run(user, code): #execute code given as a string
    with open(f'{user}.txt', 'w') as output:
        sys.stdout = output
        exec(code)

#formatting
def authorheader(bot):
    return border('Code by: '+bot.author.mention)

def codeblock(code):
    return f'\n```\n{code}\n```\n'

def outputblock(out):
    return border('Output')+f'\n```\n{out}\n```'

def border(s):
    return 10*'='+' **'+s+'** '+10*'='

#Displays the results as a server channel message
def result(bot, code):
    try:
        run(str(bot.author), code)
        return authorheader(bot)+codeblock(readcode(code))+outputblock(readfile(open(str(bot.author)+'.txt', 'r'), True))
    except Exception as error:
        os.remove(f'{str(bot.author)}.txt')
        return authorheader(bot)+codeblock(readcode(code))+outputblock(error)

#Displays the results as a DM
def DMresult(msg):
    try:
        run(str(msg.author), msg.content)
        return codeblock(readcode(msg.content))+outputblock(readfile(open(str(msg.author)+'.txt', 'r'), True))
    except Exception as error:
        os.remove(f'{str(msg.author)}.txt')
        return codeblock(readcode(msg.content))+outputblock(error)