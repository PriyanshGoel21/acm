import discord
from discord.ext import commands, tasks
from discord import app_commands, utils

from tick import TicketBot


class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        ...

    @commands.hybrid_command(
        name="ticket", with_app_command=True, description="Ticket message"
    )
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def ticketing(self, ctx):
        canale = ctx.message.channel
        embed = discord.Embed(
            title="Open a ticket!",
            description="How can we help?\nWelcome to our help channel. If you have any questions or inquiries, "
            "please click on the ‘Open ticket’ button below to contact the staff!",
            color=discord.Color.green(),
        )
        await canale.send(embed=embed, view=TicketBot())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ticket(bot))
