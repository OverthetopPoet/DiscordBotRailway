import random
random.Random


def generate_roll(nr_rolls, dice_size):
    rolls = []
    if dice_size == 1:
        return[nr_rolls]
    for i in range(nr_rolls):
        rolls.append(random.randrange(1, dice_size+1))

    return rolls


def decipher_roll_message(message):
    rolls = []
    roll_msg = message.replace(' ', '')
    roll_list = roll_msg.split('+')
    for roll in roll_list:
        if 'd' in roll:
            omitted_dice_number = False
            if roll.startswith('d'):
                omitted_dice_number = True

            split_roll = roll.split('d')
            if len(split_roll) == 2 and split_roll[0].isnumeric() and split_roll[1].isnumeric() and int(split_roll[0]) >= 0 and int(split_roll[1]) >= 0:
                rolls.append((int(split_roll[0]), int(split_roll[1])))
            elif len(split_roll) == 2 and split_roll[1].isnumeric() and omitted_dice_number and int(split_roll[1]) >= 0:
                rolls.append((1, int(split_roll[1])))
            else:
                return False
        elif roll.isnumeric() and int(roll) >= 0:
            rolls.append((int(roll), 1))

        else:
            return False
    return rolls


def generate_dice_results(roll_msg, roll_type='roll'):

    rolls = decipher_roll_message(roll_msg)
    if rolls == False:
        return ' Could not interpret roll:\n'+roll_type+' '+roll_msg
    else:
        results = []

        for roll in rolls:
            if roll_type == 'roll':
                results.extend(generate_roll(roll[0], roll[1]))
            else:
                if roll[0] > 1 and roll[1] == 1:
                    results.append(roll[0])
                elif roll[0] > 1 and roll[1] > 1:
                    for i in range(roll[0]):
                        results.append(generate_roll(2, roll[1]))
                elif roll[0] == 1 and roll[1] > 1:
                    results.append(generate_roll(2, roll[1]))

        result_sum = 0
        result_text = ''

        for result in results:
            if type(result) == int:
                result_sum += result
                result_text = result_text+', '+str(result)
            elif roll_type == 'advantage':
                result_sum += max(result)
                result_text = result_text+', ['+str(min(result))+', **'+str(max(result))+'**]'
            elif roll_type == 'disadvantage':
                result_sum += min(result)
                result_text = result_text+', [**'+str(min(result))+'**, '+str(max(result))+']'
        result_text = '[' + result_text[2:] + ']'

        result_message = roll_type + ' ' + roll_msg + \
            ':\nResults: '+result_text+'\nSum: '+str(result_sum)
        return result_message


def generate_stat_array(roll_method):
    if roll_method == 'standard':
        roll_result = generate_roll(4, 6).sort()
        return '[*'+str(roll_result[0])+'*, '+str(roll_result[1])+', '+str(roll_result[2])+', '+str(roll_result[3])+'] = '+str(roll_result[1]+roll_result[2]+roll_result[3])
    elif roll_method == 'hard':
        roll_result = generate_roll(3, 6).sort()
        return '['+str(roll_result[0])+', '+str(roll_result[1])+', '+str(roll_result[2])+'] = '+str(roll_result[0]+roll_result[1]+roll_result[2])
