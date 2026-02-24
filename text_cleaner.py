# Criado por Melhym Quemel <mpquemel@gmail.com>

import re

def clean_srt_text(srt_content):
    # Remove numeração de blocos do SRT
    text = re.sub(r'^\d+$\n', '', srt_content, flags=re.MULTILINE)
    # Remove marcações de tempo (ex: 00:00:00,000 --> 00:00:00,000)
    text = re.sub(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$\n', '', text, flags=re.MULTILINE)
    # Remove linhas em branco extras
    text = re.sub(r'\n+', '\n', text).strip()
    return text

def consolidate_transcriptions(transcriptions_dict):
    consolidated = ""
    for filename, text in transcriptions_dict.items():
        clean_text = clean_srt_text(text)
        consolidated += f"\n\n--- INÍCIO DO DEPOIMENTO: {filename} ---\n\n"
        consolidated += clean_text
        consolidated += f"\n\n--- FIM DO DEPOIMENTO: {filename} ---\n"
    return consolidated