# Importa 「datetime」 ⇒ Valida e compara datas!
from datetime import date, datetime


# Função padrão caso o módulo seja usado sem a persistência externa definida
def salvar_contatos(contatos):
    pass


# ---------------------------------------------------------------
# 【VALIDAÇÕES】⇒ Define as regras para não virar bagunça!
# ---------------------------------------------------------------

# 【REGRA】Filtra o input do usuário, deixando apenas números.
def apenas_digitos(texto):
    resultado = ""
    for caractere in texto:
        if caractere.isdigit():
            resultado += caractere
    return resultado


# 【REGRA】Checa caracteres permitidos e quantidade de dígitos.
def telefone_valido(telefone):
    for caractere in telefone:
        if not caractere.isdigit() and caractere not in "()- ":
            return False
    return len(apenas_digitos(telefone)) in (10, 11)


# 【REGRA】Se não tiver EXATAMENTE 1 "@", invalide!
def email_valido(email):
    if " " in email or email.count("@") != 1:
        return False

    # 【REGRA】Checa a estrutura do e-mail.
    usuario, dominio = email.split("@")

    return (
        bool(usuario)
        and "." in dominio
        and not dominio.startswith(".")
        and not dominio.endswith(".")
        and ".." not in dominio
        and len(dominio.rsplit(".", 1)[-1]) >= 2
    )


# 【REGRA】Checa formato da data e devolve date ou None.
def parse_data(texto):
    limpo = texto.strip().replace("-", "/")

    if "/" not in limpo and len(limpo) == 8 and limpo.isdigit():
        limpo = f"{limpo[:2]}/{limpo[2:4]}/{limpo[4:]}"

    try:
        data = datetime.strptime(limpo, "%d/%m/%Y").date()
    except ValueError:
        return None

    if not (1900 <= data.year and data <= date.today()):
        return None

    return data


# 【REGRA】Checa formato da data. Sem data futura e datas antes de 1900.
def data_valida(texto):
    return parse_data(texto) is not None


# 【REGRA】Checa se há um contato duplicado.
def buscar_duplicado(contatos, nome=None, telefone=None, ignorar=None):
    digitos_telefone = apenas_digitos(telefone) if telefone else ""

    for i, contato in enumerate(contatos):
        if i == ignorar:
            continue

        mesmo_nome = bool(nome) and contato["nome"].strip().lower() == nome.strip().lower()
        mesmo_telefone = (
            bool(digitos_telefone)
            and apenas_digitos(contato.get("telefone", "")) == digitos_telefone
        )

        if mesmo_nome or mesmo_telefone:
            return contato

    return None


# ---------------------------------------------------------------
# 【VALIDAÇÕES】⇒ Verificando o input do usuário.
# ---------------------------------------------------------------

# Lê o input do usuário, exigindo preenchimento quando obrigatório e
# oferecendo atalhos de manter (Enter) ou apagar ('-') durante a edição.
def ler_texto(mensagem, obrigatorio=True, atual=None):
    while True:
        if atual is not None:
            texto = input(f"{mensagem} [{atual}]: ").strip()
            if texto == "":
                return atual
            if texto == "-" and not obrigatorio:
                return ""
        else:
            texto = input(f"{mensagem}: ").strip()

        if texto != "" or not obrigatorio:
            return texto
        print("  Campo obrigatório. Tente novamente.")


def ler_telefone(atual=None):
    while True:
        telefone = ler_texto("Telefone com DDD", atual=atual)
        if telefone_valido(telefone):
            return telefone
        print(" ※ Telefone inválido. Use 10 ou 11 dígitos.")


def ler_email(atual=None):
    while True:
        email = ler_texto("E-mail (opcional)", obrigatorio=False, atual=atual)
        if email == "" or email_valido(email):
            return email
        print(" ※ E-mail inválido! Use o padrão: nome@dominio.com")


def ler_data(atual=None):
    while True:
        data_texto = ler_texto(
            "Data de nascimento ⇒ DD/MM/AAAA ※ Opcional",
            obrigatorio=False,
            atual=atual,
        )
        if data_texto == "":
            return ""
        data_obj = parse_data(data_texto)
        if data_obj is not None:
            return data_obj.strftime("%d/%m/%Y")
        print(" ※ Data inválida! Use o formato: DD/MM/AAAA")


# ---------------------------------------------------------------
# FUNÇÃO PRINCIPAL DESTA PARTE
# ---------------------------------------------------------------
def cadastrar_contato(contatos):
    """Cadastra um novo contato e o adiciona à lista principal."""
    print("\n=== NOVO CONTATO ===")
    print("(Campos marcados como 'opcional' podem ficar em branco: aperte Enter)\n")

    # 1. Nome (obrigatório) - já confere se o contato existe
    nome = ler_texto("Nome")
    if buscar_duplicado(contatos, nome=nome) is not None:
        print("Já existe um contato com esse nome. Cadastro cancelado.")
        return
    print("---------------------------------")

    # 2. Telefone (obrigatório) - valida o formato e confere se já existe
    telefone = ler_telefone()
    existente = buscar_duplicado(contatos, telefone=telefone)
    if existente is not None:
        print(f"Esse telefone já está cadastrado para: {existente['nome']}.")
        print("Cadastro cancelado.")
        return
    print("---------------------------------")

    # 3. Campos opcionais
    email = ler_email()
    endereco = ler_texto("Endereço (Opcional)", obrigatorio=False)
    apelido = ler_texto("Apelido (Opcional)", obrigatorio=False)
    nascimento = ler_data()
    observacoes = ler_texto("Observações (Opcional)", obrigatorio=False)
    print("---------------------------------")

    # 4. Organizar os dados em um dicionário
    contato = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "endereco": endereco,
        "apelido": apelido,
        "nascimento": nascimento,
        "observacoes": observacoes,
    }

    # 5. Adicionar à lista principal e salvar no arquivo
    contatos.append(contato)
    salvar_contatos(contatos)
    print("Contato cadastrado com sucesso!")


# ---------------------------------------------------------------
# PARTE 2 - BUSCA E LISTAGEM DE CONTATOS
# ---------------------------------------------------------------
def buscar_contato(contatos):
    """Pesquisa contatos pelo nome e mostra os dados encontrados."""
    print("\n=== BUSCAR CONTATO ===")

    nome = input("Nome: ").strip().lower()
    if not nome:
        print("Digite um nome para buscar.")
        return

    encontrado = False

    for contato in contatos:
        if nome in contato["nome"].lower():
            print("\n=== CONTATO ENCONTRADO ===")
            print("Nome:", contato["nome"])
            print("Telefone:", contato["telefone"])
            print("E-mail:", contato["email"])
            print("Endereço:", contato["endereco"])
            print("Apelido:", contato["apelido"])
            print("Nascimento:", contato["nascimento"])
            print("Observações:", contato["observacoes"])
            encontrado = True

    if not encontrado:
        print("Nenhum contato encontrado!")


def listar_contatos(contatos):
    """Mostra todos os dados dos contatos cadastrados."""
    print("\n=== LISTA DE CONTATOS ===")

    if len(contatos) == 0:
        print("Nenhum contato cadastrado!")
    else:
        for contato in contatos:
            print("\n-------------------------")
            print("Nome:", contato["nome"])
            print("Telefone:", contato["telefone"])
            print("E-mail:", contato["email"])
            print("Endereço:", contato["endereco"])
            print("Apelido:", contato["apelido"])
            print("Nascimento:", contato["nascimento"])
            print("Observações:", contato["observacoes"])

    print("\n=== FIM DA LISTA ===")


# ---------------------------------------------------------------
# PARTE 3 - EDIÇÃO E EXCLUSÃO DE CONTATOS
# ---------------------------------------------------------------
def escolher_contato(contatos, acao):
    """Pesquisa por nome e devolve a posição (índice) do contato escolhido.
    Devolve None se nada for encontrado ou se o usuário cancelar."""
    busca = input(f"Nome do contato que deseja {acao}: ").strip().lower()
    if not busca:
        print("Digite um nome para pesquisar.")
        return None

    encontrados = []
    for i, contato in enumerate(contatos):
        if busca in contato["nome"].lower():
            encontrados.append(i)

    if len(encontrados) == 0:
        print("Nenhum contato encontrado!")
        return None

    if len(encontrados) == 1:
        return encontrados[0]

    print("\nVários contatos encontrados:")
    for numero, i in enumerate(encontrados, start=1):
        print(f"  {numero}. {contatos[i]['nome']} - {contatos[i]['telefone']}")

    while True:
        escolha = input("Digite o número do contato (ou 0 para cancelar): ").strip()
        if escolha.isdigit() and 0 <= int(escolha) <= len(encontrados):
            if int(escolha) == 0:
                return None
            return encontrados[int(escolha) - 1]
        print("  Opção inválida. Tente novamente.")


def editar_contato(contatos):
    """Altera os dados de um contato existente."""
    print("\n=== EDITAR CONTATO ===")

    indice = escolher_contato(contatos, "editar")
    if indice is None:
        return

    contato = contatos[indice]
    print("\n(Enter = manter o valor atual | '-' = apagar campo opcional)\n")

    # 1. Nome (obrigatório) - não pode repetir o nome de OUTRO contato
    while True:
        nome = ler_texto("Nome", atual=contato["nome"])
        if buscar_duplicado(contatos, nome=nome, ignorar=indice) is None:
            break
        print(" ※ Já existe outro contato com esse nome.")

    # 2. Telefone (obrigatório) - não pode repetir o de OUTRO contato
    while True:
        telefone = ler_telefone(atual=contato["telefone"])
        existente = buscar_duplicado(contatos, telefone=telefone, ignorar=indice)
        if existente is None:
            break
        print(f" ※ Esse telefone já pertence a: {existente['nome']}.")

    # 3. Campos opcionais
    email = ler_email(atual=contato["email"])
    endereco = ler_texto("Endereço (Opcional)", obrigatorio=False, atual=contato["endereco"])
    apelido = ler_texto("Apelido (Opcional)", obrigatorio=False, atual=contato["apelido"])
    nascimento = ler_data(atual=contato["nascimento"])
    observacoes = ler_texto(
        "Observações (Opcional)", obrigatorio=False, atual=contato["observacoes"]
    )

    # 4. Só altera o dicionário depois que tudo foi preenchido com sucesso
    contato["nome"] = nome
    contato["telefone"] = telefone
    contato["email"] = email
    contato["endereco"] = endereco
    contato["apelido"] = apelido
    contato["nascimento"] = nascimento
    contato["observacoes"] = observacoes

    salvar_contatos(contatos)
    print("Contato atualizado com sucesso!")


def excluir_contato(contatos):
    """Remove um contato da lista, após confirmação."""
    print("\n=== EXCLUIR CONTATO ===")

    indice = escolher_contato(contatos, "excluir")
    if indice is None:
        return

    contato = contatos[indice]
    confirmacao = (
        input(f"Tem certeza que deseja excluir '{contato['nome']}'? (s/n): ")
        .strip()
        .lower()
    )

    if confirmacao == "s":
        del contatos[indice]
        salvar_contatos(contatos)
        print("Contato excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


# ---------------------------------------------------------------
# TESTE SOZINHO (só roda se você executar ESTE arquivo diretamente)
# Ao juntar com o grupo, não é necessário copiar esta parte.
# ---------------------------------------------------------------
if __name__ == "__main__":
    contatos = []
    cadastrar_contato(contatos)
    cadastrar_contato(contatos)
    cadastrar_contato(contatos)
    cadastrar_contato(contatos)

    print("\nLista final:")
    for c in contatos:
        print(c)