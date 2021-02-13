import scrim_scheduler.scrim_scheduler_config as scrim_scheduler_conifg
import utils.ids as ids
import utils.ui
import utils.team
import utils.member
import discord
import copy
import random

class Scrim_Scheduler:
    def __init__(self, scheduler_dbinter, guild):
        self.dbinter = scheduler_dbinter
        self.guild = guild
    
    async def refresh_menus(self):
        """
        Refreshs the menus by re building and sending the embed
        """
        await self.send_lfscrim()

        teams = utils.team.get_teams(self.guild)
        for team in teams:
            await self.send_team_agenda(team[0], team[1])

    async def reset_scheduler(self):
        """
        Resets the scrim scheduler
        Warning: Deletes all saved data
        """
        self.dbinter.delete_all_blocked_slots()
        self.dbinter.delete_all_invites()
        self.dbinter.delete_all_scheduled_matches()
        self.assign_invite_codes()
        await self.send_lfscrim()

        teams = utils.team.get_teams(self.guild)
        for team in teams:
            await self.send_team_agenda(team[0], team[1])
    
    async def unblock_slot(self, message, code):
        """
        Unblocks a time slot for a team
        """
        invite_data = self.dbinter.get_invite_from_code(code)
        if invite_data is None:
            await message.author.send("That is not a valid code")
            await message.delete()
            return

        # If they are trying to unblock a slot that they dont own
        unblocking_team = utils.member.get_member_team(message.author)
        if unblocking_team != invite_data[1]:
            await message.author.send("You are not on that team")
            await message.delete()
            return
        
        day = invite_data[2]
        time = invite_data[3]

        # Make sure that the slot they are trying to unblock is blocked
        blocked_slots = self.dbinter.get_teams_blocked_slots(unblocking_team)
        flag = False
        for blocked_slot in blocked_slots:
            if blocked_slot[1] == day and blocked_slot[2] == time:
                flag = True

        if not flag:
            await message.author.send("That slot is not blocked")
            return
        
        # Removed the blocked slot and update the menus
        self.dbinter.delete_blocked_slot(unblocking_team, day, time)

        await self.send_team_agenda(unblocking_team, utils.team.get_team_category(self.guild, unblocking_team))
        await self.send_lfscrim()


    async def block_slot(self, message, code):
        """
        Blocks a time slot for a team
        """
        invite_data = self.dbinter.get_invite_from_code(code)
        if invite_data is None:
            await message.author.send("That is not a valid code")
            await message.delete()
            return

        # If they are trying to block a slot that they dont own
        blocking_team = utils.member.get_member_team(message.author)
        if blocking_team != invite_data[1]:
            await message.author.send("You are not on that team")
            await message.delete()
            return
        
        day = invite_data[2]
        time = invite_data[3]

        # If they already have a scrim scheduled for that time
        teams_scheduled_matches = self.dbinter.get_scheduled_matches_for_team(blocking_team)

        for scheduled_match in teams_scheduled_matches:
            if scheduled_match[2] == day and scheduled_match[3] == time:
                await message.author.send("You are already scheduled at that time!")
                return
        
        # Remove all of their sent invites and refresh the affected teams agendas
        team_sent_invites = self.dbinter.get_invites_sent_by_team(blocking_team, day, time)
        self.dbinter.delete_invites_sent_from_team(blocking_team, day, time)

        for sent_invite in team_sent_invites:
            await self.send_team_agenda(sent_invite[0], utils.team.get_team_category(self.guild, sent_invite[0]))

        # Add their blocked time slot
        self.dbinter.insert_blocked_slot(blocking_team, day, time)
        # Refresh the blocking teams agenda
        await self.send_team_agenda(blocking_team, utils.team.get_team_category(self.guild, blocking_team))
        # Refresh lfscrim
        await self.send_lfscrim()

        


    async def cancel_scrim(self, message, code):
        """
        Cancels a scrim for a team
        """
        invite_data = self.dbinter.get_invite_from_code(code)
        if invite_data is None:
            await message.author.send("That is not a valid code")
            return

        scheduled_team = invite_data[1]
        cancelling_team = utils.member.get_member_team(message.author)
        day = invite_data[2]
        time = invite_data[3]

        # Make sure these two teams are actually scheduled
        scheduled_matches_data = self.dbinter.get_scheduled_matches()

        flag = False
        for scheduled_match in scheduled_matches_data:
            if scheduled_match[0] == scheduled_team or scheduled_match[1] == scheduled_team:
                if scheduled_match[0] == cancelling_team or scheduled_match[1] == cancelling_team:
                    if scheduled_match[2] == day and scheduled_match[3] == time:
                        flag = True
                        break
        
        if flag == False:
            await message.author.send("You are not scheduled with this team at that time")
            return

        # Remove scrim from scheduled matches
        self.dbinter.delete_scheduled_match(scheduled_team, cancelling_team, day, time)

        # Resend menus
        await self.send_team_agenda(scheduled_team, utils.team.get_team_category(self.guild, scheduled_team))
        await self.send_team_agenda(cancelling_team, utils.team.get_team_category(self.guild, cancelling_team))
        await self.send_lfscrim()

    
    async def accept_invite(self, message, code):
        """
        Accepts an invite to a team
        """
        invite_data = self.dbinter.get_invite_from_code(code)
        if invite_data is None:
            await message.author.send("That is not a valid code")
            return

        sending_team = invite_data[1]
        day = invite_data[2]
        time = invite_data[3]
        accepting_team = utils.member.get_member_team(message.author)
        recieved_invites_data = self.dbinter.get_recieved_invites(accepting_team)
        
        # Make sure the sending team invited the accepting team
        flag = False
        for recieved_invite in recieved_invites_data:
            # Check if this invite matches the invite data
            if recieved_invite[1] == invite_data[1] and recieved_invite[2] == invite_data[2] and recieved_invite[3] == invite_data[3]:
                flag = True
                break
        
        if flag == False:
            await message.author.send("You do not have an invite with that code")
            await message.delete()
            return
        
        # Get invites sent from both teams so we know which team agendas to refresh
        accepting_team_sent = self.dbinter.get_invites_sent_by_team(accepting_team, day, time)
        sending_team_sent = self.dbinter.get_invites_sent_by_team(sending_team, day, time)

        affected_teams = set()

        for sent_invite in accepting_team_sent:
            if sent_invite[0] not in affected_teams:
                affected_teams.add(sent_invite[0])
        
        for sent_invite in sending_team_sent:
            if sent_invite[0] not in affected_teams:
                affected_teams.add(sent_invite[0])

        # Check if the accepting and sending teams arent in the affected teams and add them
        if accepting_team not in affected_teams:
            affected_teams.add(accepting_team)
        if sending_team not in affected_teams:
            affected_teams.add(sending_team)

        # Remove sent invites from both teams
        self.dbinter.delete_invites_sent_from_team(accepting_team, day, time)
        self.dbinter.delete_invites_sent_from_team(sending_team, day, time)
        
        # Add scheduled match to db
        self.dbinter.insert_scheduled_match(accepting_team, sending_team, day, time)

        # Refresh all affecting menus
        for team in affected_teams:
            await self.send_team_agenda(team, utils.team.get_team_category(self.guild, team))
        await self.send_lfscrim()

    
    async def send_invite(self, code, sending_member):
        """
        Sends an invite to a team
        """
        invite_data = self.dbinter.get_invite_from_code(code)

        sending_team = utils.member.get_member_team(sending_member)
        recieving_team = invite_data[1]

        # Check for inviting of yourself
        if sending_team == recieving_team:
            await sending_member.send("You cannot invite your own team")
            return
        
        # Check to make sure this team is not blocked at that time
        recieving_team_blocked = self.dbinter.get_teams_blocked_slots(recieving_team)
        for blocked_slot in recieving_team_blocked:
            if blocked_slot[1] == invite_data[2] and blocked_slot[2] == invite_data[3]:
                await sending_member.send("This team is not available")
                return
        
        # Check to make sure this team doesnt already have a scrim scheduled
        scheduled_matches_data = self.dbinter.get_scheduled_matches()

        for scheduled_match in scheduled_matches_data:
            team1 = scheduled_match[0]
            team2 = scheduled_match[1]
            match_day = scheduled_match[2]
            match_time = scheduled_match[3]
            
            if match_day == invite_data[2] and match_time == invite_data[3]:
                if sending_team == team1 or sending_team == team2:
                    await sending_member.send("You are already scheduled at this time")
                    return
                if recieving_team == team1 or recieving_team == team2:
                    await sending_member.send("This team is already scheduled at that time")

        # Send invite
        self.dbinter.insert_invite(recieving_team, sending_team, invite_data[2], invite_data[3])

        # Refresh recieving teams agenda
        team_category = utils.team.get_team_category(self.guild, recieving_team)

        await self.send_team_agenda(recieving_team, team_category)
    
    async def send_team_agenda(self, team_name, team_category):
        """
        Sends a new team agenda for the given team using data from the database
        """      
        agenda_channel = discord.utils.get(team_category.channels, name="agenda")

        scheduled_matches_data = self.dbinter.get_scheduled_matches()
        blocked_slots_data = self.dbinter.get_teams_blocked_slots(team_name)
        
        #Create empty agenda data
        agenda_data = {}
        for day in scrim_scheduler_conifg.days:

            empty_day = []
            for time in scrim_scheduler_conifg.times[day]:
                empty_day.append(None)

            agenda_data[day] = empty_day
        
        # Add any scheduled matches to the agenda data
        for scheduled_match in scheduled_matches_data:
            team1 = scheduled_match[0]
            team2 = scheduled_match[1]
            match_day = scheduled_match[2]
            match_time = scheduled_match[3]

            if team1 != team_name and team2 != team_name:
                continue
            else:
                if team1 == team_name:
                    agenda_data[match_day][match_time] = team2
                elif team2 == team_name:
                    agenda_data[match_day][match_time] = team1
        
        # Add any blocked slots to the agenda data
        for blocked_slot in blocked_slots_data:
            blocked_day = blocked_slot[1]
            blocked_time = blocked_slot[2]
            agenda_data[blocked_day][blocked_time] = "Blocked"
    
        team_ranks = utils.team.get_team_ranks(self.guild)
        loading_emoji = discord.utils.get(self.guild.emojis, name="loading")

        embed = utils.ui.new_embed_template()
        embed.title = "Agenda"
        embed.description = "Type ``accept (code)`` to accept an invite\nType ``cancel (code)`` to cancel a scheduled match\nType ``unblock (code)`` to unblock a blocked time slot"

        for day in scrim_scheduler_conifg.days:
            for i in range(len(scrim_scheduler_conifg.times)):

                text = ["","",""]
                count = 0
                if agenda_data[day][i] is None:
                    
                    # Check if team has any invites for this time
                    recieved_invite = self.dbinter.get_recieved_invite_at_time(team_name, day, i)
                    if recieved_invite is not None:
                        # If there is an invite

                        sending_team_name = recieved_invite[1]
                        sending_team_multi = await utils.team.get_team_multi(utils.team.get_team_category(self.guild, sending_team_name))
                        sending_team_rank = '❔'
                        code = self.dbinter.get_invite_code(sending_team_name, recieved_invite[2], recieved_invite[3])

                        # Get the team rank emoji
                        if team_ranks[sending_team_name] is not None:
                            sending_team_rank = str(discord.utils.get(self.guild.emojis, name=team_ranks[sending_team_name].lower()))

                        # Create invite display
                        if sending_team_multi is not None:
                            # Format with multi
                            temp = text[count] + "`" + code + "` " + sending_team_rank + " - [__**" + sending_team_name + "**__](" + sending_team_multi + ")\n"
                            if len(temp) > 1024:
                                count += 1
                                text[count] = "`" + code + "` " + sending_team_rank + " - [__**" + sending_team_name + "**__](" + sending_team_multi + ")\n"
                            else:
                                text[count] = temp
                        else:
                            # Format without multi
                            temp = text[count] + "`" + code + "` " + sending_team_rank + " - __**" + sending_team_name + "**__\n"
                            if len(temp) > 1024:
                                count += 1
                                text[count] = "`" + code + "` " + sending_team_rank + " - __**" + sending_team_name + "**__\n"
                            else:
                                text[count] = temp
                    else:
                        # If no invites
                        text[0] = "None"

                    embed.add_field(name=scrim_scheduler_conifg.days[day] + " " + scrim_scheduler_conifg.times[day][i] + " " + str(loading_emoji),value=text[0])
                    if len(text[1]) != 0:
                        embed.add_field(name="** **",value=text[1])
                    else:    
                        embed.add_field(name="** **",value="** **")
                    if len(text[2]) != 0:
                        embed.add_field(name="** **",value=text[2])
                    else:    
                        embed.add_field(name="** **",value="** **")
                elif agenda_data[day][i] == "Blocked":
                    # If the slot is blocked
                    code = self.dbinter.get_invite_code(team_name, day, i)
                    embed.add_field(name=scrim_scheduler_conifg.days[day] + " " + scrim_scheduler_conifg.times[day][i] + " ❌",value="`" + code + "` - **Blocked**")
                    embed.add_field(name="** **",value="** **")
                    embed.add_field(name="** **",value="** **")
                else:
                    # If the slot has a scheduled match

                    scheduled_team_name = agenda_data[day][i]
                    scheduled_team_multi = await utils.team.get_team_multi(utils.team.get_team_category(self.guild, scheduled_team_name))
                    code = self.dbinter.get_invite_code(scheduled_team_name, day, i)

                    # Get rank
                    scheduled_team_rank = '❔'
                    if team_ranks[scheduled_team_name] is not None:
                        scheduled_team_rank = str(discord.utils.get(self.guild.emojis, name=team_ranks[scheduled_team_name].lower()))

                    # Get multi and format value
                    if scheduled_team_multi is not None:
                        temp = "`" + code + "` " + scheduled_team_rank + " " + "[__**" + scheduled_team_name + "**__](" + scheduled_team_multi + ")"
                    else:
                        temp = "`" + code + "` " + scheduled_team_rank + " - __**" + scheduled_team_name + "**__"

                    embed.add_field(name=scrim_scheduler_conifg.days[day] + " " + scrim_scheduler_conifg.times[day][i] + " ✅",value=temp)
                    embed.add_field(name="** **",value="** **")
                    embed.add_field(name="** **",value="** **")

        await agenda_channel.purge()
        message = await agenda_channel.send(embed=embed)
        self.dbinter.replace_team_agenda(team_name, message.id)


    async def send_lfscrim(self):
        """
        Sends the #lfscrim channels available scrim menu
        """
        categories = self.guild.categories
        scheduled_matches = self.dbinter.get_scheduled_matches()
        blocked_slots = self.dbinter.get_blocked_slots()

        # Create empty team agendas
        team_agendas = {}

        empty_agenda = {}
        for day in scrim_scheduler_conifg.days:
            time_slot_list = []
            for time in scrim_scheduler_conifg.times[day]:
                time_slot_list.append(None)
            empty_agenda[day] = time_slot_list

        teams = utils.team.get_teams(self.guild)
        
        for team in teams:
            team_agendas[team[0]] = copy.deepcopy(empty_agenda)

        # Add the scheduled matches to the agendas
        for scheduled_match in scheduled_matches:
            team1 = scheduled_match[0]
            team2 = scheduled_match[1]
            match_day = scheduled_match[2]
            match_time = scheduled_match[3]

            team_agendas[team1][match_day][match_time] = team2
            team_agendas[team2][match_day][match_time] = team1
        
        # Add blocked slots to the agenda
        for blocked_slot in blocked_slots:
            team_agendas[blocked_slot[0]][blocked_slot[1]][blocked_slot[2]] = "Blocked"

        # Create and send the embed
        team_emojis = utils.team.get_team_emojis(self.guild)
        team_ranks = utils.team.get_team_ranks(self.guild)
        embed = utils.ui.new_embed_template()
        embed.title = "Available Scrims"
        embed.description = "Type  a ``(code)`` to send invite\nType ``block (code)`` to block a time slot"
        
        channel = self.guild.get_channel(utils.ids.lf_scrim_channel)
        await channel.purge() # Delete all old messages

        count = 0
        for team in team_agendas:
            
            # Create new page every 24 teams
            if count == 24:
                count = 0
                await channel.send(embed=embed)
                embed = utils.ui.new_embed_template()
                embed.description = "Type  a ``(code)`` to send invite\nType ``block (code)`` to block a time slot"
            
            # Get the team rank emoji
            if team_ranks[team] is None:
                rank_emoji = '❔'
            else:
                rank_emoji = str(discord.utils.get(self.guild.emojis, name=team_ranks[team].lower()))

            # Get the teams multi
            team_category = utils.team.get_team_category(self.guild, team)
            multi_link = await utils.team.get_team_multi(team_category)
            if multi_link is not None:
                formatted_agenda = rank_emoji + " - [__**" + team + "**__](" + multi_link + ")\n"
            else:
                formatted_agenda = rank_emoji + " - __**" + team + "**__\n"

            # Build the embed field value
            for day in team_agendas[team]:
                for i in range(len(team_agendas[team][day])):
                    code = self.dbinter.get_invite_code(team, day, i)
                    time_slot = team_agendas[team][day][i]
                    time_slot_name = scrim_scheduler_conifg.day_codes[day] + ' ' + scrim_scheduler_conifg.times[day][i]
                    if time_slot is None:
                        formatted_agenda = formatted_agenda + "`" + code + "` - " + time_slot_name + "\n"

            embed.add_field(name="** **", value = formatted_agenda)
            count += 1

        await channel.send(embed=embed)
    
    async def add_team(self, team_name, team_category):
        """
        Adds a team into the scrim scheduler
        """
        # Assign new codes to team
        codes = self.get_random_codes()

        count = 0
        for day in scrim_scheduler_conifg.days:
            for i in range(len(scrim_scheduler_conifg.times[day])):
                # Loop until a non used code is found
                while (True):
                    if self.dbinter.get_invite_from_code(codes[count]) is None:
                        self.dbinter.insert_invite_code(codes[count], team_name, day, i)
                        count+=1
                        break
                    else:
                        count+=1
        
        # Send lf scrim and agenda menus
        await self.send_team_agenda(team_name, team_category)
        await self.send_lfscrim()
    
    async def remove_team(self, team_name):
        """
        Removes a team from the scrim scheduler
        """
        team_matches = self.dbinter.get_scheduled_matches_for_team(team_name)
        team_sent_invites = self.dbinter.get_ALL_invites_sent_by_team(team_name)

        # Get set of teams that were affected by the removal
        affected_teams = set()
        for sent_invite in team_sent_invites:
            affected_teams.add(sent_invite[0])
        for scheduled_match in team_matches:
            if scheduled_match[0] == team_name:
                affected_teams.add(scheduled_match[1])
            else:
                affected_teams.add(scheduled_match[0])
        
        # Remove teams data in scrim scheduler
        self.dbinter.delete_invites_involving_team(team_name)
        self.dbinter.delete_scheduled_matches_involving_team(team_name)
        self.dbinter.delete_teams_blocked_slots(team_name)
        self.dbinter.delete_team_agenda_id(team_name)
        self.dbinter.delete_teams_invite_codes(team_name)

        # Refresh all affected menus
        for affected_team in affected_teams:
            await self.send_team_agenda(affected_team, utils.team.get_team_category(self.guild, affected_team))
        await self.send_lfscrim()

    def assign_invite_codes(self):
        """
        Assigns random invite codes to teams and time slots
        """
        self.dbinter.delete_all_invite_codes() # Remove old codes

        teams = utils.team.get_teams(self.guild)
        codes = self.get_random_codes()        

        count = 0
        for team in teams:
            for day in scrim_scheduler_conifg.days:
                for i in range(len(scrim_scheduler_conifg.times[day])):
                    self.dbinter.insert_invite_code(codes[count], team[0], day, i)
                    count += 1

    def get_random_codes(self):
        """
        Generates a list of random 3 letter codes
        """
        codes = []
        val1 = 'A'
        val2 = 'A'
        val3 = 'A'

        while True:
            codes.append(val1+val2+val3)
            #Increment code
            if val2 == 'Z' and val3 == 'Z':
                if val1 == 'Z':
                    break
                val1 = chr(ord(val1) + 1)
                val2 = 'A'
                val3 = 'A'
            elif val3 == 'Z':
                val2 = chr(ord(val2) + 1)
                val3 = 'A'
            else:
                val3 = chr(ord(val3) + 1)
        
        random.shuffle(codes)

        return codes