#!/usr/bin/env python3

# This is a F1 result terminal application!
# github.com/jtorniainen 2016
# MIT license

import requests

# Define some colors and effects
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def print_race_results(race):
    """ Prints the contents of a race result dict. """
    for item in race:
        if 'Time' in item.keys():
            time = item['Time']['time']
            if len(time) < 11:
                time = (11- len(time)) * ' ' + time
            time = OKGREEN + time + ENDC
        else:
            time = FAIL + 8 * ' ' +'DNF' + ENDC

        print(BOLD + '{:02d}. '.format(int(item['position'])) + ENDC, end="")
        print('{}\t{}'.format(item['Driver']['familyName'], time), end="")
        print('')

def get_last_race():
    """ Pulls and displays the results of the latest race. """
    response = requests.get('http://ergast.com/api/f1/current/last/results.json').json()
    race = response['MRData']['RaceTable']['Races'][0]


    print('Round {} [{}]'.format(race['round'], race['date']))
    print(BOLD + race['raceName'] + ENDC + '\n')
    print_race_results(race['Results'])


if __name__ == '__main__':
    get_last_race()
