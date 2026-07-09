import time

def chama_llm(pergunta: str) -> str:
    time.sleep(2)
    return f"resposta para: {pergunta}"

def main():
    resultados = [
        chama_llm("pergunta 1"),
        chama_llm("pergunta 2"),
        chama_llm("pergunta 3"),
    ]
    print(resultados)

inicio = time.time()
main()
print(f"Tempo: {time.time() - inicio:.3f}s")