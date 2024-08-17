def main():
    print("Bem-vindo ao somador de números!")
    while True:
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
            soma = num1 + num2
            print(f"A soma de {num1} e {num2} é {soma}.")
        except ValueError:
            print("Por favor, insira um número válido.")
        except KeyboardInterrupt:
            print("\nSaindo...")
            break

if __name__ == "__main__":
    main()
