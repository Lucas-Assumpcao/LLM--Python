import asyncio

async def chama_llm(pergunta: str) -> str:
    await asyncio.sleep(2)  # simula a espera da API
    return f"resposta para: {pergunta}"

async def main():
    resultados = await asyncio.gather(
        chama_llm("pergunta 1"),
        chama_llm("pergunta 2"),
        chama_llm("pergunta 3"),
    )
    print(resultados)

asyncio.run(main())