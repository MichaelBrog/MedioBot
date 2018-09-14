import discord
import asyncio
import random
import pickle 
import os
from discord.ext import commands

class settings:
    def __init__(self):
        self.bot = bot

    taglist = ["roll", "8ball", "help", "test", "whoami"]


def setup(bot):
    bot.add_cog(settings(bot))