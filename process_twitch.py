#!/usr/bin/env python
from projects import twitch
from notes import google_sheets

twitch_connection = twitch.Twitch()
# twitch_connection.test('chisaipete', '18xxperson', 'S1faka', 'ninja')

# grab a full list of twitch videos (VODs) (Time, Title, Category, Tags)
twitch_videos = twitch_connection.client.user('chisaipete').videos()
candidate_videos = []
for video in twitch_videos:
    if video.viewable:
        print(f"{video.created_at} | {video.title} | {video.type}")
    candidate_videos.append([video.created_at, video.title, '', '', video.duration])

# grab a list of known twitch videos in a google sheet
sheets_connection = google_sheets.Sheets()
existing_archive_videos = sheets_connection.get_values_from_spreadsheet('1RBvkAk8-ksnJd5O7SsSazk8j4p6Rkzq1oDJgdSOrYS4', 'Twitch Archive', 'A2:E')

# compare and add new twitch videos to the end of the google sheet
# FIXME: This does not properly handle the currently LIVE video (stream), duration will be inaccurate
for c_video in candidate_videos:
    found = False
    for a_video in existing_archive_videos:
        if c_video[0] == a_video[0]:
            found = True
    if not found:
        # add video to archive
        # print(c_video)
        sheets_connection.append_list_to_table('1RBvkAk8-ksnJd5O7SsSazk8j4p6Rkzq1oDJgdSOrYS4', 'Twitch Archive', 'A2:E', c_video)
