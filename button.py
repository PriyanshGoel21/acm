import asyncpg
import discord


class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Get Started', style=discord.ButtonStyle.green, custom_id='persistent_view:id')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.db_pool.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.execute('''INSERT INTO "User"(id, name) VALUES($1, $2)''',
                                         str(interaction.user.id), interaction.user.display_name)
                except asyncpg.UniqueViolationError as E:
                    await connection.execute('''UPDATE "User" set name=$1 WHERE id=$2''',
                                         interaction.user.display_name, str(interaction.user.id))

        await interaction.response.send_message(f'Your decode ID is {interaction.user.id}', ephemeral=True)
