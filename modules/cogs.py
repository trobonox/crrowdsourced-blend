import logging, aiofiles.os
from discord.ext import commands

# class for tasks like loading, unloading and restarting cogs/modules
# all commands are moderator only, so they cannot be abused
class cogs(commands.Cog):
    def __init__(self, client):
        logging.info(f"Loaded {self.__class__.__name__.title()} module.")

        self.client = client

    @commands.command(
        command="loadmodule", aliases=["lm", "load"], brief="Loads a module."
    )
    @commands.has_permissions(manage_guild=True)
    async def loadmodule(self, ctx, module):
        module_exists = await aiofiles.os.path.isfile(f"./modules/{module}.py")

        if not module_exists:
            return await ctx.reply("That module does not exist! Please check your spelling and try again.") 

        await self.client.load_extension(f"modules.{module}")
        await ctx.message.add_reaction("✅")

    @commands.command(
        command="unloadmodule", aliases=["unload", "ulm"], brief="Unloads a module."
    )
    @commands.has_permissions(manage_guild=True)
    async def unloadmodule(self, ctx, module):
        module_exists = await aiofiles.os.path.isfile(f"./modules/{module}.py")

        if not module_exists:
            return await ctx.reply("That module does not exist! Please check your spelling and try again.") 

        await self.client.unload_extension(f"modules.{module}")
        await ctx.message.add_reaction("✅")

    @commands.command(
        command="reloadmodule", aliases=["reload", "rl"], brief="Reloads a module."
    )
    @commands.has_permissions(manage_guild=True)
    async def reloadmodule(self, ctx, module):
        module_exists = await aiofiles.os.path.isfile(f"./modules/{module}.py")

        if not module_exists:
            return await ctx.reply("That module does not exist! Please check your spelling and try again.") 

        await self.client.reload_extension(f"modules.{module}")
        await ctx.message.add_reaction("✅")


async def setup(client):
    await client.add_cog(cogs(client))