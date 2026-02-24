# Criado por Melhym Quemel <mpquemel@gmail.com>

import wx
import os
import threading
import time
import winsound
from config_manager import load_config, save_config
from audio_processor import extract_audio, transcribe_audio_local, transcribe_audio_groq
from text_cleaner import consolidate_transcriptions
from llm_handler import process_with_llm
from docx_builder import save_to_docx

class TranscritorFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Transcritor Jurídico por IA', size=(850, 800))
        self.config = load_config()
        self.input_dir = ""
        self.output_dir = ""
        self.is_processing = False
        
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.build_ui()
        self.panel.SetSizer(self.vbox)
        self.Centre()
        self.Show()
        
        self.update_api_field_label(None)
        self.provider_combo.SetFocus()

    def build_ui(self):
        # --- Seção 0: Transcrição Rápida Groq ---
        groq_box = wx.StaticBox(self.panel, label="1. Motor de Transcrição de Áudio (Opcional para Velocidade Máxima)")
        groq_sizer = wx.StaticBoxSizer(groq_box, wx.VERTICAL)
        
        groq_hbox = wx.BoxSizer(wx.HORIZONTAL)
        groq_label = wx.StaticText(self.panel, label="Chave API da Groq (Deixe em branco para usar o Whisper Local lento):")
        self.groq_entry = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        self.groq_entry.SetValue(self.config.get("groq_api", ""))
        groq_hbox.Add(groq_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        groq_hbox.Add(self.groq_entry, proportion=1)
        groq_sizer.Add(groq_hbox, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(groq_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        # --- Seção 1: Provedor e Validação LLM ---
        api_box = wx.StaticBox(self.panel, label="2. Motor de Inteligência Artificial (Formatação)")
        api_sizer = wx.StaticBoxSizer(api_box, wx.VERTICAL)
        
        prov_hbox = wx.BoxSizer(wx.HORIZONTAL)
        prov_label = wx.StaticText(self.panel, label="Selecione o Provedor:")
        providers = ["Google Gemini", "OpenAI", "OpenRouter", "Ollama (Local)"]
        self.provider_combo = wx.ComboBox(self.panel, choices=providers, style=wx.CB_READONLY)
        self.provider_combo.SetValue(self.config.get("provider", "Google Gemini"))
        self.provider_combo.Bind(wx.EVT_COMBOBOX, self.update_api_field_label)
        prov_hbox.Add(prov_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        prov_hbox.Add(self.provider_combo, proportion=1)
        api_sizer.Add(prov_hbox, flag=wx.EXPAND | wx.ALL, border=5)

        api_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.api_label = wx.StaticText(self.panel, label="Chave API:")
        self.api_entry = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        api_hbox.Add(self.api_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        api_hbox.Add(self.api_entry, proportion=1)
        api_sizer.Add(api_hbox, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.btn_validate = wx.Button(self.panel, label="Validar Conexão e Listar Modelos")
        self.btn_validate.Bind(wx.EVT_BUTTON, self.validate_and_fetch_models)
        api_sizer.Add(self.btn_validate, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        mod_hbox = wx.BoxSizer(wx.HORIZONTAL)
        mod_label = wx.StaticText(self.panel, label="Modelo Disponível:")
        self.model_combo = wx.ComboBox(self.panel, style=wx.CB_READONLY)
        mod_hbox.Add(mod_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        mod_hbox.Add(self.model_combo, proportion=1)
        api_sizer.Add(mod_hbox, flag=wx.EXPAND | wx.ALL, border=5)

        self.vbox.Add(api_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # --- Seção 2: Seleção de Pastas ---
        folder_box = wx.StaticBox(self.panel, label="3. Seleção de Pastas (Pasta Inteligente aceita .mp4, .mp3, .srt ou .txt)")
        folder_sizer = wx.StaticBoxSizer(folder_box, wx.VERTICAL)
        
        self.btn_input = wx.Button(self.panel, label="Selecionar Pasta de Entrada")
        self.btn_input.Bind(wx.EVT_BUTTON, self.select_input)
        folder_sizer.Add(self.btn_input, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.btn_output = wx.Button(self.panel, label="Selecionar Pasta de Destino")
        self.btn_output.Bind(wx.EVT_BUTTON, self.select_output)
        folder_sizer.Add(self.btn_output, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.vbox.Add(folder_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # --- Seção 3: Execução ---
        self.btn_start = wx.Button(self.panel, label="4. Iniciar Processamento Mágico")
        self.btn_start.Bind(wx.EVT_BUTTON, self.start_processing_thread)
        self.btn_start.Disable() 
        self.vbox.Add(self.btn_start, flag=wx.EXPAND | wx.ALL, border=10)
        
        self.status_label = wx.StaticText(self.panel, label="Status: Aguardando configuração.")
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.status_label.SetFont(font)
        self.vbox.Add(self.status_label, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

    def update_api_field_label(self, event):
        provider = self.provider_combo.GetValue()
        if provider == "Google Gemini":
            self.api_label.SetLabel("Chave API do Google Gemini:")
            self.api_entry.SetValue(self.config.get("gemini_api", ""))
            self.api_entry.SetWindowStyleFlag(wx.TE_PASSWORD)
        elif provider == "OpenAI":
            self.api_label.SetLabel("Chave API da OpenAI:")
            self.api_entry.SetValue(self.config.get("openai_api", ""))
            self.api_entry.SetWindowStyleFlag(wx.TE_PASSWORD)
        elif provider == "OpenRouter":
            self.api_label.SetLabel("Chave API do OpenRouter:")
            self.api_entry.SetValue(self.config.get("openrouter_api", ""))
            self.api_entry.SetWindowStyleFlag(wx.TE_PASSWORD)
        elif provider == "Ollama (Local)":
            self.api_label.SetLabel("URL do Ollama Local:")
            self.api_entry.SetValue(self.config.get("ollama_url", "http://localhost:11434/v1"))
            self.api_entry.SetWindowStyleFlag(wx.TE_LEFT)
            
        self.api_entry.Refresh()
        self.model_combo.Clear()
        self.btn_start.Disable()
        self.update_status("Provedor alterado. Por favor, valide a conexão.")

    def save_current_api_config(self):
        provider = self.provider_combo.GetValue()
        api_val = self.api_entry.GetValue()
        self.config["provider"] = provider
        
        if provider == "Google Gemini": self.config["gemini_api"] = api_val
        elif provider == "OpenAI": self.config["openai_api"] = api_val
        elif provider == "OpenRouter": self.config["openrouter_api"] = api_val
        elif provider == "Ollama (Local)": self.config["ollama_url"] = api_val
        
        save_config(self.config)

    def validate_and_fetch_models(self, event):
        self.save_current_api_config()
        self.update_status("Validando credenciais e buscando modelos...")
        self.btn_validate.Disable()
        self.model_combo.Clear()
        threading.Thread(target=self._fetch_models_thread, daemon=True).start()

    def _fetch_models_thread(self):
        provider = self.provider_combo.GetValue()
        api_val = self.api_entry.GetValue().strip()
        models = []
        error_msg = None
        
        try:
            if not api_val:
                raise ValueError("O campo de Chave API ou URL não pode estar vazio.")

            if provider == "Google Gemini":
                import google.generativeai as genai
                genai.configure(api_key=api_val)
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        models.append(m.name.replace('models/', ''))
                        
            elif provider == "OpenAI":
                from openai import OpenAI
                client = OpenAI(api_key=api_val)
                models = [m.id for m in client.models.list().data]
                models.sort()
                
            elif provider == "OpenRouter":
                from openai import OpenAI
                client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_val)
                models = [m.id for m in client.models.list().data]
                models.sort()
                
            elif provider == "Ollama (Local)":
                from openai import OpenAI
                url = api_val.rstrip('/')
                if not url.endswith('/v1'):
                    url += '/v1'
                client = OpenAI(base_url=url, api_key="ollama")
                models = [m.id for m in client.models.list().data]
                models.sort()
                
        except Exception as e:
            error_msg = str(e)
            
        wx.CallAfter(self._on_models_fetched, models, error_msg)

    def _on_models_fetched(self, models, error_msg):
        self.btn_validate.Enable()
        
        if error_msg:
            self.update_status("Erro na validação.")
            wx.MessageBox(f"Falha ao conectar:\n{error_msg}", "Erro de Conexão", wx.OK | wx.ICON_ERROR)
            self.api_entry.SetFocus()
        elif not models:
            self.update_status("Conectado, mas nenhum modelo encontrado.")
            wx.MessageBox("A conexão foi bem sucedida, mas não há modelos disponíveis.", "Atenção", wx.OK | wx.ICON_WARNING)
        else:
            self.model_combo.AppendItems(models)
            saved_model = self.config.get("model", "")
            if saved_model in models:
                self.model_combo.SetValue(saved_model)
            else:
                self.model_combo.SetValue(models[0])
                
            self.update_status("Modelos listados com sucesso. Pronto para iniciar.")
            winsound.MessageBeep(winsound.MB_OK)
            self.btn_start.Enable()
            self.model_combo.SetFocus()

    def select_input(self, event):
        with wx.DirDialog(self, "Selecione a pasta de entrada", style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.input_dir = dlg.GetPath()
                self.update_status("Pasta de entrada selecionada.")
        self.btn_input.SetFocus()

    def select_output(self, event):
        with wx.DirDialog(self, "Selecione a pasta para salvar os resultados", style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.output_dir = dlg.GetPath()
                self.update_status("Pasta de saída selecionada.")
        self.btn_output.SetFocus()

    def update_status(self, message):
        wx.CallAfter(self.status_label.SetLabel, f"Status: {message}")

    def progress_beep_thread(self):
        while self.is_processing:
            winsound.Beep(1000, 100) 
            time.sleep(5)

    def start_processing_thread(self, event):
        self.config["model"] = self.model_combo.GetValue()
        self.config["groq_api"] = self.groq_entry.GetValue().strip()
        save_config(self.config)
        
        if not self.input_dir or not self.output_dir:
            wx.MessageBox("Selecione as pastas antes de iniciar.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
            
        self.btn_start.Disable()
        self.btn_validate.Disable()
        self.is_processing = True
        
        threading.Thread(target=self.progress_beep_thread, daemon=True).start()
        threading.Thread(target=self.process_pipeline, daemon=True).start()

    def process_pipeline(self):
        try:
            all_files = os.listdir(self.input_dir)
            if not all_files:
                raise ValueError("A pasta de entrada está vazia.")

            file_groups = {}
            for f in all_files:
                base_name, ext = os.path.splitext(f)
                ext = ext.lower()
                if base_name not in file_groups:
                    file_groups[base_name] = {}
                file_groups[base_name][ext] = os.path.join(self.input_dir, f)

            transcriptions = {}
            
            for base_name, exts in file_groups.items():
                self.update_status(f"Processando grupo: {base_name}...")
                
                # Regra 1: Se tem TXT ou SRT, pega direto (pula áudio e vídeo)
                if '.txt' in exts or '.srt' in exts:
                    text_file = exts.get('.txt') or exts.get('.srt')
                    self.update_status(f"Lendo legenda existente: {os.path.basename(text_file)}")
                    with open(text_file, 'r', encoding='utf-8') as f:
                        transcriptions[base_name] = f.read()
                    continue

                # Regra 2: Se não tem legenda, mas tem MP3 ou WAV
                audio_path = exts.get('.mp3') or exts.get('.wav')
                
                # Regra 3: Se não tem áudio, mas tem Vídeo, extrai o áudio
                if not audio_path and ('.mp4' in exts or '.mkv' in exts or '.avi' in exts):
                    video_file = exts.get('.mp4') or exts.get('.mkv') or exts.get('.avi')
                    self.update_status(f"Extraindo áudio de: {os.path.basename(video_file)}")
                    audio_path = extract_audio(video_file, self.output_dir)

                # Se conseguimos um áudio (via regra 2 ou 3), transcrevemos
                if audio_path:
                    if self.config.get("groq_api"):
                        self.update_status(f"Transcrição Ultra Rápida (Groq) de: {os.path.basename(audio_path)}")
                        srt_path, raw_text = transcribe_audio_groq(audio_path, self.output_dir, self.config["groq_api"])
                    else:
                        self.update_status(f"Transcrevendo Local (Whisper) de: {os.path.basename(audio_path)} Aguarde...")
                        srt_path, raw_text = transcribe_audio_local(audio_path, self.output_dir)
                    
                    transcriptions[base_name] = raw_text

            if not transcriptions:
                raise ValueError("Nenhum arquivo válido (.mp4, .mp3, .txt, .srt) encontrado para processar.")

            self.update_status("Consolidando e formatando os textos no padrão Jurídico...")
            consolidated_text = consolidate_transcriptions(transcriptions)
            formatted_result = process_with_llm(consolidated_text, self.config)
            
            self.update_status("Gerando documento Word final...")
            save_to_docx(formatted_result, self.output_dir)
            
            self.is_processing = False
            winsound.MessageBeep(winsound.MB_OK)
            self.update_status("Concluído com Sucesso!")
            wx.CallAfter(wx.MessageBox, "Processamento inteligente finalizado! Confira a pasta de saída.", "Sucesso", wx.OK | wx.ICON_INFORMATION)
            
        except Exception as e:
            self.is_processing = False
            winsound.MessageBeep(winsound.MB_ICONHAND)
            self.update_status("Erro durante o processamento.")
            wx.CallAfter(wx.MessageBox, str(e), "Erro na Execução", wx.OK | wx.ICON_ERROR)
        finally:
            self.is_processing = False
            wx.CallAfter(self.btn_start.Enable)
            wx.CallAfter(self.btn_validate.Enable)
            wx.CallAfter(self.btn_start.SetFocus)

if __name__ == '__main__':
    app = wx.App(False)
    frame = TranscritorFrame()
    app.MainLoop()