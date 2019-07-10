#!/usr/bin/env python
from notes import google_sheets
import json
from pprint import pprint
from datetime import datetime

def convert_to_date(timestamp):
    return str(datetime.utcfromtimestamp(int(timestamp)/1000).strftime('%m/%d/%Y'))


def convert_to_lbs(kgs):
    # rounds results to .5 lb granularity (matches plate sizes)
    return round((kgs*2.20462)*2)/2


def filter_exercise(exercise):
    return 'V-Bar' not in exercise and \
            'Chinup' not in exercise and \
            'Dumbbell' not in exercise and \
            'Incline' not in exercise and \
            'Curl' not in exercise and \
            'Pushup' not in exercise and \
            'Pulldown' not in exercise


programs = {}

with open('E:\\Dropbox\\projects\\fitness\\progression_backup\\up.json', 'r') as prgms:
    program_data = json.load(prgms)
    for program in program_data:
        programs[program['id']] = {'name': program['name'], 'activities': {}}
        for day in program['days']:
            for activity in day['activities']:
                programs[program['id']]['activities'][activity['id']] = activity['name']

exercises_to_append = []

with open('E:\\Dropbox\\projects\\fitness\\progression_backup\\fws.json', 'r') as logs:
    logs_data = json.load(logs)
    for entry in logs_data:
        date = convert_to_date(entry['startTime'])
        try:
            program = programs[entry['programId']]['name']
        except KeyError:
            program = 'None'
        for activity in entry['activities']:
            exercise = activity['name']\
                .replace('Barbell ', '')\
                .replace('Shoulder', 'Overhead')\
                .replace('Chinup', 'Chinup Negative')\
                .replace('Machine ', '')\
                .replace('Bent-Over', 'Barbell')
            sets = []
            for _set in activity['performance']['completedSets']:
                sets.append((_set['reps'], convert_to_lbs(_set['weight'])))
            if filter_exercise(exercise) and program is not 'None':
                # print(f"{date} | {program} | {exercise} | {max(sets)}")
                exercises_to_append.append([date, exercise, max(sets)[1], max(sets)[0]])

# grab a list of known workouts in a google sheet
sheets_connection = google_sheets.Sheets()
for entry in exercises_to_append:
    print(entry)
    sheets_connection.append_list_to_table(
        '1-vRxFamZOI_doMbcfVIpoEGaeDFvVM6OBWg0QM9YbBw',
        'Connor-Historical',
        'A2:D',
        entry)
