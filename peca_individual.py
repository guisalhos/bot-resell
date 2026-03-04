import streamlit as st

from avaliação_flow import proxima_pergunta

preço_revenda = {"hoodie carhartt":40 , "hoodie nike":30 , "hoodie dickies":25,"t-shirt carhartt": 25, "t-shirt nike":15 , "t-shirt dickies":15,"casaco carhartt": 60, "casaco nike": 35, "casaco dickies":30,"hoodie adidas":20, "casaco adidas":30, "t-shirt adidas":12,"hoodie the north face":30, "casaco the north face":55, "t-shirt the north face": 17,"hoodie ralph lauren":35, "casaco ralph lauren": 60, "t-shirt ralp lauren":20,"hoodie stussy":40, "casaco stussy":75, "t-shirt stussy":30}

lucro_minimo_por_tipo = {"t-shirt": 7,"hoodie": 10,"casaco": 15,"calças": 10}

TIPOS_VALIDOS = ["T-shirt", "Hoodie", "Casaco", "Calças"]
ESTADOS_VALIDOS = ["Novo", "Bom", "Usado"]
TAMANHOS_VALIDOS = ["XS", "S", "M", "L", "XL", "XXL"]

topmarcas=["nike","carhartt","stussy","ralph lauren","the north face"]
boasmarcas=["dickies","adidas"]

epoca = 1

st.title("Bot Resell - Avaliação de Artigos")
st.write("Responde às seguintes perguntas sobre o artigo para o bot calcular lucro, risco e recomendação de preço de revenda")


tipo_peça = st.selectbox("Qual é o tipo de peça?", TIPOS_VALIDOS)
marca = st.text_input("Qual é a marca?").lower().strip()
tamanho = st.selectbox("Qual é o tamanho da peça?", TAMANHOS_VALIDOS)
estado = st.selectbox("Qual é o estado da peça?", ESTADOS_VALIDOS)
preço_total = st.number_input("Quanto foi o preço total? (artigo + taxas + portes)", min_value=0.00, step=0.5)

if "respostas" not in st.session_state:
    st.session_state.respostas = {}

pergunta = proxima_pergunta(st.session_state.respostas)

if pergunta:
    st.subheader(pergunta["texto"])

    if pergunta["tipo_input"] == "select":
        resposta = st.selectbox(
            "Escolhe:",
            pergunta["opcoes"]
        )

    elif pergunta["tipo_input"] == "text":
        resposta = st.text_input("Resposta:")

    elif pergunta["tipo_input"] == "number":
        resposta = st.number_input("Valor:", min_value=0.0)

    if st.button("Continuar"):
        st.session_state.respostas[pergunta["id"]] = resposta
        st.experimental_rerun()

st.success("Avaliação concluída!")
st.write(st.session_state.respostas)


if st.button("Calcular"):
    tipo_peça = tipo_peça.lower().strip()
    marca = marca.lower().strip()
    tamanho = tamanho.lower().strip()
    estado = estado.lower().strip()

    chave = f"{tipo_peça} {marca}"
    preco_revenda = preço_revenda.get(chave, 0)

    if preco_revenda == 0:
        st.warning("⚠️ Artigo não pertence à base de dados. Confirma os nomes. Caso o erro persista, por favor contacta o suporte.")
    else:
        if estado=="usado":
            preco_revenda *= 0.70
        elif estado=="bom":
            preco_revenda *= 0.85

        lucro_minimo = lucro_minimo_por_tipo.get(tipo_peça, 10)
        lucro = preco_revenda - preço_total

        score = 0
        if tamanho in ["s","xl"]:
            score -= 1
        elif tamanho in ["xs","xxl"]:
            score -= 3
        if lucro >= lucro_minimo:
            score += 3
        if preço_total*2 <= preco_revenda:
            score += 2
        if estado=="novo":
            score += 1
        elif estado=="usado":
            score -=1
        if marca in topmarcas:
            score +=2
        elif marca in boasmarcas:
            score +=1
        if epoca==1:
            score +=1

        if score>=8:
            risco="Baixo"
        elif 5<=score<8:
            risco="Médio"
        else:
            risco="Alto"

        if score>0 and lucro>=lucro_minimo:
            decisao="Sim"
        elif score<0 and lucro>2*lucro_minimo:
            decisao="Sim (com cautela)"
        else:
            decisao="Não"

        pontos_positivos=[]
        pontos_negativos=[]
        if decisao=="Sim":
            pontos_positivos.append("✔ Lucro acima do mínimo definido")
        else:
            pontos_negativos.append("🚫 Margem baixa, não vale a pena")
        if lucro - 4 < lucro_minimo:
            pontos_negativos.append("⚠️ Margem perto do mínimo")
        if marca in topmarcas:
            pontos_positivos.append("✔ Marca com boa liquidez")
        if marca not in topmarcas and marca not in boasmarcas:
            pontos_negativos.append("⚠️ Marca com rotação lenta")
        if tamanho in ["m","l"]:
            pontos_positivos.append("✔ Bom tamanho")
        if tamanho in ["xs","xxl"]:
            pontos_negativos.append("⚠️ Tamanho aumenta bastante o risco")
        if estado=="novo":
            pontos_positivos.append("✔ Estado da peça não penaliza o preço de revenda")
        else:
            pontos_negativos.append("⚠️ Estado penaliza o preço de revenda")

        st.subheader("Decisão")
        st.write(f"**Preço sugerido de revenda:** {preco_revenda:.2f}€")
        st.write(f"**Lucro estimado:** {lucro:.2f}€")
        st.write(f"**Risco:** {risco}")
        st.write(f"**Comprar:** {decisao}")

        if pontos_positivos:
            st.write("**Pontos a favor:**")
            for p in pontos_positivos:
                st.write(p)
        if pontos_negativos:
            st.write("**Pontos de risco:**")
            for p in pontos_negativos:
                st.write(p)
