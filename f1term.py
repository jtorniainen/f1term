#!/usr/bin/env python3

# This is a F1 result terminal application!
# github.com/jtorniainen 2016
# MIT license

import requests


TRUNK = 'http://ergast.com/api/f1/'
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
    response = requests.get(TRUNK + 'current/last/results.json').json()
    race = response['MRData']['RaceTable']['Races'][0]


    print('Round {} [{}]'.format(race['round'], race['date']))
    print(BOLD + race['raceName'] + ENDC + '\n')
    print_race_results(race['Results'])

def get_standings(season='current'):
    resp = requests.get(TRUNK + 'current/driverStandings.json').json()
    data = resp['MRData']['StandingsTable']
    season = data['season']
    standings = data['StandingsLists'][0]['DriverStandings']

    print('Season {}\n'.format(season))

    for standing in standings:
        # print('{:02d}. {}\t{}\t{}'.format(int(standing['position']), standing['Driver']['familyName'], standing['Constructors'][0]['name'], standing['wins']))
        print(BOLD + '{:02d}. '.format(int(standing['position'])) + ENDC, end='')
        print(standing['Driver']['familyName'] + '\t', end='')
        print(OKBLUE + standing['wins'] + ' ' + HEADER + standing['points'] + '\t' + ENDC, end='')
        print(WARNING + standing['Constructors'][0]['name'] + ENDC)




if __name__ == '__main__':
    # get_last_race()
    get_standings()
