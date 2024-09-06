from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela
from colorama import Fore

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
            mostrar_texto_gradualmente(f"- {item[0]} (Durabilidade: {item[1] or 'N/A'})", Fore.CYAN)
    else:
        mostrar_texto_gradualmente("Seu inventário está vazio.", Fore.CYAN)

    input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...{Fore.RESET}")
    limpar_tela()
    

# Comando: Usar Item (alimento ou funcional)
def utilizar_item(cursor, nomeUser, nomeItem):
    """
    Permite ao jogador utilizar um item do inventário. 
    Se o item for um alimento, recupera fome. 
    Se for funcional, executa uma funcionalidade específica.
    """
    cursor.execute("""
        SELECT Item.tipo_item, Alimento.pts_fome, InstanciaItem.durabilidade_atual
        FROM InstanciaItem
        JOIN Item ON InstanciaItem.nome_item = Item.nome
        LEFT JOIN Alimento ON Item.nome = Alimento.nome_item
        WHERE InstanciaItem.nome_item = %s AND EXISTS (
            SELECT 1 FROM Inventario WHERE id_inst_item = InstanciaItem.id_inst_item AND id_inventario = (
                SELECT id_jogador FROM Jogador WHERE nome = %s
            )
        );
    """, (nomeItem, nomeUser))
    
    item_data = cursor.fetchone()
    
    if item_data:
        tipo_item, pts_fome, durabilidade = item_data
        
        if tipo_item == 'alimento':
            cursor.execute("UPDATE Jogador SET fome = fome + %s WHERE nome = %s;", (pts_fome, nomeUser))
            mostrar_texto_gradualmente(f"Você consumiu {nomeItem} e recuperou {pts_fome} pontos de fome.", Fore.GREEN)
        elif tipo_item == 'craftavel':
            # Implementar funcionalidades específicas para itens funcionais
            mostrar_texto_gradualmente(f"Você usou {nomeItem}. Função: em breve disponível.", Fore.YELLOW)

        cursor.execute("UPDATE Inventario SET qtd = qtd - 1 WHERE id_inst_item = (SELECT id_inst_item FROM InstanciaItem WHERE nome_item = %s);", (nomeItem,))
    else:
        mostrar_texto_gradualmente(f"Item {nomeItem} não encontrado no inventário.", Fore.RED)
