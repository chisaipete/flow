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

    for o_evt in ovents:
        o_end = o_evt[2]
        o_id = o_evt[4]
        o_location = o_evt[3]
        o_start = o_evt[1]
        o_summary = o_evt[0]
        print("Outlook Event: {} {}".format(o_summary, o_start))

        event_match = False
        detail_different = False

        for c_evt in cvents:
            c_end = c_evt[2]
            c_id = c_evt[3]
            c_location = c_evt[4]
            c_oid = c_evt[5]
            c_start = c_evt[1]
            c_summary = c_evt[0]

            # if there is an event which does match oid, but details are different, update google
            if c_oid == o_id and o_start == c_start:
                # check event lists for matching oid's
                print("  Matching event: {} {}".format(c_summary, c_start))
                event_match = True
                if c_location != o_location or c_end != o_end or \
                    c_summary != o_summary:
                    detail_different = True

        if event_match:
            if detail_different:
                print("  Event found, updating to match Outlook: {} {}".format(o_summary, o_start))
                evt = {'summary':o_summary,'start':o_start,'end':o_end,'location':o_location,'oid':o_id,'id':c_id}
                c.update_event(evt)
        else:
            print("  Event not found, adding to Google Calendar: {} {}".format(o_summary, o_start))
            # if there is an event which doesn't match oid, it needs to be added to google
            evt = {'summary':o_summary,'start':o_start,'end':o_end,'location':o_location,'oid':o_id}
            c.create_event(evt)


    # # if there is an event in google, but not in oevent list, remove it from google
    # # VERY BUGGY, DIMINISHING RETURNS HERE
    # for c_evt in cvents:
    #     c_id = c_evt[3]
    #     c_oid = c_evt[5]
    #     c_summary = c_evt[0]

    #     no_matching_oid = True

    #     for o_evt in ovents:
    #         o_id = o_evt[4]
    #         if not o_id:
    #             # event doesn't have a oid, so shouldn't be compared
    #             continue
    #         if c_oid == o_id:
    #             no_matching_oid = False

    #     if no_matching_oid:
    #         print("  Stale event in Google Calendar, removing: {} {}".format(c_summary, c_start))
    #         evt = {'summary':c_summary,'id':c_id}
    #         c.delete_event(evt)


else:
    print('Processing aborted.')
