PERGUNTAS = [{"id": "tipo","texto": "Que tipo de peça é?","tipo_input": "select","opcoes": ["T-shirt", "Sweatshirt", "Casaco", "Calças"]},{"id": "marca","texto": "Qual é a marca?","tipo_input": "text"},{"id": "estado","texto": "Qual é o estado da peça?","tipo_input": "select","opcoes": ["Novo", "Muito bom", "Bom", "Usado"]},{"id": "preco_compra","texto": "Preço de compra (€)?","tipo_input": "number"}]

def proxima_pergunta(respostas):
    indice = len(respostas)

    if indice < len(PERGUNTAS):
        return PERGUNTAS[indice]
    else:
        return None
