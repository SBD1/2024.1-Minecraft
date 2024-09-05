import re
from colorama import Fore
import os
import time

# Função para validar o nick do usuário
def validar_nick(nomeUser):
    """
    Verifica se o nome de usuário é válido, permitindo apenas letras, números e sublinhados,
    com até 30 caracteres. Exibe uma mensagem de erro se for inválido.

    :param nomeUser: Nome de usuário a ser validado
    :return: Retorna True se o nome for válido, False caso contrário
    """
    if re.fullmatch(r'^[a-zA-Z0-9_]{1,30}$', nomeUser):
        return True
    else:
        mostrar_texto_gradualmente(
            "Nome de usuário inválido! Use apenas letras, números e sublinhados, com no máximo 30 caracteres.",
            Fore.RED
        )
        return False

def mostrar_texto_gradualmente(texto, cor=Fore.CYAN, velocidade=0.03):
    """Exibe o texto gradualmente, como uma máquina de escrever."""
    for char in texto:
        print(cor + char, end='', flush=True)
        time.sleep(velocidade)
    print()

def limpar_tela():
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Mostrar bioma com cor específica
def mostrar_bioma_com_cor(bioma):
    cor_bioma = determinar_cor_bioma(bioma)
    mostrar_texto_gradualmente("Do bioma:", Fore.CYAN)
    mostrar_texto_gradualmente(bioma, cor_bioma)

# Determinar a cor do bioma
def determinar_cor_bioma(bioma):
    cores_biomas = {
        'Lago': Fore.BLUE,
        'Deserto': Fore.YELLOW,
        'Planície': Fore.LIGHTGREEN_EX,
        'Floresta': Fore.GREEN,
        'Selva': Fore.LIGHTBLACK_EX,
        'Pântano': Fore.MAGENTA, 
        'Montanha': Fore.WHITE,
        'Neve': Fore.LIGHTCYAN_EX,
        'Descampado': Fore.LIGHTYELLOW_EX,  
        'Floresta carmesim': Fore.RED,      
        'Floresta distorcida': Fore.LIGHTBLUE_EX,  
        'Fortaleza': Fore.LIGHTBLACK_EX,    
        'Ilha do fim': Fore.LIGHTMAGENTA_EX
    }
    return cores_biomas.get(bioma, Fore.WHITE)

