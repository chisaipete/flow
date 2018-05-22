#!/usr/bin/env python
import os

from inbox import outlook
from planner import google_calendar

r = input('Is your Outlook calendar ready to shadow into google calendar? [y] ')

# find all events in outlook which aren't family or non-work and create generic "Work" events in gcal

if not r.strip().lower() or r.strip().lower()[0] == 'y':
    
    print('Processing Outlook events...')
    o = outlook.Outlook()
    # get all upcoming events in the next two weeks
    ovents = o.get_events(14)

    print('Collecting Google events...')
    c = google_calendar.Calendar()
    c.setup_service()
    cevents = c.get_events(14)

    for event in ovents:
        print('Checking {} on Google Calendar'.format(event[0]))

        present = False
        different = False
        eid = ''

        #TODO: Issue with reoccurring events with same name getting duplicated
        #TODO: events getting updated...always
        for c_evt in cevents:
            if event[0] == c_evt[0]:
                present = True
                if event[1] != c_evt[1] or event[2] != c_evt[2]:
                    different = True
                    eid = c_evt[3]
                    break

        if not present:
            print('    Adding event')
            evt = {'summary':event[0],'start':event[1],'end':event[2]}
            c.create_event(evt)
        elif different:
            print('    Updating event')
            evt = {'summary':event[0],'start':event[1],'end':event[2],'id':eid}
            c.update_event(evt)
        else:
            print('    Event is up to date')

else:
    print('Processing aborted.')
