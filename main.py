# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands

from dice_roller import generate_dice_results, generate_stat_array
import random
from card_picker import draw_cards
import aiohttp
import io
import flickrapi


f_load_msg = open('loading_screen_messages.txt', 'r', encoding='utf-8')
loading_screen_messages = f_load_msg.readlines()
f_load_msg.close()


flickr_key = os.environ["FLICKR_KEY"]
flickr_secret = os.environ["FLICKR_SECRET"]
flickr_user = os.environ["FLICKR_USER"]


flickr = flickrapi.FlickrAPI(flickr_key, flickr_secret, format='parsed-json')
sets = flickr.photosets.getList(user_id=flickr_user)

flickr_folders = {}

for folder in sets['photosets']['photoset']:
    flickr_folders.update({folder['title']['_content']: folder['id']})

memes_id = flickr_folders['Memes']
cards_id = flickr_folders['Cards']

meme_photos = flickr.photosets.getPhotos(api_key=flickr_key, photoset_id=memes_id, user_id=flickr_user)
meme_list = meme_photos['photoset']['photo']

card_photos = flickr.photosets.getPhotos(api_key=flickr_key, photoset_id=cards_id, user_id=flickr_user)

card_list = {}
for photo in card_photos['photoset']['photo']:

    card_list.update({photo['title']: photo['id']})


command_identifier = '$'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=command_identifier, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def cards(ctx, card_count, deck_type, *options):

    if not card_count.isnumeric():
        card_count = 1
    else:
        card_count = int(card_count)
    draw_msg = 'cards '+str(card_count)+' '+deck_type+' '+' '.join(options)

    added_jokers = 0
    add_orientation = False

    if 'oriented' in options:
        add_orientation = True

    for option in options:
        if 'Jokers' in option:
            msg = option[:-6]
            if msg.isnumeric():
                added_jokers = int(msg)

    if card_count > 10:
        result_message = ' You can only pick a maximum of 10 cards at a time.'
        emb = discord.Embed(color=discord.Colour(16777030), description=result_message, title='Error:')
        await ctx.reply(embed=emb)
    else:

        result = draw_cards(card_count, deck_type, added_jokers, True, add_orientation)

        result_message = ''
        card_files = []
        if result == []:
            result_message = 'Unable to interpret request. Type '+command_identifier+'help cards for more information.'
            emb = discord.Embed(color=discord.Colour(16777030), description=result_message, title='Error:')
            await ctx.reply(embed=emb)

        else:
            emb = []
            emb.append(discord.Embed(color=discord.Colour(16777030),
                                     description='Draw cards ' + draw_msg, title='Results:'))

            for card in result:
                new_embed = discord.Embed(color=discord.Colour(16777030), title=card)
                card_file = card
                card_file = card_file.replace(' ', '')
                card_file = card_file.replace('(U)', '')
                card_file = card_file.replace('(R)', '-rotated')

                link = ''
                photo = flickr.photos.getSizes(api_key=flickr_key, photo_id=card_list[card_file])
                for i in range(len(photo['sizes']['size'])):

                    if photo['sizes']['size'][i]['label'] == 'Original':
                        link = photo['sizes']['size'][i]['source']
                        break

                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        if resp.status != 200:
                            return await ctx.send('Could not download file...')
                        card_files.append(discord.File(io.BytesIO(await resp.read()), card_file+'.jpg'))

                card_files.append(discord.File('cards/'+card_file+'.jpg', filename=card_file+'.jpg'))
                new_embed.set_image(url='attachment://'+card_file+'.jpg')
                emb.append(new_embed)

            await ctx.reply(files=card_files, embeds=emb)


@bot.command()
async def randmeme(ctx):

    first_photo = meme_list[random.randrange(0, len(meme_list))]
    photo_id = first_photo['id']
    photo = flickr.photos.getSizes(api_key=flickr_key, photo_id=photo_id)

    link = ''
    for i in range(len(photo['sizes']['size'])):

        if photo['sizes']['size'][i]['label'] == 'Original':
            link = photo['sizes']['size'][i]['source']
            break
    emb = discord.Embed(color=discord.Colour(16777030))
    emb.set_image(url='attachment://'+'unknown.jpg')

    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.reply(file=discord.File(data, 'unknown.jpg'), embed=emb)


@bot.command()
async def roll(ctx, *args):
    result_message = ''
    if len(args) >= 1 and 'advantage' not in args[0]:
        roll_msg = ''.join(str(x) for x in args)
        result_message = '\n'+generate_dice_results(roll_msg, 'roll')

    elif len(args) >= 2 and 'advantage' in args[0]:
        roll_msg = ''.join(str(x) for x in args[1:])
        result_message = '\n'+generate_dice_results(roll_msg, args[0])

    else:
        result_message = ' Could not interpret roll:\n'+' '.join(str(x) for x in args)

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
            '[roll/advantage/disadvantage] [1]d10 + 2d4 + 2\n Note: If you only want to roll a single die, you can omit the 1 in front of "d".'
    elif type == 'cards':
        result_message = 'These are my card commands:\n' + command_identifier+'cards - draws any number of cards from different deck types.\n' + 'Example: ' + command_identifier + \
            'cards [number of cards] [deck type] [options]\n' + 'deck type: you can choose from the following: standard-52, standard-32,tarot-major, tarot-minor, tarot, deck-of-omens, uno\n' + \
            'options (choose any number that apply that apply): \n-xJokers - add x Joker cards to the deck, x must be a number\n-oriented - include tarot card orientation in result (u for upright, r for reversed)'

    else:
        result_message = 'Type "'+command_identifier+'bothelp" for all  available help commands'

    emb = discord.Embed(color=discord.Colour(16777030), description=result_message, title='Help:')
    await ctx.reply(embed=emb)


bot.run(os.environ["DISCORD_TOKEN"])
