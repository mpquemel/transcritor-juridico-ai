# ⚖️ Transcritor Jurídico AI
### Eficiência Operacional e Automação de Depoimentos (Padrão MPRJ)

O **Transcritor Jurídico AI** é uma aplicação desktop projetada para eliminar o gargalo da transcrição manual de depoimentos jurídicos. Focado na precisão e na conformidade normativa, o software automatiza a conversão de áudio/vídeo em documentos formatados, seguindo rigorosamente os padrões do Ministério Público do Rio de Janeiro (MPRJ).

---

## 🎯 O Problema
A transcrição de depoimentos é uma das etapas mais lentas e onerosas do processo jurídico. A digitação manual é propensa a erros, e a formatação de documentos extensos consome horas de produtividade de servidores e advogados, impactando a celeridade processual.

## 💡 A Solução
O sistema implementa um pipeline de processamento de alta fidelidade que combina o estado da arte em reconhecimento de fala com a inteligência de LLMs para limpeza e formatação.

### ✨ Funcionalidades Principais
- **Transcrição Híbrida:** Escolha entre **Whisper Local** (Privacidade Total/Offline) ou **Groq API** (Transcrição Ultra-Rápida).
- **Inteligência de Formatação:** Integração com Google Gemini, OpenAI e Ollama para limpar vícios de linguagem e estruturar o texto no padrão jurídico.
- **Processamento Multimídia:** Extração automática de áudio de diversos formatos de vídeo (MP4, AVI, MKV) e áudio (MP3, WAV, M4A).
- **Geração de Documentos:** Exportação direta para `.docx`, pronta para revisão e assinatura.
- **Interface Acessível:** GUI desenvolvida em wxPython, priorizando a clareza e a navegação eficiente.

---

## 🛠️ Guia de Instalação

### Pré-requisitos
- **FFmpeg:** Necessário para a extração de áudio. [Instruções de instalação](https://ffmpeg.org/download.html).
- **Python 3.8+**

### Instalação
```bash
# Clone o repositório
git clone https://github.com/mpquemel/transcritor-juridico-ai.git
cd transcritor-juridico-ai

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python main.py
```

---

## ⚙️ Fluxo de Operação
`[Arquivo de Áudio/Vídeo]` $\rightarrow$ `[Extração FFmpeg]` $\rightarrow$ `[STT: Whisper/Groq]` $\rightarrow$ `[Limpeza via LLM]` $\rightarrow$ `[DOCX Builder]`

---

## 📜 Licença e Conformidade
Este projeto está licenciado sob a **GPL-3.0**.

**Aviso de Segurança:** Por lidar com depoimentos jurídicos, recomenda-se o uso de modelos locais (Ollama/Whisper) para garantir a conformidade com a LGPD e o sigilo processual.

Desenvolvido por **Melhym Pereira Quemel**.
Sinergia entre a precisão do Direito e a eficiência do Software. ☕
