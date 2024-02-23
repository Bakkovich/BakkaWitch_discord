import disnake
import os
from mafic import NodePool
from disnake.ext import commands
import logging
from typing import TYPE_CHECKING, Any
from config import TOKEN

# Логи в консоли
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s")
logger = logging.getLogger("discord")

intents = disnake.Intents.all()
intents.message_content = True

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True


class Alexbot(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.ready_ran = False
        self.pool = NodePool(self)

    async def on_ready(self):
        if self.ready_ran:
            return

        await self.pool.create_node(
            host="127.0.0.1",
            port=2333,
            label="MAIN",
            password="youshallnotpass",
        )
        logger.info("Connected.")
        logger.info(f"Бот {bot.user.name} запущен!")
        self.ready_ran = True


bot = Alexbot(
    command_prefix="/",
    intents=intents,
    test_guilds=[1128831109896097874],
    command_sync_flags=command_sync_flags,
)

@bot.event
async def on_disconnect():
    logger.info(f"Бот {bot.user.name} остановлен!")


# @bot.slash_command(name='hello', description='Приветственное сообщение') # Тестовая команда
# async def hello(ctx):
#     await ctx.send('Привет!')

# @bot.slash_command(name='delmsg', description='Удалить сообщения') # Массовое удаление сообщений
# async def delmsg(ctx, limit: int):
#     if limit <= 0 or limit > 100:
#         await ctx.send('Пожалуйста, укажите число от 1 до 100 для удаления сообщений.', ephemeral=True)
#         return

#     await ctx.channel.purge(limit=limit + 1)

bot.load_extension("cogs.test")
# Загружаем коги
# for file in os.listdir("./cogs"):
#     if file.endswith(".py"):
#         bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN)
