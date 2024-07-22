# Dicionário de dados

## Entidade: Mapa

- Descrição:
- Observação:

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Nome | Nome identificador do mapa | varchar | 35 | PK |
| Tempo | Nome identificador do mapa | --- | --- | --- |

## Entidade: Chunk

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Mapa.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Coord_X | Nome identificador do mapa | int | --- | PK |
| Coord_Y | Nome identificador do mapa | int | --- | PK |
| Chunk_N | Chunk localizado no norte do mapa | --- | --- | FK|
| Chunk_S | Chunk localizado no sul do mapa | --- | --- | FK|
| Chunk_L | Chunk localizado no leste do mapa | --- | --- | FK|
| Chunk_O | Chunk localizado no oeste do mapa | --- | --- | FK|

## Entidade: Item

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Item | ID identificador do item | int | --- | PK |
| Tipo_item |  | --- | --- | FK |
| Nome |  | --- | --- | --- |

## Entidade: Alimento

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Item | ID identificador do item | int | --- | PK |
| Pontos_fome | --- | --- | --- | FK |

## Entidade: Craftavel

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Item | ID identificador do item | int | --- | FK |
| Tipo_craftavel | --- | --- | --- | FK |

## Entidade: Funcional

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Craftavel | ID identificador do item | int | --- | FK |
| Funcao | --- | --- | --- | FK |

## Entidade: Duravel

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Craftavel | ID identificador do item | int | --- | FK |
| Tipo_duravel | --- | --- | --- | FK |
| Durabilidade | --- | --- | --- | FK |

## Entidade: Armadura

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Duravel | ID identificador do item | int | --- | FK |
| Pts_armadura | --- | --- | --- | FK |

## Entidade: Ferramenta

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Duravel | ID identificador do item | int | --- | FK |
| Fonte | --- | --- | --- | FK |
| Pontos_dano | --- | --- | --- | --- |

## Entidade: Estrutura

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Estrutura | ID identificador da estrutura | int | --- | PK |
| Item |  | --- | --- | FK |
| Nome |  | --- | --- | --- |

## Entidade: Fonte

- Descrição:
- Observação:

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Fonte | ID identificador da fonte | int | --- | PK |
| Item |  | --- | --- | FK |
| Nome |  | --- | --- | --- |

## Entidade: Bioma

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Bioma | Nome identificador do mapa | int | --- | PK |
| Chunk | Nome identificador do mapa | int | --- | FK |
| Estrutura | Chunk localizado no norte do mapa | --- | --- | FK|
| Fonte | Chunk localizado no sul do mapa | --- | --- | FK|
| Nome | Nome do bioma | varchar | 35 | --- |

## Entidade: Inventario

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Inventario | Nome identificador do mapa | int | --- | PK |
| Item | Nome identificador do mapa | int | --- | FK |

## Entidade: Jogador

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Jogador | Nome identificador do mapa | int | --- | PK |
| Bioma | Nome identificador do mapa | int | --- | FK |
| Inventario | Chunk localizado no norte do mapa | --- | --- | FK|
| Nome | Chunk localizado no sul do mapa | --- | --- | --- |
| Fome | Nome do bioma | varchar | 35 | --- |
| Vida | Nome do bioma | varchar | 35 | --- |
| Nivel | Nome do bioma | varchar | 35 | --- |
| Experiencia | Nome do bioma | varchar | 35 | --- |

## Entidade: Mob

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Mob | --- | int | --- | PK |
| Bioma | --- | int | --- | FK |
| Vida |  | --- | --- | ---|
| Nome_mob |  | --- | --- | ---|
| Tipo_mob |  | --- | --- | --- |

## Entidade: Agressivo

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Mob | --- | --- | --- | FK |
| Impulsivo | --- | --- | --- |  |

## Entidade: Pacífico

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Mob | --- | --- | --- | FK |
| Tipo_Pacifico | --- | --- | --- |  |

## Entidade: NPC

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| Pacifico | --- | --- | --- | FK |

## Entidade: Missão

- Descrição:
- Observação: Essa tabela possui chave estrangeira das entidades Chunk, Estrutura e Fonte.

| Nome | Descrição | Tipo de Dado | Tamanho | Restrições de domínio |
| :---: | :---: | :---: | :---: | :---: |
| ID_Missao | --- | --- | --- | PK |
| NPC | --- | --- | --- | FK |
| Nome_Missao | --- | --- | --- |  |
| Descricao | --- | --- | --- |  |
| Objetivo | --- | --- | --- |  |
| Recompensa | --- | --- | --- | --- |
