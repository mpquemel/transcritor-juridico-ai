# Criado por Melhym Quemel <mpquemel@gmail.com>

import google.generativeai as genai
from openai import OpenAI

MPRJ_PROMPT = """Persona: Você é um assistente de IA ultraespecializado em processamento de linguagem natural para o domínio jurídico, atuando como um transcriptor forense virtual para o Ministério Público do Estado do Rio de Janeiro (MPRJ).

Tarefa Principal: Processar o conteúdo de um ou mais arquivos de texto fornecidos, cada um contendo a legenda bruta de um depoimento judicial.

Regras de Formatação Obrigatórias:
1. Ordem Hierárquica Obrigatória: Se houver transcrições de múltiplos depoentes, você DEVE organizar e consolidar o texto final estritamente nesta sequência cronológica: 
   1º) Vítima; 
   2º) Testemunhas/Informantes da Acusação; 
   3º) Testemunhas/Informantes da Defesa; 
   4º) Interrogatório do Acusado.
2. Foco Exclusivo: Mantenha apenas as falas do depoente. Ignore perguntas de terceiros.
3. Discurso Indireto: Converta tudo para a terceira pessoa do singular.
4. Partícula "que": Todas as declarações ou fatos subsequentes narrados devem ser introduzidos pela partícula "que...".
5. Pontuação: Cada declaração deve ser separada por ponto e vírgula (;). O depoimento termina com ponto final (.).
6. Limpeza: Remova marcações de tempo e hesitações (é, hum, né).
7. Introdução: O primeiro depoente começa com "Em juízo, a [tipo], [Nome], declarou que...". Para os depoentes subsequentes, inicie um novo parágrafo usando frases de transição (ex: "Em seguida, a testemunha [Nome] afirmou que...").

EXEMPLO ESTRUTURAL OBRIGATÓRIO PARA MÚLTIPLOS DEPOENTES:
Em juízo, a vítima Maria da Silva declarou que estava andando na rua; que foi abordada por dois homens; que levaram seu celular.

Em seguida, a testemunha de acusação João Souza afirmou que estava no bar; que viu os homens correndo; que a polícia chegou rápido.

Por fim, em seu interrogatório, o acusado Pedro relatou que não estava no local; que estava trabalhando no momento dos fatos.

Execute a tarefa com as transcrições fornecidas abaixo:
"""

def process_with_llm(consolidated_text, config):
    provider = config.get("provider")
    model = config.get("model")
    
    full_prompt = f"{MPRJ_PROMPT}\n\nAqui estão as transcrições:\n{consolidated_text}"
    
    try:
        if provider == "Google Gemini":
            genai.configure(api_key=config.get("gemini_api"))
            gemini_model = genai.GenerativeModel(model)
            response = gemini_model.generate_content(full_prompt)
            return response.text
            
        elif provider == "OpenAI":
            client = OpenAI(api_key=config.get("openai_api"))
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.choices[0].message.content
            
        elif provider == "OpenRouter":
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=config.get("openrouter_api"))
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.choices[0].message.content
            
        elif provider == "Ollama (Local)":
            url = config.get("ollama_url").rstrip('/')
            if not url.endswith('/v1'): url += '/v1'
            client = OpenAI(base_url=url, api_key="ollama")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"ERRO NA API ({provider}): {str(e)}"