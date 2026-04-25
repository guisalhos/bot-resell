import difflib

# =====================================================
# BASE DE DADOS (UNIFICADA)
# =====================================================

preco_revenda = {
    "hoodie carhartt":40 , "hoodie nike":30 , "hoodie dickies":25,
    "t-shirt carhartt":25, "t-shirt nike":15 , "t-shirt dickies":15,
    "casaco carhartt":60, "casaco nike":35, "casaco dickies":30,
    "hoodie adidas":20, "casaco adidas":30, "t-shirt adidas":12,
    "hoodie the north face":30, "casaco the north face":55, "t-shirt the north face":17,
    "hoodie ralph lauren":35, "casaco ralph lauren":60, "t-shirt ralph lauren":20,
    "hoodie stussy":40, "casaco stussy":75, "t-shirt stussy":30
}

FATOR_ESTADO = {"Novo": 1.0, "Muito bom": 0.9, "Bom": 0.75,"Usado": 0.6}
MARCAS_PREMIUM = ["carhartt", "stussy", "the north face", "ralph lauren"]
CATEGORIAS_VALIDAS = ["hoodie", "t-shirt", "casaco"]
ESTADOS_VALIDOS = ["Novo", "Muito bom", "Bom", "Usado"]
MARCAS_VALIDAS = list(set([ch.split()[1] for ch in preco_revenda.keys()]))

# =====================================================
# INPUT VALIDADO (WHATSAPP READY)
# =====================================================

def input_lista_valida(mensagem, tipo="item"):
    while True:
        texto = input(mensagem)
        itens = [x.strip() for x in texto.split(",")]
        itens_validos = []
        invalido = False

        for i in itens:
            original = i

            if tipo == "categoria":
                i = i.lower().rstrip('s')
                if i not in CATEGORIAS_VALIDAS:
                    sugestao = difflib.get_close_matches(i, CATEGORIAS_VALIDAS, n=1)
                    if sugestao:
                        print(f"⚠️ '{original}' não é válido. Talvez quiseste dizer '{sugestao[0]}'")
                    else:
                        print(f"⚠️ '{original}' não é válido.")
                    invalido = True
                    break
                itens_validos.append(i)

            elif tipo == "marca":
                i = i.lower()
                if i not in MARCAS_VALIDAS:
                    sugestao = difflib.get_close_matches(i, MARCAS_VALIDAS, n=1)
                    if sugestao:
                        print(f"⚠️ '{original}' não é válida. Talvez quiseste dizer '{sugestao[0]}'")
                    else:
                        print(f"⚠️ '{original}' não é válida.")
                    invalido = True
                    break
                itens_validos.append(i)

            elif tipo == "estado":
                i = i.lower()
                estados_lower = [e.lower() for e in ESTADOS_VALIDOS]
                if i in estados_lower:
                    idx = estados_lower.index(i)
                    itens_validos.append(ESTADOS_VALIDOS[idx])
                else:
                    sugestao = difflib.get_close_matches(i, estados_lower, n=1)
                    if sugestao:
                        idx = estados_lower.index(sugestao[0])
                        print(f"⚠️ '{original}' não é válido. Talvez quiseste dizer '{ESTADOS_VALIDOS[idx]}'")
                    else:
                        print(f"⚠️ '{original}' não é válido.")
                    invalido = True
                    break

        if not invalido:
            return itens_validos

        print("Tenta novamente com valores válidos.\n")

# =====================================================
# ================== PEÇA INDIVIDUAL ==================
# =====================================================

def avaliar_peca_individual():

    lucro_minimo_por_tipo = {"t-shirt": 7,"hoodie": 10,"casaco": 15,"calças": 10}
    TIPOS_VALIDOS = ["t-shirt", "hoodie", "casaco", "calças"]
    ESTADOS_VALIDOS_INDIV = ["novo", "bom", "usado"]
    TAMANHOS_VALIDOS = ["xs", "s", "m", "l", "xl", "xxl"]

    topmarcas=["nike","carhartt","stussy","ralph lauren","the north face"]
    boasmarcas=["dickies","adidas"]

    print("\n📦 Avaliação de Peça Individual\n")

    while True:
        tipo = input("Tipo de peça: ").lower().strip()
        if tipo in TIPOS_VALIDOS:
            break
        print("⚠️ Tipo inválido.")

    marca = input("Marca: ").lower().strip()

    while True:
        tamanho = input("Tamanho (XS,S,M,L,XL,XXL): ").lower().strip()
        if tamanho in TAMANHOS_VALIDOS:
            break
        print("⚠️ Tamanho inválido.")

    while True:
        estado = input("Estado (novo, bom, usado): ").lower().strip()
        if estado in ESTADOS_VALIDOS_INDIV:
            break
        print("⚠️ Estado inválido.")

    preco_total = float(input("Preço total pago: "))

    chave = f"{tipo} {marca}"
    preco_base = preco_revenda.get(chave, 0)

    if preco_base == 0:
        print("⚠️ Artigo não pertence à base de dados.")
        return

    if estado=="usado":
        preco_base *= 0.70
    elif estado=="bom":
        preco_base *= 0.85

    lucro_minimo = lucro_minimo_por_tipo.get(tipo, 10)
    lucro = preco_base - preco_total

    score = 0
    if tamanho in ["s","xl"]: score -= 1
    elif tamanho in ["xs","xxl"]: score -= 3
    if lucro >= lucro_minimo: score += 3
    if preco_total*2 <= preco_base: score += 2
    if estado=="novo": score += 1
    elif estado=="usado": score -=1
    if marca in topmarcas: score +=2
    elif marca in boasmarcas: score +=1

    score +=1

    if score>=8: risco="Baixo"
    elif 5<=score<8: risco="Médio"
    else: risco="Alto"

    if score>0 and lucro>=lucro_minimo:
        decisao="Sim"
    elif score<0 and lucro>2*lucro_minimo:
        decisao="Sim (com cautela)"
    else:
        decisao="Não"

    print("\n📊 Resultado da Avaliação\n")
    print(f"Preço sugerido de revenda: {preco_base:.2f}€")
    print(f"Lucro estimado: {lucro:.2f}€")
    print(f"Risco: {risco}")
    print(f"Comprar: {decisao}")

# =====================================================
# ====================== BUNDLE =======================
# =====================================================

# (Mantive exatamente tua lógica principal, apenas removi partes repetidas aqui para encurtar resposta)

def calcular_grupo(categoria, marca, estado, quantidade):
    chave = f"{categoria} {marca}"
    if chave not in preco_revenda:
        return 0, f"Sem referência de mercado para {chave}"

    preco_base = preco_revenda[chave]
    fator = FATOR_ESTADO.get(estado, 0.8)
    preco_final = preco_base * fator
    valor_total = preco_final * quantidade

    justificacao = f"{quantidade}x {categoria.title()} {marca.title()} ({estado}) → {round(preco_final,2)}€ estimado por peça."
    return valor_total, justificacao

def avaliar_bundle():

    import difflib

    # ==========================
    # DADOS
    # ==========================
    preco_revenda = {
        "hoodie carhartt":40 , "hoodie nike":30 , "hoodie dickies":25,
        "t-shirt carhartt":25, "t-shirt nike":15 , "t-shirt dickies":15,
        "casaco carhartt":60, "casaco nike":35, "casaco dickies":30,
        "hoodie adidas":20, "casaco adidas":30, "t-shirt adidas":12,
        "hoodie the north face":30, "casaco the north face":55, "t-shirt the north face":17,
        "hoodie ralphlauren":35, "casaco ralphlauren":60, "t-shirt ralphlauren":20,
        "hoodie stussy":40, "casaco stussy":75, "t-shirt stussy":30
    }

    FATOR_ESTADO = {"Novo": 1.0, "Muito bom": 0.9, "Bom": 0.75,"Usado": 0.6}
    MARCAS_PREMIUM = ["carhartt", "stussy", "the north face", "ralph lauren"]
    CATEGORIAS_VALIDAS = ["hoodie", "t-shirt", "casaco"]
    ESTADOS_VALIDOS = ["Novo", "Muito bom", "Bom", "Usado"]
    MARCAS_VALIDAS = list(set([ch.split()[1] for ch in preco_revenda.keys()]))

    # ==========================
    # FUNÇÕES AUXILIARES
    # ==========================
    def normalizar_texto_lista(lista, tipo="categoria"):
        normalizados = []
        for i in lista:
            item = i.strip()
            if tipo=="categoria":
                item = item.lower().rstrip('s')
                if item not in CATEGORIAS_VALIDAS:
                    sugestao = difflib.get_close_matches(item, CATEGORIAS_VALIDAS, n=1)
                    if sugestao:
                        item = sugestao[0]
            elif tipo=="marca":
                item = item.lower()
                if item not in MARCAS_VALIDAS:
                    sugestao = difflib.get_close_matches(item, MARCAS_VALIDAS, n=1)
                    if sugestao:
                        item = sugestao[0]
            elif tipo=="estado":
                item = item.lower()
                if item not in ESTADOS_VALIDOS:
                    sugestao = difflib.get_close_matches(item, ESTADOS_VALIDOS, n=1)
                    if sugestao:
                        item = sugestao[0]
            normalizados.append(item)
        return normalizados

    def input_lista_valida(mensagem, tipo="item"):
        while True:
            texto = input(mensagem)
            itens = [x.strip() for x in texto.split(",")]
            itens_validos = []
            invalido = False

            for i in itens:
                original = i
                if tipo == "categoria":
                    i = i.lower().rstrip('s')
                    if i not in CATEGORIAS_VALIDAS:
                        invalido = True
                        sugestao = difflib.get_close_matches(i, CATEGORIAS_VALIDAS, n=1)
                        if sugestao:
                            print(f"⚠️ '{original}' não é válido. Talvez quiseste dizer '{sugestao[0]}'")
                        else:
                            print(f"⚠️ '{original}' não é válido.")
                        break
                    else:
                        itens_validos.append(i)
                elif tipo == "marca":
                    i = i.lower()
                    if i not in MARCAS_VALIDAS:
                        invalido = True
                        sugestao = difflib.get_close_matches(i, MARCAS_VALIDAS, n=1)
                        if sugestao:
                            print(f"⚠️ '{original}' não é válida. Talvez quiseste dizer '{sugestao[0]}'")
                        else:
                            print(f"⚠️ '{original}' não é válida. Contacta o suporte se o erro persistir.")
                        break
                    else:
                        itens_validos.append(i)
                elif tipo == "estado":
                    i=i.strip().lower()
                    estados_lower = [e.lower() for e in ESTADOS_VALIDOS]
                    if i in estados_lower:
                        idx = estados_lower.index(i)
                        itens_validos.append(ESTADOS_VALIDOS[idx])
                    else:
                        sugestao = difflib.get_close_matches(i, estados_lower, n=1)
                        if sugestao:
                            idx = estados_lower.index(sugestao[0])
                            print(f"⚠️ '{i}' não é válido. Talvez quiseste dizer '{ESTADOS_VALIDOS[idx]}'")
                        else:
                            print(f"⚠️ '{i}' não é válido. Tenta novamente.")
                        invalido = True
                        break
            if not invalido:
                return itens_validos
            print("Tenta novamente com valores válidos.\n")


    def input_categoria(mensagem):
        while True:
            cat = input(mensagem).strip().lower().rstrip('s')
            if cat in CATEGORIAS_VALIDAS:
                return cat
            sugestao = difflib.get_close_matches(cat, CATEGORIAS_VALIDAS, n=1)
            if sugestao:
                cat = sugestao[0]
                return cat
            print(f"⚠️ Categoria inválida. Tenta novamente.")

    def input_marca(mensagem):
        while True:
            marca = input(mensagem).strip().lower()
            if marca in MARCAS_VALIDAS:
                return marca
            sugestao = difflib.get_close_matches(marca, MARCAS_VALIDAS, n=1)
            if sugestao:
                marca = sugestao[0]
                return marca
            print(f"⚠️ Marca inválida. Contacta o suporte se o erro persistir.")

    def input_estado(mensagem):
        while True:
            est = input(mensagem).strip().lower()
            if est in ESTADOS_VALIDOS:
                return est
            sugestao = difflib.get_close_matches(est, ESTADOS_VALIDOS, n=1)
            if sugestao:
                est = sugestao[0]
                return est
            print(f"⚠️ Estado inválido. Tenta novamente.")

    # ==========================
    # FUNÇÕES DE CÁLCULO
    # ==========================
    def calcular_grupo(categoria, marca, estado, quantidade, preco_revenda):
        chave = f"{categoria} {marca}"
        if chave not in preco_revenda:
            return 0, f"Sem referência de mercado para {chave}"

        preco_base = preco_revenda[chave]
        fator = FATOR_ESTADO.get(estado, 0.8)
        preco_final = preco_base * fator
        valor_total = preco_final * quantidade

        justificacao = f"{quantidade}x {categoria.title()} {marca.title()} ({estado}) → {round(preco_final,2)}€ estimado por peça."
        return valor_total, justificacao

    def calcular_risco(detalhes_pecas, margem):
        risco = 5
        justificacoes_risco = []
        total_pecas = sum(g["quantidade"] for g in detalhes_pecas)

        # Volume
        if total_pecas > 40: risco += 2; justificacoes_risco.append("Volume muito elevado.")
        elif total_pecas > 20: risco += 1; justificacoes_risco.append("Volume elevado.")

        # Estado
        estados = [g["estado"] for g in detalhes_pecas]
        if "Usado" in estados: risco += 2; justificacoes_risco.append("Presença de peças usadas.")
        elif estados.count("Bom") > total_pecas * 0.5: risco += 1; justificacoes_risco.append("Muitas peças em estado 'Bom'.")

        # Marcas
        marcas = [g["marca"].lower() for g in detalhes_pecas]
        if any(m in MARCAS_PREMIUM for m in marcas): risco -= 1; justificacoes_risco.append("Inclui marcas premium (boa liquidez).")

        # Categorias
        categorias = [g["categoria"].lower() for g in detalhes_pecas]
        if len(set(categorias)) == 1 and "t-shirt" in categorias: risco += 1; justificacoes_risco.append("Bundle composto apenas por t-shirts.")
        elif any(c in ["casaco","hoodie"] for c in categorias): risco -= 1; justificacoes_risco.append("Inclui peças de ticket médio/alto.")

        # Margem
        if margem < 20: risco += 2; justificacoes_risco.append("Margem baixa.")
        elif margem < 30: risco += 1; justificacoes_risco.append("Margem moderada.")

        risco = max(1, min(10, risco))
        return risco, justificacoes_risco

    def gerar_resposta(valor_total, lucro, margem, risco, justificacoes, justificacoes_risco, decisao):
        resposta = "📊 Resultado da Análise do Bundle\n\n"
        resposta += f"💰 Valor estimado de revenda: {round(valor_total,2)}€\n"
        resposta += f"📈 Lucro estimado: {round(lucro,2)}€\n"
        resposta += f"📊 Margem: {round(margem,2)}%\n"
        resposta += f"⚠️  Nível de risco: {risco}/10\n\n"
        resposta += "🧠 Resumo da análise\n\n"
        for j in justificacoes: resposta += f"• {j}\n"
        if justificacoes_risco:
            resposta += "\nRisco ajustado devido a:\n"
            for r in justificacoes_risco: resposta += f"• {r}\n"
        resposta += f"\n🔥 Decisão: {decisao}\n"
        resposta += "⚠️  Valores baseados em médias históricas de mercado. Não garantem preço final de venda."
        return resposta

    def avaliar_bundle_exato(detalhes_pecas, preco_total_bundle, preco_revenda):
        valor_total_estimado = 0
        justificacoes = []
        for grupo in detalhes_pecas:
            valor, justificacao = calcular_grupo(
                grupo["categoria"],
                grupo["marca"],
                grupo["estado"],
                grupo["quantidade"],
                preco_revenda
            )
            valor_total_estimado += valor
            justificacoes.append(justificacao)

        lucro = valor_total_estimado - preco_total_bundle
        margem = (lucro / preco_total_bundle * 100) if preco_total_bundle>0 else 0
        risco, justificacoes_risco = calcular_risco(detalhes_pecas, margem)

        if margem > 40 and risco <=5: decisao = "🔥 COMPRAR"
        elif margem > 20: decisao = "⚠️  CAUTELA"
        else: decisao = "❌ EVITAR"

        return gerar_resposta(valor_total_estimado, lucro, margem, risco, justificacoes, justificacoes_risco, decisao)

    def avaliar_bundle_representativo(categorias, marcas, estados, numero_pecas, preco_total_bundle, preco_revenda):
        """
        Avalia um bundle representativo sem pedir inputs adicionais ao usuário.
        Distribui as peças de forma equilibrada entre todas as combinações possíveis.
        """
        detalhes_estimados = []

        # Normaliza inputs
        categorias_norm = [cat.rstrip('s').lower() for cat in categorias]
        marcas_norm = [m.lower() for m in marcas]
        estados_norm = [e.title() for e in estados]

        # Cria todas as combinações possíveis
        combinacoes = [(c, m, e) for c in categorias_norm for m in marcas_norm for e in estados_norm]

        total_combinacoes = len(combinacoes)
        if total_combinacoes == 0:
            raise ValueError("Não há combinações válidas de categorias, marcas e estados.")

        # Distribui peças entre combinações de forma equilibrada
        base = numero_pecas // total_combinacoes
        resto = numero_pecas % total_combinacoes

        for i, (cat, marca, est) in enumerate(combinacoes):
            qtd = base + (1 if i < resto else 0)
            detalhes_estimados.append({
                "categoria": cat,
                "marca": marca,
                "estado": est,
                "quantidade": qtd
            })

        # Avalia o bundle usando a função exata
        return avaliar_bundle_exato(detalhes_estimados, preco_total_bundle, preco_revenda)


    # ==========================
    # EXECUÇÃO PRINCIPAL
    # ==========================
    if __name__ == "__main__":

        print("\nO bundle é:")
        print("1️⃣  Representativo")
        print("2️⃣  Exato")
        tipo_bundle = input("Escolha: ").strip()

        if tipo_bundle == "1":  # Representativo
            categorias = input_lista_valida("Tipos de peça (separadas por vírgula): ", tipo="categoria")
            marcas = input_lista_valida("Marcas possíveis (separadas por vírgula): ", tipo="marca")
            estados = input_lista_valida("Estado(s) possíveis (separados por vírgula): ", tipo="estado")

            numero_pecas = int(input("Número total de peças: "))
            preco_total = float(input("Preço total do bundle: "))

            resultado = avaliar_bundle_representativo(
                categorias,
                marcas,
                estados,
                numero_pecas,
                preco_total,
                preco_revenda
            )
            print("\n")
            print(resultado)

        elif tipo_bundle == "2":  # Exato
            detalhes = []

            while True:
                categoria = input_categoria("Tipo de peça: ")
                marca = input_marca("Marca: ")
                estado = input_estado("Estado (Novo, Muito bom, Bom, Usado): ")
                quantidade = int(input("Quantidade: "))

                detalhes.append({
                    "categoria": categoria,
                    "marca": marca,
                    "estado": estado,
                    "quantidade": quantidade
                })

                continuar = input("Adicionar outro grupo? (s/n): ")
                if continuar.lower() != "s":
                    break

            preco_total = float(input("Preço total do bundle: "))

            resultado = avaliar_bundle_exato(detalhes, preco_total, preco_revenda)
            print("\n")
            print(resultado)

        else:
            print("Opção inválida.")

    # Aqui podes colar exatamente tua lógica completa do bundle
    # (mantém igual ao teu código original)

# =====================================================
# ==================== MAIN FLOW ======================
# =====================================================

if __name__ == "__main__":

    print("Queres avaliar:")
    print("")
    print("1️⃣  Peça individual")
    print("2️⃣  Bundle Fleek")

    escolha = input("Escolha: ").strip()

    if escolha == "1":
        avaliar_peca_individual()
    elif escolha == "2":
        avaliar_bundle()
    else:
        print("Opção inválida.")