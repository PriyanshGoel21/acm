# import discord
# from discord.ext import commands, tasks
# from discord import app_commands, utils
# import json, time
# from colorama import init as colorama_init
# from colorama import Fore
# from colorama import Style
# import chat_exporter, io
# from discord import ui
#
# colorama_init()
#
#
# class TicketBot(discord.ui.View):
#     def __init__(self) -> None:
#         super().__init__(timeout=None)
#         self.cooldown = commands.CooldownMapping.from_cooldown(
#             1, 2, commands.BucketType.member
#         )
#         self.counter = 0
#
#     @discord.ui.button(
#         label="Open ticket",
#         style=discord.ButtonStyle.blurple,
#         custom_id="ticket_button_1",
#         emoji="📩",
#     )
#     async def create_ticket(
#         self, interaction: discord.Interaction, button: discord.ui.Button
#     ):
#         cooldown_status = self.cooldown.get_bucket(
#             interaction.message
#         ).update_rate_limit()
#         if cooldown_status:
#             return await interaction.response.send_message(
#                 f"You are on cooldown! Wait {round(cooldown_status, 1)} seconds!",
#                 ephemeral=True,
#             )
#         open_tickets: discord.CategoryChannel = interaction.guild.get_channel(
#             1157394672591839262
#         )
#         ticket_channel_exist = utils.get(
#             open_tickets.text_channels,
#             topic=str(interaction.user.id),
#         )
#         if ticket_channel_exist:
#             await interaction.response.send_message(
#                 f"You already have an open ticket {ticket_channel_exist.mention}!",
#                 ephemeral=True,
#             )
#         else:
#             mod = interaction.guild.get_role(1157394375198912644)
#             perms_ticket = {
#                 interaction.guild.default_role: discord.PermissionOverwrite(
#                     view_channel=False
#                 ),
#                 interaction.user: discord.PermissionOverwrite(
#                     view_channel=True,
#                     send_messages=True,
#                 ),
#                 mod: discord.PermissionOverwrite(
#                     view_channel=True,
#                     send_messages=True,
#                 ),
#             }
#             ticket_channel = await interaction.guild.create_text_channel(
#                 name=f"ticket-{self.counter}",
#                 topic=f"{interaction.user.id}",
#                 overwrites=perms_ticket,
#                 reason=f"Ticket for {interaction.user}",
#                 category=open_tickets,
#             )
#             self.counter += 1
#             embed = discord.Embed(
#                 title=f"Thankyou for contacting support",
#                 description=f"Please describe your issue and wait for a response",
#                 color=discord.Color.green(),
#             )
#             await ticket_channel.send(
#                 f"<@&1157394375198912644>", embed=embed, view=CloseTicket()
#             )
#
#             embed = discord.Embed(
#                 title=f"Ticket",
#                 description=f"Opened a new ticket",
#                 color=discord.Color.green(),
#             )
#
#             await interaction.response.send_message(embed=embed, ephemeral=True)
#
#
# class Confirm(discord.ui.View):
#     def __init__(self) -> None:
#         super().__init__(timeout=None)
#
#     @discord.ui.button(
#         label="Confirm", style=discord.ButtonStyle.red, custom_id="confirm"
#     )
#     async def confirm_button(self, interaction: discord.Interaction, button):
#         embed = discord.Embed(color=discord.Color.red())
#         await interaction.channel.edit(
#             category=interaction.guild.get_channel(1157398172822413434)
#         )
#         await interaction.response.send_message(
#             embed=discord.Embed(title="Ticket Closed", color=discord.Color.red()),
#             reply=False,
#         )
#
#
# class CloseTicket(discord.ui.View):
#     def __init__(self) -> None:
#         super().__init__(timeout=None)
#
#     @discord.ui.button(
#         label="Close Ticket",
#         style=discord.ButtonStyle.red,
#         emoji="🔒",
#         custom_id="close_ticket",
#     )
#     async def close(self, interaction, button):
#         embed = discord.Embed(
#             title="Are you sure you want to close the ticket?",
#             color=discord.Color.red(),
#         )
#         await interaction.response.send_message(
#             embed=embed, view=Confirm(), ephemeral=True
#         )
#
#
# class Ticket(commands.Cog):
#     def __init__(self, bot: commands.Bot) -> None:
#         self.bot = bot
#
#     @commands.Cog.listener()
#     async def on_ready(self):
#         print(f"[Ticket] {Fore.LIGHTGREEN_EX}Online!{Style.RESET_ALL}")
#
#     @commands.hybrid_command(
#         name="ticket", with_app_command=True, description="Ticket message"
#     )
#     @app_commands.default_permissions(manage_guild=True)
#     @app_commands.checks.bot_has_permissions(manage_channels=True)
#     async def ticketing(self, ctx):
#         canale = ctx.message.channel
#         embed = discord.Embed(
#             title="Open a ticket!",
#             description="How can we help?\nWelcome to our help channel. If you have any questions or inquiries, "
#             "please click on the ‘Open ticket’ button below to contact the staff!",
#             color=discord.Color.green(),
#         )
#         embed.set_author(
#             name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url
#         )
#         await canale.send(embed=embed, view=TicketBot())
#         print(
#             f"[Ticket Log] {Fore.LIGHTGREEN_EX}Ticket message created! [@{ctx.message.author} - #{canale}]{Style.RESET_ALL}"
#         )
#
#
# async def setup(bot: commands.Bot) -> None:
#     await bot.add_view(TicketBot())
#     await bot.add_cog(Ticket(bot))
