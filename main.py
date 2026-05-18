import discord
from discord.ext import commands
import os
import re
import json
import asyncio
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# ========== CONFIG ==========
AUTO_ROLE_NAME = 'Member'
TICKET_CATEGORY = 'Tickets'
LOG_CHANNEL = 'mod-logs'
WARNINGS_FILE = 'warnings.json'
warnings = {}

# ========== LOAD WARNINGS FROM FILE ==========
def load_warnings():
    global warnings
    if os.path.exists(WARNINGS_FILE):
        try:
            with open(WARNINGS_FILE, 'r') as f:
                warnings = json.load(f)
        except:
            warnings = {}

def save_warnings():
    try:
        with open(WARNINGS_FILE, 'w') as f:
            json.dump(warnings, f, indent=2)
    except:
        pass

load_warnings()

# ========== SCRIPT TEMPLATES ==========
FLY_SCRIPT = '''-- FLY SCRIPT (Press SPACE to fly)
local p=game.Players.LocalPlayer
local uis=game:GetService("UserInputService")
local fly=false
local bv,bg
uis.JumpRequest:Connect(function()
if not fly then
fly=true
local c=p.Character or p.CharacterAdded:Wait()
bv=Instance.new("BodyVelocity")
bv.MaxForce=Vector3.new(1,1,1)*1e5
bv.Velocity=Vector3.new(0,50,0)
bv.Parent=c.HumanoidRootPart
bg=Instance.new("BodyGyro")
bg.MaxTorque=Vector3.new(1,1,1)*1e5
bg.Parent=c.HumanoidRootPart
c.Humanoid.PlatformStand=true
game:GetService("RunService").RenderStepped:Connect(function()
if not fly then return end
local m=Vector3.new(
(uis:IsKeyDown(Enum.KeyCode.D)and 1 or 0)-(uis:IsKeyDown(Enum.KeyCode.A)and 1 or 0),
(uis:IsKeyDown(Enum.KeyCode.Space)and 1 or 0)-(uis:IsKeyDown(Enum.KeyCode.LeftShift)and 1 or 0),
(uis:IsKeyDown(Enum.KeyCode.S)and 1 or 0)-(uis:IsKeyDown(Enum.KeyCode.W)and 1 or 0)
)
if m.Magnitude>0 then m=m.Unit*85 end
if bv then bv.Velocity=m end
end)
else
fly=false
if bv then bv:Destroy()end
if bg then bg:Destroy()end
if c then c.Humanoid.PlatformStand=false end
end
end)
print("Fly loaded - Press SPACE")'''

GOD_SCRIPT = '''-- GOD MODE
local p=game.Players.LocalPlayer
game:GetService("RunService").RenderStepped:Connect(function()
local c=p.Character
if c then
local h=c:FindFirstChild("Humanoid")
if h then
h.MaxHealth=math.huge
h.Health=math.huge
h.BreakJointsOnDeath=false
end
end
end)
print("God mode activated")'''

AIMBOT_SCRIPT = '''-- AIMBOT
local p=game.Players.LocalPlayer
local cam=workspace.CurrentCamera
local uis=game:GetService("UserInputService")
game:GetService("RunService").RenderStepped:Connect(function()
local closest,cd=nil,300
local mp=uis:GetMouseLocation()
for _,pl in ipairs(game.Players:GetPlayers())do
if pl~=p then
local c=pl.Character
if c and c:FindFirstChild("Humanoid")and c.Humanoid.Health>0 then
local t=c:FindFirstChild("Head")or c:FindFirstChild("HumanoidRootPart")
if t then
local pos,on=cam:WorldToViewportPoint(t.Position)
if on then
local dist=(Vector2.new(pos.X,pos.Y)-mp).Magnitude
if dist<cd then cd=dist closest=pl end
end
end
end
end
end
if closest and closest.Character then
local t=closest.Character:FindFirstChild("Head")or closest.Character:FindFirstChild("HumanoidRootPart")
if t then
local pos=cam:WorldToViewportPoint(t.Position)
mousemoveabs(pos.X,pos.Y)
end
end
end)
print("Aimbot loaded")'''

ESP_SCRIPT = '''-- ESP
local p=game.Players.LocalPlayer
local function addESP(pl)
pl.CharacterAdded:Connect(function(c)
task.wait(0.5)
local h=Instance.new("Highlight")
h.FillColor=Color3.fromRGB(255,0,0)
h.FillTransparency=0.7
h.Adornee=c
h.Parent=c
end)
if pl.Character then
local h=Instance.new("Highlight")
h.FillColor=Color3.fromRGB(255,0,0)
h.FillTransparency=0.7
h.Adornee=pl.Character
h.Parent=pl.Character
end
end
for _,pl in ipairs(game.Players:GetPlayers())do
if pl~=p then addESP(pl)end
end
game.Players.PlayerAdded:Connect(addESP)
print("ESP loaded")'''

SPEED_SCRIPT = '''-- SPEED HACK
local p=game.Players.LocalPlayer
local speed={speed}
game:GetService("RunService").RenderStepped:Connect(function()
local c=p.Character
if c then
local h=c:FindFirstChild("Humanoid")
if h then h.WalkSpeed=speed end
end
end)
print("Speed set to "..speed)'''

JUMP_SCRIPT = '''-- INFINITE JUMP
local uis=game:GetService("UserInputService")
uis.JumpRequest:Connect(function()
local c=game.Players.LocalPlayer.Character
local h=c and c:FindFirstChild("Humanoid")
if h then h:ChangeState(Enum.HumanoidStateType.Jumping)end
end)
print("Infinite jump loaded")'''

KILLAURA_SCRIPT = '''-- KILL AURA
local p=game.Players.LocalPlayer
local range={range}
game:GetService("RunService").RenderStepped:Connect(function()
local c=p.Character
local rt=c and c:FindFirstChild("HumanoidRootPart")
if not rt then return end
for _,pl in ipairs(game.Players:GetPlayers())do
if pl~=p then
local tc=pl.Character
local tr=tc and tc:FindFirstChild("HumanoidRootPart")
if tr then
if(rt.Position-tr.Position).Magnitude<range then
local h=tc:FindFirstChild("Humanoid")
if h and h.Health>0 then h.Health=0 end
end
end
end
end
end)
print("Kill aura loaded - Range: "..range)'''

FARM_SCRIPT = '''-- AUTO FARM
local p=game.Players.LocalPlayer
while true do
for _,o in ipairs(workspace:GetDescendants())do
if o:IsA("BasePart")then
local n=o.Name:lower()
if n:find("coin")or n:find("gem")or n:find("diamond")then
local c=p.Character
local r=c and c:FindFirstChild("HumanoidRootPart")
if r then r.CFrame=o.CFrame task.wait(0.5)end
end
end
end
task.wait(1)
end
print("Auto farm loaded")'''

NOCLIP_SCRIPT = '''-- NO CLIP
local p=game.Players.LocalPlayer
game:GetService("RunService").Stepped:Connect(function()
local c=p.Character
if c then
for _,part in ipairs(c:GetDescendants())do
if part:IsA("BasePart")then part.CanCollide=false end
end
end
end)
print("No clip activated")'''

TELEPORT_SCRIPT = '''-- TELEPORT TO MOUSE
local p=game.Players.LocalPlayer
local mouse=p:GetMouse()
mouse.Button1Down:Connect(function()
local c=p.Character
local r=c and c:FindFirstChild("HumanoidRootPart")
if r and mouse.Hit then r.CFrame=CFrame.new(mouse.Hit.Position)end
end)
print("Click to teleport")'''

SILENT_SCRIPT = '''-- SILENT AIM
local p=game.Players.LocalPlayer
local cam=workspace.CurrentCamera
local uis=game:GetService("UserInputService")
local mouse=p:GetMouse()
local function getTarget()
local closest,cd=nil,300
local mp=uis:GetMouseLocation()
for _,pl in ipairs(game.Players:GetPlayers())do
if pl~=p then
local c=pl.Character
if c and c:FindFirstChild("Humanoid")and c.Humanoid.Health>0 then
local part=c:FindFirstChild("HumanoidRootPart")or c:FindFirstChild("Head")
if part then
local pos,on=cam:WorldToViewportPoint(part.Position)
if on then
local dist=(Vector2.new(pos.X,pos.Y)-mp).Magnitude
if dist<cd then cd=dist closest=pl end
end
end
end
end
end
return closest
end
hookfunction(mouse.Hit,function()
local target=getTarget()
if target and target.Character then
local part=target.Character:FindFirstChild("HumanoidRootPart")or target.Character:FindFirstChild("Head")
if part then return CFrame.new(part.Position)end
end
return mouse.Hit
end)
print("Silent aim loaded")'''

FLYNOCLIP_SCRIPT = '''-- FLY + NO CLIP
local p=game.Players.LocalPlayer
local uis=game:GetService("UserInputService")
local fly=false
local noclip=true
local bv,bg
game:GetService("RunService").Stepped:Connect(function()
if noclip then
local c=p.Character
if c then
for _,part in ipairs(c:GetDescendants())do
if part:IsA("BasePart")then part.CanCollide=false end
end
end
end
end)
uis.JumpRequest:Connect(function()
if not fly then
fly=true
local c=p.Character or p.CharacterAdded:Wait()
bv=Instance.new("BodyVelocity")
bv.MaxForce=Vector3.new(1,1,1)*1e5
bv.Velocity=Vector3.new(0,50,0)
bv.Parent=c.HumanoidRootPart
bg=Instance.new("BodyGyro")
bg.MaxTorque=Vector3.new(1,1,1)*1e5
bg.Parent=c.HumanoidRootPart
c.Humanoid.PlatformStand=true
game:GetService("RunService").RenderStepped:Connect(function()
if not fly then return end
local m=Vector3.new(
(uis:IsKeyDown(Enum.KeyCode.D)and 1 or 0)-(uis:IsKeyDown(Enum.KeyCode.A)and 1 or 0),
(uis:IsKeyDown(Enum.KeyCode.Space)and 1 or 0)-(uis:IsKeyDown(Enum.KeyCode.LeftShift)and 1 or 0),
(uis:IsKeyDown(Enum.KeyCode.S)and 1 or 0)-(uis:IsKeyDown(Enum.KeyCode.W)and 1 or 0)
)
if m.Magnitude>0 then m=m.Unit*85 end
if bv then bv.Velocity=m end
end)
else
fly=false
if bv then bv:Destroy()end
if bg then bg:Destroy()end
if c then c.Humanoid.PlatformStand=false end
end
end)
print("Fly+NoClip loaded")'''

BOXESP_SCRIPT = '''-- BOX ESP
local p=game.Players.LocalPlayer
local cam=workspace.CurrentCamera
local boxes={}
local function createBox(pl)
local box=Drawing.new("Square")
box.Thickness=2
box.Color=Color3.fromRGB(255,0,0)
box.Filled=false
boxes[pl]=box
end
game:GetService("RunService").RenderStepped:Connect(function()
for _,pl in ipairs(game.Players:GetPlayers())do
if pl~=p then
if not boxes[pl]then createBox(pl)end
local c=pl.Character
if c and c:FindFirstChild("HumanoidRootPart")then
local pos,on=cam:WorldToViewportPoint(c.HumanoidRootPart.Position)
if on then
local size=100/(pos.Z+1)
boxes[pl].Visible=true
boxes[pl].Size=Vector2.new(size*1.5,size*2)
boxes[pl].Position=Vector2.new(pos.X-boxes[pl].Size.X/2,pos.Y-boxes[pl].Size.Y)
else
boxes[pl].Visible=false
end
else
boxes[pl].Visible=false
end
end
end
end)
print("Box ESP loaded")'''

def get_script(prompt):
    p = prompt.lower()
    
    if "fly" in p and ("noclip" in p or "no clip" in p):
        return FLYNOCLIP_SCRIPT
    if "box" in p and "esp" in p:
        return BOXESP_SCRIPT
    if "silent" in p:
        return SILENT_SCRIPT
    if "kill" in p or "aura" in p:
        nums = re.findall(r'\d+', p)
        range_val = nums[0] if nums else "20"
        return KILLAURA_SCRIPT.replace("{range}", range_val)
    if "speed" in p:
        nums = re.findall(r'\d+', p)
        speed_val = nums[0] if nums else "50"
        return SPEED_SCRIPT.replace("{speed}", speed_val)
    if "fly" in p:
        return FLY_SCRIPT
    if "god" in p or "immortal" in p:
        return GOD_SCRIPT
    if "aimbot" in p:
        return AIMBOT_SCRIPT
    if "esp" in p:
        return ESP_SCRIPT
    if "jump" in p:
        return JUMP_SCRIPT
    if "farm" in p:
        return FARM_SCRIPT
    if "noclip" in p or "no clip" in p:
        return NOCLIP_SCRIPT
    if "teleport" in p:
        return TELEPORT_SCRIPT
    
    return f'''-- SCRIPT: {prompt}
print("Script for: {prompt}")
print("Try: fly, god, aimbot, silent, esp, speed 50, jump, farm, noclip, teleport, kill aura")'''

# ========== BOT EVENTS ==========
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Loaded {len(warnings)} warning records')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=AUTO_ROLE_NAME)
    if role:
        await member.add_roles(role)

# ========== SCRIPT COMMAND ==========
@bot.command(name='genscript', aliases=['script', 'make'])
async def genscript(ctx, *, prompt: str):
    script = get_script(prompt)
    if len(script) > 1900:
        file = discord.File(fp=bytes(script, 'utf-8'), filename=f"script.lua")
        await ctx.send(f'📜 **Script for:** {prompt}', file=file)
    else:
        await ctx.send(f'📜 **Script for:** {prompt}\n```lua\n{script}\n```')

# ========== MODERATION ==========
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason='No reason provided'):
    await member.kick(reason=reason)
    await ctx.send(f'✅ Kicked {member.mention} | Reason: {reason}')
    await log(ctx, f'🦵 {member} was kicked by {ctx.author} | Reason: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='No reason provided'):
    await member.ban(reason=reason)
    await ctx.send(f'✅ Banned {member.mention} | Reason: {reason}')
    await log(ctx, f'🔨 {member} was banned by {ctx.author} | Reason: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, name):
    banned = [entry async for entry in ctx.guild.bans()]
    for entry in banned:
        if entry.user.name == name:
            await ctx.guild.unban(entry.user)
            await ctx.send(f'✅ Unbanned {entry.user.mention}')
            return
    await ctx.send('User not found in ban list')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason='No reason provided'):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not role:
        role = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f'✅ Muted {member.mention} | Reason: {reason}')
    await log(ctx, f'🔇 {member} was muted by {ctx.author} | Reason: {reason}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f'✅ Unmuted {member.mention}')
    else:
        await ctx.send(f'{member.mention} is not muted')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    amount = min(amount, 100)
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'✅ Cleared {amount} messages', delete_after=3)

# ========== WARNINGS ==========
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason='No reason provided'):
    global warnings
    uid = str(member.id)
    if uid not in warnings:
        warnings[uid] = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warnings[uid].append({'reason': reason, 'mod': str(ctx.author), 'date': timestamp})
    save_warnings()
    count = len(warnings[uid])
    await ctx.send(f'⚠️ {member.mention} warned | Reason: {reason} | Total: {count}')
    await log(ctx, f'⚠️ {member} warned by {ctx.author} | Reason: {reason} | Total: {count}')

@bot.command()
async def warnings(ctx, member: discord.Member):
    uid = str(member.id)
    if uid not in warnings or not warnings[uid]:
        await ctx.send(f'{member.mention} has no warnings')
        return
    msg = f'**⚠️ Warnings for {member.name}**\n\n'
    for i, w in enumerate(warnings[uid], 1):
        msg += f'`{i}.` **Reason:** {w["reason"]}\n   **Mod:** {w["mod"]}\n   **Date:** {w["date"]}\n\n'
    await ctx.send(msg[:2000])

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearwarnings(ctx, member: discord.Member):
    global warnings
    uid = str(member.id)
    if uid in warnings:
        del warnings[uid]
        save_warnings()
        await ctx.send(f'✅ Cleared warnings for {member.mention}')
        await log(ctx, f'{ctx.author} cleared warnings for {member}')
    else:
        await ctx.send(f'{member.mention} has no warnings')

# ========== ROLES ==========
@bot.command()
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f'✅ Gave {role.name} to {member.mention}')
        await log(ctx, f'{ctx.author} gave {role.name} to {member}')
    else:
        await ctx.send(f'Role "{role_name}" not found')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.remove_roles(role)
        await ctx.send(f'✅ Removed {role.name} from {member.mention}')
        await log(ctx, f'{ctx.author} removed {role.name} from {member}')
    else:
        await ctx.send(f'Role "{role_name}" not found')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def createrole(ctx, *, role_name):
    role = await ctx.guild.create_role(name=role_name)
    await ctx.send(f'✅ Created role: {role.mention}')
    await log(ctx, f'{ctx.author} created role {role_name}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def deleterole(ctx, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await role.delete()
        await ctx.send(f'✅ Deleted role: {role_name}')
        await log(ctx, f'{ctx.author} deleted role {role_name}')
    else:
        await ctx.send(f'Role "{role_name}" not found')

@bot.command()
async def roles(ctx):
    roles = [r.mention for r in ctx.guild.roles if r.name != "@everyone"]
    await ctx.send(f'📋 **Roles:** {" ".join(roles)}' if roles else 'No roles found')

# ========== TICKETS ==========
@bot.command()
async def ticket(ctx, *, reason='No reason provided'):
    category = discord.utils.get(ctx.guild.categories, name=TICKET_CATEGORY)
    if not category:
        category = await ctx.guild.create_category(TICKET_CATEGORY)
    channel = await ctx.guild.create_text_channel(
        f'ticket-{ctx.author.name}',
        category=category
    )
    await channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    embed = discord.Embed(title='🎫 New Ticket', description=f'Reason: {reason}', color=0x00ff00)
    embed.set_footer(text=f'Opened by {ctx.author} | Type !closeticket to close')
    await channel.send(ctx.author.mention, embed=embed)
    await ctx.send(f'✅ Ticket created: {channel.mention}')

@bot.command()
@commands.has_permissions(manage_channels=True)
async def closeticket(ctx):
    if 'ticket-' in ctx.channel.name:
        await ctx.send('🔒 Closing ticket...')
        await asyncio.sleep(2)
        await ctx.channel.delete()
    else:
        await ctx.send('This is not a ticket channel')

# ========== LOG HELPER ==========
async def log(ctx, message):
    channel = discord.utils.get(ctx.guild.text_channels, name=LOG_CHANNEL)
    if channel:
        embed = discord.Embed(title='📋 Mod Log', description=message, color=0x5865F2, timestamp=datetime.now())
        await channel.send(embed=embed)

# ========== ERROR HANDLING ==========
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You do not have permission to use this command')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send('❌ Member not found')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Missing required argument')
    else:
        await ctx.send(f'❌ Error: {str(error)}')

# ========== RUN BOT WITH TOKEN FROM ENVIRONMENT ==========
bot.run(os.environ.get('TOKEN'))
