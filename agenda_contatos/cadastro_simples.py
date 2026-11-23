def cadastrar_contato(contatos):
    print("\n=== NOVO CONTATO ===")

    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("E-mail: ").strip()
    endereco = input("Endereço: ").strip()

    if nome == "" or telefone == "":
        print("Erro: nome e telefone são obrigatórios!")
        return

    contato = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "endereco": endereco
    }

    contatos.append(contato)
    print("Contato cadastrado com sucesso!")


# Teste da função
contatos = []
cadastrar_contato(contatos)
print(contatos)