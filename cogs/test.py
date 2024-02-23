import disnake
from disnake.ext import commands

#Добавляем класс с командами
class Testcommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.slash_command(name='hello', description='Приветственное сообщение') # Тестовая команда
        async def hello(ctx):
          await ctx.send('Привет!')

        @bot.slash_command(name='delmsg', description='Удалить сообщения') # Массовое удаление сообщений
        async def delmsg(ctx, limit: int): 
          if limit <= 0 or limit > 100:
            await ctx.send('Пожалуйста, укажите число от 1 до 100 для удаления сообщений.', ephemeral=True)
            return

          await ctx.channel.purge(limit=limit + 1)

#Добавляем коги в бота
def setup(bot: commands.Bot):
    bot.add_cog(Testcommands(bot))
