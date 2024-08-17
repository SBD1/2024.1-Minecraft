# 2024.1 - Minecraft

<div style="text-align:center">
    <img src= "assets/images/minecraft.jpg" alt="Ícone do Minecraft" style="border-radius: 12px;"/>
</div>

Este repositório contém a recriação do jogo Minecraft no estilo MUD (Multi-User Dungeon), desenvolvida como parte da disciplina de Sistemas de Bancos de Dados 1, na Universidade de Brasília. 

## Equipe

<table align="center">
  <tr>
    <td align="center">
      <a class="membro-equipe" href="https://github.com/trindadea">
        <img src="https://github.com/trindadea.png">
        <br>
        <p class="nome">Arthur Carneiro Trindade</p>
        <p class="matricula">180098080</p>
      </a>
    </td>
    <td align="center">
      <a class="membro-equipe" href="https://github.com/EhOBruno">
        <img src="https://github.com/EhOBruno.png">
        <br>
        <p class="nome">Bruno Ricardo de Menezes</p>
        <p class="matricula">221007680</p>
      </a>
    </td>
    <td align="center">
      <a class="membro-equipe" href="https://github.com/EhOMiguel">
        <img src="https://github.com/EhOMiguel.png">
        <br>
        <p class="nome">Miguel Moreira da Silva de Oliveira</p>
        <p class="matricula">202023968</p>
      </a>
    </td>
  </tr>
</table>

### Jogo

No mundo de Minecraft, o jogador inicia sua jornada em um ambiente vasto e gerado aleatoriamente, repleto de biomas diversos como florestas, montanhas, desertos e oceanos. A principal missão é sobreviver, coletando recursos naturais como madeira, pedra e metais para criar ferramentas, construir abrigos e enfrentar monstros que surgem à noite.

Conforme o jogador avança, ele pode explorar cavernas e minas em busca de materiais raros, criar equipamentos mais avançados e até construir estruturas complexas. A viagem também leva o jogador a outros reinos, como o Nether, um mundo infernal cheio de perigos e tesouros.

A jornada culmina na busca pelo Ender Dragon, o chefe final do jogo, localizado em uma dimensão chamada The End. Para chegar lá, o jogador precisa encontrar e ativar um portal escondido em uma fortaleza subterrânea. A batalha contra o Ender Dragon é intensa e requer preparação meticulosa, mas derrotá-lo marca a conclusão épica da aventura, embora o jogo continue oferecendo inúmeras possibilidades de exploração e construção.

# ![Ícone do Minecraft](link_para_ícone_do_minecraft) Como Rodar o Jogo



### 1. Instale o Docker

Primeiro, é necessário instalar o Docker. Você pode fazer isso acessando o seguinte link: [Instalar Docker](https://www.docker.com/get-started).

### 2. Clone o Repositório

Após instalar o Docker, clone o repositório do jogo usando o comando abaixo:

```bash
git clone https://github.com/SBD1/2024.1-Minecraft.git
```

### 3. Acesse o Diretório do Jogo

Depois de clonar o repositório, entre no diretório do jogo com o seguinte comando:

```bash
cd 2024.1-Minecraft
```

### 4. Acesse o Diretório Docker

Agora que você está dentro da pasta do jogo, é necessário acessar a pasta do Docker:

```bash
cd Docker
```

### 5. Suba o Container Docker
Dentro da pasta Docker, suba e entre no container com os comandos:

```bash
docker-compose up -d --build
docker exec -it python_app bash
```
O Docker é uma ferramenta poderosa porque garante que o jogo rodará em um ambiente consistente, evitando problemas de versões ou dependências.

### 6. Rode o Jogo

Com todas as dependências instaladas no container, rode o jogo usando:

```bash
python main.py
```

### 7. Finalize o Jogo

Quando terminar de jogar, finalize o jogo pressionando Ctrl + C.

### 8. Saia do Container

Saia do container do Docker digitando:

```bash
exit
```

### 9. Encerre o Container

Por fim, não se esqueça de encerrar o container do Docker com:

```bash
docker-compose down
```

### Tenha uma ótima diversão!
