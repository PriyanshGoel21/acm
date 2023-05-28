import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_member_join(self, member:discord.Member):
        channel: discord.TextChannel = member.guild.get_channel(1112320464346431598)
        await channel.send(f"Hi {member.mention} Welcome to ACM MUJ! Head over to <id:customize>"
                           f" to get roles and get started.")


intents = discord.Intents.all()
client = MyClient(intents=intents)

client.run('MTExMjExMTEyMzQyMDkzODI3MA.G0Yh0J.wskncyVWURB-r5C1gLgwhvNB3Bc7e87eFprx5Y')