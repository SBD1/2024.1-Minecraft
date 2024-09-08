from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela
from colorama import Fore
import time

# Comando: Visualizar Inventário
def visualizar_inventario(cursor, nomeUser):
    """
    Exibe os itens no inventário do jogador.
    """
    cursor.execute("""
        SELECT Item.nome AS item_nome, InstanciaItem.durabilidade_atual
        FROM Inventario
        JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
        JOIN Item ON InstanciaItem.nome_item = Item.nome
        WHERE Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s);
    """, (nomeUser,))
    
    inventario = cursor.fetchall()
    if inventario:
        mostrar_texto_gradualmente("Seu inventário:", Fore.CYAN)
        for item in inventario:
            if item[1] is not None:
                mostrar_texto_gradualmente(f"- {item[0]} (Durabilidade: {item[1]})", Fore.CYAN)
            else:
                mostrar_texto_gradualmente(f"- {item[0]}", Fore.CYAN)
    else:
        mostrar_texto_gradualmente("Seu inventário está vazio.", Fore.CYAN)

    input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...{Fore.RESET}")
    
# Comando: Comer Item (alimento)
def comer(cursor, nomeUser, nomeItem):
    """
    Permite ao jogador consumir um alimento do inventário, recuperando fome e removendo o item do inventário e da tabela de InstanciaItem.
    """

    # Verifica se o item é alimento e se está no inventário do jogador
    cursor.execute("""
        SELECT Alimento.pts_fome, InstanciaItem.id_inst_item
        FROM InstanciaItem
        JOIN Item ON InstanciaItem.nome_item = Item.nome
        JOIN Alimento ON Item.nome = Alimento.nome_item
        WHERE InstanciaItem.nome_item = %s 
        AND EXISTS (
            SELECT 1 FROM Inventario 
            WHERE id_inst_item = InstanciaItem.id_inst_item 
            AND id_inventario = (
                SELECT id_jogador FROM Jogador WHERE nome = %s
            )
        );
    """, (nomeItem, nomeUser))

    item_data = cursor.fetchone()

    if item_data:
        pts_fome, id_inst_item = item_data
        # Atualiza a fome do jogador
        cursor.execute("UPDATE Jogador SET fome = fome + %s WHERE nome = %s;", (pts_fome, nomeUser))
        
        # Remove o item do inventário e da tabela de instância
        cursor.execute("DELETE FROM Inventario WHERE id_inst_item = %s;", (id_inst_item,))
        cursor.execute("DELETE FROM InstanciaItem WHERE id_inst_item = %s;", (id_inst_item,))
        
        mostrar_texto_gradualmente(f"Você consumiu {nomeItem} e recuperou {pts_fome} pontos de fome.", Fore.GREEN)
    else:
        mostrar_texto_gradualmente(f"Item {nomeItem} não encontrado no inventário ou não é um alimento.", Fore.RED)

    time.sleep(2)

# Comando: Utilizar Item (funcional)
def utilizar_item(cursor, nomeUser, nomeItem):
    """
    Permite ao jogador utilizar um item funcional do inventário.
    Verifica se o item é funcional, se sim, executa a funcionalidade específica.
    Se não for utilizável, exibe uma mensagem.
    """
    # Verifica se o item está no inventário do jogador e se é do tipo craftavel
    cursor.execute("""
        SELECT Item.tipo_item, InstanciaItem.id_inst_item
        FROM InstanciaItem
        JOIN Item ON InstanciaItem.nome_item = Item.nome
        WHERE InstanciaItem.nome_item = %s 
        AND EXISTS (
            SELECT 1 FROM Inventario 
            WHERE id_inst_item = InstanciaItem.id_inst_item 
            AND id_inventario = (
                SELECT id_jogador FROM Jogador WHERE nome = %s
            )
        );
    """, (nomeItem, nomeUser))

    item_data = cursor.fetchone()

    if item_data:
        tipo_item, id_inst_item = item_data

        # Se o item é do tipo 'craftavel', verificamos se é um dos itens funcionais
        if tipo_item == 'craftavel':
            if nomeItem in ["Mapa", "Bússola", "Olho do Ender"]:
                # Implementar funcionalidades específicas para itens funcionais
                if nomeItem == "Isqueiro":
                    mostrar_texto_gradualmente(f"Você usou {nomeItem} para acender uma chama.", Fore.YELLOW)
                elif nomeItem == "Mapa":
                    mostrar_texto_gradualmente(f"Você abriu o {nomeItem} para visualizar a região.", Fore.YELLOW)
                elif nomeItem == "Bússola":
                    mostrar_texto_gradualmente(f"Você usou a {nomeItem} para encontrar a direção.", Fore.YELLOW)
                elif nomeItem == "Olho do Ender":
                    mostrar_texto_gradualmente(f"Você usou o {nomeItem} para localizar uma fortaleza.", Fore.YELLOW)
            else:
                mostrar_texto_gradualmente(f"O item {nomeItem} não tem uma função utilizável.", Fore.RED)
        else:
            mostrar_texto_gradualmente(f"O item {nomeItem} não pode ser utilizado.", Fore.RED)
    else:
        mostrar_texto_gradualmente(f"Item {nomeItem} não encontrado no inventário.", Fore.RED)

    time.sleep(2)