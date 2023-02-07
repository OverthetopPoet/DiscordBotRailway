# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands

from dice_roller import generate_dice_results, generate_stat_array
import random
from card_picker import draw_cards


f_load_msg = open('loading_screen_messages.txt', 'r', encoding='utf-8')
loading_screen_messages = f_load_msg.readlines()
f_load_msg.close()

command_identifier = '$'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=command_identifier, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def roll(ctx, *args):
    result_message = ''
    if len(args) >= 1 and 'advantage' not in args[0]:
        roll_msg = "".join(str(x) for x in args)
        result_message = '\n'+generate_dice_results(roll_msg, 'roll')

    elif len(args) >= 2 and 'advantage' in args[0]:
        roll_msg = "".join(str(x) for x in args[1:])
        result_message = '\n'+generate_dice_results(roll_msg, args[0])

    else:
        result_message = ' Could not interpret roll:\n'+" ".join(str(x) for x in args)

    emb = discord.Embed(color=discord.Colour(16777030), description=result_message, title='Results:')
    await ctx.reply(embed=emb)


@bot.command()
async def loading(ctx):
    emb = discord.Embed(color=discord.Colour(16777030), description=loading_screen_messages[random.randrange(
        0, len(loading_screen_messages))], title='Loading...')
    await ctx.reply(embed=emb)


@bot.command()
async def bothelp(ctx, type=None):
    result_message = ''
    if type == None:
        result_message = 'If you need assistance with one of the features please type one of the following commands:\n' + command_identifier+'help dice - information about the dice roller\n' + command_identifier+'help cards - information about the card picker\n' + \
            command_identifier+'help rollup - help on how to generate a random character\n' + command_identifier + \
            'loading- receive a randomized loading screen message\n' + command_identifier+'randmeme - sends a random dnd meme'
    elif type == 'dice':
        result_message = 'These are my dice rolling commands:\n' + command_identifier+'roll - rolls any number of dice or bonuses and calculates the end result.\n' + command_identifier + \
            'advantage - rolls any number of dice or bonuses and calculates the end result. All dice are rolled at advantage. (the die is rolled twice and the higher result is highlighted and added to the end result)\n' + command_identifier+'disadvantage - rolls any number of dice or bonuses and calculates the end result. All dice are rolled at disadvantage. (the die is rolled twice and the lower result is highlighted and added to the end result)\n' + \
            'Example: ' + command_identifier + \
            '[roll/advantage/disadvantage] [1]d10 + 2d4 + 2\n Note: If you only want to roll a single die, you can omit the 1 in front of "d". You do not need to add spaces except for immediately after the command name.'
    elif type == 'cards':
        result_message = 'These are my card commands:\n' + command_identifier+'draw cards - draws any number of cards from different deck types.\n' + 'Example: ' + command_identifier + \
            'draw cards [number of cards] [deck type] [options]\nIf you only want to draw one card you can omit the number of cards' + 'deck type: you can choose from the following: standard-52, standard-32,tarot-major, tarot-minor, tarot, deck-of-omens, uno\n' + \
            'options (choose any number that apply that apply): \n-xJokers - add x Joker cards to the deck, x must be a number\n-oriented - include tarot card orientation in result (u for upright, r for reversed)'

    elif type == 'rollup':
        result_message = 'You can roll up ability scores either one at a time or roll up all six at once. Additionally you have the option to specify, what method of stat generation you want to use.'+'\nTemplate: '+command_identifier + \
            'rollup [type] [method]\ntype: \n- single: rolls up one ability score\n- character: rolls up six ability scores\nmethod: \n- standard: roll 4d6 and drop the lowest (this will be the used method, if you leave this part out)\n- hard: roll 3d6'
    else:
        result_message = 'Type "'+command_identifier+'bothelp" for all  available help commands'

    emb = discord.Embed(color=discord.Colour(16777030), description=result_message, title='Help:')
    await ctx.reply(embed=emb)


bot.run(os.environ["DISCORD_TOKEN"])
