from dataclasses import dataclass

@dataclass
class Mensagem:
    remetente: str
    texto: str
    timestamp: str

msg = Mensagem(remetente="Lucas", texto="Oi", timestamp="2026-07-07")
print(msg)
print(msg.remetente)