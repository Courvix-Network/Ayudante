import discord
from discord.ext import commands
import json
from discord.ext.commands import CheckFailure
from datetime import datetime


class Admin(commands.Cog):
    """
        A module of commands to manage the bot
    """
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def generate_ping_report(time, member, amount) -> str:
        return f"**Ping Report**\nTime taken: {time}\nMember pinged: {member}\nAmount of times pinged: {amount}"

    @commands.command()
    @commands.has_any_role(815266964238630952)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx, to_ping: discord.Member, amount: int):
        await ctx.message.delete()
        endamount: int = amount
        if amount > 5 or amount < 1:
            await ctx.author.send("That's too many or too little pings! Range of 1 - 5")
            return None
        else:
            start: datetime = datetime.now()
            while amount > 1:
                message: discord.Message = await ctx.send(f"{to_ping.mention}")
                await message.delete()
                amount -= 1
            report = self.generate_ping_report(datetime.now()-start, to_ping, endamount)
            await ctx.author.send(report)


def setup(bot):
    bot.add_cog(Admin(bot))