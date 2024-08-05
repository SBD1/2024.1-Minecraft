# Dicionário de dados

## Introdução

O Dicionário de Dados é uma descrição detalhada dos elementos que compõem o banco de dados, fornecendo informações sobre cada atributo e suas características. Ele serve como uma referência centralizada para desenvolvedores, administradores e usuários, garantindo uma compreensão clara dos dados armazenados e de como devem ser utilizados.

O dicionário de dados desse projeto inclui as seguintes colunas:

- <strong>Nome:</strong> O nome do atributo no banco de dados.
- <strong>Descrição:</strong> Uma descrição detalhada do que o atributo ou entidade representa e sua função no contexto do jogo.
- <strong>Tipo de Dado:</strong> O tipo de dado que o atributo armazenará, como inteiro, texto, data, etc.
- <strong>Tamanho:</strong> O comprimento máximo ou a capacidade do dado.
- <strong>Restrições de Domínio:</strong> As regras e restrições que limitam os valores que o atributo pode assumir, como valores possíveis, valores obrigatórios, ou restrições de unicidade.

A seguir, apresentamos o dicionário de dados completo.

## Dicionário

### [Mapa](#mapa)

A entidade [Mapa](#mapa) descreve o mapa completo do jogo. O mapa do jogo é único e possui Nome e Tempo representando o ciclo dia e noite.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Nome | Nome identificador do mapa. | --- | --- | PK |
| Tempo | Indica o ciclo dia e noite. | --- | --- | --- |

### [Chunk](#chunk)

A entidade [Chunk](#chunk) descreve cada bloco que compõe o mapa. Para abstrair, associe o mapa a uma matriz e cada instância de Chunk a uma célula. Cada instância de Chunk pode ser identificada pelas suas coordenadas X e Y e cada um possui um acesso para o Norte, Sul, Leste e Oeste.

- **Observação**: Essa tabela possui chave estrangeira da entidade [Mapa](#mapa).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Coord_X | Coordenada X da Chunk dentro do Mapa. | --- | --- | PK |
| Coord_Y | Coordenada Y da Chunk dentro do Mapa. | --- | --- | PK |
| Mapa | Nome identificador do mapa. | --- | --- | FK |
| Chunk_N | Chunk acessada pelo norte da chunk atual. | --- | --- | --- |
| Chunk_S | Chunk acessada pelo sul da chunk atual. | --- | --- | --- |
| Chunk_L | Chunk acessada pelo leste da chunk atual. | --- | --- | --- |
| Chunk_O | Chunk acessada pelo oeste da chunk atual. | --- | --- | --- |

### [Item](#item)

A entidade [Item](#item) descreve todos os itens disponíveis no jogo. Todos os itens podem ser identificados pelo seu ID. Cada item pode ser especializado em [Material](#material), [Craftável](#craftavel) e [Alimento](#alimento).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Item | ID identificador do item. | --- | --- | PK |
| Tipo_item | Identifica a especialização do item. | --- | --- | --- |
| Nome | Nome do item. | --- | --- | --- |

### [Alimento](#alimento)

A entidade [Alimento](#alimento) descreve os itens consumíveis do jogo. Itens consumíveis fornecem pontos de fome ao jogador ao serem consumidos e são obtidos através de [Mobs](#mob) e [Fontes](#fonte).

- **Observação**: Essa entidade é uma especialização da entidade [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Item | ID identificador do item. | --- | --- | FK |
| Pontos_fome | Indica quantos pontos de fome do jogador o alimento preenche. | --- | --- | --- |

### [Craftável](#craftavel)

A entidade [Craftável](#craftavel) descreve os itens que podem ser fabricados dentro do jogo. Os itens Craftáveis possuem Receita e são podem ser especializados em [Funcional](#funcional) ou [Durável](#duravel).

- **Observação**: Essa entidade é uma especialização da entidade [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Item | ID identificador do item. | --- | --- | PK, FK |
| Tipo_craftavel | Identifica a especialização do item em durável ou funcional. | --- | --- | --- |
| Receita | Descreve a receita para fabricar o item. | --- | --- | --- |

### [Funcional](#funcional)

A entidade [Funcional](#funcional) representa os itens que possuem uma funcionalidade específica. Cada item funcional possui uma função distinta e única.

- **Observação**: Essa entidade é uma especialização da entidade [Craftável](#craftavel).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Craftavel | ID identificador do item. | --- | --- | FK |
| Funcao | Descreve a função do item. | --- | --- | FK |

### [Durável](#duravel)

A entidade [Durável](#duravel) representa os itens que possuem durabilidade. Os itens duráveis são gastos com o uso e podem quebrar caso não sejam reforjados. Os itens duráveis podem ser especializados em [Armadura](#armadura) ou [Ferramenta](#ferramenta).

- **Observação**: Essa entidade é uma especialização da entidade [Craftável](#craftavel).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Craftavel | ID identificador do item. | --- | --- | PK, FK |
| Tipo_duravel | Identifica a especialização do item em ferramenta ou armadura. | --- | --- | --- |
| Durabilidade | Indica a durabilidade do item. | --- | --- | --- |

### [Armadura](#armadura)

A entidade [Armadura](#armadura) modela os itens de vestimenta do jogo. Armaduras possuem pontos de armadura, que bloqueiam pontos de dano de [Ferramentas](#ferramenta) e [Mobs](#mob) e aumentam a resistência do [Jogador](#jogador).

- **Observação**: Essa entidade é uma especialização da entidade [Durável](#duravel).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Duravel | ID identificador da armadura. | --- | --- | FK |
| Pts_armadura | Indica a capacidade de proteção da armadura. | --- | --- | --- |

### [Estrutura](#estrutura)

A entidade [Estrutura](#estrutura) descreve as diversas estruturas pré-geradas no mapa do jogo. Cada [Bioma](#bioma) pode conter uma estrutura que pode ser explorada pelo [Jogador](#jogador) para obter recompensas.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Estrutura | ID identificador da estrutura. | --- | --- | PK |
| Item | Identifica o item que a estrutura fornece. | --- | --- | FK |
| Nome | Nome da estrutura. | --- | --- | --- |

### [Fonte](#fonte)

A entidade [Fonte](#fonte) descreve as fontes naturais de recursos dentro do jogo. Cada [Bioma](#bioma) possui diferentes fontes, que podem ser mineradas pelo [Jogador](#jogador) utilizando [Ferramenta](#ferramenta), para obter [Item](#item) específicos. 

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Fonte | ID identificador da fonte. | --- | --- | PK |
| Item | Identifica o item que a fonte fornece. | --- | --- | FK |
| Nome | Nome da fonte. | --- | --- | --- |

### [Ferramenta](#ferramenta)

A entidade [Ferramenta](#ferramenta) descreve um dos tipos de itens mais importantes do jogo. As ferramentas englobam desde Armas até demais itens. Ferramentas causam pontos de dano ao serem utilizadas contra [Mobs](#mob) e [Jogadores](#jogador) e podem ser utilizadas para minerar [Fonte](#fonte), fornecendo [Item](#item).

- **Observação**: Essa entidade é uma especialização da entidade [Durável](#duravel) e possui chave estrangeira da entidade [Fonte](#fonte).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Duravel | ID identificador do item. | --- | --- | PK, FK |
| Fonte | Representa a fonte que a ferramenta é capaz de minerar. | --- | ---

 | FK |
| Pontos_dano | Indica o dano que a ferramenta causa em um mob. | --- | --- | --- |

### [Bioma](#bioma)

A entidade [Bioma](#bioma) descreve os biomas do jogo. Cada instância de Bioma pode ser localizada pelo ID do Bioma ou pela coordenada X e Y da [Chunk](#chunk) da qual a instância faz parte. O Bioma define as características de cada célula do [Mapa](#mapa) e é uma das entidades mais complexas por relacionar uma grande quantidade de entidades.

- **Observação**: Essa entidade possui chave estrangeira das entidades [Chunk](#chunk), [Estrutura](#estrutura) e [Fonte](#fonte).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Bioma | ID identificador do bioma | --- | --- | PK |
| ChunkX | Identifica a coordenada X do chunk que o bioma está localizado. | --- | --- | FK |
| ChunkY | Identifica a coordenada Y do chunk que o bioma está localizado. | --- | --- | FK |
| Estrutura | Identifica a estrutura disponível no chunk. | --- | --- | FK |
| Fonte | Identifica a fonte disponível na fonte. | --- | --- | FK |
| Nome | Nome do bioma | --- | --- | --- |

### [Inventário](#inventario)

A entidade [Inventário](#inventario) descreve o inventário do [Jogador](#jogador).

- **Observação**: Essa entidade possui chave estrangeira da entidade [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Inventario | ID identificador do inventário | --- | --- | PK |
| Item | Identifica o item armazenado no inventário. | --- | --- | FK |

### [Jogador](#jogador)

A entidade [Jogador](#jogador) representa o jogador, o personagem principal do jogo. Cada instância de Jogador possui um ID e diversos atributos que o caracterizam.

- **Observação**: Essa entidade possui chave estrangeira das entidades [Bioma](#bioma) e [Inventário](#inventario).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Jogador | ID identificador do jogador. | --- | --- | PK |
| Bioma | Nome do bioma em que o jogador está em determinado instante. | --- | --- | FK |
| Inventario | Inventário único do jogador. | --- | --- | FK |
| Nome | Nome do jogador. | --- | --- | --- |
| Fome | Quantidade de fome que o jogador está em determinado instante. | --- | --- | --- |
| Vida | Quantidade de pontos de vida que o jogador está em determinado instante. | --- | --- | --- |
| Nivel | Nível que o jogador está em determinado instante. | --- | --- | --- |
| Experiencia | Quantidade de experiência que um jogador tem em determinado instante. Essa experiência poderá ser utilizada para melhorar as ferramentas. | --- | --- | --- |

### [Mob](#mob)

A entidade [Mob](#mob) descreve as demais entidades vivas no jogo como inimigos e NPCs. A entidade Mob pode ser especializada em [Agressivo](#agressivo) ou [Pacífico](#pacifico).

- **Observação**: Essa entidade possui chave estrangeira da entidade [Bioma](#bioma).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Mob | ID identificador do mob. | --- | --- | PK |
| Bioma | Nome do bioma que o mob está em determinado instante. | --- | --- | FK |
| Vida | Quantidade de pontos de vida que o mob está em determinado instante. | --- | --- | --- |
| Nome_mob | Nome do mob. | --- | --- | --- |
| Tipo_mob | Identifica a especialização do mob. | --- | --- | --- |

### [Agressivo](#agressivo)

A entidade [Agressivo](#agressivo) modela os mobs de comportamento agressivo ou neutro. Mobs agressivos possuem pontos de dano que removem Vida do [Jogador](#jogador) quando os atacam, além disso, eles podem ser impulsivos, sempre atacando o jogador, ou não, atacando somente se forem atacados. 

- **Observação**: Essa entidade é uma especialização da entidade [Mob](#mob).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Mob | ID identificador do mob. | --- | --- | PK, FK |
| Impulsivo | Declara se o mob é impulsivo ou não, ou seja, se ele ataca ao chegar próximo dele. | --- | --- |  |
| Pts_dano | Declara a quantidade de dano que o mob causa. | --- | --- |  |

### [Pacífico](#pacifico)

A entidade [Pacífico](#pacifico) modela os mobs de comportamento pacífico. Mobs pacíficos nunca atacam o [Jogador](#jogador) e podem ser especializados em [NPC](#npc).

- **Observação**: Essa entidade é uma especialização da entidade [Mob](#mob).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Mob | ID identificador do mob. | --- | --- | FK |
| Tipo_Pacifico | Identifica a especialização do mob pacífico. | --- | --- |  |

### [NPC](#npc)

A entidade [NPC](#npc) modela os mobs pacíficos conhecidos como Aldeões. Aldeões são os únicos mobs do jogo que podem oferecer [Missão](#missao), atuando como guia do jogador no jogo.

- **Observação**: Essa entidade é uma especialização da entidade [Pacífico](#pacifico).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Pacifico | ID identificador do mob. | --- | --- | FK |

### [Missão](#missao)

A entidade [Missão](#missao) representa as diferentes missões fornecidas pelos Aldeões. As missões têm como objetivo guiar o jogador dentro do jogo, sendo de critério do jogador segui-las ou não. Cada instância de Missão fornece uma recompensa quando concluída.

- **Observação**: Essa tabela possui chave estrangeira da entidade [NPC](#npc).

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
