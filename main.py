from discord.ext import commands
import requests
import os

import speech_recognition as sr
from pydub import AudioSegment

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
  print(client.user)

@client.command()
async def tts(ctx):
  # check for message reference
  if ctx.message.reference is not None:
    # only respond if the reply was within last 100 messages
    async for message in ctx.message.channel.history(limit=100):
      if message.id == ctx.message.reference.message_id:
        if message.attachments != []:
          # loop through attachments
          for attachment in message.attachments:
            if '.mp3' in attachment.url:
              with open('audio.mp3', 'wb') as file:
                file.write(requests.get(attachment.url).content)
    
    # convert mp3 file to wav  
    src=('audio.mp3')
    sound = AudioSegment.from_mp3(src)
    sound.export('audio.wav', format="wav")
    
    file_audio = sr.AudioFile('audio.wav')
    
    # use the audio file as the audio source                                        
    r = sr.Recognizer()
    with file_audio as source:
      audio_text = r.record(source)

    await ctx.send(r.recognize_google(audio_text))

client.run(os.environ['TOKEN'])
