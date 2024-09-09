from ..utils.helpers import mostrar_texto_gradualmente
from colorama import Fore
import random
import time

# Comando: Atacar Mob
def atacar_mob(connection, cursor, nomeUser, nomeMob, nomeFerramenta, estaEmEstrutura):
    """
    Permite ao jogador atacar um mob utilizando uma ferramenta ou arma do inventário.
    Lida com mobs pacíficos e agressivos, incluindo armaduras e estruturas.
    """

    # Variáveis chave para o ataque
    DURABILIDADE_PERDIDA_FERRAMENTA = 1  # Quantidade de durabilidade perdida por ataque na ferramenta
    DURABILIDADE_PERDIDA_ARMADURA = 1  # Quantidade de durabilidade perdida por ataque na armadura

    # Verificar se o mob está no mesmo chunk e na mesma estrutura (se aplicável)
    if estaEmEstrutura:
        cursor.execute("""
            SELECT InstanciaMob.vida_atual, Mob.tipo_mob
            FROM InstanciaMob
            JOIN Mob ON InstanciaMob.nome_mob = Mob.nome
            WHERE InstanciaMob.nome_mob = %s
            AND InstanciaMob.numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s)
            AND InstanciaMob.nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s)
            AND InstanciaMob.nome_estrutura = (SELECT nome_estrutura FROM Jogador WHERE nome = %s);
        """, (nomeMob, nomeUser, nomeUser, nomeUser))
    else:
        cursor.execute("""
            SELECT InstanciaMob.vida_atual, Mob.tipo_mob
            FROM InstanciaMob
            JOIN Mob ON InstanciaMob.nome_mob = Mob.nome
            WHERE InstanciaMob.nome_mob = %s
            AND InstanciaMob.numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s)
            AND InstanciaMob.nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s);
        """, (nomeMob, nomeUser, nomeUser))

    mob_data = cursor.fetchone()

    if not mob_data:
        mostrar_texto_gradualmente(f"O mob {nomeMob} não está presente neste chunk ou estrutura.", Fore.RED)
        time.sleep(2)
        return

    vida_mob_atual, tipo_mob = mob_data

    # Verificar se o jogador possui a ferramenta para atacar e sua durabilidade
    cursor.execute("""
        SELECT FerramentaDuravel.pts_dano, InstanciaItem.durabilidade_atual, InstanciaItem.id_inst_item
        FROM InstanciaItem
        JOIN FerramentaDuravel ON InstanciaItem.nome_item = FerramentaDuravel.nome_item
        WHERE InstanciaItem.nome_item = %s
        AND EXISTS (
            SELECT 1 FROM Inventario 
            WHERE id_inst_item = InstanciaItem.id_inst_item 
            AND id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s)
        );
    """, (nomeFerramenta, nomeUser))

    ferramenta = cursor.fetchone()

    if not ferramenta or ferramenta[1] <= 0:
        mostrar_texto_gradualmente("Você não tem uma ferramenta válida ou ela está quebrada.", Fore.RED)
        time.sleep(2)
        return

    pts_dano_ferramenta, durabilidade_atual, id_inst_item_ferramenta = ferramenta

    # Reduzir a vida do mob
    nova_vida_mob = vida_mob_atual - pts_dano_ferramenta
    cursor.execute("""
        UPDATE InstanciaMob 
        SET vida_atual = %s 
        WHERE nome_mob = %s 
        AND numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s);
    """, (nova_vida_mob, nomeMob, nomeUser))

    # Reduzir a durabilidade da ferramenta
    nova_durabilidade_ferramenta = durabilidade_atual - DURABILIDADE_PERDIDA_FERRAMENTA
    cursor.execute("""
        UPDATE InstanciaItem 
        SET durabilidade_atual = %s 
        WHERE id_inst_item = %s;
    """, (nova_durabilidade_ferramenta, id_inst_item_ferramenta))

    mostrar_texto_gradualmente(f"Você atacou {nomeMob} com {nomeFerramenta}.", Fore.GREEN)
    time.sleep(1.5)

    # Informar sobre a perda de durabilidade da ferramenta
    mostrar_texto_gradualmente(f"A {nomeFerramenta} perdeu {DURABILIDADE_PERDIDA_FERRAMENTA} ponto(s) de durabilidade. Durabilidade atual: {nova_durabilidade_ferramenta}.", Fore.LIGHTBLUE_EX)
    time.sleep(1.5)

    # Verificar se o mob morreu
    if nova_vida_mob <= 0:
        mostrar_texto_gradualmente(f"Você derrotou {nomeMob}!", Fore.YELLOW)
        time.sleep(1.5)

        # Remover o mob morto da instância
        cursor.execute("""
            DELETE FROM InstanciaMob 
            WHERE nome_mob = %s 
            AND numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s);
        """, (nomeMob, nomeUser))

        # Verificar e aplicar drops do mob
        cursor.execute("""
            SELECT nome_item, probabilidade, quantidade 
            FROM MobDropaItem 
            WHERE nome_mob = %s;
        """, (nomeMob,))
        drops = cursor.fetchall()

        for drop in drops:
            nome_item, probabilidade, quantidade = drop
            if random.random() <= probabilidade / 100:
                # Adicionar o item dropado ao inventário do jogador (quantidade correta)
                for _ in range(quantidade):
                    cursor.execute("""
                        INSERT INTO InstanciaItem (nome_item) 
                        VALUES (%s) RETURNING id_inst_item;
                    """, (nome_item,))
                    id_inst_item = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO Inventario (id_inst_item, id_inventario)
                        VALUES (%s, (SELECT id_jogador FROM Jogador WHERE nome = %s));
                    """, (id_inst_item, nomeUser))

                mostrar_texto_gradualmente(f"O mob {nomeMob} dropou {quantidade}x {nome_item}.", Fore.YELLOW)
                time.sleep(1.5)

    else:
        # Se o mob for agressivo, ele ataca de volta
        if tipo_mob == 'agressivo':
            mostrar_texto_gradualmente(f"{nomeMob} ainda está vivo e ataca de volta!", Fore.RED)
            time.sleep(1.5)

            # Mob ataca de volta, aplicar dano ao jogador com base no `pts_dano` da tabela `Agressivo`
            cursor.execute("""
                SELECT pts_dano 
                FROM Agressivo 
                WHERE nome_mob = %s;
            """, (nomeMob,))
            dano_mob = cursor.fetchone()[0]

            # Verificar armadura do jogador
            cursor.execute("""
                SELECT cabeca, peito, pernas, pes 
                FROM Jogador WHERE nome = %s;
            """, (nomeUser,))
            armaduras = cursor.fetchone()

            total_armadura = 0
            for peca_armadura in armaduras:
                if peca_armadura is not None:
                    cursor.execute("""
                        SELECT pts_armadura FROM armaduraduravel WHERE nome_item = %s;
                    """, (peca_armadura,))
                    pontos_armadura = cursor.fetchone()
                    if pontos_armadura:
                        total_armadura += pontos_armadura[0]

            # Calcular o dano mitigado
            dano_recebido = dano_mob / (1 + (total_armadura / 10))
            dano_mitigado = dano_mob - dano_recebido

            cursor.execute("""
                UPDATE Jogador 
                SET vida = vida - %s 
                WHERE nome = %s;
            """, (dano_recebido, nomeUser))

            # Verificar a vida do jogador
            cursor.execute("""
                SELECT vida 
                FROM Jogador 
                WHERE nome = %s;
            """, (nomeUser,))
            vida_jogador = cursor.fetchone()[0]

            # Informar ao jogador quanto dano foi mitigado pela armadura
            mostrar_texto_gradualmente(f"Você sofreu {int(dano_recebido)} de dano. Sua armadura mitigou {int(dano_mitigado)} de dano.", Fore.YELLOW)
            time.sleep(1.5)

            if vida_jogador <= 0:
                mostrar_texto_gradualmente(f"{nomeMob} derrotou você!", Fore.RED)
                time.sleep(2)

                # Remover o jogador do jogo
                cursor.execute("""
                    DELETE FROM Jogador WHERE nome = %s;
                """, (nomeUser,))
            else:
                mostrar_texto_gradualmente(f"Sua vida agora é {vida_jogador}.", Fore.YELLOW)
                time.sleep(1.5)

    # Verificar se a ferramenta quebrou
    if nova_durabilidade_ferramenta <= 0:
        mostrar_texto_gradualmente(f"Sua {nomeFerramenta} quebrou após o ataque!", Fore.RED)
        time.sleep(1.5)

        cursor.execute("""
            DELETE FROM Inventario 
            WHERE id_inst_item = %s;
        """, (id_inst_item_ferramenta,))

        cursor.execute("""
            DELETE FROM InstanciaItem 
            WHERE id_inst_item = %s;
        """, (id_inst_item_ferramenta,))

    connection.commit()
