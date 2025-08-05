import whisper
from openai import OpenAI
from dotenv import load_dotenv
from pytubefix import YouTube
from pytubefix.cli import on_progress
from ffmpeg import FFmpeg
import os

load_dotenv()

url = input('URL > ')
filename = r'./arquivos/audio.wav'
arquivos = r'./arquivos'

def mkdir():
    if not os.path.exists(arquivos):
        os.mkdir(arquivos)

def audio(url):
    yt = YouTube(url,on_progress_callback=on_progress)
    ys = yt.streams[0].url
    
    if os.path.exists(filename):
        os.remove(filename)
    
    ffmpeg = (
        FFmpeg()
        .input(ys)
        .output(filename)
    )
    ffmpeg.execute()

def transcrever():
    model = whisper.load_model('base')
    result = model.transcribe(filename)
    return result["text"]

def resumir(file='./arquivos/resumo.md'):
    assistent = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv('OPENROUTER_API_KEY'),
    )
    
    texto = transcrever()
    resumo_video = assistent.chat.completions.create(
        model="qwen/qwen3-coder:free",
        messages=[
            {
                "role" : "system",
                "content" : "você é um assistente que faz resumos de video no youtube e responda em formatação markdown"
            },
            {
                "role" : "user",
                "content" : f"faça um resumo do seguinte video {texto}"
            }
        ]
    )
    
    with open(file,'w+',encoding='utf-8') as resumo:
        resumo.write(resumo_video.choices[0].message.content)

if __name__ == '__main__':
    mkdir()
    audio(url)
    resumir()