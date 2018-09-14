class MeChecker:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return ctx.author.id == 449222204534816768

def setup(bot):
    bot.add_cog(MeChecker(bot))