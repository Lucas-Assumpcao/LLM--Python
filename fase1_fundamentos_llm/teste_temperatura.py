import numpy as np

def aplica_temperatura(probabilidades: list[float], temperatura: float) -> list[float]:
    logits = np.log(probabilidades)
    logits_ajustados = logits / temperatura
    exp_logits = np.exp(logits_ajustados)
    return exp_logits / np.sum(exp_logits)

tokens = ["azul", "lindo", "cinza", "grande"]
probs_originais = [0.45, 0.20, 0.15, 0.03]

for temp in [0.1, 1.0, 2.0]:
    novas_probs = aplica_temperatura(probs_originais, temp)
    print(f"\nTemperatura {temp}:")
    for tok, p in zip(tokens, novas_probs):
        print(f"  {tok}: {p:.1%}")