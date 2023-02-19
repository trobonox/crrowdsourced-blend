import discord as discord, datetime, pytz
from discord.ext import commands
from utils import config

config = config.config()

# custom help that neatly packs all commands into categories and sends them in an embed
class CustomHelp(commands.MinimalHelpCommand):
    def get_command_signature(self, command, extended=False):
        if extended:
            return "%s%s %s" % (
                self.context.clean_prefix,
                command.qualified_name,
                command.signature,
            )
        return command.qualified_name

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help",
            timestamp=datetime.datetime.now(tz=pytz.timezone("Europe/Berlin"))
        )
        embed.set_footer(text="Bot made by Trobonox (trobo.tech)")
        embed.description = f"""
        Use `{config.prefix}help [command]` for more info on a command.\nYou can also use `{config.prefix}help [category]` for more info on a category.\n\n
        """

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Other")
                embed.add_field(
                    name=f"__**{cog_name.title()}**__",
                    value=" ".join(command_signatures),
                    inline=False,
                )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        help_text = command.help or command.brief or "❌ No description provided."

        embed = discord.Embed(
            title=self.get_command_signature(command, extended=True),
            timestamp=datetime.datetime.now(tz=pytz.timezone("Europe/Berlin"))
        )
        embed.set_footer(text="Bot made by Trobonox (trobo.tech)")
        embed.add_field(name="Help", value=help_text)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"Commands in {cog.qualified_name}",
            timestamp=datetime.datetime.now(tz=pytz.timezone("Europe/Berlin"))
        )
        embed.set_footer(text="Bot made by Trobonox (trobo.tech)")

        filtered_commands = await self.filter_commands(cog.get_commands(), sort=True)

        description = ""
        description += f"Use `{config.prefix}help [command]` for more info on a command.\n\n"
        for command in filtered_commands:
            if command.brief != None:
                description += f"**{command.name}** • {command.brief}\n"
            else:
                description += f"**{command.name}**\n"
        embed.description = description

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error, color=0x990D00)
        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, client):
        self._original_help_command = client.help_command
        client.help_command = CustomHelp()
        client.help_command.cog = self

    def cog_unload(self):
        self.client.help_command = self._original_help_command


async def setup(client):
    await client.add_cog(Help(client))