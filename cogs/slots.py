import discord
import asyncio
import random
import re
import urllib.request
import json
import datetime
from datetime import datetime, timedelta
from discord.ext import commands
import sqlite3
import math
import time

class slots:
    def __init__(self, bot):
        self.bot = bot
        mod_cog = self.bot.get_cog('moderation')

    def checker(self, ctx):
        mediocreBot.c.execute(f"INSERT OR IGNORE INTO is_tag_enabled (guild_id, slots) VALUES(?, ?)", (server.id, "slots"))
        self.bot.c.execute(
            f"SELECT coin_count FROM is_tag_enabled WHERE tag_name = 'slots' AND guild_id = '{ctx.guild.id}' ")
        if self.bot.c.fetchone() is None:
            return True
        if self.bot.c.fetchone()[0] == 1:
            return 


    def timeDoer(self, time_now, last_time_used):
        
        totaltime = last_time_used - time_now

        minutes, seconds = divmod(int(totaltime.total_seconds()), 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return ("You have already used your allowance. You have: {} hours and {} minutes and {} seconds left until your next one.".format(hours, minutes, seconds))
        if minutes:
            return ("You have already used your allowance. You have: {} minutes and {} seconds left until your next one.".format(minutes, seconds))
        else:
            return ("You have already used your allowance. You have: {} seconds left until your next one.".format(seconds))


    @commands.command()
    async def allowance(self, ctx, *, betCount=None, user: discord.Member = None):
        mod_cog = self.bot.get_cog('moderation')
        if mod_cog.enable_checker(ctx, "allowance"):
            await ctx.send("Tag has been disabled.")
            return 
        
        self.bot.c.execute(
        f"SELECT last_used FROM slotMachine WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
        last_time_used = datetime.strptime(str(self.bot.c.fetchone()[0]), '%Y-%m-%d %H:%M:%S')#self.bot.c.fetchone()[0]#time.strptime#self.bot.c.fetchone()[0]#datetime.strptime(str(self.bot.c.fetchone()[0]), '%Y-%b-%d %I:%M%S')#self.bot.c.fetchone()[0]#
        time_now = datetime.utcnow() - timedelta(hours=24)
        if last_time_used > time_now:
            await ctx.send(self.timeDoer(time_now, last_time_used))
            return
        else:

            try:
                self.bot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id, last_used, coin_Count, home) VALUES(?, ?, ?, ?, ?)", (
                    ctx.guild.id, ctx.author.id, datetime.utcnow(), 0, 0))
                self.bot.conn.commit()

                self.bot.c.execute(
                    f"SELECT coin_count FROM slotMachine WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
                allowance = int(self.bot.c.fetchone()[0])
                allowance += 1500
                self.bot.c.execute(
                    f"UPDATE slotMachine SET coin_count ='{allowance}' WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
                self.bot.c.execute(
                    f"UPDATE slotMachine SET last_used = (datetime('now')) WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")

                await ctx.send("Your allowance is 1500 coins. Your current balance is: {}".format(allowance))
                self.bot.conn.commit()

            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                self.bot.execute(
                    f"SELECT coin_count FROM slotMachine WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
                allowance = self.bot.c.fetchone()
                await ctx.send("Could not add to your allowance")
                await ctx.send("Your allowance is 1500 coins. Your current balance is: {}".format(allowance))


    @commands.command()
    async def slots(self, ctx, *, betCount=None):
        mod_cog = self.bot.get_cog('moderation')
        if mod_cog.enable_checker(ctx, "slots"):
            await ctx.send("Tag has been disabled.")
            return  

        self.bot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id) VALUES(?, ?)", (ctx.guild.id, 999999))
        self.bot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id) VALUES(?, ?)", (ctx.guild.id, ctx.author.id))
        self.bot.conn.commit()
        try:
            betCount = int(betCount)
        except:
            return await ctx.send("Your betcount was not an integer: {}".format(betCount))
        self.bot.c.execute(
            f"SELECT coin_count FROM slotMachine WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
        coinCount = int(self.bot.c.fetchone()[0])
        if betCount > coinCount:
            return await ctx.send("Your betcount: {} was higher than your total number of coins:{}. Please choose a lower value.".format(betCount, coinCount))
 
        slotMachine1 =  random.sample(slot_machine_choices, 3)
        slotMachine2 =  random.sample(slot_machine_choices, 3)
        slotMachine3 =  random.sample(slot_machine_choices, 3)
        slot_string = f"{slotMachine1[0]} : {slotMachine2[0]} : {slotMachine3[0]}\n{slotMachine1[1]} : {slotMachine2[1]} : {slotMachine3[1]}:arrow_left:\n{slotMachine1[2]} : {slotMachine2[2]} : {slotMachine3[2]}\n"
        prizemoney = 0
        wintype = "n"
        if slotMachine1[1] == slotMachine2[1] and slotMachine2[1] == slotMachine3[1]:
            if slotMachine1[1] == ":seven:":
                wintype = "J"
            if slotMachine1[1] == ":gem:":
                prizemoney = betCount * 20
                wintype = "W"
            if slotMachine1[1] == ":apple:":
                prizemoney = betCount * 10
                wintype = "W"
            if slotMachine1[1] == ":cherries:":
                prizemoney = betCount * 6
                wintype = "W"
            if slotMachine1[1] == ":grapes:":
                prizemoney = betCount * 4.5
                wintype = "W"
            if slotMachine1[1] == ":moneybag:":
                prizemoney = betCount * 4
                wintype = "W"
            if slotMachine1[1] == ":moneybag:":
                prizemoney = betCount * 4
                wintype = "W"
            if slotMachine1[1] == ":bell:":
                prizemoney = betCount * 2.5
                wintype = "W"
            if slotMachine1[1] == ":bell:":
                prizemoney = betCount * 2.5
                wintype = "W"

        self.bot.c.execute(
                f"SELECT coin_count FROM slotMachine WHERE user_id = '999999' AND guild_id = '{ctx.guild.id}' ")
        jackpot = int(self.bot.c.fetchone()[0])
        jackpot += betCount

        if wintype == "n":
            slotMessage = "You didn't win anything!"
            jackpot_msg= "The jackpot is: {}".format(jackpot)
            self.bot.c.execute(
                f"UPDATE slotMachine SET coin_count = '{jackpot}' WHERE user_id = '999999' AND guild_id = '{ctx.guild.id}' ")
        if wintype == "W":
            self.bot.c.execute(
                    f"SELECT coin_count FROM slotMachine WHERE user_id = '999999' AND guild_id = '{ctx.guild.id}' ")
            jackpot = int(self.bot.c.fetchone()[0])
            jackpot += betCount
            jackpot_msg= "The jackpot is: {}".format(jackpot)
            slotMessage = "You won: {}!!!".format(prizemoney)
            self.bot.c.execute(
                    f"UPDATE slotMachine SET coin_count = '{jackpot}' WHERE user_id = '999999' AND guild_id = '{ctx.guild.id}' ")

        if wintype == "J":
            prizemoney = jackpot
            self.bot.c.execute(
                    f"UPDATE slotMachine SET coin_count ='0' WHERE user_id = '999999' AND guild_id = '{ctx.guild.id}' ")
            jackpot_msg = "The jackpot was: {}".format(jackpot)
            slotMessage = f"You won the jackpot!!! of {jackpot}"


        final_coin_count = coinCount - betCount + prizemoney
        self.bot.c.execute(
                    f"UPDATE slotMachine SET coin_count ='{final_coin_count}' WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
        
        self.bot.conn.commit()
        await ctx.send(f":slot_machine: **SLOTS** :slot_machine:\n"+
                        f"===========\n :gem: {jackpot} \n"+
                        "===========\n"
                        f"{slot_string}"+
                        f"===========\n" +
                        f"{slotMessage}\n" +
                        f"===========\n" +
                        f"You lost {betCount} coins.")


    @commands.command()
    async def balance(self, ctx):
        mod_cog = self.bot.get_cog('moderation')
        if mod_cog.enable_checker(ctx, "balance"):
            await ctx.send("Tag has been disabled.")
            return 
        self.bot.c.execute(
                f"SELECT coin_count FROM slotMachine WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
        coincount = int(self.bot.c.fetchone()[0])
        await ctx.send(f"Your current number of coins is: {coincount}")

    @commands.command()
    async def givemoney(self, ctx, user: discord.Member = None, *, giveCount=None):
        mod_cog = self.bot.get_cog('givemoney')
        if mod_cog.enable_checker(ctx, "givemoney"):
            await ctx.send("Tag has been disabled.")
            return 
        if user is None:
            await ctx.send("Please pick a user to give money to.")
            return
        if giveCount is None:
            await ctx.send("Please insert an amount to give the user.")
            return
        try:
            giveCount = int(giveCount)
        except:
            await ctx.send("The value given was not an integer.")
            return
        self.bot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id) VALUES(?, ?)", (ctx.guild.id, ctx.author.id))
        self.bot.c.execute(f"INSERT OR IGNORE INTO slotMachine (guild_id, user_id) VALUES(?, ?)", (ctx.guild.id, user.id))
        self.bot.c.execute(
                f"SELECT coin_count FROM slotMachine WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")
        coinGiver_money = int(self.bot.c.fetchone()[0])

        if coinGiver_money < giveCount:
            await ctx.send("You are trying to give more money than you have, pick a smaller number.")
            return
        
        author_Money = coinGiver_money - giveCount
        self.bot.c.execute(
                f"UPDATE slotMachine SET coin_count ='{author_Money}' WHERE user_id = '{ctx.author.id}' AND guild_id = '{ctx.guild.id}' ")

        self.bot.c.execute(
            f"SELECT coin_count FROM slotMachine WHERE user_id = '{user.id}' AND guild_id = '{ctx.guild.id}' ")
        coinGet = int(self.bot.c.fetchone()[0])
        author_username = ctx.author.display_name.replace("@", "\u200b@")
        reciever_username = user.display_name.replace("@", "\u200b@")
        coinGiver = coinGet + giveCount
        self.bot.c.execute(
                f"UPDATE slotMachine SET coin_count ='{coinGiver}' WHERE user_id = '{user.id}' AND guild_id = '{ctx.guild.id}' ")
        self.bot.conn.commit()
        await ctx.send(f"{author_username} gave: {giveCount} to {reciever_username}")
        

        
    #command to reset command
    #command to change users money
    #command to change the jackpot

    
slot_machine_choices = [
    ":cherries:",
    ":moneybag:",
    ":gem:",
    ":seven:",
    ":moneybag:",
    ":apple:",
    ":grapes:",
    ":bell:",
    ":bell:",
]


def setup(bot):
    bot.add_cog(slots(bot))

