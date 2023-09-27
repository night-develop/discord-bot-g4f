import discord
import threading
import asyncio

from textwrap import wrap
from itertools import islice
from discord.ext import commands

from tool.config import Config
from tool.scheduler import run_scheduler_loop
from tool.sender import Sender
from tool.logger import logger_factory
from tool.links_gulds import LinksGuilds


config = Config().config
bot = commands.Bot(
    command_prefix=config['discord']['prefix'], 
    intents=discord.Intents.all()
)
context = {}
sender = Sender(config=config)
links_guilds = LinksGuilds()
links = asyncio.run(links_guilds.get_refresh_links())
logger = logger_factory(**config['logger'])

scheduler_thread = threading.Thread(target=run_scheduler_loop, kwargs={'config': config})
scheduler_thread.start()


@bot.hybrid_command(name='ping', description=config['alert_messages']['ping_command'])
async def ping(ctx):
    await ctx.send('pong')


@bot.hybrid_command(name='link', description=config['alert_messages']['link_channel'])
@commands.has_permissions(administrator=True)
async def link(ctx):
    guild_id = ctx.channel.guild.id
    channel_id = ctx.channel.id
    global links
    links = await links_guilds.set_links(guild_id=guild_id, channel_id=channel_id)
    await ctx.send('ok')


@bot.hybrid_command(name='unlink', description=config['alert_messages']['unlink_channel'])
@commands.has_permissions(administrator=True)
async def unlink(ctx):
    guild_id = ctx.channel.guild.id
    global links
    links = await links_guilds.delete_link(guild_id=guild_id)
    await ctx.send('ok')

bot.remove_command("help")
@bot.hybrid_command(name='help', description=config['alert_messages']['help_command'])
async def help(ctx):
    help_message = "```" \
                    F"ping - {config['alert_messages']['ping_command']} \n" \
                    F"link - {config['alert_messages']['link_channel']} \n" \
                    F"unlink - {config['alert_messages']['unlink_channel']} \n" \
                    F"help - {config['alert_messages']['help_command']}```"
    await ctx.send(help_message)


@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        flag_answer = False
        flag_request = False
        flag_link = False

        for m in ctx.mentions:
            if m.name == bot.application.name:
                flag_answer = True
                break
        
        bot_name = F"@{bot.application.name}"
        if bot_name in ctx.clean_content:
            flag_request = True

        if str(ctx.channel.guild.id) in links:
            if links[str(ctx.channel.guild.id)] == ctx.channel.id:
                flag_link = True
        else: 
            flag_link = True

        message = ctx.clean_content.replace(bot_name, "")

        if (flag_request or flag_answer) and flag_link:
            emoji = '\N{RIGHT-POINTING MAGNIFYING GLASS}'
            channel = bot.get_channel(ctx.channel.id)
            returned_responses = []

            global context
            
            if ctx.author.id not in context:
                context.update({ctx.author.id: []})

            tmp_context = [*context[ctx.author.id]]

            try:
                await ctx.add_reaction(emoji)

                async with channel.typing():
                    tmp_context.append({"role": "user", "content": message})
                    response = await sender.send_message(messages=tmp_context)
                    tmp_context.append({"role": "assistant", "content": response})
                    context[ctx.author.id] = list(reversed(list(islice(reversed(tmp_context), 0, config['bot']['deep_rate']))))

                if len(response) > config['bot']['message_length']:
                    returned_responses = wrap(response, config['bot']['message_length'])
                else:
                    returned_responses.append(response)

            except Exception as e:
                logger.error(repr(e))
                returned_responses.append(config['alert_messages']['message_exception'])

            await ctx.remove_reaction(emoji, member=bot.application)

            for res in returned_responses:
                await ctx.reply(res)

        else:
            message = message.replace(config['discord']['prefix'], '').strip()
            commands = [c.name for c in bot.tree.get_commands()]
            if message in commands:
                await bot.process_commands(ctx)

bot.run(config['discord']['token'])
