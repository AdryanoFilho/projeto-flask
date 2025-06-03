Página Inicial(/): Apresenta as informções iniciais do site.
Sobre a Equipe (/sobre-equipe): Informações sobre a equipe responsável pelo projeto.
Glossário (/glossario): Mostra um glossário de termos armazenados no arquivo bd_glossario.csv.
Fundamentos (/fundamentos): Seção dedicada aos fundamentos do tema abordado.
Dúvidas (/duvidas): Formulário para o usuário enviar uma pergunta, que será respondida através da integração com a API do Gemini.
Dicionário (/dicionario): Exibição de um dicionário com termos e definições.

Tecnologias Utilizadas:

Linguagem de Programação: Python 3

Framework Web: Flask

Integração com APIs: google-generativeai (API Gemini)

Bibliotecas Adicionais:

flask_cors para permitir requisições de diferentes origens.

markdown para renderizar as respostas do Gemini.

csv para manipulação de arquivos de dados (bd_glossario.csv).

Frontend: Templates HTML utilizando render_template junto ao bootstrap.

Integração com a API do Gemini:

A integração com a API do Gemini foi realizada através da biblioteca google-generativeai.

Principais Partes do Código Python

Estrutura de Rotas
/: Página inicial.

/sobre-equipe, /fundamentos, /dicionario: Páginas estáticas.

/duvidas: Recebe uma pergunta via formulário, consulta a API Gemini e exibe a resposta.

/glossario: Lê o arquivo bd_glossario.csv e exibe os termos.

/novo_termo e /criar_termo: Formulário e inserção de novos termos no glossário.

Integração com Arquivos
Glossário: Manipulado via arquivo CSV.

API REST: CRUD de termos em um arquivo de texto termos.txt.

API RESTful
GET /api/termos: Lista todos os termos.

POST /api/termos: Adiciona um novo termo.

PUT /api/termos/<termo>: Atualiza a definição de um termo existente.

DELETE /api/termos/<termo>: Remove um termo.
