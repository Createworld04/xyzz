import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
from details import api_id, api_hash, bot_token
from pyrogram.types import User, Message
import os

import requests
bot = Client(
    "Careerwill",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)


@bot.on_message(filters.command(["start"]))
async def start(bot, update):
       await update.reply_text("Hi i am **Careerwill Downloader**.\n\n"
                              "**NOW:-** "
                                       
                                       "Press **/login** to continue..\n\n"
                                     "Bot made by **ACE**" )

ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd"
bc_url = (
    f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
)
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

url="https://elearn.crwilladmin.com/api/v1/"

info= {
 "deviceType":"android",
    "password":"",
    "deviceModel":"Asus ASUS_X00TD",
    "deviceVersion":"Pie(Android 9.0)",
    "email":"",
}

@bot.on_message(filters.command(["login"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**"
    )

    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)

    login_response=requests.post(url+"login-other",info)
    token=login_response.json( )["data"]["token"]
    await editable.edit("**login Successful**")
    await editable.edit("You have these Batches :-\n\n**Batch Name : Batch ID**")
    
    url1 = requests.get("https://elearn.crwilladmin.com/api/v1/comp/my-batch?&token="+token)
    b_data = url1.json()['data']['batchData']

    cool=""
    for data in b_data:
        aa=f"**{data['batchName']}** : ```{data['id']}```\n\n"
        if len(f'{cool}{aa}')>4096:
            await m.reply_text(aa)
            cool =""
        cool+=aa
    await m.reply(cool)

    editable1= await m.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

# topic id url = https://elearn.crwilladmin.com/api/v1/comp/batch-topic/881?type=class&token=d76fce74c161a264cf66b972fd0bc820992fe576
    url2 = requests.get("https://elearn.crwilladmin.com/api/v1/comp/batch-topic/"+raw_text2+"?type=class&token="+token)
    topicid = url2.json()["data"]["batch_topic"]
    await m.reply_text("**Topic Name : Topic ID are :**")
    cool1 = ""
    for data in topicid:
        t_name=(data["topicName"])
        tid = (data["id"])
        hh = f"**{t_name}** : ```{tid}```\n"
        
        if len(f'{cool1}{hh}')>4096:
            await m.reply_text(hh)
            cool1=""
        cool1+=hh
    await m.reply_text(cool1)

    editable2= await m.reply_text("**Now send the Topic ID to Download**")
    input3 = message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    
    
    #gettting all json with diffrent topic id https://elearn.crwilladmin.com/api/v1/comp/batch-detail/881?redirectBy=mybatch&topicId=2324&token=d76fce74c161a264cf66b972fd0bc820992fe57
    
    url3 = "https://elearn.crwilladmin.com/api/v1/comp/batch-detail/"+raw_text2+"?redirectBy=mybatch&topicId="+raw_text3+"&token="+token   
    ff = requests.get(url3)
    vv =ff.json()["data"]["class_list"]["classes"]
    vv.reverse()
    for data in vv:
        vidid = (data["id"])
        lessonName = (data["lessonName"])  
        bcvid = (data["lessonUrl"][0]["link"])
        #print(bcvid)
       
        if bcvid.startswith("62"):
            
            video_response = requests.get(f"{bc_url}/{bcvid}", headers=bc_hdr)
            video = video_response.json()
            video_source = video["sources"][5]
            video_url = video_source["src"]
            #print(video_url)
                
            surl=requests.get("https://elearn.crwilladmin.com/api/v1/livestreamToken?type=brightcove&vid="+vidid+"&token="+token)
            stoken = surl.json()["data"]["token"]
            #print(stoken)
            
            link = video_url+"&bcov_auth="+stoken
            #print(link)

        else:
            link="https://www.youtube.com/embed/"+bcvid
        # await m.reply_text(link)

        editable3= await m.reply_text("**Now send the Resolution**")
        input4 = message = await bot.listen(editable.chat.id)
        raw_text4 = input4.text

        
        ytf=f"bestvideo[height<={raw_text4}]"
        cmd = f'yt-dlp -o "{lessonName}.mp4" -f "{ytf}+bestaudio" "{link}"'
        os.system(cmd)

        filename = f"{lessonName}.mp4"
        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:19 -vframes 1 "{filename}.jpg"', shell=True)
        thumbnail = f"{filename}.jpg"

        await m.reply_video(f"{lessonName}.mp4",caption=lessonName, supports_streaming=True,height=720,width=1280,thumb=thumbnail)
        os.remove(f"{lessonName}.mp4")
        os.remove(f"{filename}.jpg")
        





        
                
        














bot.run()