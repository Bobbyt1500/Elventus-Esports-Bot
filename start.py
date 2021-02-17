# Third party modules
import discord
import os
import asyncio
from dotenv import load_dotenv

# Commands
import commands.meeting as meeting
import commands.addteam as addteam
import commands.removeteam as removeteam
import commands.addchannel as addchannel
import commands.removechannel as removechannel
import commands.modmail as modmail
import commands.teammates as teammates

# Extras
import extras.addstarter as addstarter
import extras.removestarter as removestarter
import extras.chat_channel_handler as chat_channel_handler
import extras.gform_handler as gform_handler

import role_assign.role_assign as role_assign

import sqldb.general_dbinter

# Scrim scheduler
import sqldb.scheduler_dbinter
import scrim_scheduler.scrim_scheduler as scrim_scheduler

# Utilities
import utils.ids as ids

load_dotenv()


class Bot(discord.Client):

    async def on_ready(self):
        print("Online - Elventus Esports Bot")
        scheduler_dbinter = sqldb.scheduler_dbinter.DBInterface("sqldb/scrim_scheduler.db")
        self.scrim_scheduler = scrim_scheduler.Scrim_Scheduler(scheduler_dbinter, self.get_guild(ids.guild))

        self.general_dbinter = sqldb.general_dbinter.DBInterface("sqldb/general.db")

        print("Environment = "+ os.getenv("ENVIRONMENT"))

        # Only enable gform_task if credentials were provided
        if os.getenv("GOOGLE_CREDENTIALS") != "NONE":
            self.gform_task = self.loop.create_task(self.gform_task(self.get_guild(ids.guild)))
    
    async def gform_task(self, guild):
        while not self.is_closed():
            await gform_handler.update(guild)
            await asyncio.sleep(300)


    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return

        if self.general_dbinter.is_role_assign_id(payload.message_id):
            await role_assign.invite_handler(payload, self.guilds)
            return
        
    async def on_voice_state_update(self, member, before, after):
        await chat_channel_handler.activate(self.get_guild(ids.guild))

    async def on_member_update(self, before, after):
        guild = discord.utils.get(self.guilds, id=ids.guild)
        entries = await guild.audit_logs(limit=1).flatten()
        member = discord.utils.get(guild.members, id=entries[0].user.id)
        captain_role = discord.utils.get(guild.roles, id=ids.captain)
        moderator_role = discord.utils.get(guild.roles, id=ids.moderator)

        # Checks for a change in roles
        if before.roles != after.roles:

            # Prevents multiple color roles from being given out
            count = 0
            for role in after.roles:
                if "Elventus " in role.name and role.id not in ids.elventus_space:
                    count += 1

            if count > 1:
                await after.edit(roles=before.roles)
                return


            before_set = set(before.roles)
            after_set = set(after.roles)
            removed_roles = list(before_set.difference(after_set))
            added_roles = list(after_set.difference(before_set))

            # Prevent spying between teams by preventing people from giving out other color roles
            if captain_role in member.roles or moderator_role in member.roles:
                if len(added_roles) > 0:
                    if "Elventus " in added_roles[0].name and added_roles[0].id not in ids.elventus_space:
                        if member.id == after.id:
                            await after.edit(roles=before.roles)
                            return
                        if added_roles[0] not in member.roles:
                            await after.edit(roles=before.roles)
                            return

            # Update new players roles to starter roles
            if len(added_roles) > 0:
                await addstarter.activate(added_roles, after)

            # Remove old players starter roles
            if len(removed_roles) > 0:
                await removestarter.activate(removed_roles, after)

    async def on_message(self, message):
        split_message = message.content.split(" ")
        channel = message.channel
        guild = message.guild

        if isinstance(channel, discord.channel.DMChannel):
            # Dm channel handler

            # Make sure message isnt from bot
            if message.author.id != self.user.id:
                await modmail.activate(message, self.guilds)

        elif message.channel.name == "agenda":
            # Agenda commands handler

            # Commands require two arguments
            if len(split_message) != 2:
                return
            else:
                if split_message[0].lower() == "accept":
                    await self.scrim_scheduler.accept_invite(message, split_message[1].upper())

                if split_message[0].lower() == "cancel":
                    await self.scrim_scheduler.cancel_scrim(message, split_message[1].upper())

                if split_message[0].lower() == "unblock":
                    await self.scrim_scheduler.unblock_slot(message, split_message[1].upper())

        elif message.channel.id == ids.lf_scrim_channel:
            # Lf_scrim commands handler

            # Ignore messages from bot
            if message.author.id == self.user.id:
                return

            # Block command
            if split_message[0].lower() == "block":
                if len(split_message) != 2: return
                await self.scrim_scheduler.block_slot(message, split_message[1].upper())
                return

            # Invite sending, check that code is valid first
            if self.scrim_scheduler.dbinter.get_invite_from_code(message.content) is not None:
                await self.scrim_scheduler.send_invite(message.content.upper(), message.author)
                await message.delete()
                return
            else:
                await message.author.send("That is not a valid code")
                await message.delete()
                return
        else:
            # General commands handler

            if message.content == "^reset_scheduler":
                if message.author.id not in ids.admins:
                    await self.send_not_enough_perms_message(message)
                    return
                await self.scrim_scheduler.reset_scheduler()
            
            if message.content == "^refresh_scheduler":
                if message.author.id not in ids.admins:
                    await self.send_not_enough_perms_message(message)
                    return
                await self.scrim_scheduler.refresh_menus()
            
            if message.content == "^meeting":
                await meeting.activate(message)

            if split_message[0] == "^addteam":
                await addteam.activate(message, split_message, self.scrim_scheduler)

            if split_message[0] == "^removeteam":
                await removeteam.activate(message, split_message, self.scrim_scheduler)
            
            if split_message[0] == "^addteammate":
                await teammates.add_teammate(message, split_message)
            
            if split_message[0] == "^removeteammate":
                await teammates.remove_teammate(message, split_message)

            

            if split_message[0] == "^addchannel":
                await addchannel.activate(message, split_message)

            if message.content == "^removechannel":
                await removechannel.activate(message)

            if message.content == "^update_role_assign":
                if message.author.id not in ids.admins:
                    return
                await role_assign.send_menus(message, self.general_dbinter)

    async def send_not_enough_perms_message(self, message):
        await message.channel.send("You have to get to a higher mountain before you can do that! (Not enough permissions)")


intents = discord.Intents.default()
intents.members = True

client = Bot(intents=intents)
client.run(os.getenv("TOKEN"))