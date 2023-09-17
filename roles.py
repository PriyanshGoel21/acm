import discord


async def handle_role(interaction: discord.Interaction, role_id: int):
    role: discord.Role = interaction.guild.get_role(role_id)
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(
            f"{role.mention} role removed.", ephemeral=True
        )
    else:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(
            f"{role.mention} role added.", ephemeral=True
        )


class Events(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Hacks 8.0",
        style=discord.ButtonStyle.blurple,
        custom_id="hacks",
    )
    async def hacks(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1157408511064547448)

    @discord.ui.button(
        label="Defi Hacks",
        style=discord.ButtonStyle.blurple,
        custom_id="defi",
    )
    async def defi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1157408523995578519)

    @discord.ui.button(
        label="Im-Prompt-O",
        style=discord.ButtonStyle.blurple,
        custom_id="prompt",
    )
    async def prompt(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1157408517028843544)

    @discord.ui.button(
        label="UX Evolve",
        style=discord.ButtonStyle.blurple,
        custom_id="evolve",
    )
    async def evolve(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1157408533160149063)

    @discord.ui.button(
        label="Polysis",
        style=discord.ButtonStyle.blurple,
        custom_id="polysis",
    )
    async def polysis(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await handle_role(interaction, 1157408538881163294)
