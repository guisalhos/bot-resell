import difflib

# =====================================================
# BASE DE DADOS (UNIFICADA) - IGUAL AO TEU CÓDIGO
# =====================================================

preco_revenda = {
    "hoodie carhartt":40 , "hoodie nike":30 , "hoodie dickies":25,
    "t-shirt carhartt":25, "t-shirt nike":15 , "t-shirt dickies":15,
    "casaco carhartt":60, "casaco nike":35, "casaco dickies":30,
    "hoodie adidas":20, "casaco adidas":30, "t-shirt adidas":12,
    "hoodie the north face":30, "casaco the north face":55, "t-shirt the north face":17,
    "hoodie ralph lauren":35, "casaco ralph lauren":60, "t-shirt ralph lauren":20,
    "hoodie stussy":40, "casaco stussy":75, "t-shirt stussy":30, "hoodie supreme":45, "t-shirt supreme":30, "casaco supreme":80,
    "hoodie palace":40, "t-shirt palace":28, "casaco palace":70,
    "hoodie stone island":45, "t-shirt stone island":30, "casaco stone island":85,
    "hoodie patagonia":35, "t-shirt patagonia":22, "casaco patagonia":65,
    "hoodie arc'teryx":40, "t-shirt arc'teryx":25, "casaco arc'teryx":90,
    "hoodie bape":45, "t-shirt bape":30, "casaco bape":75,
    "hoodie kith":40, "t-shirt kith":28, "casaco kith":70,
    "hoodie aime leon dore":42, "t-shirt aime leon dore":28, "casaco aime leon dore":75,
    "hoodie cp company":40, "t-shirt cp company":25, "casaco cp company":75,
    "hoodie human made":42, "t-shirt human made":28, "casaco human made":70,
    "hoodie noah":38, "t-shirt noah":25, "casaco noah":65,
    "hoodie neighborhood":40, "t-shirt neighborhood":27, "casaco neighborhood":70,
    "hoodie wtaps":40, "t-shirt wtaps":27, "casaco wtaps":72,
    "hoodie billionaire boys club":38, "t-shirt billionaire boys club":25, "casaco billionaire boys club":65,
    "hoodie corteiz":40, "t-shirt corteiz":28, "casaco corteiz":70, "hoodie puma":22, "t-shirt puma":13, "casaco puma":32,
    "hoodie champion":24, "t-shirt champion":15, "casaco champion":35,
    "hoodie reebok":22, "t-shirt reebok":13, "casaco reebok":32,
    "hoodie vans":22, "t-shirt vans":13, "casaco vans":32,
    "hoodie ellesse":22, "t-shirt ellesse":13, "casaco ellesse":32,
    "hoodie starter":22, "t-shirt starter":13, "casaco starter":32,
    "hoodie kappa":22, "t-shirt kappa":13, "casaco kappa":32,
    "hoodie russell athletic":22, "t-shirt russell athletic":13, "casaco russell athletic":32,
    "hoodie converse":22, "t-shirt converse":13, "casaco converse":32,
    "hoodie lee":24, "t-shirt lee":14, "casaco lee":35,
    "hoodie quiksilver":22, "t-shirt quiksilver":13, "casaco quiksilver":32,
    "hoodie volcom":22, "t-shirt volcom":13, "casaco volcom":32,
    "hoodie dc shoes":22, "t-shirt dc shoes":13, "casaco dc shoes":32,
    "hoodie element":22, "t-shirt element":13, "casaco element":32,
    "hoodie superdry":24, "t-shirt superdry":14, "casaco superdry":35,
    "hoodie puma":22, "t-shirt puma":13, "casaco puma":32,
    "hoodie champion":24, "t-shirt champion":15, "casaco champion":35,
    "hoodie reebok":22, "t-shirt reebok":13, "casaco reebok":32,
    "hoodie vans":22, "t-shirt vans":13, "casaco vans":32,
    "hoodie ellesse":22, "t-shirt ellesse":13, "casaco ellesse":32,
    "hoodie starter":22, "t-shirt starter":13, "casaco starter":32,
    "hoodie kappa":22, "t-shirt kappa":13, "casaco kappa":32,
    "hoodie russell athletic":22, "t-shirt russell athletic":13, "casaco russell athletic":32,
    "hoodie converse":22, "t-shirt converse":13, "casaco converse":32,
    "hoodie lee":24, "t-shirt lee":14, "casaco lee":35,
    "hoodie quiksilver":22, "t-shirt quiksilver":13, "casaco quiksilver":32,
    "hoodie volcom":22, "t-shirt volcom":13, "casaco volcom":32,
    "hoodie dc shoes":22, "t-shirt dc shoes":13, "casaco dc shoes":32,
    "hoodie element":22, "t-shirt element":13, "casaco element":32,
    "hoodie superdry":24, "t-shirt superdry":14, "casaco superdry":35,
    "hoodie zara":17, "t-shirt zara":7, "casaco zara": 22
}

FATOR_ESTADO = {"Novo": 1.0, "Muito bom": 0.85, "Bom": 0.75,"Usado": 0.6}
MARCAS_PREMIUM = ["carhartt", "stussy", "the north face", "ralph lauren", "supreme",
    "palace","stone island","patagonia","arc'teryx","bape","kith","aime leon dore","cp company",
    "human made","noah","neighborhood","wtaps","billionaire boys club","hoodie corteiz"]
CATEGORIAS_VALIDAS = ["hoodie", "t-shirt", "casaco"]
ESTADOS_VALIDOS = ["Novo", "Muito bom", "Bom", "Usado"]
MARCAS_VALIDAS = list(set([ch.split(" ", 1)[1] for ch in preco_revenda.keys()]))


# =====================================================
# HELPERS (mesma ideia de sugestão que tu tinhas)
# =====================================================

def _sugestao(valor, lista):
    sug = difflib.get_close_matches(valor, lista, n=1)
    return sug[0] if sug else None

def _parse_float(txt):
    return float(txt.strip().replace(",", "."))

def _parse_int(txt):
    return int(txt.strip())

def _split_csv(txt):
    return [x.strip() for x in txt.split(",") if x.strip()]

def _validar_lista(txt, tipo):
    """
    Replica o teu input_lista_valida:
    - devolve (lista_validada, erro_msg ou None)
    - Se erro: devolve exatamente as mensagens ⚠️ + sugestão + "Tenta novamente..."
    """
    itens = _split_csv(txt)
    if not itens:
        return None, "⚠️ Entrada vazia.\nTenta novamente com valores válidos.\n"

    itens_validos = []
    for i in itens:
        original = i

        if tipo == "categoria":
            v = i.lower().rstrip("s")
            if v not in CATEGORIAS_VALIDAS:
                sug = _sugestao(v, CATEGORIAS_VALIDAS)
                if sug:
                    return None, f"⚠️ '{original}' não é válido. Talvez quiseste dizer '{sug}'\nTenta novamente com valores válidos.\n"
                return None, f"⚠️ '{original}' não é válido.\nTenta novamente com valores válidos.\n"
            itens_validos.append(v)

        elif tipo == "marca":
            v = i.lower()
            if v not in MARCAS_VALIDAS:
                sug = _sugestao(v, MARCAS_VALIDAS)
                if sug:
                    return None, f"⚠️ '{original}' não é válida. Talvez quiseste dizer '{sug}'\nTenta novamente com valores válidos.\n"
                return None, f"⚠️ '{original}' não é válida.\nTenta novamente com valores válidos.\n"
            itens_validos.append(v)

        elif tipo == "estado":
            v = i.lower()
            estados_lower = [e.lower() for e in ESTADOS_VALIDOS]
            if v in estados_lower:
                idx = estados_lower.index(v)
                itens_validos.append(ESTADOS_VALIDOS[idx])
            else:
                sug = _sugestao(v, estados_lower)
                if sug:
                    idx = estados_lower.index(sug)
                    return None, f"⚠️ '{original}' não é válido. Talvez quiseste dizer '{ESTADOS_VALIDOS[idx]}'\nTenta novamente com valores válidos.\n"
                return None, f"⚠️ '{original}' não é válido.\nTenta novamente com valores válidos.\n"

    return itens_validos, None

# =====================================================
# PEÇA INDIVIDUAL (cálculo igual ao teu)
# =====================================================

def _avaliar_peca_individual_core(tipo, marca, tamanho, estado, preco_total):
    lucro_minimo_por_tipo = {"t-shirt": 7, "hoodie": 10, "casaco": 15, "calças": 10}
    topmarcas = ["carhartt", "stussy", "the north face", "ralph lauren", "supreme",
    "palace","stone island","patagonia","arc'teryx","bape","kith","aime leon dore","cp company",
    "human made","noah","neighborhood","wtaps","billionaire boys club","hoodie corteiz"]
    boasmarcas = ["nike", "ralph lauren", "the north face"]

    chave = f"{tipo} {marca}"
    preco_base = preco_revenda.get(chave, 0)

    if preco_base == 0:
        return "⚠️ Artigo não pertence à base de dados."

    # Ajuste de revenda por estado (igual ao teu)
    if estado == "usado":
        preco_base *= 0.65
    elif estado == "bom":
        preco_base *= 0.80

    lucro_minimo = lucro_minimo_por_tipo.get(tipo, 10)
    lucro = preco_base - preco_total
    margem = (lucro / preco_total * 100) if preco_total > 0 else 0

    # =========================
    # SCORE (EXATAMENTE como enviaste)
    # =========================
    score = 0

    # 1) Regra principal: lucro >= lucro mínimo
    if lucro >= lucro_minimo:
        score += 3

    # 2) Regra secundária: percentagem <= 50% (paguei no máximo metade do valor revenda)
    #    percentagem = preco_total / preco_base
    if preco_base > 0 and (preco_total / preco_base) <= 0.50:
        score += 2

    # 3) Estado da peça: Novo +1 | Bom 0 | Usado -1
    if estado == "novo":
        score += 1
    elif estado == "bom":
        score += 0
    elif estado == "usado":
        score -= 1

    # 4) Marca / Liquidez: Top +2 | Boa +1 | Comum 0
    if marca in topmarcas:
        score += 2
    elif marca in boasmarcas:
        score += 1
    else:
        score += 0

    # 5) Tamanho: M/L 0 | S/XL -1 | XS/XXL -3
    if tamanho in ["m", "l"]:
        score += 0
    elif tamanho in ["s", "xl"]:
        score -= 1
    elif tamanho in ["xs", "xxl"]:
        score -= 3

    # 6) Época / Tendência: +1
    score += 1

    # =========================
    # RISCO 1–10 (mapeado do score)
    # Range típico do score: min=-3, max=9  (pelas tuas regras)
    # score alto = risco baixo
    # =========================
    min_score = -3
    max_score = 9
    span = max_score - min_score  # 12

    # Normaliza 0..1
    norm = (score - min_score) / span if span > 0 else 0.5

    # Converte para risco 10..1
    risco_num = int(round(10 - norm * 9))
    risco_num = max(1, min(10, risco_num))

    if risco_num <= 3:
        risco_txt = "Baixo"
    elif risco_num <= 6:
        risco_txt = "Médio"
    else:
        risco_txt = "Alto"

    # =========================
    # DECISÃO (como tu disseste)
    # - Se score < 0 e lucro > 2x lucro mínimo → SIM (COM CAUTELA)
    # - Se score < 0 e só → NÃO
    # - Caso contrário: se lucro >= mínimo → SIM ; senão NÃO
    # =========================
    if score < 0 and lucro > 2 * lucro_minimo:
        decisao_final = "⚠️  CAUTELA"
    elif score < 0:
        decisao_final = "❌ EVITAR"
    else:
        if lucro >= lucro_minimo:
            decisao_final = "🔥 COMPRAR"
        else:
            decisao_final = "❌ EVITAR"

    # =========================
    # JUSTIFICAÇÕES (estilo bundle, mas baseadas na tua lógica)
    # =========================
    pontos_positivos = []
    pontos_negativos = []

    # Lucro
    if lucro >= lucro_minimo:
        pontos_positivos.append("✔ Lucro acima do mínimo definido")
    else:
        pontos_negativos.append("🚫 Lucro abaixo do mínimo definido")

    # Percentagem <= 50%
    if preco_base > 0 and (preco_total / preco_base) <= 0.50:
        pontos_positivos.append("✔ Pagaste ≤ 50% do valor de revenda estimado")
    else:
        pontos_negativos.append("⚠️ Pagaste > 50% do valor de revenda estimado (margem apertada)")

    # Marca
    if marca in topmarcas:
        pontos_positivos.append("✔ Marca Top (boa liquidez)")
    elif marca in boasmarcas:
        pontos_positivos.append("✔ Boa marca (rotação aceitável)")
    else:
        pontos_negativos.append("⚠️ Marca comum (pode demorar mais a vender)")

    # Tamanho
    if tamanho in ["m", "l"]:
        pontos_positivos.append("✔ Tamanho M/L (melhor rotação)")
    elif tamanho in ["s", "xl"]:
        pontos_negativos.append("⚠️ Tamanho S/XL (um pouco mais difícil)")
    elif tamanho in ["xs", "xxl"]:
        pontos_negativos.append("⚠️ Tamanho XS/XXL (aumenta bastante o risco)")

    # Estado
    if estado == "novo":
        pontos_positivos.append("✔ Estado Novo (não penaliza a revenda)")
    elif estado == "bom":
        pontos_negativos.append("⚠️ Estado Bom (penaliza ligeiramente a revenda)")
    elif estado == "usado":
        pontos_negativos.append("⚠️ Estado Usado (penaliza bastante a revenda)")

    # Época
    pontos_positivos.append("✔ Época/Tendência a favor (+1)")

    # =========================
    # OUTPUT estilo bundle
    # =========================
    resposta = "📊 Resultado da Análise da Peça Individual\n\n"
    resposta += f"💰 Valor estimado de revenda: {round(preco_base,2)}€\n"
    resposta += f"📈 Lucro estimado: {round(lucro,2)}€\n"
    resposta += f"📊 Margem: {round(margem,2)}%\n"
    resposta += f"⚠️  Nível de risco: {risco_num}/10 ({risco_txt})\n\n"

    resposta += "🧠 Resumo da análise\n\n"
    for p in pontos_positivos:
        resposta += f"• {p}\n"

    if pontos_negativos:
        resposta += "\nPontos de risco:\n"
        for p in pontos_negativos:
            resposta += f"• {p}\n"

    resposta += f"\n🔥 Decisão: {decisao_final}\n"
    resposta += "⚠️  Valores baseados em médias históricas de mercado. Não garantem preço final de venda."
    return resposta

# =====================================================
# BUNDLE (cálculo igual ao teu)
# =====================================================

def _calcular_grupo(categoria, marca, estado, quantidade, preco_db):
    chave = f"{categoria} {marca}"
    if chave not in preco_db:
        return 0, f"Sem referência de mercado para {chave}"

    preco_base = preco_db[chave]
    fator = FATOR_ESTADO.get(estado, 0.8)
    preco_final = preco_base * fator
    valor_total = preco_final * quantidade

    justificacao = f"{quantidade}x {categoria.title()} {marca.title()} ({estado}) → {round(preco_final,2)}€ estimado por peça."
    return valor_total, justificacao

def _calcular_risco(detalhes_pecas, margem):
    risco = 5
    justificacoes_risco = []
    total_pecas = sum(g["quantidade"] for g in detalhes_pecas)

    if total_pecas > 40: risco += 2; justificacoes_risco.append("Volume muito elevado.")
    elif total_pecas > 20: risco += 1; justificacoes_risco.append("Volume elevado.")

    estados = [g["estado"] for g in detalhes_pecas]
    if "Usado" in estados: risco += 2; justificacoes_risco.append("Presença de peças usadas.")
    elif estados.count("Bom") > total_pecas * 0.5: risco += 1; justificacoes_risco.append("Muitas peças em estado 'Bom'.")

    marcas = [g["marca"].lower() for g in detalhes_pecas]
    if any(m in MARCAS_PREMIUM for m in marcas): risco -= 1; justificacoes_risco.append("Inclui marcas premium (boa liquidez).")

    categorias = [g["categoria"].lower() for g in detalhes_pecas]
    if len(set(categorias)) == 1 and "t-shirt" in categorias: risco += 1; justificacoes_risco.append("Bundle composto apenas por t-shirts.")
    elif any(c in ["casaco","hoodie"] for c in categorias): risco -= 1; justificacoes_risco.append("Inclui peças de ticket médio/alto.")

    if margem < 20: risco += 2; justificacoes_risco.append("Margem baixa.")
    elif margem < 30: risco += 1; justificacoes_risco.append("Margem moderada.")

    risco = max(1, min(10, risco))
    return risco, justificacoes_risco

def _gerar_resposta(valor_total, lucro, margem, risco, justificacoes, justificacoes_risco, decisao):
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

def _avaliar_bundle_exato(detalhes_pecas, preco_total_bundle, preco_db):
    valor_total_estimado = 0
    justificacoes = []
    for grupo in detalhes_pecas:
        valor, justificacao = _calcular_grupo(
            grupo["categoria"], grupo["marca"], grupo["estado"], grupo["quantidade"], preco_db
        )
        valor_total_estimado += valor
        justificacoes.append(justificacao)

    lucro = valor_total_estimado - preco_total_bundle
    margem = (lucro / preco_total_bundle * 100) if preco_total_bundle>0 else 0
    risco, justificacoes_risco = _calcular_risco(detalhes_pecas, margem)

    if margem > 40 and risco <=5: decisao = "🔥 COMPRAR"
    elif margem > 20: decisao = "⚠️  CAUTELA"
    else: decisao = "❌ EVITAR"

    return _gerar_resposta(valor_total_estimado, lucro, margem, risco, justificacoes, justificacoes_risco, decisao)

def _avaliar_bundle_representativo(categorias, marcas, estados, numero_pecas, preco_total_bundle, preco_db):
    detalhes_estimados = []
    categorias_norm = [cat.rstrip('s').lower() for cat in categorias]
    marcas_norm = [m.lower() for m in marcas]
    estados_norm = [e.title() for e in estados]

    combinacoes = [(c, m, e) for c in categorias_norm for m in marcas_norm for e in estados_norm]
    total_combinacoes = len(combinacoes)
    if total_combinacoes == 0:
        raise ValueError("Não há combinações válidas de categorias, marcas e estados.")

    base = numero_pecas // total_combinacoes
    resto = numero_pecas % total_combinacoes

    for i, (cat, marca, est) in enumerate(combinacoes):
        qtd = base + (1 if i < resto else 0)
        detalhes_estimados.append({"categoria": cat, "marca": marca, "estado": est, "quantidade": qtd})

    return _avaliar_bundle_exato(detalhes_estimados, preco_total_bundle, preco_db)

# =====================================================
# MOTOR DE CONVERSA (para o site)
# =====================================================

def bot_inicio():
    return {
        "etapa": "menu",
        "dados": {}
    }

def bot_prompt(estado):
    e = estado["etapa"]
    d = estado["dados"]

    if e == "menu":
        return "Queres avaliar:\n1️⃣  Peça individual\n2️⃣  Bundle Fleek\n\nEscolha:"

    if e == "peca_tipo":
        return "\n📦 Avaliação de Peça Individual\n\nTipo de peça:"

    if e == "peca_marca":
        return "Marca:"

    if e == "peca_tamanho":
        return "Tamanho (XS,S,M,L,XL,XXL):"

    if e == "peca_estado":
        return "Estado (novo, bom, usado):"

    if e == "peca_preco":
        return "Preço total pago:"

    if e == "bundle_tipo":
        return "\nO bundle é:\n1️⃣  Representativo\n2️⃣  Exato\nEscolha:"

    if e == "bundle_rep_categorias":
        return "Tipos de peça (separadas por vírgula):"

    if e == "bundle_rep_marcas":
        return "Marcas possíveis (separadas por vírgula):"

    if e == "bundle_rep_estados":
        return "Estado(s) possíveis (separados por vírgula):"

    if e == "bundle_rep_numero":
        return "Número total de peças:"

    if e == "bundle_rep_preco":
        return "Preço total do bundle:"

    if e == "bundle_exato_categoria":
        return "Tipo de peça:"

    if e == "bundle_exato_marca":
        return "Marca:"

    if e == "bundle_exato_estado":
        return "Estado (Novo, Muito bom, Bom, Usado):"

    if e == "bundle_exato_quantidade":
        return "Quantidade:"

    if e == "bundle_exato_continuar":
        return "Adicionar outro grupo? (s/n):"

    if e == "bundle_exato_preco":
        return "Preço total do bundle:"

    return "..."

def bot_processar(estado, mensagem):
    """
    Recebe estado+mensagem do utilizador e devolve:
    (resposta_texto, novo_estado)
    Mantém avisos e permite repetir até válido.
    """
    msg = (mensagem or "").strip()
    e = estado["etapa"]
    d = estado["dados"]

    # MENU
    if e == "menu":
        if msg == "1":
            estado["etapa"] = "peca_tipo"
            return bot_prompt(estado), estado
        elif msg == "2":
            estado["etapa"] = "bundle_tipo"
            return bot_prompt(estado), estado
        else:
            # aviso igual à ideia do teu "Opção inválida."
            return "Opção inválida.\n\n" + bot_prompt(estado), estado

    # =======================
    # PEÇA INDIVIDUAL
    # =======================
    if e == "peca_tipo":
        TIPOS_VALIDOS = ["t-shirt", "hoodie", "casaco", "calças"]
        tipo = msg.lower()
        if tipo not in TIPOS_VALIDOS:
            return "⚠️ Tipo inválido.\n\n" + bot_prompt(estado), estado
        d["tipo"] = tipo
        estado["etapa"] = "peca_marca"
        return bot_prompt(estado), estado

    if e == "peca_marca":
        d["marca"] = msg.lower()
        estado["etapa"] = "peca_tamanho"
        return bot_prompt(estado), estado

    if e == "peca_tamanho":
        TAMANHOS_VALIDOS = ["xs", "s", "m", "l", "xl", "xxl"]
        t = msg.lower()
        if t not in TAMANHOS_VALIDOS:
            return "⚠️ Tamanho inválido.\n\n" + bot_prompt(estado), estado
        d["tamanho"] = t
        estado["etapa"] = "peca_estado"
        return bot_prompt(estado), estado

    if e == "peca_estado":
        ESTADOS_VALIDOS_INDIV = ["novo", "bom", "usado"]
        est = msg.lower()
        if est not in ESTADOS_VALIDOS_INDIV:
            return "⚠️ Estado inválido.\n\n" + bot_prompt(estado), estado
        d["estado"] = est
        estado["etapa"] = "peca_preco"
        return bot_prompt(estado), estado

    if e == "peca_preco":
        try:
            preco_total = _parse_float(msg)
        except:
            return "Preço inválido.\n\n" + bot_prompt(estado), estado

        resultado = _avaliar_peca_individual_core(
            d["tipo"], d["marca"], d["tamanho"], d["estado"], preco_total
        )
        # no teu código, depois imprime e termina. Aqui volta ao menu.
        estado["etapa"] = "menu"
        estado["dados"] = {}
        return resultado + "\n\n" + bot_prompt(estado), estado

    # =======================
    # BUNDLE
    # =======================
    if e == "bundle_tipo":
        if msg == "1":
            d.clear()
            estado["etapa"] = "bundle_rep_categorias"
            return bot_prompt(estado), estado
        elif msg == "2":
            d.clear()
            d["detalhes"] = []
            estado["etapa"] = "bundle_exato_categoria"
            return bot_prompt(estado), estado
        else:
            return "Opção inválida.\n\n" + bot_prompt(estado), estado

    # Representativo
    if e == "bundle_rep_categorias":
        categorias, err = _validar_lista(msg, "categoria")
        if err:
            return err + bot_prompt(estado), estado
        d["categorias"] = categorias
        estado["etapa"] = "bundle_rep_marcas"
        return bot_prompt(estado), estado

    if e == "bundle_rep_marcas":
        marcas, err = _validar_lista(msg, "marca")
        if err:
            return err + bot_prompt(estado), estado
        d["marcas"] = marcas
        estado["etapa"] = "bundle_rep_estados"
        return bot_prompt(estado), estado

    if e == "bundle_rep_estados":
        estados, err = _validar_lista(msg, "estado")
        if err:
            return err + bot_prompt(estado), estado
        d["estados"] = estados
        estado["etapa"] = "bundle_rep_numero"
        return bot_prompt(estado), estado

    if e == "bundle_rep_numero":
        try:
            d["numero_pecas"] = _parse_int(msg)
        except:
            return "⚠️ Número inválido.\n\n" + bot_prompt(estado), estado
        estado["etapa"] = "bundle_rep_preco"
        return bot_prompt(estado), estado

    if e == "bundle_rep_preco":
        try:
            preco_total = _parse_float(msg)
        except:
            return "⚠️ Preço inválido.\n\n" + bot_prompt(estado), estado

        resultado = _avaliar_bundle_representativo(
            d["categorias"], d["marcas"], d["estados"], d["numero_pecas"], preco_total, preco_revenda
        )
        estado["etapa"] = "menu"
        estado["dados"] = {}
        return "\n" + resultado + "\n\n" + bot_prompt(estado), estado

    # Exato (grupos)
    if e == "bundle_exato_categoria":
        cat = msg.strip().lower().rstrip("s")
        if cat not in CATEGORIAS_VALIDAS:
            sug = _sugestao(cat, CATEGORIAS_VALIDAS)
            if sug:
                return f"⚠️ Categoria inválida. Talvez quiseste dizer '{sug}'.\n\n" + bot_prompt(estado), estado
            return "⚠️ Categoria inválida.\n\n" + bot_prompt(estado), estado
        d["tmp_cat"] = cat
        estado["etapa"] = "bundle_exato_marca"
        return bot_prompt(estado), estado

    if e == "bundle_exato_marca":
        marca = msg.strip().lower()
        if marca not in MARCAS_VALIDAS:
            sug = _sugestao(marca, MARCAS_VALIDAS)
            if sug:
                return f"⚠️ Marca inválida. Talvez quiseste dizer '{sug}'.\n\n" + bot_prompt(estado), estado
            return "⚠️ Marca inválida.\n\n" + bot_prompt(estado), estado
        d["tmp_marca"] = marca
        estado["etapa"] = "bundle_exato_estado"
        return bot_prompt(estado), estado

    if e == "bundle_exato_estado":
        est = msg.strip().lower()
        estados_lower = [x.lower() for x in ESTADOS_VALIDOS]
        if est not in estados_lower:
            sug = _sugestao(est, estados_lower)
            if sug:
                idx = estados_lower.index(sug)
                return f"⚠️ Estado inválido. Talvez quiseste dizer '{ESTADOS_VALIDOS[idx]}'.\n\n" + bot_prompt(estado), estado
            return "⚠️ Estado inválido.\n\n" + bot_prompt(estado), estado

        d["tmp_estado"] = ESTADOS_VALIDOS[estados_lower.index(est)]
        estado["etapa"] = "bundle_exato_quantidade"
        return bot_prompt(estado), estado

    if e == "bundle_exato_quantidade":
        try:
            qtd = _parse_int(msg)
        except:
            return "⚠️ Quantidade inválida.\n\n" + bot_prompt(estado), estado

        d["detalhes"].append({
            "categoria": d["tmp_cat"],
            "marca": d["tmp_marca"],
            "estado": d["tmp_estado"],
            "quantidade": qtd
        })
        estado["etapa"] = "bundle_exato_continuar"
        return bot_prompt(estado), estado

    if e == "bundle_exato_continuar":
        if msg.lower() == "s":
            estado["etapa"] = "bundle_exato_categoria"
            return bot_prompt(estado), estado
        elif msg.lower() == "n":
            estado["etapa"] = "bundle_exato_preco"
            return bot_prompt(estado), estado
        else:
            return "⚠️ Opção inválida.\n\n" + bot_prompt(estado), estado

    if e == "bundle_exato_preco":
        try:
            preco_total = _parse_float(msg)
        except:
            return "⚠️ Preço inválido.\n\n" + bot_prompt(estado), estado

        resultado = _avaliar_bundle_exato(d["detalhes"], preco_total, preco_revenda)
        estado["etapa"] = "menu"
        estado["dados"] = {}
        return "\n" + resultado + "\n\n" + bot_prompt(estado), estado

    # fallback
    return "Opção inválida.\n\n" + bot_prompt(estado), estado