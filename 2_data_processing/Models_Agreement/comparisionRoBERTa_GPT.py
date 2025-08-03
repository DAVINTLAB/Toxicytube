import json

def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def comparar_sentimentos(arquivo1, arquivo2, saida="sentiments_comparision_<VIDEO_ID>.json"):
    dados1 = carregar_json(arquivo1)
    dados2 = carregar_json(arquivo2)

    # Índice por ID para busca rápida
    mapa_arquivo2 = {item["id"]: item for item in dados2}

    concordantes = []

    for item1 in dados1:
        id_ = item1["id"]
        if id_ in mapa_arquivo2:
            item2 = mapa_arquivo2[id_]
            if item1["sentimento"] == item2["sentimento"]:
                concordantes.append(item1)

    # Salvar resultado
    with open(saida, 'w', encoding='utf-8') as f:
        json.dump(concordantes, f, ensure_ascii=False, indent=2)

    print(f"✅ Total comments with agreeing sentiment: {len(concordantes)}")
    print(f"📁 Generated file: {saida}")

# Execução via terminal
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python comparisionRoBRETa_GPT.py arquivo1.json arquivo2.json")
    else:
        comparar_sentimentos(sys.argv[1], sys.argv[2])
