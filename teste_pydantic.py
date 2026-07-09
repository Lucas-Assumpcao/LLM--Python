from pydantic import BaseModel

class Mensagem(BaseModel):
    remetente: str
    texto: str
    timestamp: str

msg = Mensagem(remetente="Lucas", texto="Oi", timestamp="2026-07-07")
print(msg)

# Agora o teste importante: passar um tipo errado
msg_invalida = Mensagem(remetente="Lucas", texto=123, timestamp="2026-07-07")
print(msg_invalida)