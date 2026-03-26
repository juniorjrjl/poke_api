# Projeto para ciação de base de dados postgres de pokémon

![technology Python](https://img.shields.io/badge/techonolgy-Python-yellow)
![techonolgy PostgeSQL](https://img.shields.io/badge/techonolgy-PostgreSQL-blue)
![technology Docker](https://img.shields.io/badge/techonolgy-Docker-blue)

Rodando o Projeto:

## Sigas os seguintes passos para criar a base de dados postgres:
1 - Configurar o arquivo .env com as configurações desejadas:

| Variável           | Valor                                                                                                                                                  | Descrição |
|:---:|:---:|:---:|
| DATABASE_URL       | postgresql://poke-api:poke-api@localhost:5432/poke-api                                                                                                | URL para conexão com o banco de dados. |
| POKEMON_AMOUNT     | 1025                                                                                                                                                   | Na PokeAPI existem alguns registros no recurso de Pokémon que não representam Pokémon de fato. Esse valor é usado para limitar até qual número queremos buscar apenas os Pokémon válidos. |
| GENERATIONS_AMOUNT | 9                                                                                                                                                      | Indica até qual geração de Pokémon queremos considerar. |
| EGG_GROUP_AMOUNT   | 16                                                                                                                                                     | Essa variável resolve o mesmo problema descrito em `POKEMON_AMOUNT`, mas aplicado aos *egg groups*. |
| GENERATIONS        | {"generation-i":1996,"generation-ii":1999,"generation-iii":2002,"generation-iv":2006,"generation-v":2010,"generation-vi":2013,"generation-vii":2016,"generation-viii":2019,"generation-ix":2022} | A PokeAPI não registra o ano de cada geração. Por isso, foi criada essa configuração para mapear manualmente cada geração ao seu respectivo ano de lançamento. |
|POKEMON_TYPES_WHITELIST|lista de tipos que serão usados da poke-api|normal,fire,water,grass,electric,ice,fighting,poison,ground,flying,psychic,bug,rock,ghost,dragon,dark,steel,fairy|
|TYPES_INTRO_MAP|mapa indicando quando cada tipo surgiu no jogo, para evitar aparecer tipos em gerações que não existiam|{"steel": "generation-ii","dark": "generation-ii","fairy": "generation-vi"}|

## caso queria usar containers basta agora criar a network *poke-api-net* (```docker network create poke-api-net```) e rodar o comando docker compose up --build que o container do postgres irá ser populado

## Caso opte por usar o postgres fora de container será necessário alterar o database_url para apontar para sua instancia

## Caso queira rodar o script fora do docker você precisará do python 3.13.x, instalar via pip as dependencias contidas em requirements.txt
