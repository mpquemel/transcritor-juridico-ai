# Transcritor Jurídico por IA

Aplicação desktop para transcrição e formatação automatizada de depoimentos jurídicos no padrão MPRJ (Ministério Público do Rio de Janeiro).

## 🎯 Objetivo

Automatizar o fluxo de trabalho de transcrição de documentos jurídicos, garantindo:
- **Precisão**: Usando modelos de IA state-of-the-art (Whisper, Groq)
- **Padronização**: Formatação conforme normas do MPRJ
- **Eficiência**: Redução drástica no tempo de processamento
- **Conformidade**: Alinhamento com normas de sigilo e procedimentos legais

## 🚀 Funcionalidades

### 1. Motor de Transcrição
- 🎙️ **Whisper Local**: Transcrição offline usando OpenAI Whisper
- ⚡ **Groq API**: Transcrição ultra-rápida via API Groq (whisper-large-v3-turbo)
- 🔄 **Extração de Áudio**: Suporte a vídeos (MP4, AVI, MKV) e áudios (MP3, WAV, M4A)

### 2. Motor de IA (Formatação Jurídica)
Suporte a múltiplos provedores de LLM:
- 🤖 Google Gemini
- 🤖 OpenAI
- 🤖 OpenRouter
- 🤖 Ollama (Local)

### 3. Pós-Processamento
- 🧹 Limpeza automática de textos
- 📄 Consolidação de transcrições
- 📝 Geração de documentos DOCX formatados

### 4. Interface Gráfica
- 💻 GUI em wxPython
- 🎨 Interface acessível e intuitiva
- ⚙️ Gerenciamento de configurações

## 📋 Requisitos

### Sistema
- Windows 10/11 ( desenvolvido e testado)
- Python 3.8+
- FFmpeg (para extração de áudio)

### Dependências Python
```bash
pip install wxPython
pip install openai-whisper
pip install python-docx
pip install requests
```

### APIs Opcionais
- **Groq API Key**: Para transcrição rápida (obter em https://console.groq.com)
- **Google Gemini**: Para formatação (obter em https://aistudio.google.com)
- **OpenAI/OpenRouter**: Alternativas para formatação

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/mpquemel/transcritor-juridico-ai.git
cd transcritor-juridico-ai
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python main.py
```

## 📖 Como Usar

1. **Configure o Motor de Transcrição**:
   - Insira sua chave API da Groq (opcional, mas recomendado)
   - Ou deixe em branco para usar Whisper local (mais lento)

2. **Configure o Provedor de IA**:
   - Selecione o provedor (Google Gemini, OpenAI, etc.)
   - Insira a chave API correspondente
   - Valide a conexão

3. **Selecione os Arquivos**:
   - Pasta de entrada (vídeos/áudios)
   - Pasta de saída (documentos DOCX)

4. **Inicie o Processamento**:
   - Clique em "Iniciar Processamento"
   - Acompanhe o progresso na barra de status

## 🏗️ Estrutura do Projeto

```
transcritor-juridico-ai/
├── main.py              # Interface e orquestração
├── audio_processor.py   # Extração e transcrição
├── text_cleaner.py      # Limpeza de textos
├── llm_handler.py       # Integração com LLMs
├── docx_builder.py      # Geração de documentos
├── config_manager.py    # Configurações
├── requirements.txt     # Dependências
└── LICENSE              # Licença GPL-3.0
```

## 👨‍💻 Autor

**Melhym Pereira Quemel**
- Advogado, Mestre em Direito (UNESA)
- Graduando em Engenharia de Software
- Certificado NVDA Expert 2025 (Nº 00756)
- Email: mpquemel@gmail.com

## 📄 Licença

Este projeto está licenciado sob a licença GPL-3.0 - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Notas

- Desenvolvido originalmente para uso no MPRJ
- Requer validação jurídica antes do uso em produção
- Dados sensíveis devem ser tratados conforme LGPD

---

**Desenvolvido com 💙 e ☕ para tornar a justiça mais eficiente.**
