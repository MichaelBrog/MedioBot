import discord
import asyncio
import random
import re
import datetime
from datetime import datetime, timedelta
from discord.ext import commands
import sqlite3
import math
import time


class tags:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def taglist(self, ctx):
        await ctx.send("!roll, !8ball, !whoami !say, !hello, !allowance, !tag, !slots")

    @commands.command()
    async def createtable(self, ctx):
        if ctx.author.id != 449222204534816768:
            return
        self.bot.execute(
            # f'''CREATE TABLE slotTable (PRIMARY KEY (guild_id, user_Id), allowenceTime, coinCount, homecity)''')
            '''CREATE TABLE IF NOT EXISTS slotMachine (
                guild_id BIGINT,
                user_id BIGINT,
                last_used DATETIME DEFAULT (datetime('now')),
                coin_count INTEGER DEFAULT 2500,
                home VARCHAR(50),
                PRIMARY KEY (guild_id, user_id)
            )'''
        )

        self.bot.conn.commit()
        await ctx.send("Table has been created")


    @commands.command()
    async def tag(self, ctx, modifier=None, entry=None, *, tagValue=None):
        #send error if the tag is too long
        #make blacklist
        #allow command to be disabled 
        if entry in Black_listed_tags:
            await ctx.send("This tag name is reserved.")
            return 
        tag_list_string = ""
        if modifier == "list":
            self.bot.c.execute(f"SELECT tag_name FROM tags WHERE tag_name = ? AND guild_id = ? ", ("*", ctx.guild.id))
            tag_list = self.bot.c.fetchone()
            if tag_list is None:
                return 
            while tag_list.fetchone() is not None:
                tag_list_string += "\n" + tag_list[0]
                
            await ctx.send(tag_list_string)
        #if self.bot.cogs.MeChecker.__local_check(ctx):
         #   await ctx.send("it worked")
          #  return

        modifi = modifier
        if modifi != "+" and modifi != "a" and modifi != "e":
            await ctx.send("After !tag, use either +, a or e. Use 'tag help' for to see the proper format.")
            return
        if entry is None:
            await ctx.send("Input required after {modifi}. Use 'tag help' for to see the proper format.")
            return

        self.bot.c.execute(
                f"SELECT tag_content FROM tags WHERE tag_name = ? AND guild_id = ? ", (entry, ctx.guild.id) )
        tag_contents = self.bot.c.fetchone()
        if tag_contents is None and modifi == "+":
            self.bot.c.execute(f"INSERT OR IGNORE INTO tags (guild_id, tag_name, tag_content, date_created, author ) VALUES(?, ?, ?, ?, ?)", (ctx.guild.id, entry, tagValue, datetime.utcnow(), ctx.author.id))
            self.bot.conn.commit()
            return
        if tag_contents is None and modifier == "a" or modifier == "b":
            await ctx.send("There exists a tag with the name {entry} already, use 'tag help' if you are unsure how to use the tag.")
            return
        if modifi == "a":
            appender = tag_contents + tagValue
            self.bot.c.execute(
                f"UPDATE tags SET tag_content = ? WHERE guild_id = ? AND tag_name = ? ", (appender, ctx.guild.id, entry))
            await ctx.send("The tag has been appended.")
            return
        if modifi == "e":
            #this is where we edit?? the tag
            return
        else:
            await ctx.send("There exists no tag with that name, you cannot append a nonexistant tag. Use 'tag help'  ")
            print(self.bot.c.fetchone())


    @commands.command()
    async def tagget(self, ctx, *, content):
        
        self.bot.c.execute(
            f"SELECT tag_content FROM tags WHERE tag_name = ? AND guild_id = ? ", (content, ctx.guild.id))
        something = self.bot.c.fetchone()
        if something is None:
            return
        else:
            await ctx.send(something[0])

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, module: str):
        if ctx.author.id != 449222204534816768:
            return
        #if not self.bot.__local_check:
            #return
        """Reloads a module."""
        e = discord.Embed(title="Unloading...", color=0xffff8c)
        msg = await ctx.send(embed=e)
        if not module.startswith("cogs."):
            module = f"cogs.{module}"
        self.bot.unload_extension(module)
        try:
            self.bot.load_extension(module)
        except Exception as error:
            e.title = f"<:redtick:318044813444251649> Could not load module {module}"
            err = f"{type(error).__name__!s}: {error}"
            e.description = err
            e.colour = 0xff8c8c
            await msg.edit(embed=e)
        else:
            e.colour = 0x8cffa4
            e.title = f"<:greentick:318044721807360010> Successfully reloaded {module!s}"
            await msg.edit(embed=e)

   # def fetchval(self):
        #row = c.fetchone()
     #   return row if row is None else row[0]


Black_listed_tags = [
    "tag",
    "8ball",
    "info",
    "roll",
    "whoami",
    "say",
    "hello,"
    "allowance",
    "slots",
    "givemoney",
]



def setup(bot):
    bot.add_cog(tags(bot))
