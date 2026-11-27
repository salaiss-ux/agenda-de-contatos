"""
PARTE 1 - CADASTRO DE CONTATOS

Contém a função cadastrar_contato() e as funções de apoio que ela usa:
validações (telefone, e-mail, data), verificação de contato duplicado
e leitura dos campos.

Obs.: a função salvar_contatos() é da parte de persistência em arquivo
(outro integrante). Aqui ela só é chamada.
"""

from datetime import datetime


# ---------------------------------------------------------------
# VALIDAÇÕES
# ---------------------------------------------------------------
def apenas_digitos(texto):
    """Devolve só os números de um texto.
    Ex.: '(81) 99999-1234' -> '81999991234'"""
    resultado = ""
    for caractere in texto:
        if caractere.isdigit():
            resultado += caractere
    return resultado


def telefone_valido(telefone):
    """Telefone com DDD: 10 dígitos (fixo) ou 11 dígitos (celular).
    Só são aceitos números e os símbolos ( ) - e espaço."""
    for caractere in telefone:
        if not caractere.isdigit() and caractere not in "()- ":
            return False
    return len(apenas_digitos(telefone)) in (10, 11)


def email_valido(email):
    """Formato básico: usuario@dominio.extensao, sem espaços."""
    if " " in email or email.count("@") != 1:
        return False

    usuario, dominio = email.split("@")
    if usuario == "":
        return False
    if "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        return False
    if ".." in dominio:
        return False
    return len(dominio.split(".")[-1]) >= 2   # extensão com 2+ letras


def data_valida(texto):
    """Data no formato DD/MM/AAAA, existente, não futura e a partir de 1900."""
    try:
        data = datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        return False
    return 1900 <= data.year and data <= datetime.now()


def buscar_duplicado(contatos, nome=None, telefone=None, ignorar=None):
    """Procura um contato já cadastrado com o mesmo nome OU o mesmo telefone.
    - ignorar: índice de um contato a desconsiderar (usado na edição).
    Devolve o contato encontrado, ou None se não existir."""
    for i, contato in enumerate(contatos):
        if i == ignorar:
            continue
        if nome is not None and contato["nome"].lower() == nome.lower():
            return contato
        if telefone is not None and \
                apenas_digitos(contato["telefone"]) == apenas_digitos(telefone):
            return contato
    return None


# ---------------------------------------------------------------
# LEITURA DOS CAMPOS (input)
# ---------------------------------------------------------------
def ler_texto(mensagem, obrigatorio=True, atual=None):
    """Pede um texto ao usuário.
    - obrigatorio: se True, repete até digitar algo.
    - atual: valor atual (usado na edição; Enter mantém o valor).
      Em campos opcionais, digitar '-' apaga o valor."""
    while True:
        if atual is not None:
            texto = input(f"{mensagem} [{atual}]: ").strip()
            if texto == "":
                return atual              # Enter = manter o valor atual
            if texto == "-" and not obrigatorio:
                return ""                 # '-' = apagar campo opcional
        else:
            texto = input(f"{mensagem}: ").strip()

        if texto != "" or not obrigatorio:
            return texto
        print("  Campo obrigatório. Tente novamente.")


def ler_telefone(atual=None):
    """Lê o telefone repetindo até ser válido."""
    while True:
        telefone = ler_texto("Telefone com DDD", atual=atual)
        if telefone_valido(telefone):
            return telefone
        print("  Telefone inválido. Use 10 ou 11 dígitos, ex.: (81) 99999-1234")


def ler_email(atual=None):
    """Lê o e-mail (opcional) repetindo até ser válido ou vazio."""
    while True:
        email = ler_texto("E-mail (opcional)", obrigatorio=False, atual=atual)
        if email == "" or email_valido(email):
            return email
        print("  E-mail inválido. Exemplo: nome@dominio.com")


def ler_data(atual=None):
    """Lê a data de nascimento (opcional) repetindo até ser válida ou vazia."""
    while True:
        data = ler_texto("Data de nascimento DD/MM/AAAA (opcional)",
                         obrigatorio=False, atual=atual)
        if data == "" or data_valida(data):
            return data
        print("  Data inválida. Use o formato DD/MM/AAAA, ex.: 25/12/2000")


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

    # 2. Telefone (obrigatório) - valida o formato e confere se já existe
    telefone = ler_telefone()
    existente = buscar_duplicado(contatos, telefone=telefone)
    if existente is not None:
        print(f"Esse telefone já está cadastrado para: {existente['nome']}.")
        print("Cadastro cancelado.")
        return

    # 3. Campos opcionais
    email = ler_email()
    endereco = ler_texto("Endereço (Opcional)", obrigatorio=False)
    apelido = ler_texto("Apelido (Opcional)", obrigatorio=False)
    nascimento = ler_data()
    observacoes = ler_texto("Observações (Opcional)", obrigatorio=False)

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
    salvar_contatos(contatos)       # função da parte de persistência
    print("Contato cadastrado com sucesso!")
    
# ---------------------------------------------------------------
# PARTE 2 - BUSCA E LISTAGEM DE CONTATOS
# ---------------------------------------------------------------
def buscar_contato(contatos):
    """pesquisa contatos pelo nome e mostra os dados encontrados."""
    print("\n=== BUSCAR CONTATO ===")

    # pede o nome que o usuário deseja pesquisar
    nome = input("Nome: ").strip().lower()

    # verifica se algum contato foi encontrado
    encontrado = False

    # percorre todos os contatos cadastrados
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

    # informa quando a pesquisa não encontra resultados
    if encontrado == False:
        print("Nenhum contato encontrado!")
# informa quando a pesquisa não encontra resultados
    if encontrado == False:
        print("Nenhum contato encontrado!")

def listar_contatos(contatos):
    """mostra todos os dados dos contatos cadastrados."""
    print("\n=== LISTA DE CONTATOS ===")

    # verifica se a lista possui contatos
    if len(contatos) == 0:
        print("Nenhum contato cadastrado!")
    else:
        # percorre e exibe todos os dados de cada contato
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
# TESTE SOZINHO (só roda se você executar ESTE arquivo diretamente)
# Ao juntar com o grupo, não é necessário copiar esta parte.
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Versão provisória, só para testar sem o arquivo CSV.
    # No projeto final, a função verdadeira vem da parte de persistência.
    def salvar_contatos(contatos):
        pass

    contatos = []
    cadastrar_contato(contatos)
    cadastrar_contato(contatos)
    cadastrar_contato(contatos)
    cadastrar_contato(contatos)

    print("\nLista final:")
    for c in contatos:
        print(c)
