import json
import requests

allowed_category_lists = ["ability-scores", "alignments", "classes", "conditions",
                          "damage-types", "languages", "magic-schools", "races", "skills", "weapon-properties"]


def call_api(url, category):
    if not url.endswith('/'):
        url += '/'
    response = requests.get(url+category)
    json_data = json.loads(response.text)
    return json_data


def generate_lookup_result(category, specifier='overview'):
    return_string = ''

    if category == 'overview':
        return_string += "Use the following lookup requests to receive some information about different D&D 5e topics. if you are looking for some specific information about a topic e.g. a specific spell, you can add it after the topic you're loking for. Make sure to hyphenate your individual search terms.\nExample: \"lookup spell fireball\" or \"lookup spell shield-of-faith\"\nInformation provided by https://www.dnd5eapi.co " +\
            "\n- lookup overview - get an overview over all available topics" +\
            "\n- lookup ability-scores - get a list of all ability scores" +\
            "\n- lookup ability-score [ability score name or abbreviation] - get a specific ability score" +\
            "\n- lookup alignments - get a list of all alignments" +\
            "\n- lookup alignment [alignment] - get a specific alignment" +\
            "\n- lookup classes - get a list of all classes" +\
            "\n- lookup conditions - get a list of all conditions" +\
            "\n- lookup condition [condition] - get a specific condition" +\
            "\n- lookup damage-types - get a list of all damage types" +\
            "\n- lookup equipment [equipment] - get a specific piece of equipment" +\
            "\n- lookup feature [class feature] - get a specific class feature" +\
            "\n- lookup trait [racial trait] - get a specific racial trait" +\
            "\n- lookup languages - get a list of all languages" +\
            "\n- lookup language [language] - get a specific language" +\
            "\n- lookup magic-item [magic item] - get a specific magic item" +\
            "\n- lookup magic-schools - get a list of all magic schools" +\
            "\n- lookup magic-school [magic school] - get a specific magic school" +\
            "\n- lookup monster [monster] - get a specific monster" +\
            "\n- lookup races - get a list of all races" +\
            "\n- lookup race [race] - get a specific race" +\
            "\n- lookup rule [rule] - get a specific rule or a list of rules that might fit your search term" +\
            "\n- lookup skills - get a list of all skills" +\
            "\n- lookup skill [skill] - get a specific skill" +\
            "\n- lookup spell [spell] - get a specific spell" +\
            "\n- lookup weapon-properties - get a list of all weapon properties" +\
            "\n- lookup weapon-property [weapon property] - get a specific weapon property"

    elif category.endswith('s') and category in allowed_category_lists:
        try:
            return_string = "These are all available "+category+":"
            json_data = call_api('https://www.dnd5eapi.co/api/', category)
            results = json_data["results"]

            for entry in results:
                return_string += '\n- '+str(entry["index"])

        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'ability-score' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'ability-scores/'+specifier[:2])

            return_string = json_data['name']
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
            return_string = return_string+'\nSkills: '
            for skill in json_data['skills']:
                return_string = return_string+skill['name']+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'alignment' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'alignments/'+specifier)

            return_string = json_data['name']
            return_string = return_string+'\n' + json_data['desc']
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'condition' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'conditions/'+specifier)
            return_string = json_data['name']
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'equipment' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'equipment/'+specifier)

            return_string = json_data['name']
            return_string = return_string + '\nCost:'+str(json_data['cost']['quantity'])+' '+json_data['cost']['unit']
            return_string = return_string + '\nWeight:'+str(json_data['weight'])+'lb'
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'feature' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'features/'+specifier)

            return_string = json_data['name']
            return_string = return_string+'\n Class/Level: '+json_data['class']['name']+' '+str(json_data['level'])
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'trait' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'traits/'+specifier)

            return_string = json_data['name']
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
            return_string = return_string+'\nRaces: '
            for race in json_data['races']:
                return_string = return_string+race['name']+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'language' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'languages/'+specifier)

            return_string = json_data['name']
            return_string = return_string+'\nScript: '+json_data['script']
            return_string = return_string+'\nTypical speakers: '
            for race in json_data['races']:
                return_string = return_string+race+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'magic-item' and specifier != 'overview':
        try:
            specifier = specifier.replace('+', '-')
            json_data = call_api('https://www.dnd5eapi.co/api/', 'magic-items/'+specifier)

            return_string = json_data['name']
            return_string = return_string+'\nRarity: '+json_data['rarity']['name']
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'magic-school' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'magic-schools/'+specifier)

            return_string = json_data['name']
            return_string = return_string+'\n'+json_data['desc']
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'monster' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'monsters/'+specifier)

            return_string = json_data['name']
            return_string = return_string+'\n'+json_data['size']+' '+json_data['type']
            return_string = return_string+'\nChallenge Rating: ' + \
                str(json_data['challenge_rating'])+' ('+str(json_data['xp'])+' XP)'
            return_string = return_string+'\nArmor Class: '+str(json_data['armor_class'])
            return_string = return_string+'\nHit Points: ' + \
                str(json_data['hit_points'])+' ('+json_data['hit_points_roll']+')'
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'race' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'races/'+specifier)

            return_string = json_data['name']
            return_string = return_string+'\nSpeed: '+str(json_data['speed'])+'ft.'
            return_string = return_string+'\nAge: '+json_data['age']
            return_string = return_string+'\nSize: '+json_data['size']
            return_string = return_string+'\nLanguages: '
            for language in json_data['languages']:
                return_string = return_string+language['name']+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
            return_string = return_string+'\nTraits: '
            for trait in json_data['traits']:
                return_string = return_string+trait['name']+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
            return_string = return_string+'\nSubraces: '
            for subrace in json_data['subraces']:
                return_string = return_string+subrace['name']+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'rule' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'rule-sections/'+specifier)
            return_string = json_data['desc']
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'skill' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'skills/'+specifier)

            return_string = json_data['name']
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'spell' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'spells/'+specifier)
            return_string = json_data['name']
            return_string = return_string + '\nLevel: '+str(json_data['level'])+' '+json_data['school']['name']+' spell'
            return_string = return_string + '\nRange: ' + \
                json_data['range']+', Duration: '+json_data['duration']+', Casting Time: '+json_data['casting_time']
            if json_data['ritual']:
                return_string = return_string + ', Ritual'
            if json_data['concentration']:
                return_string = return_string + ', Concentration'
            return_string = return_string+'\nComponents: '
            for component in json_data['components']:
                return_string = return_string+component+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
            for line in json_data['higher_level']:
                return_string = return_string+'\n'+line
            return_string = return_string+'\nClasses: '
            for cls in json_data['classes']:
                return_string = return_string+cls['name']+', '
            for cls in json_data['subclasses']:
                return_string = return_string+cls['name']+', '
            if return_string.endswith(', '):
                return_string = return_string[:-2]
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    elif category == 'weapon-property' and specifier != 'overview':
        try:
            json_data = call_api('https://www.dnd5eapi.co/api/', 'weapon-properties/'+specifier)

            return_string = json_data['name']
            for line in json_data['desc']:
                return_string = return_string+'\n'+line
        except:
            return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    else:
        return_string = "This topic could not be found. Either it does not exist in the SRD, the API Server is down, or it is not yet implemented"

    return return_string
