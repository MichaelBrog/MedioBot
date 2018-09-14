import discord
from discord.ext import commands

class moderation:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def kick(self, ctx, user: discord.Member = None):
        if not ctx.author.guild_permissions.administrator: #or is on the whitelist
            return
        
        await user.kick()
        await ctx.send(f"User: {ctx.user.id} has been kicked")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, user: discord.Member = None):
        if not ctx.author.guild_permissions.administrator: #or is on the whitelist
            return
        await user.ban()
        await ctx.send(f"User: {ctx.user.id} has been banned")

    @commands.command()
    async def enable(self, ctx, *, tag_tbe=None):
        if tag_tbe is None:
            return
        if not ctx.author.guild_permissions.administrator: #or on whitelist?
            return
        if tag_tbe not in Black_listed_tags:
            await ctx.send("Tag selected cannot be enabled or disabled.")
            return
        self.bot.c.execute(f"INSERT OR IGNORE INTO is_tag_enabled (guild_id, tag_name) VALUES(?, ?)", (ctx.guild.id, tag_tbe))
        self.bot.conn.commit()
        self.bot.c.execute(
            f"UPDATE is_tag_enabled SET enabled = 1 WHERE tag_name = ? AND guild_id = ? ", (tag_tbe, ctx.guild.id))
        self.bot.conn.commit()
        
        await ctx.send("Tag has been enabled")
        
    @commands.command()
    async def disable(self, ctx, *, tag_tbe=None):
        if tag_tbe is None:
            return
        if not ctx.author.guild_permissions.administrator: #or on whitelist?
            return
        if tag_tbe not in Black_listed_tags:
            await ctx.send("Tag selected cannot be enabled or disabled.")
            return
        self.bot.c.execute(f"INSERT OR IGNORE INTO is_tag_enabled (guild_id, tag_name) VALUES(?, ?)", (ctx.guild.id, tag_tbe))
        self.bot.conn.commit()
        self.bot.c.execute(
            f"UPDATE is_tag_enabled SET enabled = 0 WHERE tag_name = ? AND guild_id = ? ", (tag_tbe, ctx.guild.id))
        self.bot.conn.commit()
    
        await ctx.send(f"Tag: {tag_tbe} has been disabled")

    def enable_checker(self, ctx, name_tag=None):
        #await ctx.send("it got to the command")
        self.bot.c.execute(f"INSERT OR IGNORE INTO is_tag_enabled (guild_id, tag_name) VALUES(?, ?)", (ctx.guild.id, name_tag))
        self.bot.conn.commit()
        self.bot.c.execute(
            f"SELECT enabled FROM is_tag_enabled WHERE guild_id = ? AND tag_name = ? ", (ctx.guild.id, name_tag))
        enableValue = self.bot.c.fetchone()
        #eturn enableValue
        if enableValue is None:
            return False
        if enableValue[0] == 1:
            return False
        else:
            return True



Black_listed_tags = [
    "tag",
    "8ball",
    "info",
    "roll",
    "whoami",
    "say",
    "hello",
    "allowance",
    "slots",
    "givemoney",
    "enable",
    "disable",
]







#figure out permissions
#make a whitelist for tags
#make softban
#change nickname tag
#make a mute role
#pick a mute role
#mute a person


#one day
#purge last 100 messages
#purge bot messages
#purge specifc messages by a user
#purge messages by type


#create a modlog
#pick a channel as the modlog
#create a table for banned users
#enable editing of banned reason 
#log events, avatar change, edits, role changes, deletes, bans, joins, name changes, 
#make a bot ignore messages from a channel
#makes the bot unignore messages from a channel

#disable tags
#enable tags
#disable mod commands
#make a black list 
#ban user from using bot

#greeting message
#farewell message
#ban message
#dm on join message

def setup(bot):
    bot.add_cog(moderation(bot))