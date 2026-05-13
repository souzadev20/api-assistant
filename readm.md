# Chatbot Inteligente com Prompt de Contexto (Groq + Flask)

 Este projeto consiste em uma API em Python desenvolvida com Flask que recebe mensagens de texto e gera respostas inteligentes utilizando a infraestrutura da Groq com o modelo Llama 3. O sistema utiliza uma estratégia de engenharia de prompt para simular o comportamento de ferramentas específicas [calendario, calculadora, clima]. A IA analisa o texto do usuário e adapta sua persona de forma nativa e contextualizada através do prompt de sistema.
 
 ## 🧠 Lógica de Funcionamento
 
 O sistema não executa chamadas de código externas (Function Calling). Toda a inteligência de seleção é baseada em regras embutidas no prompt que orientam o Llama 3:
 
 * Contexto de Calendário: Ativado quando o usuário menciona datas, dias da semana ou agendamentos
 * Contexto de Calculadora: Ativado para resolver problemas matemáticos e lógicos numéricos.
 * Contexto de Clima: Ativado para simular interações sobre previsões meteorológicas e temperaturas.

 ## Tecnologias

 * Python 3.14.3
 * Flask: Microframework web para gerenciamento da rota.
 * Groq Cloud SDK: Inferência de linguagem natural em alta velocidade.
 * Llama 3: Modelo de linguagem de código aberto otimizado pela Groq.
 
 ## 📋 Pré-requisitos
 * Python instalado na máquina.
 * Uma chave de API gerada no painel da Groq Cloud.

## 🔧 Configuração e Instalação
 
* Clone o repositório:  

bash  

```git clone github.com```  

```cd api-assistant```

## Instale as dependências necessárias:  

bash  

```pip install flask groq python-dotenv```


## Configure a sua credencial em um arquivo .env na raiz do projeto:

env  

```GROQ_API_KEY=sua_chave_api_aqui```

## 🔌 Uso da API
Enviar Mensagem
* Rota: POST /assistant
* Headers: Content-Type: application/json

## Exemplo de Envio (Request):

json  

{  
"message": "Preciso marcar uma reunião amanhã às 14h."  
}

## Exemplo de Resposta (Response):  

json  

{  
  "response": "Entendido. Ativando o contexto de calendário para ajudar com o seu agendamento de amanhã às 14h."  
}

## 🔄 Fluxo de Execução

* O cliente faz uma requisição HTTP POST enviando uma mensagem.
* O Flask recebe o payload e anexa as diretrizes do prompt definitivo (calendario, calculadora e clima) como uma mensagem de sistema (system).
* O payload unificado é enviado à API da Groq chamando o modelo Llama 3.
* O modelo interpreta o texto sob as regras estipuladas e gera a resposta contextualizada.
* O Flask formata e retorna o texto final em formato JSON para o cliente.