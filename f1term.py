#!/usr/bin/env python3

# This is a F1 result terminal application!
# github.com/jtorniainen 2016
# MIT license

import requests
import argparse
import time


TRUNK = 'http://ergast.com/api/f1/'
MAX_NAME_LENGTH = 10
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
            time = FAIL + 8 * ' ' +'DNF {}'.format(item['status']) + ENDC

        print(BOLD + '{:02d}. '.format(int(item['position'])) + ENDC, end="")
        print('{}\t{}'.format(item['Driver']['familyName'], time), end="")
        print('')

def get_race(season, round_num):
    """ Pulls and displays the results of the latest race. """
    if not season:
        season = 'current'

    if not round_num:
        round_num = 'last'

    response = requests.get(TRUNK + season + '/' + round_num + '/results.json').json()
    race = response['MRData']['RaceTable']['Races'][0]


    print('Round {} [{}]'.format(race['round'], race['date']))
    print(BOLD + race['raceName'] + ENDC + '\n')
    print_race_results(race['Results'])

def get_schedule(season):
    if not season:
        season = 'current'
    resp = requests.get(TRUNK + season + '.json').json()
    races = resp['MRData']['RaceTable']['Races']
    pattern = '%Y-%m-%d %H:%M:%S'
    next_race = False
    for race in races:
        race_name = race['raceName']
        if len(race_name) < 24:
            race_name = race_name + (24 - len(race_name)) * ' '
        date = (race['date'] + ' ' + race['time'])[:-1]
        date_str = race['date']
        epoch = int(time.mktime(time.strptime(date, pattern)))
        if time.time() - epoch > 0:
            date_color = OKGREEN
        else:
            if next_race == False:
                date_color = WARNING + BOLD
                date_str = date_str + ' «'
                next_race = True
            else:
                date_color = WARNING

        print(BOLD + '{:02d}. '.format(int(race['round'])) + ENDC, end='')
        print(race_name + '\t', end='')
        print(date_color + date_str + ENDC)




def get_standings(season):
    """ Pulls and displays standings for the specified season. """

    if not season:
        season = 'current'
    resp = requests.get(TRUNK + season + '/driverStandings.json').json()
    data = resp['MRData']['StandingsTable']
    season = data['season']
    standings = data['StandingsLists'][0]['DriverStandings']

    print('Season {}\n'.format(season))

    for standing in standings:
        print(BOLD + '{:02d}. '.format(int(standing['position'])) + ENDC, end='')
        driver_name = standing['Driver']['familyName']
        if len(driver_name) > MAX_NAME_LENGTH:
            driver_name = driver_name[0:MAX_NAME_LENGTH - 1] + '.'
        else:
            driver_name = driver_name + (MAX_NAME_LENGTH - len(driver_name)) * ' '
        print(driver_name + '\t', end='')
        print(OKBLUE + standing['wins'] + ' ' + HEADER + standing['points'] + '\t' + ENDC, end='')
        print(WARNING + standing['Constructors'][0]['name'] + ENDC)


if __name__ == '__main__':
    # get_last_race()
    # get_standings()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help="results, standings or schedule")
    parser.add_argument('-s','--season', help="Season as a year, leave blank for the latest",type=str)
    parser.add_argument('-r','--round', help="Round as a number, leave blank for latest",type=str)
    arguments = parser.parse_args()

    if arguments.command == 'standings':
        get_standings(arguments.season)
    elif arguments.command == 'results':
        get_race(arguments.season, arguments.round)
    elif arguments.command == 'schedule':
        get_schedule(arguments.season)
    elif arguments.command == 'next_race':
        pass
