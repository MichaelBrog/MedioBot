import random
import discord
from discord.ext import commands
import asyncio


class random:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def whoami(self, ctx, user: discord.Member = None):
        await ctx.send(f"You are {user.name}")

    @commands.command()
    async def addbot(self, ctx):
        await ctx.send("https://discordapp.com/oauth2/authorize?&client_id=459782673305436161&scope=bot&permissions=0")

    @commands.command()
    async def roll(self, ctx, *, diceCount=None):
        if diceCount is None:
            retnum = random.randint(1, 6)
            return await ctx.send('You rolled: {}'.format(retnum))
        if "d" not in diceCount:
            return await ctx.send('Error: Incorrect format, please use the following format \n #dice d #faces')
        try:
            diceNum, diceFace = [x.strip() for x in diceCount.split("d")]
        except:
            return await ctx.send('Error: Incorrect format, please use the following format \n #dice d #faces \n The amount of dice should be less than 1000, and the number of faces should be less than 5000.')
        try:
            diceNum = int(diceNum)
        except:
            return await ctx.send("One of your values was not an integer: {}".format(diceNum))
        try:
            diceFace = int(diceFace)
        except:
            return await ctx.send("One of your values was not an integer: {}".format(diceFace))
        if diceNum > 1000 or diceFace > 5000:
            return await ctx.send('Error: The amount of dice should be less than 1000, and the number of faces should be less than 5000.')
        diceTot = diceNum * diceFace
        roll = random.randint(diceNum, diceTot)
        await ctx.send('you rolled: {}'.format(roll))

    @commands.command(name="8ball")
    async def eightball(self, ctx, message=None):
        if message is None:
            return
        await ctx.send(random.choice(eight_ball_responses))

    @commands.command()
    async def say(self, ctx, *, words: commands.clean_content):
        sender = words
        channel = self.bot.get_channel(ctx)
        await channel.send(sender)

    @commands.command()
    async def info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        try:
            avatar = user.avatar_url
        except:
            avatar = user.default_avatar_url
        joined_at = user.joined_at.strftime("%Y-%m-%d\n%H:%M:%S")
        created = user.created_at.strftime("%Y-%m-%d\n%H:%M:%S")
        usercolor = user.color

        roles = '\n'.join(x.name for x in user.roles)

        em = discord.Embed(title=None, description=None, colour=usercolor)
        em.set_author(name=user.name, icon_url=user.avatar_url,
                      url=user.avatar_url.replace(".webp", ".png"))
        em.add_field(name="Name", value="{}#{}".format(
            user.name, user.discriminator), inline=True)
        em.add_field(name="ID:", value="{}".format(user.id))
        em.add_field(name="Roles:", value="{}".format(roles))
        em.add_field(name="join date", value="{}".format(joined_at))
        em.add_field(name="creation date", value="{}".format(created))
        await ctx.send(embed=em)

eight_ball_responses = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
]

def setup(bot):
    bot.add_cog(random(bot))