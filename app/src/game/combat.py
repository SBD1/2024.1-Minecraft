from ..utils.helpers import mostrar_texto_gradualmente
from colorama import Fore
import random
import time

# Comando: Atacar Mob
def atacar_mob(connection, cursor, nomeUser, nomeMob, nomeFerramenta):
    """
    Permite ao jogador atacar um mob utilizando uma ferramenta ou arma do inventário.
    """

    # Variáveis chave para o ataque
    DURABILIDADE_PERDIDA = 1  # Quantidade de durabilidade perdida por ataque

    # Verificar se o mob está no mesmo chunk que o jogador e obter suas informações de dano e vida
    cursor.execute("""
        SELECT InstanciaMob.vida_atual, Agressivo.pts_dano 
        FROM InstanciaMob 
        JOIN Agressivo ON InstanciaMob.nome_mob = Agressivo.nome_mob
        WHERE InstanciaMob.nome_mob = %s 
        AND InstanciaMob.numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s)
        AND InstanciaMob.nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s);
    """, (nomeMob, nomeUser, nomeUser))
    
    mob_data = cursor.fetchone()

    if not mob_data:
        mostrar_texto_gradualmente(f"O mob {nomeMob} não está presente neste chunk.", Fore.RED)
        time.sleep(2)
        return

    vida_mob_atual, dano_mob = mob_data

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
    nova_durabilidade = durabilidade_atual - DURABILIDADE_PERDIDA
    cursor.execute("""
        UPDATE InstanciaItem 
        SET durabilidade_atual = %s 
        WHERE id_inst_item = %s;
    """, (nova_durabilidade, id_inst_item_ferramenta))

    mostrar_texto_gradualmente(f"Você atacou {nomeMob} com {nomeFerramenta}.", Fore.GREEN)
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
        mostrar_texto_gradualmente(f"{nomeMob} ainda está vivo e ataca de volta!", Fore.RED)
        time.sleep(1.5)

        # Mob ataca de volta, aplicar dano ao jogador com base no `pts_dano` da tabela `Agressivo`
        cursor.execute("""
            UPDATE Jogador 
            SET vida = vida - %s 
            WHERE nome = %s;
        """, (dano_mob, nomeUser))

        # Verificar a vida do jogador
        cursor.execute("""
            SELECT vida 
            FROM Jogador 
            WHERE nome = %s;
        """, (nomeUser,))
        vida_jogador = cursor.fetchone()[0]

        if vida_jogador <= 0:
            mostrar_texto_gradualmente(f"{nomeMob} derrotou você!", Fore.RED)
            time.sleep(2)

            # Remover o jogador do jogo
            cursor.execute("""
                DELETE FROM Jogador WHERE nome = %s;
            """, (nomeUser,))
        else:
            mostrar_texto_gradualmente(f"Você sofreu {dano_mob} de dano. Sua vida agora é {vida_jogador}.", Fore.YELLOW)
            time.sleep(1.5)

    # Verificar se a ferramenta quebrou
    if nova_durabilidade <= 0:
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
