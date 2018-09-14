import discord
from discord.ext import commands

class commands:
    def __init__(self, bot):
        self.bot = bot

    tag_list = ["!roll", "!8ball", "!whoami"]

    @commands.command()
    async def whoami():
        await client.send_message(message.channel, 'ur a little bitch')

    @commands.command()
    async def roll():
        retnum = random.randint(1,6)
        await client.send_message(message.channel, 'you rolled a: {}'.format(retnum))

    @commands.command(name="8ball")
    async def eightball():
        await client.send_message(message.channel, random.choice(eight_ball_responses))

def setup(bot):
    bot.add_cog(commands(bot))