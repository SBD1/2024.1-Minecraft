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

# Dicionário de Dados

# Dicionário de Dados

## Tabelas Entidade

### [Mapa](#mapa)
A entidade [Mapa](#mapa) descreve o mundo do MUD. Essa entidade é identificada pelo seu nome, além disso, ela possui um atributo hora, representando o ciclo de dia e noite dentro do jogo.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome | Nome único que identifica o mapa. | VARCHAR | 30 | PRIMARY KEY |
| hora | Representa o ciclo de dia e noite no jogo. | ciclo_dia | --- | NOT NULL |

### [Chunk](#chunk)
A entidade [Chunk](#chunk) representa os blocos que compõem o [mapa](#mapa). O mapa é estruturado como uma matriz, onde cada chunk corresponde a uma célula. Chunks são identificados por um número sequencial, que varia de 0 até o tamanho total do mapa, numerados da esquerda superior para a direita inferior. Além disso, cada chunk está associado a um [bioma](#bioma) específico e possui um identificador que o vincula ao nome do [mapa](#mapa) ao qual pertence. A entidade Chunk é uma das entidades centrais do jogo pois serve como ponto de interseção entre várias outras entidades, estabelecendo conexões importantes dentro da estrutura do jogo.

- **Observação**: Essa tabela possui chave estrangeira para a entidade [Mapa](#mapa) e [Bioma](#bioma).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| numero | Número sequencial que identifica o chunk. | INT | --- | PRIMARY KEY |
| nome_bioma | Nome do bioma ao qual o chunk pertence. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| nome_mapa | Nome do mapa ao qual o chunk pertence. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| PRIMARY KEY | (numero, nome_mapa) | --- | --- | --- |

### [Construível](#construivel)
A entidade [Construível](#construivel) descreve estruturas construíveis pelo [jogador](#jogador). Essas estruturas são identificadas por um nome específico, possuem uma receita de construção própria e desempenham uma funcionalidade particular dentro do jogo.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome | Nome único que identifica o construível. | VARCHAR | 30 | PRIMARY KEY |
| descricao | Receita da construção. | TEXT | --- | NOT NULL |

### [Item](#item)
A entidade [Item](#item) descreve todos os itens disponíveis no jogo. Todos os itens podem ser identificados pelo seu nome único, e cada item pode ser especializado em [Material](#material), [Craftável](#craftavel) e [Alimento](#alimento).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome | Nome único que identifica o item. | VARCHAR | 30 | PRIMARY KEY |
| tipo_item | Tipo de especialização do item | tipo_item | --- | NOT NULL |

### [Alimento](#alimento)
A entidade [Alimento](#alimento) refere-se aos itens consumíveis do jogo, que restauram pontos de fome do [jogador](#jogador) ao serem ingeridos. Esses itens podem ser obtidos por meio de drops de [mobs](#mob) ou pela exploração de [fontes](#fonte).

- **Observação**: Essa entidade é uma especialização da entidade [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_item | Nome do item que é um alimento. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| pts_fome | Indica quantos pontos de fome do jogador o alimento restaura. | INT | --- | NOT NULL |

### [Craftável](#craftavel)
A entidade [Craftável](#craftavel) descreve os itens que podem ser fabricados pelo [jogador](#jogador) dentro do jogo. Esses itens possuem receitas específicas de fabricação e podem ser especializados em [Funcional](#funcional), [Ferramenta Durável](#ferramenta-duravel) e [Armadura Durável](#armadura-duravel).

- **Observação**: Essa entidade é uma especialização da entidade [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_item | Nome do item que é craftável. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| tipo_craftavel | Tipo de especialização do item craftável. | tipo_craftavel | --- | NOT NULL |

### [Funcional](#funcional)
A entidade [Funcional](#funcional) representa os itens que desempenham uma funcionalidade específica. Cada item funcional possui uma função distinta e única.

- **Observação**: Essa entidade é uma especialização da entidade [Craftável](#craftavel).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_item | Nome do item que é funcional. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| funcao | Descreve a função específica do item. | TEXT | --- | NOT NULL |

### [Ferramenta Durável](#ferramenta-duravel)
A entidade [Ferramenta Durável](#ferramenta-duravel) representa os itens que os [jogadores](#jogador) utilizam para executar diversas ações, como minerar [recursos](#fonte) e atacar [mobs](#mob). As ferramentas têm uma durabilidade limitada e causam uma quantidade específica de dano quando usadas contra mobs.

- **Observação**: Essa entidade é uma especialização da entidade [Craftável](#craftavel).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_item | Nome do item que é uma ferramenta. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| durabilidade_total | Durabilidade total da ferramenta. | INT | --- | NOT NULL |
| pts_dano | Pontos de dano que a ferramenta causa em mobs. | INT | --- | NOT NULL |

### [Armadura Durável](#armadura-duravel)
A entidade [Armadura Durável](#armadura-duravel) representa os itens que os [jogadores](#jogador) podem equipar para aumentar sua resistência a danos causados por [ferramentas](#ferramenta-duravel) e [mobs](#mob). Assim como as ferramentas, as armaduras possuem durabilidade limitada e oferecem uma quantidade definida de pontos de armadura.

- **Observação**: Essa entidade é uma especialização da entidade [Craftável](#craftavel).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_item | Nome do item que é uma armadura durável. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| pts_armadura | Pontos de armadura que o item fornece ao jogador. | INT | --- | NOT NULL |
| durabilidade_total | Durabilidade total da armadura. | INT | --- | NOT NULL |

### [Estrutura](#estrutura)
A entidade [Estrutura](#estrutura) descreve as estruturas pré-geradas no [mapa](#mapa) do jogo. Cada [chunk](#chunk) pode abrigar uma dessas estruturas de acordo com a sua probabilidade, que podem ser exploradas pelo jogador em busca de recompensas.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome | Nome único que identifica a estrutura. | VARCHAR | 30 | PRIMARY KEY |
| probabilidade | Probabilidade de a estrutura ser gerada em um chunk. | DECIMAL(5,2) | --- | NOT NULL |

### [Fonte](#fonte)
A entidade [Fonte](#fonte) descreve as fontes naturais de recursos dentro do jogo. Cada fonte fornece uma quantidade máxima de [itens](#item) específicos que podem ser minerados pelo [jogador](#jogador) utilizando [ferramentas](#ferramenta-duravel).

- **Observação**: Essa entidade possui chave estrangeira para a entidade [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome | Nome único que identifica a fonte. | VARCHAR | 30 | PRIMARY KEY |
| qtd_max | Quantidade máxima de itens que a fonte pode fornecer. | INT | --- | NOT NULL |
| nome_item_drop | Nome do item que pode ser extraído desta fonte. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |

### [Bioma](#bioma)
A entidade [Bioma](#bioma) descreve os diferentes biomas presentes no jogo, identificados por um nome único. O bioma determina as características específicas de cada [chunk](#chunk) no [mapa](#mapa).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome | Nome único que identifica o bioma. | VARCHAR | 30 | PRIMARY KEY |

### [Inventário](#inventario)
A entidade [Inventário](#inventario) representa o inventário do [jogador](#jogador). A tabela Inventário atua como uma tabela intermediária que resulta da relação entre jogador e item. Sendo uma entidade fraca, o inventário é identificado exclusivamente pelo ID do jogador que possui os itens nele contidos.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Jogador](#jogador) e [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_inventario | Identificador referenciando o jogador que possui o item. | INT | --- | FOREIGN KEY |
| id_inst_item | Identificador da instância de item possuído pelo jogador. | INT | --- | FOREIGN KEY, UNIQUE |

### [Jogador](#jogador)
A entidade [Jogador](#jogador) representa o personagem principal do jogo. Cada instância de Jogador possui um identificador único, além de diversos atributos que o caracterizam. O jogador conta com quatro atributos específicos para equipar itens de [armadura](#armadura-duravel). Além disso, o jogador possui chaves estrangeiras que indicam o [chunk](#chunk) em que ele se encontra no momento e a [missão](#missao) que está realizando.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Chunk](#chunk), [Missão](#missao) e [Armadura](#armadura-duravel).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_jogador | Identificador único do jogador. | SERIAL | --- | PRIMARY KEY |
| nome | Nome do jogador. | VARCHAR | 30 | NOT NULL |
| fome | Quantidade de pontos de fome que o jogador possui em determinado instante. | INT | --- | NOT NULL |
| vida | Quantidade de pontos de vida que o jogador possui em determinado instante. | INT | --- | NOT NULL |
| nivel | Nível que o jogador está em determinado instante. | INT | --- | NOT NULL |
| exp | Quantidade de experiência que um jogador tem em determinado instante. Essa experiência poderá ser utilizada para reparar as ferramentas. | INT | --- | NOT NULL |
| cabeca | Identificador da armadura equipada na cabeça. | INT | --- | FOREIGN KEY |
| peito | Identificador da armadura equipada no peito. | INT | --- | FOREIGN KEY |
| pernas | Identificador da armadura equipada nas pernas. | INT | --- | FOREIGN KEY |
| pes | Identificador da armadura equipada nos pés. | INT | --- | FOREIGN KEY |
| numero_chunk | Identificador do chunk onde o jogador está localizado. | INT | --- | FOREIGN KEY, NOT NULL |
| missao | Identificador da missão atual do jogador. | INT | --- | FOREIGN KEY |

### [Missão](#missao)
A entidade [Missão](#missao) armazena a lista de missões disponíveis no jogo, que auxiliam o [jogador](#jogador) na exploração do mundo. Cada missão é identificada por um ID único e segue uma sequência específica de missões. As missões incluem uma descrição, um objetivo, e oferecem experiência e recompensas para o jogador. As missões sequenciais são desbloqueadas e apresentadas ao jogador por meio de uma interface ao interagir com um [NPC](#npc), embora o NPC atue apenas como uma interface, sem qualquer relação direta com a missão em si.

- **Observação**: Essa entidade possui chave estrangeira para a entidade [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_missao | Identificador único da missão. | SERIAL | --- | PRIMARY KEY |
| nome | Nome da missão. | VARCHAR | 30 | NOT NULL |
| descricao | Descrição detalhada da missão. | TEXT | --- | NOT NULL |
| objetivo | Objetivo que deve ser cumprido pelo jogador para completar a missão. | TEXT | --- | NOT NULL |
| exp | Quantidade de experiência oferecida pela conclusão da missão. | INT | --- | NOT NULL |
| recompensa | Recompensa fornecida ao completar a missão. | TEXT | --- | NOT NULL |
| nome_item | Identificador do item fornecido como recompensa. | VARCHAR | 30 | FOREIGN KEY |

### [Mob](#mob)
A entidade [Mob](#mob) representa todas as entidades vivas no jogo, como inimigos e NPCs. Cada mob possui um nome único, uma vida máxima e uma probabilidade de spawn. Além disso, os mobs podem ser especializados como [Agressivos](#agressivo) ou [Pacíficos](#pacifico), dependendo de seu comportamento no jogo.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome | Nome único que identifica o mob. | VARCHAR | 30 | PRIMARY KEY |
| tipo_mob | Tipo de especialização do mob. | tipo_mob | --- | NOT NULL |

### [Agressivo](#agressivo)
A entidade [Agressivo](#agressivo) modela os mobs com comportamento agressivo ou neutro. Mobs agressivos possuem pontos de dano que reduzem a vida do [jogador](#jogador) quando o atacam. Esses mobs podem ser impulsivos, atacando o jogador sempre que o encontram, ou podem adotar um comportamento reativo, atacando apenas se forem provocados.

- **Observação**: Essa entidade é uma especialização da entidade [Mob](#mob).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_mob | Nome do mob que é agressivo. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| impulsivo | Determina o comportamento impulsivo do mob. | BOOLEAN | --- | NOT NULL |
| pts_dano | Declara a quantidade de dano que o mob causa ao jogador. | INT | --- | NOT NULL |

### [Pacífico](#pacifico)
A entidade [Pacífico](#pacifico) modela os mobs com comportamento pacífico. Mobs pacíficos nunca atacam o [jogador](#jogador) e podem ser especializados como [NPC](#npc).

- **Observação**: Essa entidade é uma especialização da entidade [Mob](#mob).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_mob | Nome do mob que é pacífico. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| vida_max | Vida máxima do mob pacífico. | INT | --- | NOT NULL |
| tipo_pacifico | Tipo de especialização do mob pacífico | tipo_pacifico | --- | NOT NULL |

### [NPC](#npc)
A entidade [NPC](#npc) modela os mobs pacíficos conhecidos como Aldeões. Os Aldeões são os únicos mobs no jogo que podem oferecer [missões](#missao), auxiliando o jogador a progredir no fluxo do jogo.

- **Observação**: Essa entidade é uma especialização da entidade [Pacífico](#pacifico).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_pacifico | Nome do mob pacífico que é um NPC. | VARCHAR | 30 | PRIMARY KEY, FOREIGN KEY |
| nome_proprio | Nome próprio do NPC (específico para cada instância). | VARCHAR | 30 | NOT NULL |


## Tabelas Instância

### [Instância Construível](#instancia-construivel)
A entidade [Instância Construível](#instancia-construivel) representa as diferentes ocorrências da entidade [Construível](#construivel) dentro do [mapa](#mapa). Cada instância é identificada por um ID único, permitindo distinguir entre as diversas construções presentes no jogo.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Construível](#construivel) e [Chunk](#chunk).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_inst_construivel | Identificador único da instância de construível. | SERIAL | --- | PRIMARY KEY |
| nome_construivel | Nome do construível associado a esta instância. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| numero_chunk | Número do chunk onde esta instância está localizada. | INT | --- | FOREIGN KEY, NOT NULL |
| nome_mapa | Nome do mapa onde a instância está localizada. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |

### [Instância Item](#instancia-item)
A entidade [Instância Item](#instancia-item) representa as ocorrências específicas de itens no jogo. Cada instância possui um identificador único e uma durabilidade atual. As instâncias de item podem estar armazenadas no [inventário](#inventario) de um [jogador](#jogador) ou situadas no chão de algum [chunk](#chunk).

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Item](#item) e [Inventário](#inventario).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_inst_item | Identificador único da instância de item. | SERIAL | --- | PRIMARY KEY |
| nome_item | Nome do item associado a esta instância. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| durabilidade_atual | Durabilidade atual do item. | INT | --- | NOT NULL |

### [Instância Estrutura](#instancia-estrutura)
A entidade [Instância Estrutura](#instancia-estrutura) representa as ocorrências de estruturas pré-geradas no jogo. Cada instância possui um identificador único e o nome da [estrutura](#estrutura) que representa, além de estar vinculada ao [bioma](#bioma) e ao [chunk](#chunk) em que está localizada.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Estrutura](#estrutura), [Bioma](#bioma) e [Chunk](#chunk).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_inst_estrutura | Identificador único da instância da estrutura. | SERIAL | --- | PRIMARY KEY |
| nome_estrutura | Nome da estrutura associada a esta instância. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| nome_bioma | Identificador do bioma onde a estrutura está localizada. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| numero_chunk | Número do chunk onde a estrutura está localizada. | INT | --- | FOREIGN KEY, NOT NULL |
| nome_mapa | Nome do mapa onde a estrutura está localizada. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |

### [Instância Fonte](#instancia-fonte)
A entidade [Instância Fonte](#instancia-fonte) representa as ocorrências de fontes naturais de recursos no jogo. Cada instância possui um identificador único, o nome da [fonte](#fonte) que representa e a quantidade atual de recursos disponíveis. Além disso, cada instância está vinculada a um [chunk](#chunk) específico onde a fonte está localizada e ao [material](#item) que ela fornece.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Fonte](#fonte), [Item](#item) e [Chunk](#chunk).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_inst_fonte | Identificador único da instância da fonte. | SERIAL | --- | PRIMARY KEY |
| nome_fonte | Nome da fonte associada a esta instância. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| qtd_atual | Quantidade atual de recursos disponíveis na fonte. | INT | --- | NOT NULL |
| numero_chunk | Número do chunk onde a fonte está localizada. | INT | --- | FOREIGN KEY, NOT NULL |
| nome_mapa | Nome do mapa onde a fonte está localizada. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| nome_item_drop | Nome do item que pode ser extraído desta fonte. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |

### [Instância Mob](#instancia-mob)
A entidade [Instância Mob](#instancia-mob) representa as ocorrências de mobs no jogo. Cada instância possui um identificador único, o nome do [mob](#mob) que representa e a vida atual do mob. As instâncias de mob também estão associadas a um [chunk](#chunk) específico e, opcionalmente, a uma [estrutura](#estrutura) em que o mob pode estar presente.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Mob](#mob), [Chunk](#chunk) e [Estrutura](#estrutura).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| id_inst_mob | Identificador único da instância do mob. | SERIAL | --- | PRIMARY KEY |
| nome_mob | Nome do mob associado a esta instância. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| vida_atual | Vida atual do mob nesta instância. | INT | --- | NOT NULL |
| numero_chunk | Número do chunk onde o mob está localizado. | INT | --- | FOREIGN KEY, NOT NULL |
| nome_mapa | Nome do mapa onde o mob está localizado. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| id_estrutura | Identificador da instância de estrutura onde o mob pode estar, se aplicável. | INT | --- | FOREIGN KEY |


## Tabelas Intermediárias

### [Mob Dropa Item](#mob-dropa-item)
A tabela [Mob Dropa Item](#mob-dropa-item) modela os itens que podem ser dropados por cada [mob](#mob). Cada [item](#item) possui uma probabilidade de ser dropado pelo mob quando ele é abatido.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Mob](#mob) e [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_mob | Nome único do mob que pode dropar o item. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| nome_item | Nome do item que pode ser dropado pelo mob. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| probabilidade | Probabilidade de o item ser dropado pelo mob. | DECIMAL(5,2) | --- | NOT NULL |
| quantidade | Quantidade do item que pode ser dropado. | INT | --- | DEFAULT 1 |

### [Estrutura Fornece Item](#estrutura-fornece-item)
A tabela [Estrutura Fornece Item](#estrutura-fornece-item) modela os itens que podem ser obtidos explorando cada [estrutura](#estrutura). Cada [item](#item) possui uma probabilidade de ser encontrado dentro de uma estrutura explorada.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Estrutura](#estrutura) e [Item](#item).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_estrutura | Nome único da estrutura que fornece o item. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| nome_item | Nome do item obtido pela estrutura. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| probabilidade | Probabilidade de o item ser encontrado dentro da estrutura. | DECIMAL(5,2) | --- | NOT NULL |

### [Ferramenta Minera Instância de Fonte](#ferramenta-mienera-inst-fonte)
A tabela [Ferramenta Minera Instância de Fonte](#ferramenta-mienera-inst-fonte) define quais ferramentas são capazes de minerar cada [fonte](#fonte). Cada fonte pode ser minerada por uma ou mais ferramentas diferentes, dependendo da sua finalidade.

- **Observação**: Essa entidade possui chave estrangeira para as entidades [Ferramenta Durável](#ferramenta-duravel) e [Fonte](#fonte).

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| nome_ferramenta | Nome da ferramenta utilizada para minerar a fonte. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |
| nome_fonte | Nome único da fonte que está sendo minerada. | VARCHAR | 30 | FOREIGN KEY, NOT NULL |

## Histórico de versões

| Versão | Data       | Descrição                                        | Autor                                                 | Revisão                                                 |
| :----: | :--------: | :----------------------------------------------: | :---------------------------------------------------: | :-----------------------------------------------------: |
| `1.0`  | 22/07/2024 | Criação do Dicionário de Dados | [Bruno Ricardo de Menezes](https://github.com/EhOBruno) | [Arthur Carneiro Trindade](https://github.com/trindadea)<br>[Miguel Moreira da Silva de Oliveira](https://github.com/EhOMiguel) |
| `1.1`  | 22/07/2024 | Primeira versão do Dicionário de Dados finalizada | [Bruno Ricardo de Menezes](https://github.com/EhOBruno)<br>[Arthur Carneiro Trindade](https://github.com/trindadea) | [Miguel Moreira da Silva de Oliveira](https://github.com/EhOMiguel) |
| `2.0`  | 16/08/2024 | Segunda versão do Dicionário de Dados finalizada | [Arthur Carneiro Trindade](https://github.com/trindadea) | [Bruno Ricardo de Menezes](https://github.com/EhOBruno)<br>[Miguel Moreira da Silva de Oliveira](https://github.com/EhOMiguel) |
| `3.0`  | 09/09/2024 | Versão final do Dicionário de Dados | [Bruno Ricardo de Menezes](https://github.com/EhOBruno)<br>[Arthur Carneiro Trindade](https://github.com/trindadea) | [Miguel Moreira da Silva de Oliveira](https://github.com/EhOMiguel) |