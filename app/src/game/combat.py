from ..utils.helpers import mostrar_texto_gradualmente
from colorama import Fore
import random

# Comando: Atacar Mob
def atacar_mob(cursor, nomeUser, nomeMob, nomeFerramenta):
    """
    Permite ao jogador atacar um mob utilizando uma ferramenta ou arma do inventário.
    """
    # Verificar se o jogador possui a ferramenta adequada para o ataque e sua durabilidade
    cursor.execute("""
        SELECT FerramentaDuravel.pts_dano, InstanciaItem.durabilidade_atual 
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
    
    if ferramenta and ferramenta[1] > 0:
        # Atualizar a vida do mob após o ataque
        cursor.execute("""
            UPDATE InstanciaMob 
            SET vida_atual = vida_atual - %s
            WHERE nome_mob = %s 
            AND numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s);
        """, (ferramenta[0], nomeMob, nomeUser))
        
        # Reduzir a durabilidade da ferramenta utilizada
        cursor.execute("""
            UPDATE InstanciaItem 
            SET durabilidade_atual = durabilidade_atual - 1 
            WHERE nome_item = %s;
        """, (nomeFerramenta,))
        
        # Verificar a vida restante do mob
        cursor.execute("""
            SELECT vida_atual 
            FROM InstanciaMob 
            WHERE nome_mob = %s 
            AND numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s);
        """, (nomeMob, nomeUser))
        
        vida_mob = cursor.fetchone()[0]
        
        if vida_mob <= 0:
            # Mob morreu, remover instância do mob e notificar o jogador
            cursor.execute("""
                DELETE FROM InstanciaMob 
                WHERE nome_mob = %s 
                AND numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s);
            """, (nomeMob, nomeUser))
            mostrar_texto_gradualmente(f"Você matou {nomeMob}.", Fore.GREEN)

            # Verificar e aplicar drops do mob
            cursor.execute("""
                SELECT nome_item, probabilidade 
                FROM MobDropaItem 
                WHERE nome_mob = %s;
            """, (nomeMob,))
            drops = cursor.fetchall()
            for drop in drops:
                nome_item, probabilidade = drop
                if random.random() <= probabilidade / 100:
                    # Adicionar o item dropado ao inventário do jogador
                    cursor.execute("""
                        INSERT INTO InstanciaItem (nome_item) 
                        VALUES (%s) RETURNING id_inst_item;
                    """, (nome_item,))
                    id_inst_item = cursor.fetchone()[0]
                    cursor.execute("""
                        INSERT INTO Inventario (id_inst_item, id_inventario)
                        VALUES (%s, (SELECT id_jogador FROM Jogador WHERE nome = %s));
                    """, (id_inst_item, nomeUser))
                    mostrar_texto_gradualmente(f"O mob dropou {nome_item}.", Fore.YELLOW)
        else:
            mostrar_texto_gradualmente(f"Você atacou {nomeMob} com {nomeFerramenta}.", Fore.GREEN)
    else:
        mostrar_texto_gradualmente("Você não tem uma ferramenta válida ou ela está quebrada.", Fore.RED)
