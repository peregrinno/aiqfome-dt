# Sobre a estrutura do projeto e tecnologias utilizadas

Fiz em FastAPI pois é uma tecnologia que provê um alta quantidade de recursos modernos para construção de APIs em Python... Porém pensei bastante antes porque eu tava em duvida entre ele e o Django com Django Ninja que iria prover mais elegancia na parte de migrações e organização de dados.

## Gerenciador de dependencias e Docker

Usei para gerenciar as dependências o gerenciador uv da astral que é estupidamente mais rapido que o pip, escrito em Rust <a href="https://docs.astral.sh/uv/">Docs do uv</a>, tambem tem imagem Docker que serve o python usando Cython (transpilação de python para C) o que deixa tanto a instalação das dependencias muito rapida, os locks entre as dependencias e a execução do codigo.

## Estrutura

Eu usei um estrutura padrão de models, controllers e routes para organizar melhor o código e facilitar a manutenção, tentando ao maximo seguir os padrões de boas praticas e reaproveitar código..

Confesso que muitas das tecnicas exploradas tomei como base o que ja havia feito em outros projetos anteriores.

A API é assincrona e isso facilita a ideia de processamento assincrono e tambem o paralelismo para as operações de banco de dados.

## Banco de dados

To usando aqui Postgres porque ele foi o preferencial na solicitação do projeto, mas tambem porque foi o que eu tive mais experiencia. Porém, colocaria facilmente o mongodb por ser mais rapido e mais facil de escalar.

O cache com o redis me ajuda a acelerar bastante a consulta na API externa de produtos, evitando assim muitas requisições desnecessarias. Mas acho que em um ambiente real não faria exatamente assim porque imagine "cachear" 1 mi de produtos? kkkk é um pouco absurdo. Pensaria em algo como salvar o produto na integra ao inves do id apenas, ou até mesmo uma estrutura de mensageiria e rotinas para realmente saber o que é melhor guardar e o que não é.

## Containerização

Usaria Docker Swarm + Kubernetes para containerizar a aplicação e facilitar a escala e a manutenção. Mas como é um projeto simples, não é necessário.

## Considerações finais

Sendo bem sincero, acredito que ficou até robusto, claro que um ambiente de produção exige um conjunto de tecnologias que somadas trazem a escalabilidade. Até porque um projeto só não sustenta uma aplicação e sim uma arquitetura bem projetada.
