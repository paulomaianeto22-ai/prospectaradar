"""Senha (hash pbkdf2, só stdlib — sem dependência extra)."""
import hashlib, hmac, os


def hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, 100_000)
    return f"{salt.hex()}:{dk.hex()}"


def verificar_senha(senha: str, guardado: str) -> bool:
    try:
        salt_hex, dk_hex = guardado.split(":")
        dk = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(salt_hex), 100_000)
        return hmac.compare_digest(dk.hex(), dk_hex)
    except Exception:
        return False
