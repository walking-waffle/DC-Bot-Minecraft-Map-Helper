#導入Discord.py
import discord
from discord.ext import commands
import random

# 開啟intents權限
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client( intents = intents )

def get_help():
    input = "Yo 我是 Minecraft 地圖座標小幫手，以下是我的指令~\n\
        $l：列出所有已記錄座標\n\
        $a 名稱 0 0 0：新增座標\n\
        $d 名稱：刪除座標\n\
        $s 名稱：尋找座標\n\"
    return input

# 輸入字串型別的地區名稱，並回傳是否存在和位置
def IsExistAndReturnIP( target ):
    with open( "position.txt", mode='r', encoding="utf-8" ) as file:
        # 把所有資料讀進list
        dataList = file.readlines()

        # 把list中的元素'name 0 0 0'取出來比對
        for i in range( len(dataList) ):
            # 把元素'name 0 0 0'分成'name'和'0 0 0'
            temp = dataList[i].split( " ", 1 )
            if temp[0] == str(target):
                return True, temp[1]

    return False, "error"

# 輸入目標名稱，將他從txt檔案刪除
def DeletePosition( target ):
    with open( "position.txt", mode='r', encoding="utf-8" ) as file:
        # 把所有資料讀進list
        dataList = file.readlines()

        # 把list中的元素'name 0 0 0'取出來比對
        for i in range( len(dataList) ):
            # 把元素'name 0 0 0'分成'name'和'0 0 0'
            temp = dataList[i].split( " ", 1 )

            # 找到目標並刪除
            if temp[0] == str(target):
                dataList.pop(i)
                break

    # 將檔案寫回
    with open( "position.txt", mode='w', encoding="utf-8" ) as file:
        for i in range( len(dataList) ):
            file.write( dataList[i] )

# 調用event函式庫
@bot.event

# 機器人接收訊息
async def on_message( message ):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == bot.user :
        return
    
    # list
    if message.content.startswith( '$l' ) :
        with open( "position.txt", mode='r', encoding="utf-8" ) as file:
            input = file.read()
            await message.channel.send( input )

    # add
    elif message.content.startswith( '$a' ) :
        inputList = message.content.split( " ", 2 )
        if ( len(inputList) == 1 ):
            await message.channel.send( "Add what?" )
        elif ( len(inputList) == 2 ):
            await message.channel.send( "Where?" )
        else:
            result = inputList[1] + ' ' + inputList[2] + '\n'
            with open( "position.txt", mode='a', encoding="utf-8" ) as file:
                file.write( result )
            
            await message.channel.send( "Success!" )

    # delete
    elif message.content.startswith( '$d' ) :
        find = bool(False)
        targetIP = ""
        inputList = message.content.split( " ", 1 )
        if ( len(inputList) == 1 ):
            await message.channel.send( "Delete what?" )
        else:
            target = inputList[1]
            find, targetIP = IsExistAndReturnIP( target )

        # 有沒找到
        if find == bool(True):
            DeletePosition( target )
            await message.channel.send( "Success!" )
        else:
            await message.channel.send( "Not Found" )

    # search
    elif message.content.startswith( '$s' ) :
        find = bool(False)
        targetIP = ""
        inputList = message.content.split( " ", 1 )
        if ( len(inputList) == 1 ):
            await message.channel.send( "Search what?" )
        else:
            name = inputList[1]
            find, targetIP = IsExistAndReturnIP( name )

        # 有沒找到
        if find == bool(True):
            await message.channel.send( targetIP )
        else:
            await message.channel.send( "Not Found" )

    # help
    elif message.content.startswith( '$h' ) :
        await message.channel.send( get_help() )


# 調用event函式庫
@bot.event

# 機器人啟動
async def on_ready():
    print( '>> Bot is online <<' )

bot.run( [token] )
