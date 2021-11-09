import discord
from discord import NotificationLevel, ContentFilter
from discord.ext import commands
import traceback
import sys
import random
import requests
from datetime import datetime
from main import bot_webhook
from utils.vars import *


class Help(commands.Cog):
    """
        Aimed to help you with using the bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        """
            Shows a helpful help menu
        """
        help_embed = discord.Embed(title=f'{wave_emoji} Ayudante Help', color=chill_embed_color, description=f"Ayudante is an intituive translate bot that is perfect for international servers. Based on [Courvix API](https://api.courvix.com)'s translate functionality")
        command_names_list = "\n"
        for x in self.bot.commands:
            if x.name == "setstatus" or x.name == "ping": pass # hide those sneaky commands ;)
            else: command_names_list += f"**{x.name}**\n```{x.help}```\n"
        help_embed.add_field(name='Available Commands', value=command_names_list + "\n", inline=False)
        help_embed.set_footer(text="Created by Rivage")
        await ctx.send(embed=help_embed)

    @commands.command(aliases=['guildinfo', 'si', 'gi'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    # @commands.has_guild_permissions(kick_members=True)
    async def serverinfo(self, ctx):
        """Get current server information"""
        # Make it a bit easier
        guild = ctx.guild
        total_member = str(ctx.guild.member_count)
        total_tx = len(guild.text_channels)
        total_vc = len(guild.voice_channels)
        total_roles = len(guild.roles)
        total_emoji = len(guild.emojis)
        features = guild.features
        mfa_level = guild.mfa_level
        if mfa_level == 1:
            mfa = "On"
        elif mfa_level == 0:
            mfa = "Off"
        # since it comes in bytes
        filesize = guild.filesize_limit / 1000000
        if filesize < 10:
            filesize = 10
        else:
            pass
        filesize = f"{filesize} MB"
        emoji_count = f"{total_emoji} / {guild.emoji_limit}"
        member_count = f"{total_member} / {guild.max_members}"
        vc_count = f"{total_vc} / 100"
        tx_count = f"{total_tx} / 100"
        role_count = f"{total_roles} / 250"
        time_created_ago = datetime.now() - guild.created_at
        created_at = f"{time_created_ago} ago"
        random_embed_messages = [
            f"{wave_emoji} It's nice to see you {ctx.author.name}! Let's check out {ctx.guild.name}",
            f"{cop_emoji} FBI checking out {ctx.guild.name}", f"{ok_check_emoji} {ctx.guild.name} checkup"]
        embed = discord.Embed(title=random.choice(random_embed_messages), color=chill_embed_color)
        # Thingy on the right
        embed.set_thumbnail(url=guild.icon_url)
        if guild.banner:
            # Thingy on the bottom if the server is that goated
            embed.set_image(url=guild.banner_url)
        elif guild.splash:
            embed.set_image(url=guild.splash_url)
        embed.add_field(name="Server Owner", value=guild.owner, inline=True)
        embed.add_field(name="Region", value=guild.region, inline=True)
        embed.add_field(name="Verification Level", value=guild.verification_level, inline=True)
        embed.add_field(name="Member Count", value=member_count, inline=True)
        # Gotta user len() here or it returns the whole fuckin thing
        embed.add_field(name="Text Channels", value=tx_count, inline=True)
        embed.add_field(name="Voice Channels", value=vc_count, inline=True)
        embed.add_field(name="Roles", value=role_count, inline=True)
        embed.add_field(name="Emojis", value=emoji_count, inline=True)
        if guild.premium_subscription_count:
            embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
        if guild.premium_subscribers:
            embed.add_field(name="Boosters", value=len(guild.premium_subscribers), inline=True)
        if guild.rules_channel:
            embed.add_field(name="Rule Channel", value=guild.rules_channel.mention, inline=True)
        embed.add_field(name="Guild Creation", value=created_at, inline=True)
        embed.add_field(name="Filesize Limit", value=filesize, inline=True)
        embed.add_field(name="Two Factor Auth", value=mfa, inline=True)
        if guild.explicit_content_filter is ContentFilter.no_role:
            embed.add_field(name="Content Filter", value="On for members with no role", inline=True)
        elif guild.explicit_content_filter is ContentFilter.all_members:
            embed.add_field(name="Content Filter", value="On for everyone", inline=True)
        elif guild.explicit_content_filter is ContentFilter.disabled:
            embed.add_field(name="Content Filter", value="Off", inline=True)
        if guild.description:
            embed.add_field(name="Description", value=guild.description, inline=True)
        if guild.default_notifications is NotificationLevel.only_mentions:
            embed.add_field(name="Default Notifs", value="Only mentions", inline=True)
        elif guild.default_notifications is NotificationLevel.all_messages:
            embed.add_field(name="Default Notifs", value="Every message", inline=True)
        if guild.afk_channel is not None:
            afk_channels = f"Channel: {guild.afk_channel} | Timeout: {guild.afk_timeout} seconds"
            embed.add_field(name="AFK channels", value=afk_channels, inline=True)
        # more add_fields
        embed.add_field(name="Features", value='\n'.join(map(str, features)), inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f"Info Requested by {ctx.author.name}, User ID: {ctx.author.id}")
        await ctx.send(embed=embed)

    # When a command is called
    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.guild is None: # block shitty dm commands
            pass
        else:
            print(f"{ctx.author}: {ctx.command}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error): # handle pesky errors
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send("⚠️ This command cannot be used in private messages.")
        elif isinstance(error, commands.CommandOnCooldown):
            retry_time = round(error.retry_after, 2)
            await ctx.send(f"⚠️ You are being ratelimited! Please try again in {retry_time} seconds!")
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(
                f"⚠ Sorry, you are only allowed {error.number} concurrent session! Please finish your current one.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"⚠️ You do not have sufficient permissions! You need `{error.missing_perms}` to run this command.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('⚠️ Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'⚠️ Sorry, please provide the `{error.param}` parameter. Example: `{ctx.prefix}{ctx.command} <value of {error.param}>`')
        elif isinstance(error, commands.CommandNotFound):
            # If the command is not found, just do nothing
            pass
        elif isinstance(error, commands.CommandInvokeError):
            if ctx.guild:
                await ctx.send(
                    '⚠️ Sorry, an error occurred while running your command. The developers have been notified.')
                guild = f"{ctx.guild} (ID: {ctx.guild.id}"
            else:
                await ctx.author.send(
                    '⚠️ Sorry, an error occurred while running your command. The developers have been notified.')
                guild = "DMs"
            traceback.print_tb(error.original.__traceback__)
            data = {
                "content": f"Error occured in `{guild}` by `{ctx.author}` while running `{ctx.command}`",
                "username": "Swath Error Report"
            }
            data["embeds"] = [
                {
                    "description": f'{error.original.__class__.__name__}: {error.original}',
                    "title": "Detailed traceback"
                }
            ]
            requests.post(bot_webhook, json=data)
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            print(
                f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)


def setup(bot):
    bot.add_cog(Help(bot))