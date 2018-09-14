class help:
    def __init__(self, bot):
        self.bot = bot
        mod_cog = self.bot.get_cog('moderation')


   @commands.command()
    async def help(self, ctx, modifier=None, entry=None):
        #tags
        #slots all of them go here 

        #enable/disable
        #ban/kick/etc

        #info

        #8bal 


















def setup(bot):
    bot.add_cog(slots(help))