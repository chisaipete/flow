#!/usr/bin/env python
import os
from pprint import pprint
from itertools import groupby

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
    cvents = c.get_events(14)

    # for event in ovents:
    #     o_end = event[2]
    #     o_location = event[3]
    #     o_start = event[1]
    #     o_summary = event[0]

    #     for c_evt in cvents:
    #         c_end = c_evt[2]
    #         c_id = c_evt[3]
    #         c_location = event[4]
    #         c_start = c_evt[1]
    #         c_summary = c_evt[0]
    #         if event[0] == c_evt[0]: # summary
    #             pprint(event)
    #             pprint(c_evt)
    #             present = True
    #             if event[1] != c_evt[1] or event[2] != c_evt[2]: # start & end dates
    #                 different = True
    #                 eid = c_evt[3] # eventId for google
    #                 break

    duplicate_events = []

    ovents = sorted(ovents, key=lambda t: t[0])
    for k, v in groupby(ovents, key=lambda t: t[0]):  # assuming your list is stored in l
        if len(list(v)) > 1:
            duplicate_events.append(k)

    pprint(duplicate_events)

    #TODO: Issue with reoccurring events with same name getting duplicated
    #TODO: events getting updated...always

    # find matching event, or identify that we have a new event
    matching_events = set([ov[0] for ov in ovents]).intersection([cv[0] for cv in cvents])
    pprint(matching_events)
        # check if event of the same name is present
            # event has the same name
            # multiple events with the same name
            
        # check if matching event has the same start and end time
            # multiple events with the same time/name
        # check if only a location change
    # if it matches, check for any updates & update it
    # if it doesn't, create a new event
    unique_events_outlook = set([ov[0] for ov in ovents]).difference([cv[0] for cv in cvents])
    pprint(unique_events_outlook)
    unique_events_google = set([cv[0] for cv in cvents]).difference([ov[0] for ov in ovents])
    pprint(unique_events_google)

    # evt = {'summary':event[0],'start':event[1],'end':event[2]}
    # if update_needed:
    #     evt['id'] = eid
    #     c.update_event(evt)
    # else:
    #     c.create_event(evt)

else:
    print('Processing aborted.')
