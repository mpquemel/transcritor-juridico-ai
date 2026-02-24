# Criado por Melhym Quemel <mpquemel@gmail.com>

import os
import subprocess
from groq import Groq

def extract_audio(video_path, output_dir):
    filename = os.path.basename(video_path)
    name_only = os.path.splitext(filename)[0]
    audio_path = os.path.join(output_dir, f"{name_only}.mp3")
    
    # Extrai o áudio otimizado e leve (Mono, 16kHz, 32k)
    cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-ar", "16000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "32k", audio_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_path

def transcribe_audio_local(audio_path, output_dir):
    """Usa o Whisper instalado na máquina do usuário (Processamento Lento/Offline)"""
    cmd = [
        "whisper", audio_path, 
        "--language", "pt", 
        "--model", "small",
        "--output_format", "srt", 
        "--output_dir", output_dir
    ]
    subprocess.run(cmd)
    
    name_only = os.path.splitext(os.path.basename(audio_path))[0]
    srt_path = os.path.join(output_dir, f"{name_only}.srt")
    
    with open(srt_path, "r", encoding="utf-8") as f:
        return srt_path, f.read()

def transcribe_audio_groq(audio_path, output_dir, groq_api_key):
    """Usa a API da Groq para transcrição ultra veloz do Whisper Large V3 e converte para SRT"""
    client = Groq(api_key=groq_api_key)
    name_only = os.path.splitext(os.path.basename(audio_path))[0]
    srt_path = os.path.join(output_dir, f"{name_only}.srt")
    
    # Pede o formato verbose_json que traz os timestamps
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(audio_path), file),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            language="pt"
        )
        
    # Função interna para transformar os segundos do JSON em formato de hora do SRT
    def format_timestamp(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int(round((seconds - int(seconds)) * 1000))
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
        
    srt_content = ""
    
    # Acessa os segmentos retornados pela Groq
    segments = getattr(transcription, 'segments', [])
    if not segments and isinstance(transcription, dict):
        segments = transcription.get('segments', [])
        
    # Constrói o texto do arquivo SRT linha por linha
    for i, segment in enumerate(segments, start=1):
        start = segment['start'] if isinstance(segment, dict) else segment.start
        end = segment['end'] if isinstance(segment, dict) else segment.end
        text = segment['text'] if isinstance(segment, dict) else segment.text
        
        start_str = format_timestamp(start)
        end_str = format_timestamp(end)
        srt_content += f"{i}\n{start_str} --> {end_str}\n{text.strip()}\n\n"
        
    # Fallback de segurança caso a API da Groq não retorne segmentos
    if not srt_content:
        srt_content = getattr(transcription, 'text', str(transcription))
        
    # Salva o SRT físico para rastreabilidade do usuário
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    return srt_path, srt_content