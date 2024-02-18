import disnake
from disnake.ext import commands
import logging
from config import TOKEN

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Логи в консоли
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')
logger = logging.getLogger('discord')

@bot.event # Статус
async def on_ready():
    await bot.change_presence(activity=disnake.Game(name="Когда нибудь я стану многофункциональным"))
    logger.info(f'Бот {bot.user.name} запущен!')

@bot.event
async def on_disconnect():
    logger.info(f'Бот {bot.user.name} остановлен!')

@bot.slash_command(name='hello', description='Приветственное сообщение') # Тестовая команда
async def hello(ctx):
    await ctx.send('Привет!')

@bot.slash_command(name='delmsg', description='Удалить сообщения') # Массовое удаление сообщений
async def delmsg(ctx, limit: int): 
    if limit <= 0 or limit > 100:
        await ctx.send('Пожалуйста, укажите число от 1 до 100 для удаления сообщений.', ephemeral=True)
        return

    await ctx.channel.purge(limit=limit + 1)

bot.run(TOKEN)
