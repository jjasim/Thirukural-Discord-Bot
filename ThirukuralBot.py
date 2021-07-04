import discord
from discord.ext import commands
import random

"""Thirukural Bot
A Discord bot to get Thirukural quotes in both English and Tamil
Is also able to return random kural quotes in English and Tamil"""

client = commands.Bot(command_prefix = "!")
token = "ODU2NTI5ODI2NTI1MjE2Nzgw.YNCXkA.JdTt8Cek27j715sIBBcz6-MevCg"

#total_kurals hold the total number of Kurals 
#available in a particular langauge
#When this var is -1, the total is yet to be initialised
total_kurals_eng = -1
total_kurals_tam = -1

#Source file for text
eng_file = "TKuralEng.txt"
tam_file = "TKuralTam.txt"

#Helper method to parse through file and return Kural at index
def get_kural(index, filename, header):
    with open(filename, 'r', encoding='utf-8') as kural:
        lines = kural.readlines()

    index, pred, ans = str(index), False, ""

    #This for loop looks for index in file and sets ans to the indexth Kural
    for line in lines:
        if index in line:
            pred = True
        elif pred == True:
            ans = line
            break

    ans = ans.replace("â€™", "'").replace("$", "\n")
    print(f'\n\nKural no: {index}\nKural returned:\n{ans}') 
    kural.close()

    ans = f'\nKural no: {index}\n' + ans if header == True else ans 
    return ans

#Helper method to count the total number of Kurals in a source file.
def count_kurals(filename):
    with open(filename, 'r', encoding='utf-8') as kural:
        lines = kural.readlines()

    count = 0
    for line in lines:
        if str(count + 1) in line:
            count += 1
    return count

#Event to show that bot is ready
@client.event
async def on_ready():
    print("ThirukuralBot is ready")

#!kuraleng index - Discord command to get indexth Kural in English
@client.command()
async def kuraleng(ctx, index):
    await ctx.send(get_kural(index, eng_file, False))

#!kural index - Discord command to get indexth Kural in Tamil
@client.command()
async def kural(ctx, index):
    await ctx.send(get_kural(index, tam_file, False))

#!rkuraleng - Discord command to get random Kural in English
@client.command()
async def rkuraleng(ctx):
    global total_kurals_eng
    
    if total_kurals_eng == -1:
        total_kurals_eng = count_kurals(eng_file)
    await ctx.send(get_kural(random.randint(1, total_kurals_eng), eng_file, True))

#!rkural - Discord command to get random Kural in Tamil
@client.command()
async def rkural(ctx):
    global total_kurals_tam
    
    if total_kurals_tam == -1:
        total_kurals_tam = count_kurals(tam_file)
    await ctx.send(get_kural(random.randint(1, total_kurals_tam), tam_file, True))
        

client.run(token)
