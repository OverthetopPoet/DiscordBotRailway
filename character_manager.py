from rules_lookup import call_api
from dice_roller import generate_roll
import random


def calculate_modifier(ability_score):
    if ability_score % 2 == 0:
        return (ability_score-10)/2
    if ability_score % 2 == 1:
        return (ability_score-11)/2


def generate_random_character():
    json_data = call_api('https://www.dnd5eapi.co/api/', 'races')
    race_list = json_data["results"]
    json_data = call_api('https://www.dnd5eapi.co/api/', 'classes')
    class_list = json_data["results"]

    # class_choice=class_list[random.randrange(0,len(class_list))]['index']
    #class_info = call_api('https://www.dnd5eapi.co/api/', 'classes')

    race_choice = race_list[random.randrange(0, len(race_list))]['index']
    race_info = call_api('https://www.dnd5eapi.co/api/', 'races/'+race_choice)

    random_race = race_info['name']
    random_class = class_list[random.randrange(0, len(class_list))]['name']
    ability_scores = {
        'str_score': 0,
        'dex_score': 0,
        'con_score': 0,
        'int_score': 0,
        'wis_score': 0,
        'cha_score': 0
    }
    random_subrace = ''
    subrace_list = race_info.get('subraces')
    if subrace_list != None:
        subrace_choice = subrace_list[random.randrange(0, len(subrace_list))]['index']
        subrace_info = call_api('https://www.dnd5eapi.co/api/', 'subraces/'+subrace_choice)
        random_subrace = subrace_info['name']
        for ability_bonus in subrace_info['ability_bonuses']:
            score = ability_bonus['ability_score']['index']+'_score'
            temp = ability_scores.get(score)
            temp += ability_bonus['bonus']
            ability_scores.update({score: temp})

    if random_subrace != '':
        random_race = random_race+' ('+random_subrace+')'

    for ability_bonus in race_info['ability_bonuses']:
        score = ability_bonus['ability_score']['index']+'_score'
        temp = ability_scores.get(score)
        temp += ability_bonus['bonus']
        ability_scores.update({score: temp})

    for score in ability_scores.keys():
        temp = ability_scores.get(score)
        rolls = generate_roll(4, 6)
        rolls = rolls.sort()
        for i in range(1, len(rolls)):
            temp += rolls[i]
        ability_scores.update({score: temp})

    return '\nYour random Character has been decided:\n'+random_race+' '+random_class+'\nStrenght: '+str(ability_scores['str_score'])+' ('+str(calculate_modifier(ability_scores['str_score']))+') '+'Dexterity: '+str(ability_scores['dex_score'])+' ('+str(calculate_modifier(ability_scores['dex_score']))+') '+'Constitution: '+str(ability_scores['con_score'])+' ('+str(calculate_modifier(ability_scores['con_score']))+') '+'Intelligence: '+str(ability_scores['int_score'])+' ('+str(calculate_modifier(ability_scores['int_score']))+') '+'Wisdom: '+str(ability_scores['wis_score'])+' ('+str(calculate_modifier(ability_scores['wis_score']))+') '+'Charisma: '+str(ability_scores['cha_score'])+' ('+str(calculate_modifier(ability_scores['cha_score']))+') '
