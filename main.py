# import asyncio
# import logging
# import logging.handlers
# import os
#
# from typing import List, Optional
#
# import discord
# from discord.ext import commands
# from aiohttp import ClientSession
#
#
# class Bot(commands.Bot):
#     def __init__(
#             self,
#             *args,
#             initial_extensions: List[str],
#             testing_guild_id: Optional[int] = None,
#             **kwargs,
#     ):
#         super().__init__(*args, **kwargs)
#         self.testing_guild_id = testing_guild_id
#         self.initial_extensions = initial_extensions
#
#     async def setup_hook(self) -> None:
#
#         for filename in os.listdir("cogs"):
#             if filename.endswith(".py"):
#                 await self.load_extension(f"cogs.{filename[:-3]}")
#
#         if self.testing_guild_id:
#             guild = discord.Object(self.testing_guild_id)
#             self.tree.copy_global_to(guild=guild)
#             await self.tree.sync(guild=guild)
#
#     async def on_member_join(self, member: discord.Member):
#         channel: discord.TextChannel = self.get_channel(1112320464346431598)
#         await channel.send(f"Hi {member.mention} Welcome to ACM MUJ! Head over to <id:customize>"
#                            f" to get roles.py and get started.")
#
#
# async def main():
#     # When taking over how the bot process is run, you become responsible for a few additional things.
#
#     # 1. logging
#
#     # for this example, we're going to set up a rotating file logger.
#     # for more info on setting up logging,
#     # see https://discordpy.readthedocs.io/en/latest/logging.html and https://docs.python.org/3/howto/logging.html
#
#     logger = logging.getLogger('discord')
#     logger.setLevel(logging.INFO)
#
#     handler = logging.handlers.RotatingFileHandler(
#         filename='discord.log',
#         encoding='utf-8',
#         maxBytes=32 * 1024 * 1024,  # 32 MiB
#         backupCount=5,  # Rotate through 5 files
#     )
#     dt_fmt = '%Y-%m-%d %H:%M:%S'
#     formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#
#     # Alternatively, you could use:
#     # discord.utils.setup_logging(handler=handler, root=False)
#
#     # One of the reasons to take over more of the process though
#     # is to ensure use with other libraries or tools which also require their own cleanup.
#
#     # Here we have a web client and a database pool, both of which do cleanup at exit.
#     # We also have our bot, which depends on both of these.
#
#     extensions = ['general', 'mod', 'dice']
#     async with Bot(commands.when_mentioned, initial_extensions=extensions, intents=discord.Intents.all()) as bot:
#         await bot.start(os.getenv('TOKEN', ''))
#
#
# # For most use cases, after defining what needs to run, we can just tell asyncio to run it:
# asyncio.run(main())
#
#
# async def on_member_join(self, member: discord.Member):
#     channel: discord.TextChannel = member.guild.get_channel(1112320464346431598)
#     await channel.send(f"Hi {member.mention} Welcome to ACM MUJ! Head over to <id:customize>"
#                        f" to get roles.py and get started.")

import asyncio
import logging
import logging.handlers
import os

from typing import List, Optional

import discord
from discord.ext import commands

from roles import Events
from tick import Confirm, TicketBot, CloseTicket


class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.testing_guild_id = testing_guild_id

    async def setup_hook(self) -> None:
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        self.add_view(Events())
        self.add_view(Confirm())
        self.add_view(TicketBot())
        self.add_view(CloseTicket())

    async def on_member_join(self, member: discord.Member):
        if member.guild.id == 1157385827756818535:
            channel: discord.TextChannel = self.get_channel(1157391321707855964)
            get_started: discord.TextChannel = self.get_channel(1157391112529510492)
            await channel.send(
                f"Hi {member.mention} Welcome to Elicit! Head over to {get_started.mention}"
                f" to get roles and get started."
            )
        else:
            channel: discord.TextChannel = self.get_channel(1112320464346431598)
            await channel.send(
                f"Hi {member.mention} Welcome to ACM MUJ! Head over to <id:customize>"
                f" to get roles and get started."
            )


async def main():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    intents = discord.Intents.all()
    intents.message_content = True
    async with CustomBot(
        commands.when_mentioned,
        intents=intents,
    ) as bot:
        await bot.start(os.getenv("TOKEN", ""))


asyncio.run(main())
