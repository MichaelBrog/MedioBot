import discord
import asyncio
import random
import pickle 
import os
import copy
import sqlite3
import datetime
from datetime import datetime, timedelta


client = discord.Client()

from discord.ext import commands

INITIAL_EXTENSIONS = [
    'cogs.tags',
    'cogs.moderation',
    'cogs.slots',
    'cogs.random',
    'cogs.MeChecker',
]

class mediocreBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}n{} {}'.format(
                    extension, type(e).__name__, e))
        mediocreBot.conn = sqlite3.connect("UserInfo.db", detect_types=sqlite3.PARSE_DECLTYPES)
        mediocreBot.c = mediocreBot.conn.cursor()
        

    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        if ctx.guild is None:
            return await ctx.send('PM commands are disabled currently')
        await self.process_commands(message)
        ctx = await self.get_context(message)
        if ctx.invoked_with and ctx.invoked_with.lower() not in self.commands and ctx.command is None:
            msg = copy.copy(message)
            if ctx.prefix:
                new_content = msg.content[len(ctx.prefix):]
                msg.content = "{}tagget {}".format(ctx.prefix, new_content)
                await self.process_commands(msg)

    async def on_guild_join(self, ctx, guild):
        self.table_maker()
        x = ctx.guild.members
        for member in x:
            if member.bot:
                continue
            mediocreBot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id) VALUES(?, ?)", (ctx.guild.id, member.id))
            mediocreBot.conn.commit()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.table_maker()
        for server in self.guilds:
            x = server.members
            for member in x:
                if member.bot:
                    continue
                mediocreBot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id) VALUES(?, ?)", (server.id, member.id))
                mediocreBot.conn.commit()

    async def on_member_join(self, ctx, guild):
        mediocreBot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id) VALUES(?, ?)",
                    (guild.id, ctx.user.id))
        mediocreBot.conn.commit()

    async def on_message_delete(self, ctx, guild):
        #check if enabled
        #check if there exists an output channel
        #check if output channel hasn't been deleted
        await ctx.send(ctx.message)
        
    async def on_message_edit(self, ctx, guild):
        pass

    def table_maker(self):
        mediocreBot.c.execute(
            '''CREATE TABLE IF NOT EXISTS slotMachine (
                guild_id BIGINT,
                user_id BIGINT,
                last_used DATETIME DEFAULT (datetime('now')),
                coin_count INTEGER DEFAULT 2500,
                home VARCHAR(50),
                PRIMARY KEY (guild_id, user_id)
            )'''
        )
        mediocreBot.c.execute(
            '''CREATE TABLE IF NOT EXISTS tags (
                guild_id BIGINT,
                tag_name VARCHAR(100),
                tag_content VARCHAR(100),
                date_created DATETIME DEFAULT (datetime('now')),
                author INTEGER DEFAULT 2500,
                NSFW_Only INT DEFAULT 0,
                admin_edit_only INT DEFAULT 0,
                PRIMARY KEY (guild_id, tag_name)
            )'''
        )
        mediocreBot.c.execute(
            '''CREATE TABLE IF NOT EXISTS is_tag_enabled (
                guild_id BIGINT,
                tag_name VARCHAR(100),
                enabled INT DEFAULT 1,
                enabled_one_channel VARCHAR(100),
                channel_id INTEGER DEFAULT 2500,
                PRIMARY KEY (guild_id, tag_name)
            )'''
        )
        mediocreBot.conn.commit()

    def run(self):
        super().run("NDU5NzgyNjczMzA1NDM2MTYx.DhANyg._54mo4GhDelzhzpDFGh9XdEJ0WM", reconnect=True)

if __name__ == '__main__':
    mediocrebot = mediocreBot()
    mediocrebot.run()
    mediocreBot.conn = sqlite3.connect("UserInfo.db", detect_types=sqlite3.PARSE_DECLTYPES)
    mediocreBot.c = mediocreBot.conn.cursor()