import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput, Select

# ---------------------------
# Import Flask server (optional)
# ---------------------------
try:
    from myserver import server_on
except ImportError:
    print("Warning: myserver.py not found. The Flask server will not run.")

    def server_on():
        pass

# ---------------------------
# Colors
# ---------------------------
class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5
    INCLOCK = 0x1e6aef
    OUTCLOCK = 0xefc11e

# ---------------------------
# Logging setup
# ---------------------------
logging.basicConfig(level=logging.INFO)

# ---------------------------
# Load env
# ---------------------------
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Bangkok")

# ---------------------------
# Employee Data
# ---------------------------
# This data is static. You can manage this in a config file or database for a larger project.
EMPLOYEES = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Canadad":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703306657038408/1_england.png",
    "🇨🇦 Canada":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703309001527318/2_canada.png",
    "🇮🇹 Italy":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703308619714741/3_italy.png",
    "🇸🇯 Norway":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703308229771295/4_norway.png",
   "🇸🇴 Somalia":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703307814666260/5_somalia.png",
    "🇪🇪 Estonia":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420701248146898965/6_estonia.png",
    "🇵🇰 Pakistan":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703307348836403/7_pakistan.png",
    "🇧🇪 Belgium":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703382913552384/8_belgium.png",
    "🇵🇦 Panama":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1424367646735995013/9_panama.png",
    "🇲🇨 Indonesia":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703382443921438/10_indonesia.png",
    "🇸🇦 Saudi Arabia":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703381974024253/11_saudi_arabia.png",
    "🇦🇹 Austria":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703381529563156/12_austria.png",
    "🇴🇲 Oman":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420703381076443156/13_oman.png",
    "🇨🇳 China":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420709071316582464/14_china.png",
    "🇲🇴 Macau":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420709073288040539/15_macau.png",
    "🇵🇭 Philippines":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420709072822341672/16_philippines.png",
    "🇱🇻 Latvia":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420709072440786944/17_latvia.png",
    "🇨🇷 Costa rica":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420709072071819294/18_costa_rica.png",
    "🇨🇴 Colombia":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420709071706787840/19_colombia.png",
    "🇦🇪 UAE":
    "https://cdn.discordapp.com/attachments/1371125614815219762/1420987940515086387/20_UAE.png",
    "🇫🇮 Finland": "https://cdn.discordapp.com/attachments/1371125614815219762/1421321626368344105/21_finland.png",
    "🇵🇱 Poland": "https://cdn.discordapp.com/attachments/1371125614815219762/1423146605456003282/22_poland.png",
    "🇭🇰 Hong Kong": "https://cdn.discordapp.com/attachments/1371125614815219762/1423146605007339541/23_hong_kong.png",
    "🇷🇸 Serbia": "https://cdn.discordapp.com/attachments/1371125614815219762/1423146604541640796/24_serbia.png",
    "🇻🇦 Vatican": "https://cdn.discordapp.com/attachments/1372582719279857715/1423562108028588133/YotNakBunYai_20251003_134711_0000.png",
    "🇩🇰 Denmark":
"https://cdn.discordapp.com/attachments/1371125614815219762/1420992343623991327/1_denmark.png",
    "🇹🇷 Türkiye":    "https://cdn.discordapp.com/attachments/1371125614815219762/1420992343200370788/2_turkiye.png",
    "🇱🇹 Lithuania":
"https://cdn.discordapp.com/attachments/1371125614815219762/1420992342814490685/3_lithuania.png",
    "🇸🇪 Sweden":    "https://cdn.discordapp.com/attachments/1371125614815219762/1420992342340407390/4_sweden.png",
    "🇧🇸 Bahamas":
"https://cdn.discordapp.com/attachments/1371125614815219762/1420992341933686875/5_bahamas.png",
    "🇨🇿 Czechia": "https://cdn.discordapp.com/attachments/1371125614815219762/1423147736697671813/6.czechia.png",
    "🇨🇭 Switzerland": "https://cdn.discordapp.com/attachments/1371125614815219762/1423147736366317568/7_switzerland.png",
    "🇮🇳 India": "https://cdn.discordapp.com/attachments/1371125614815219762/1423147736001286145/8_india.png",
    "🇰🇷 South Korea": "https://cdn.discordapp.com/attachments/1371125614815219762/1423147735560749096/9_south_korea.png",
    "🇯🇵 Japan": "https://cdn.discordapp.com/attachments/1371125614815219762/1421321627374846104/1_japan.png",
    "🇳🇷 Nauru": "https://cdn.discordapp.com/attachments/1371125614815219762/1421321627848933417/2_nauru.png",
    "🇲🇳 Mongolia": "https://cdn.discordapp.com/attachments/1371125614815219762/1423148612036329523/3_mongolia.png",
    "🇱🇺 Luxembourg": "https://cdn.discordapp.com/attachments/1371125614815219762/1423148611583082616/4_luxembourg.png",
    "🇭🇲 Australia": "https://cdn.discordapp.com/attachments/1371125614815219762/1423148611117781052/5_australia.png",
    "🇧🇷 Brazil": "https://cdn.discordapp.com/attachments/1371125614815219762/1420993522915606528/1_brazil.png",
    "🇦🇱 Albania":
"https://cdn.discordapp.com/attachments/1371125614815219762/1420993522550571041/2_albania.png",
    "🇧🇼 Botswana": "https://cdn.discordapp.com/attachments/1371125614815219762/1423150240583778314/3_botswana.png",
    "🇹🇭 Thailand": "https://cdn.discordapp.com/attachments/1371125614815219762/1423150240155828254/4_thailand.png",
    "🇰🇵 North Korea": "https://cdn.discordapp.com/attachments/1371125614815219762/1423150239694717068/5_north_korea.png",
    "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland": "",
    "🇫🇷 France":"",
    "🇮🇸 Iceland": "",
    "🇩🇪 Germany": "",
    "🇸🇲 San Marino": "",
    "🇬🇱 Greenland": "",
    "🇳🇿 New Zealand": "",
    "🇲🇾 Malaysia": "",
    "🇺🇸 America": ""
}

# ---------------------------
# Bot Setup
# ---------------------------
intents = discord.Intents.default()
intents.message_content = True  # Required for command processing
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')
    print("Bot is ready to go!")


# ---------------------------
# Clock In/Out System
# ---------------------------
class NameModal(Modal, title="ลงชื่อเข้างาน/ออกงาน"):
    user_name = TextInput(label="กรุณากรอกชื่อของคุณ",
                          placeholder="เช่น: สมชาย")

    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        self.parent_view.user_name = str(self.user_name)
        self.parent_view.clear_items()
        self.parent_view.add_item(self.parent_view.btn_in)
        self.parent_view.add_item(self.parent_view.btn_out)

        await interaction.response.edit_message(
            content=(f"✅ คุณกรอกชื่อเป็น `{self.parent_view.user_name}`\n"
                     f"เลือก **ลงชื่อเข้างาน / ลงชื่อออกงาน**"),
            view=self.parent_view)


class EmployeeSelect(discord.ui.Select):
    """A dropdown menu for selecting an employee."""

    def __init__(self, parent_view, options, placeholder):
        self.parent_view = parent_view
        super().__init__(placeholder=placeholder,
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.stop()
        for item in self.view.children:
            item.disabled = True

        await interaction.response.edit_message(
        content=f"✅ คุณเลือก: {self.values[0]}", view=self.view)


        self.parent_view.selected_employee = self.values[0]

        await self.parent_view.finish(interaction)


class EmployeeSelectView(View):
    """A view that holds one or more EmployeeSelect dropdowns."""

    def __init__(self, parent_view):
        super().__init__(timeout=180)

        employee_names = list(EMPLOYEES.keys())

        chunks = [
            employee_names[i:i + 25] for i in range(0, len(employee_names), 25)
        ]

        for i, chunk in enumerate(chunks):
            options = [discord.SelectOption(label=name) for name in chunk]
            placeholder = f"เลือกพนักงาน "
            self.add_item(EmployeeSelect(parent_view, options, placeholder))


class ClockView(View):

    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.user_name = None
        self.clock_type = None
        self.selected_employee = None
        self.message = None

        self.btn_name = Button(label="กรอกชื่อผู้ใช้",
                               style=discord.ButtonStyle.primary)
        self.btn_in = Button(label="ลงชื่อเข้างาน",
                             style=discord.ButtonStyle.success,
                             custom_id="clock_in")
        self.btn_out = Button(label="ลงชื่อออกงาน",
                              style=discord.ButtonStyle.danger,
                              custom_id="clock_out")

        self.btn_name.callback = self.enter_name_callback
        self.btn_in.callback = self.clock_action_callback
        self.btn_out.callback = self.clock_action_callback

        self.add_item(self.btn_name)

    async def enter_name_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(NameModal(self))

    async def clock_action_callback(self, interaction: discord.Interaction):
        custom_id = interaction.data['custom_id']

        if custom_id == 'clock_in':
            self.clock_type = "ลงชื่อเข้างาน"
        elif custom_id == 'clock_out':
            self.clock_type = "ลงชื่อออกงาน"

        view = EmployeeSelectView(self)
        await interaction.response.send_message(
            "กรุณาเลือกชื่อพนักงานจากรายการ:", view=view, ephemeral=True)

    async def finish(self, interaction: discord.Interaction):
        now = datetime.now(ZoneInfo(TIMEZONE))
        time_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        time_iso = now.isoformat()

        embed = discord.Embed(
            title=f"🕒 {self.clock_type} สำเร็จ",
            description=
            (f"{interaction.user.mention} **{self.clock_type}** เรียบร้อย\n"
             f"👤 ชื่อที่กรอก: `{self.user_name}`\n"
             f"🧑‍💼 พนักงาน: `{self.selected_employee}`\n"
             f"⏰ เวลา: {time_str}"),
            color=colors.INCLOCK
            if self.clock_type == "ลงชื่อเข้างาน" else colors.OUTCLOCK,
            timestamp=now)
        card_url = EMPLOYEES.get(self.selected_employee)
        if card_url:
            embed.set_image(url=card_url)

        self.clear_items()

        if self.message:
            await self.message.edit(content=None, embed=embed, view=None)

        self.stop()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(content="⏰ การทำรายการหมดเวลาแล้ว",
                                    view=self)


@bot.command(name="clock")
async def clock_command(ctx):
    view = ClockView(ctx)
    message = await ctx.send("กรุณากรอกชื่อของคุณเพื่อทำรายการ", view=view)
    view.message = message


# ---------------------------
# Simple hello command
# ---------------------------
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("สวัสดีครับ!")


# ---------------------------
# Main entry
# ---------------------------
if __name__ == "__main__":
    server_on()
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        logging.error("DISCORD_TOKEN not found in environment variables.")
