import os
import cv2
numerals = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
            'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI']

omen_names = ['The Clever Animal', 'The Duelist', 'The Beloved Friends', 'The Runaway', 'The Avenger', 'The Traveller', 'The Beguiler', 'The Phantom',
              'The Brute', 'The Dragon', 'The Angel', 'The Mind-Bender', 'Time', 'New Beginnings', 'The Hunt', 'War', 'The Moon', 'The Sea',
              'The Truth', 'The Seasons', 'The Campions', 'The Dead']
omen_values = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI',
               'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII']


card_list = os.listdir(os.getcwd()+'/input/uno')
for filename in card_list:
    if '.jpg' in filename:
        file = cv2.imread(os.getcwd()+'/input/uno/'+filename)
        if filename == "WC.jpg":
            filename = "wildcard.jpg"
        if filename == "W4.jpg":
            filename = "wildcard+4.jpg"
        else:
            if filename.startswith('G'):
                filename = 'Green-'+filename[1:]
            if filename.startswith('R'):
                filename = 'Red-'+filename[1:]
            if filename.startswith('Y'):
                filename = 'Yellow-'+filename[1:]
            if filename.startswith('B'):
                filename = 'Blue-'+filename[1:]
            filename = filename.replace('-A', '-+')
            filename = filename.replace('-R', '-reverse')
            filename = filename.replace('-S', '-block')
        cv2.imwrite(os.getcwd()+'/cards/'+filename, file)

card_list = os.listdir(os.getcwd()+'/input/playing_cards')
for filename in card_list:
    if '.jpg' in filename:
        file = cv2.imread(os.getcwd()+'/input/playing_cards/'+filename)

        filename = filename.replace('jack', 'Jack')
        filename = filename.replace('king', 'King')
        filename = filename.replace('queen', 'Queen')
        filename = filename.replace('ace', 'Ace')
        filename = filename.replace('joker', 'Joker')
        filename = filename.replace('diamonds', 'Diamonds')
        filename = filename.replace('clubs', 'Clubs')
        filename = filename.replace('hearts', 'Hearts')
        filename = filename.replace('spades', 'Spades')
        filename = filename.replace('_', '-')

        cv2.imwrite(os.getcwd()+'/cards/'+filename, file)

card_list = os.listdir(os.getcwd()+'/input/tarot')
for filename in card_list:
    if '.jpg' in filename:
        file = cv2.imread(os.getcwd()+'/input/tarot/'+filename)

        if '-' in filename:
            number = filename[0:2]
            if number.startswith('0'):
                number = number[1]
            number = int(number)
            filename = numerals[number]+filename[2:]

        else:
            number = filename[-6:-4]
            if number.startswith('0'):
                number = number[1]
            if number == '11':
                number = 'Page'
            if number == '12':
                number = 'Knight'
            if number == '13':
                number = 'Queen'
            if number == '14':
                number = 'King'
            if number == '1':
                number = 'Ace'
            filename = number+'-of-'+filename[:-6]+'.jpg'
        cv2.imwrite(os.getcwd()+'/cards/'+filename, file)
        file = cv2.rotate(file, cv2.ROTATE_180)
        filename = filename.replace('.jpg', '-rotated.jpg')
        cv2.imwrite(os.getcwd()+'/cards/'+filename, file)

card_list = os.listdir(os.getcwd()+'/input/deck_of_omens')
for filename in card_list:
    if '.jpg' in filename:
        file = cv2.imread(os.getcwd()+'/input/deck_of_omens/'+filename)
        number = int(filename[:-4])-1
        filename = omen_values[number]+'-'+omen_names[number]+'.jpg'
        cv2.imwrite(os.getcwd()+'/cards/'+filename, file)
