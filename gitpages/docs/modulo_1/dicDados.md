# Dicionário de dados

## Entidade: Mapa

- Descrição: A entidade Mapa descreve o mapa completo do jogo. O mapa do jogo é único e possui Nome e Tempo representando o clico dia e noite.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Nome | Nome identificador do mapa. | --- | --- | PK |
| Tempo | Indica o ciclo dia e noite. | --- | --- | --- |

## Entidade: Chunk

- Descrição: A entidade Chunk descreve cada bloco que compõe o mapa. Para abstrair, associe o mapa a uma matriz e cada instância de Chunk a uma célula. Cada instância de Chunk pode ser identificada pelas suas coordenadas X e Y e cada um possui um acesso para o Norte, Sul, Leste e Oeste.
- Observação: Essa tabela possui chave estrangeira da entidades `Mapa`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Coord_X | Coordenada X da Chunk dentro do Mapa. | --- | --- | PK |
| Coord_Y | Coordenada da Chunk dentro do Mapa. | --- | --- | PK |
| Mapa | Nome identificador do mapa. | --- | --- | FK |
| Chunk_N | Chunk acessada pelo norte da chunk atual. | --- | --- | --- |
| Chunk_S | Chunk acessada pelo sul da chunk atual. | --- | --- | --- |
| Chunk_L | Chunk acessada pelo leste da chunk atual. | --- | --- | --- |
| Chunk_O | Chunk acessada pelo oeste da chunk atual. | --- | --- | --- |

## Entidade: Item

- Descrição: A entidade Item descreve todos os itens disponíveis no jogo. Todos os itens podem ser identificados pelo seu ID. Cada item pode ser especializado em `Material`, `Craftável` e `Alimento`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Item |ID identificador do item. | --- | --- | PK |
| Tipo_item | Identifica a especialização do item. | --- | --- | --- |
| Nome | Nome do item. | --- | --- | --- |

## Entidade: Alimento

- Descrição: A entidade Alimento descreve os itens consumiveis do jogo. Itens consumíveis fornecem pontos de fome ao jogador ao serem consumidos e são obtidos através de `Mobs` e `Fontes`.
- Observação: Essa entidade é uma especialização da entidade `Item`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Item | ID identificador do item. | --- | --- | FK |
| Pontos_fome | Indica quantos pontos de fome do jogador o alimento preenche. | --- | --- | --- |

## Entidade: Craftavel

- Descrição: A entidade Craftavel descereve os itens que podem ser fabricados dentro do jogo. Os itens Craftáveis possuem Receita e são podem ser especializados em `Funcional` ou `Duravel`.
- Observação: Essa entidade é uma especialização da entidade `Item`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Item | ID identificador do item. | --- | --- | PK, FK |
| Tipo_craftavel | Identifica a especialização do item em durável ou funcional. | --- | --- | --- |
| Receita | Descreve a receita para fabricar o item. | --- | --- | --- |

## Entidade: Funcional

- Descrição: A entidade Funcional representa os itens que possuem uma funcionalidade específica. Cada item funcional possui uma funcionalidade dist---a e única.
- Observação: Essa entidade é uma especialização da entidade `Craftavel`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Craftavel | ID identificador do item. | --- | --- | FK |
| Funcao | Descreve a função do item. | --- | --- | FK |

## Entidade: Duravel

- Descrição: A entidade Duravel representa os itens que possuem durabilidade. Os ítens duráveis são gastos com o uso e podem quebrar caso não sejam reforjados. Os ítens duráveis podem ser especializados em `Armadura` ou `Ferramenta`.
- Observação: Essa entidade é uma especialização da entidade `Craftavel`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Craftavel | ID identificador do item. | --- | --- | PK, FK |
| Tipo_duravel | Identifica a especialização do item em ferramenta ou armadura. | --- | --- | --- |
| Durabilidade | Indica a durabilidade do item. | --- | --- | --- |

## Entidade: Armadura

- Descrição: A entidade Armadura modela os itens de vestimenta do jogo. Armaduras possuem pontos de armadura, que bloqueiam pontos de dano de `Ferramentas` e `Mobs` e aumentam a resistência do `Jogador`.
- Observação: Essa entidade é uma especialização da entidade `Duravel`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Duravel | ID identificador da armadura. | --- | --- | FK |
| Pts_armadura | Indica a capacidade de proteção da armadura. | --- | --- | --- |

## Entidade: Estrutura

- Descrição: A entidade Estrutura descreve as diversas estruturas pré-geradas no mapa do jogo. Cada `Bioma` pode conter uma estrutura que pode ser explorada pelo `Jogador` para obter recompensas.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Estrutura | ID identificador da estrutura. | --- | --- | PK |
| Item | Identifica o item que a estrutura fornece. | --- | --- | FK |
| Nome | Nome da estrutura. | --- | --- | --- |

## Entidade: Fonte

- Descrição: A entidade Fonte descreve as fontes naturais de recursos dentro do jogo. Cada `Bioma` possui diferentes fontes, que podem ser mineradas pelo `Jogador` utilizando `Ferramenta`, para obter `Item` específicos. 

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Fonte | ID identificador da fonte. | --- | --- | PK |
| Item | Identifica o item que a fonte fornece. | --- | --- | FK |
| Nome | Nome da fonte. | --- | --- | --- |

## Entidade: Ferramenta

- Descrição: A entidade Ferramenta descreve um dos tipos de itens mais importantes do jogo. As ferramentas englobam desde Armas até demais itens. Ferramentas causam pontos de dano ao serem utilizados contra `Mobs` e `Jogadores` e podem ser utilizadas para minerar `Fonte`, fornecendo `Item`.
- Observação: Essa entidade é uma especialização da entidade `Duravel` e possui chave estrangeira da entidade `Fonte`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Duravel | ID identificador do item. | --- | --- | PK, FK |
| Fonte | Representa a fonte que a ferramenta é capaz de minerar. | --- | --- | FK |
| Pontos_dano | Indica o dano que a ferramenta causa em um mob. | --- | --- | --- |

## Entidade: Bioma

- Descrição: A entidade Bioma descreve os biomas do jogo. Cada instância de Bioma pode ser localizado pelo ID do Bioma ou pela coordenada X e Y da `Chunk` da qual a instância faz parte. O Bioma define as características de cada célula do `Mapa` e é uma das entidades mais complexas por relacionar uma grande quantidade de entidades.
- Observação: Essa entidade possui chave estrangeira das entidades `Chunk`, `Estrutura` e `Fonte`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Bioma | ID identificador do bioma | --- | --- | PK |
| ChunkX | Identifica a coordenada X do chunk que o bioma está localizado. | --- | --- | FK |
| ChunkY | Identifica a coordenada Y do chunk que o bioma está localizado. | --- | --- | FK |
| Estrutura | Identifica a estrutura disponível no chunk. | --- | --- | FK|
| Fonte | Identifica a fonte disponível na fonte. | --- | --- | FK|
| Nome | Nome do bioma | --- | --- | --- |

## Entidade: Inventario

- Descrição: A entidade Inventario descreve o inventário do Jogador.
- Observação: Essa entidade possui chave estrangeira da entidade `Item`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Inventario | ID identificador do inventário | --- | --- | PK |
| Item | Identifica o item armazenado no inventário. | --- | --- | FK |

## Entidade: Jogador

- Descrição: A entidade Jogador representa o jogador, o personagem principal do jogo. Cada instância de Jogador possui um ID e diversos atributos que o caracterizam.
- Observação: Essa entidade possui chave estrangeira das entidades `Bioma` e `Inventario`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Jogador | ID identificador do jogador. | --- | --- | PK |
| Bioma | Nome do bioma em que o jogador está em determinado instante. | --- | --- | FK |
| Inventario | Inventário único do jogador. | --- | --- | FK|
| Nome | Nome do jogador. | --- | --- | --- |
| Fome | Quantidade de fome que o jogador está em determinado instante. | --- | --- | --- |
| Vida | Quantidade de pontos de vida que o jogador está em determinado instante. | --- | --- | --- |
| Nivel | Nível que o jogador está em determinado instante. | --- | --- | --- |
| Experiencia | Quantidade de experiência que um jogador tem em determinado instante. Essa experiência poderá ser utilizada para melhorar as ferramentas. | --- | --- | --- |

## Entidade: Mob

- Descrição: A entidade Mob descreve as demais entidades vivas no jogo como inimigos e NPCs. A entidade Mob pode ser especializada em `Agressivo` ou `Pacífico`.
- Observação: Essa entidade possui chave estrangeira da entidade `Bioma`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Mob | ID identificador do mob. | --- | --- | PK |
| Bioma | Nome do bioma que o mob está em determinado instante. | --- | --- | FK |
| Vida | Quantidade de pontos de vida que o mob está em determinado instante. | --- | --- | ---|
| Nome_mob | Nome do mob. | --- | --- | ---|
| Tipo_mob | Identifica a especialização do mob. | --- | --- | --- |

## Entidade: Agressivo

- Descrição: A entidade Agressivo modela os mobs de comportamento agressivo ou neutro. Mobs agressivos possuem pontos de dano que removem Vida do `Jogador` quando os ataca, além disso, eles podem ser impulsivos, sempre atacando o jogador, ou não, atacando somente se forem atacados. 
- Observação: Essa entidade é uma especialização da entidade `Mob`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Mob | ID identificador do mob. | --- | --- | PK, FK |
| Impulsivo | Declara se o mob é impulsivo ou não, ou seja, se ele ataca ao chegar próximo dele. | --- | --- |  |
| Pts_dano | Declara a quantidade de dano que o mob causa. | --- | --- |  |

## Entidade: Pacífico

- Descrição: A entidade Pacífico modela os mobs de comportamento pacífico. Mobs pacíficos nunca atacam o `Jogador` e podem ser especializados em `NPC`.
- Observação: Essa entidade é uma especialização da entidade `Mob`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Mob | ID identificador do mob. | --- | --- | FK |
| Tipo_Pacifico | Identifica a especialização do mob pacífico. | --- | --- |  |

## Entidade: NPC

- Descrição: A entidade NPC modela os mobs pacíficos conhecidos como Aldeões. Aldeões são os únicos mobs do jogo que podem oferecer `Missão`, atuando como guia do jogador no jogo.
- Observação: Essa entidade é uma especialização da entidade `Pacífico`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Pacifico | ID identificador do mob. | --- | --- | FK |

## Entidade: Missão

- Descrição: A entidade Missão representa as diferentes missões fornecidas pelos Aldeões. As missões tem como objetivo guiar o jogador dentro do jogo, sendo de critério do jogador segui-las ou não. Cada instância de Missão fornece uma recompensa quando concluída.
- Observação: Essa tabela possui chave estrangeira da entidade `NPC`.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Missao | ID identificador da missão. | --- | --- | PK |
| NPC | ID identificador do mob. | --- | --- | FK |
| Nome_Missao | Nome da missão fornecida pelo NPC ao jogador. | --- | --- |  |
| Descricao | Descrição da missão fornecida pelo NPC ao jogador. | --- | --- |  |
| Objetivo | Objetivo da missão fornecida pelo NPC ao jogador. | --- | --- |  |
| Recompensa | Recompensa da missão fornecida pelo NPC destinada ao jogador quando concluída. | --- | --- | --- |

## Histórico de versões

| Versão | Data       | Descrição                                        | Autor                                                 | Revisão                                                 |
| :----: | :--------: | :----------------------------------------------: | :---------------------------------------------------: | :-----------------------------------------------------: |
| `1.0`  | 22/07/2024 | Criação do Dicionário de Dados | [Bruno Ricardo de Menezes](https://github.com/EhOBruno) | [Arthur Carneiro Trindade](https://github.com/trindadea)<br>[Miguel Moreira da Silva de Oliveira](https://github.com/EhOMiguel) |
| `1.1`  | 22/07/2024 | Primeira versão do Dicionário de Dados finalizada | [Bruno Ricardo de Menezes](https://github.com/EhOBruno)<br>[Arthur Carneiro Trindade](https://github.com/trindadea) | [Miguel Moreira da Silva de Oliveira](https://github.com/EhOMiguel) |
