# Elventus Esports Bot

## Running (Do not follow these steps for deploying on the server):

1. Install required pip modules by running: ```pip install -r requirements.txt```
2. Create .env file and set environment variables:
    1. In the same directory as start.py, run ```echo > .env``` to create an empty .env file
    2. Edit this .env file to include the following lines:<br>
    TOKEN={bot token for server}<br>
    ENVIRONMENT={PROD for Anarchy Esports, TEST for Anarchy Esports Test}
    GOOGLE_CREDENTIALS=NONE
3. Copy the files from the _sqlite_templates_ folder to the _sqldb_ folder
4. Start the bot with: ```python start.py```

## Available supported commands:
#### Admin only:
|command|description|
|-------|-----------|
|^reset_scheduler|Resets the entire scrim scheduler deleting all saved data|
|^refresh_scheduler|Resends all of the scrim scheduler menus|
|^update_role_assign|Sends a new role assign menu without deleting the old one (Old one will no longer work)|
|^meeting|Moves all members to the meeting channel|
|^addteam {teamname} {new team emoji}|Creates a new Elventus team|
|^removeteam {@teamrole}|Removes an Elventus team|
#### Captain only:
|command|description|
|-------|-----------|
|^addchannel {new_channel_name}|Creates a new channel in the captains team category
|^removechannel|Removes the channel it is ran in (Only works in a team category)|



    


