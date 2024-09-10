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
            SELECT InstanciaMob.id_inst_mob, InstanciaMob.vida_atual, Mob.tipo_mob
            FROM InstanciaMob
            JOIN Mob ON InstanciaMob.nome_mob = Mob.nome
            WHERE InstanciaMob.nome_mob = %s
            AND InstanciaMob.numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s)
            AND InstanciaMob.nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s)
            AND EXISTS (
                SELECT 1
                FROM InstanciaEstrutura
                WHERE InstanciaEstrutura.numero_chunk = InstanciaMob.numero_chunk
                AND InstanciaEstrutura.nome_mapa = InstanciaMob.nome_mapa
            )
            LIMIT 1;  -- Seleciona apenas o primeiro mob encontrado
        """, (nomeMob, nomeUser, nomeUser))
    else:
        cursor.execute("""
            SELECT InstanciaMob.id_inst_mob, InstanciaMob.vida_atual, Mob.tipo_mob
            FROM InstanciaMob
            JOIN Mob ON InstanciaMob.nome_mob = Mob.nome
            WHERE InstanciaMob.nome_mob = %s
            AND InstanciaMob.numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s)
            AND InstanciaMob.nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s)
            LIMIT 1;  -- Seleciona apenas o primeiro mob encontrado
        """, (nomeMob, nomeUser, nomeUser))

    mob_data = cursor.fetchone()

    if not mob_data:
        mostrar_texto_gradualmente(f"O mob {nomeMob} não está presente neste chunk ou estrutura.", Fore.RED)
        time.sleep(2)
        return

    id_inst_mob, vida_mob_atual, tipo_mob = mob_data

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
        WHERE id_inst_mob = %s;
    """, (nova_vida_mob, id_inst_mob))

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
            WHERE id_inst_mob = %s;
        """, (id_inst_mob,))

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

            # Verificar pontos de armadura do jogador
            cursor.execute("""
                SELECT pts_armadura, cabeca, peito, pernas, pes
                FROM Jogador 
                WHERE nome = %s;
            """, (nomeUser,))
            jogador_info = cursor.fetchone()

            pts_armadura, cabeca_id, peito_id, pernas_id, pes_id = jogador_info

            # Pegar a durabilidade atual das armaduras equipadas e diminuir a durabilidade
            ids_armaduras = {
                'cabeca': cabeca_id, 
                'peito': peito_id, 
                'pernas': pernas_id, 
                'pes': pes_id
            }

            for parte_corpo, id_arma in ids_armaduras.items():
                if id_arma is not None:
                    # Obter durabilidade da peça de armadura
                    cursor.execute("""
                        SELECT InstanciaItem.durabilidade_atual, ArmaduraDuravel.durabilidade_total, InstanciaItem.nome_item
                        FROM InstanciaItem
                        JOIN ArmaduraDuravel ON InstanciaItem.nome_item = ArmaduraDuravel.nome_item
                        WHERE InstanciaItem.id_inst_item = %s;
                    """, (id_arma,))
                    armadura_durabilidade = cursor.fetchone()

                    if armadura_durabilidade:
                        durab_atual, durab_total, nome_armadura = armadura_durabilidade
                        nova_durabilidade = durab_atual - DURABILIDADE_PERDIDA_ARMADURA

                        cursor.execute("""
                            UPDATE InstanciaItem
                            SET durabilidade_atual = %s
                            WHERE id_inst_item = %s;
                        """, (nova_durabilidade, id_arma))

                        # Informar durabilidade atual da armadura
                        mostrar_texto_gradualmente(f"Sua armadura {nome_armadura} ({parte_corpo}) perdeu {DURABILIDADE_PERDIDA_ARMADURA} ponto(s) de durabilidade. Durabilidade atual: {nova_durabilidade}.", Fore.LIGHTBLUE_EX)
                        time.sleep(1.5)

                        # Verificar se a armadura quebrou
                        if nova_durabilidade <= 0:
                            mostrar_texto_gradualmente(f"Sua armadura {nome_armadura} ({parte_corpo}) quebrou!", Fore.RED)
                            time.sleep(1.5)

                            # Primeiro, remover a referência da armadura do corpo do jogador
                            cursor.execute(f"""
                                UPDATE Jogador
                                SET {parte_corpo} = NULL
                                WHERE nome = %s;
                            """, (nomeUser,))

                            # Agora, remover a armadura do inventário
                            cursor.execute("""
                                DELETE FROM Inventario WHERE id_inst_item = %s;
                            """, (id_arma,))

                            # Finalmente, remover a armadura da tabela InstanciaItem
                            cursor.execute("""
                                DELETE FROM InstanciaItem WHERE id_inst_item = %s;
                            """, (id_arma,))

            # Calcular o dano mitigado
            dano_recebido = round(dano_mob / (1 + (pts_armadura / 10)))
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

                # Reviver o jogador em sua casa
                cursor.execute("""
                    SELECT casa_chunk, nome_mapa FROM Jogador WHERE nome = %s;
                """, (nomeUser,))
                jogador_data = cursor.fetchone()
                casa_chunk, mapa_atual = jogador_data

                # Verificar se o jogador está em um mapa que não seja a superfície
                if mapa_atual != "Superfície":
                    novo_mapa = "Superfície"
                else:
                    novo_mapa = mapa_atual 

                # Atualiza o jogador para sua casa, coloca no mapa da superfície e restaura a vida e fome ao máximo
                cursor.execute("""
                    UPDATE Jogador
                    SET numero_chunk = %s,
                        nome_mapa = %s,
                        vida = 20,
                        fome = 20
                    WHERE nome = %s;
                """, (casa_chunk, novo_mapa, nomeUser))

                connection.commit()

                mostrar_texto_gradualmente(f"Você desmaiou e foi resgatado em sua casa. Sua vida e fome foram restauradas.", Fore.GREEN)
                time.sleep(2)
                return "morreu"

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
    input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...{Fore.RESET}")

