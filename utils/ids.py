import os
from dotenv import load_dotenv

load_dotenv()


# if environment is PROD, set the id's for PROD
if os.getenv("ENVIRONMENT") == "PROD":
    bot_id = 805663879555842078

    guild = 599752943100493847

    # List of admins to check for before activating a command
    admins = [299314753220640778, 463676272510369793, 156960118141878272]

    # List of id's for specific roles
    coach = 624874643576193054
    roster_manager = 706756324658249748
    captain = 652419554865053716
    moderator = 660922990590164993
    staff = 690781218882715658
    community = 690250317530792082
    sub = 735208365738688553
    starter = 612529196027084870
    everyone = 599752943100493847
    top_starter = 653695409247485952
    jungle_starter = 653695313227546628
    mid_starter = 653695673010618397
    adc_starter = 653695464172027904
    support_starter = 653695484879306782
    top_community = 689576020860600446
    jungle_community = 689576034647015478
    mid_community = 689576051650592954
    adc_community = 689576066322530348
    support_community = 689576083418644528
    top_sub = 773479928100421692
    jungle_sub = 773479929518096415
    mid_sub = 773480366719107073
    adc_sub = 773480434364710962
    support_sub = 773480575901499393

    # Category that contains all of the chats
    chat_category = 706968077539213372

    voice_category = 809604119769251870

    # Category that contains all of the team voice chats
    teams_category = 811282464794214431

    # Channel where people react to get roles
    server_access_channel = 775520724894351390

    # Meeting voice channel
    meeting_channel = 693311657430089798

    # Modmail channel
    modmail_channel = 769585298358272030

    attendance_channel = 730535318364618803

    lf_scrim_channel=809604637900406844

    # LFT channel for applicants
    lft_channel = 787376075864670268

    # Bulk role ids

    # Rank roles
    ranks = [689520503257432141, 689520495133327427, 689520482277785624, 689542018426208334, 689542150643515488, 660922737245552650, 689542327122919496, 689542523902754854, 745424154291077281]

    # Positions [Top, Jungle, Mid, ADC, Support]
    community_positions = [top_community, jungle_community, mid_community, adc_community, support_community]
    sub_positions = [top_sub, jungle_sub, mid_sub, adc_sub, support_sub]

    # A map to use when converting between community and sub members
    community_sub_map = {top_community:top_sub, jungle_community:jungle_sub, mid_community:mid_sub, adc_community:adc_sub, support_community:support_sub}

    # Role ids that contain "Elventus " to exclude when searching for team roles
    elventus_space = [starter, sub, community]

    # Spreadsheet key used when accessing the applications spreadsheet
    applications_spread_key = "1_F7h3jbU3MdX_Awlk9Suy4hg0HdcGnuLM6BBdTu-d9o"
elif os.getenv("ENVIRONMENT") == "TEST":
    bot_id = 777314263084826667

    guild = 777248439024484373

    # List of admins to check for before activating a command
    admins = [463676272510369793, 299314753220640778, 156960118141878272]

    # List of id's for specific roles
    coach = 777248439263428627
    roster_manager = 777248439263428626
    captain = 777248439234199555
    moderator = 777248439234199557
    community = 777248439024484380
    sub = 777248439024484381
    starter = 777248439078879243
    staff = 777248439285186612
    everyone = 777248439024484373
    top_starter = 777248439078879242
    jungle_starter = 777248439078879241
    mid_starter = 777248439078879240
    adc_starter = 777248439078879239
    support_starter = 777248439024484382
    top_community = 777248439024484379
    jungle_community = 777248439024484378
    mid_community = 777248439024484377
    adc_community = 777248439024484376
    support_community = 777248439024484375
    top_sub = 777248439078879248
    jungle_sub = 777248439078879247
    mid_sub = 777248439078879246
    adc_sub = 777248439078879245
    support_sub = 777248439078879244

    # Category that contains all of the chats
    chat_category = 777248441058590747

    # Queue Room Category for all of the queue rooms
    voice_category = 780529394430509119

    # Category that contains all of the team voice chats
    teams_category = 813760024786632715

    server_access_channel = 777248440199413770

    # Meeting voice channel
    meeting_channel = 810185911735287808

    # Modmail channel
    modmail_channel = 777248440551342095

    # Channel for attendance logs

    attendance_channel = 777248440199413777

    # Scrim Scheduler Channel
    lf_scrim_channel = 777248440551342094

    # LFT channel for applicants
    lft_channel = 810530134569648139

    # Bulk role ids

    # Rank roles
    ranks = [777248439117021242, 777248439117021241, 777248439117021240, 777248439117021239, 777248439117021238, 777248439117021237, 777248439117021236, 777248439117021235, 777248439117021234]

    # Positions [Top, Jungle, Mid, ADC, Support]
    community_positions = [top_community, jungle_community, mid_community, adc_community, support_community]
    sub_positions = [top_sub, jungle_sub, mid_sub, adc_sub, support_sub]

    # A map to use when converting between community and sub members
    community_sub_map = {top_community:top_sub, jungle_community:jungle_sub, mid_community:mid_sub, adc_community:adc_sub, support_community:support_sub}

    # Role ids that contain "Elventus " to exclude when searching for team roles
    elventus_space = [starter, sub, community]

    # Spreadsheet key used when accessing the applications spreadsheet
    applications_spread_key = "1_F7h3jbU3MdX_Awlk9Suy4hg0HdcGnuLM6BBdTu-d9o"
else:
    print("no environment was specified")
