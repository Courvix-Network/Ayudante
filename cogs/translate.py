import discord
import requests
from discord.ext import commands
from utils.vars import *


class Translate(commands.Cog):
    """
        Translate functionality of the bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def translate(self, ctx, language_to, *, text=None):
        """
            Translate messages! Usages:
            .translate <language_to> <text>
            (in reply to a message) .translate <language_to>
        """
        with ctx.typing():
            if not text:
                if ctx.message.reference is not None:
                    text = await ctx.fetch_message(ctx.message.reference.message_id)
                    text = text.content
                else:
                    await ctx.send("⚠ ️Please supply the text you would like to translate!")
                    return None
            request = requests.post("https://api.courvix.com/text/translate", {'target': language_to, 'text': text}, headers={"Key": "RnNuKM6vRtLUWElC"})
            if request.status_code is 200:
                if len(request.json()["response"]) > 255: # too long? set to desc instead of title
                    translate = discord.Embed(description=request.json()["response"], color=chill_embed_color)
                else:
                    translate = discord.Embed(title=request.json()["response"], color=chill_embed_color)
                translate.set_author(name=f'Translated from {request.json()["source"]} to {request.json()["target"]}')
                translate.set_footer(icon_url=ctx.author.avatar_url,
                                 text=f"Translate requested by {ctx.author.name} | {ctx.author.id}")
                await ctx.send(embed=translate)
            else:
                translate = discord.Embed(title=request.json()["response"], color=discord.Color.red())
                translate.set_author(name=f'Error code {request.status_code}')
                translate.set_footer(icon_url=ctx.author.avatar_url,
                                 text=f"Translate requested by {ctx.author.name} | {ctx.author.id}")
                await ctx.send(embed=translate)


def setup(bot):
    bot.add_cog(Translate(bot))