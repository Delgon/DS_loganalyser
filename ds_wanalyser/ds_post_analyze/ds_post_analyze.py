#!/usr/bin/env python
# encoding: utf-8

import csv
from datetime import datetime, timedelta

#file = r"E:\bmolle\Documents\perso\Warcraft Logs - Combat Analysis for Warcraft.csv"

# Variables
time0 = 0.0
who = []
format = '%H:%M:%S.%f'
delta = timedelta(seconds=2)
stack = 0
stacks = []
cpt = 1
to_print = ''

# Ouverture du fichier csv en export de Warcraft Log (format utf-8 with BOM)
with open(file, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    # Pour chaque event
    for row in reader:
        name = row['Event'].split(' ')[0]
        time = row['Time']

        # Si premier event
        if time0 == 0.0:
            time0 = datetime.strptime(time, format)
            stack = 1
            who.append([name,1])
        # sinon
        else :
            time1 = datetime.strptime(time,format)
            # s'il ce passe moins de 2 seconds entre les stacks
            if time1 - time0 <= delta:
                stack += 1
                time0 = time1

                for w in who:
                    if name == w[0]:
                        w[1] += 1
                        break
                else:
                    who.append([name,1])

                # si on dépasse 4 stacks, affichage
                if stack > 4:
                    to_print += ('\nA %s:%s %s nous fait passer à %s stacks' % (time1.minute, time1.second, row['Event'].split(' ')[0], stack))

            # sinon reset compteur
            else:
                if stack > 0:
                    print('\n-----------------------------\n'
                          'Stacking n°%s : Les personnes à avoir stack sont :' % cpt)
                    for w in who:
                        print('     - %s (%s)' % (w[0], w[1]))
                    if to_print != '':
                        print(to_print)
                    to_print = ''
                cpt += 1
                who = [[name, 1]]

                stacks.append(stack)
                stack = 1
                time0 = time1
