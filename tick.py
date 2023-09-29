import discord
from discord import utils
from discord.ext import commands


class TicketBot(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(
            1, 2, commands.BucketType.member
        )
        self.counter = 0

    @discord.ui.button(
        label="Open ticket",
        style=discord.ButtonStyle.blurple,
        custom_id="ticket_button_1",
        emoji="📩",
    )
    async def create_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        cooldown_status = self.cooldown.get_bucket(
            interaction.message
        ).update_rate_limit()
        if cooldown_status:
            return await interaction.response.send_message(
                f"You are on cooldown! Wait {round(cooldown_status, 1)} seconds!",
                ephemeral=True,
            )
        open_tickets: discord.CategoryChannel = interaction.guild.get_channel(
            1157425296732078192
        )
        ticket_channel_exist = utils.get(
            open_tickets.text_channels,
            topic=str(interaction.user.id),
        )
        if ticket_channel_exist:
            await interaction.response.send_message(
                f"You already have an open ticket {ticket_channel_exist.mention}!",
                ephemeral=True,
            )
        else:
            mod = interaction.guild.get_role(1157394375198912644)
            perms_ticket = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                ),
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                ),
                mod: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                ),
            }
            ticket_channel = await interaction.guild.create_text_channel(
                name=f"ticket-{self.counter}",
                topic=f"{interaction.user.id}",
                overwrites=perms_ticket,
                reason=f"Ticket for {interaction.user}",
                category=open_tickets,
            )
            self.counter += 1
            embed = discord.Embed(
                title=f"Thankyou for contacting support",
                description=f"Please describe your issue and wait for a response",
                color=discord.Color.green(),
            )
            await ticket_channel.send(
                f"<@&1157394375198912644>", embed=embed, view=CloseTicket()
            )

            embed = discord.Embed(
                title=f"Ticket",
                description=f"Opened a new ticket: {ticket_channel.mention}",
                color=discord.Color.green(),
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)


class Confirm(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Confirm", style=discord.ButtonStyle.red, custom_id="confirm"
    )
    async def confirm_button(self, interaction: discord.Interaction, button):
        if interaction.channel.category_id == 1157425296732078192:
            embed = discord.Embed(color=discord.Color.red())
            perms_ticket = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                ),
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=False,
                ),
            }
            await interaction.channel.edit(
                category=interaction.guild.get_channel(1157425345851564052),
                overwrites=perms_ticket,
            )
            await interaction.response.send_message(
                embed=discord.Embed(title="Ticket Closed", color=discord.Color.red()),
            )


class CloseTicket(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        emoji="🔒",
        custom_id="close_ticket",
    )
    async def close(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.channel.category_id == 1157425296732078192:
            embed = discord.Embed(
                title="Are you sure you want to close the ticket?",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, view=Confirm())
