"""
Operaciones aritméticas básicas con validación de tipos y rangos representables.
"""

from __future__ import annotations

import math
from typing import Any, Final

# Constante π con la precisión nativa de float (IEEE 754 doble precisión).
PI: Final[float] = math.pi


def _validar_operando(valor: Any, nombre: str) -> float:
    """
    Normaliza un operando a float y valida tipo y finitud.

    Rechaza bool (subclase de int en Python), otros tipos y valores no finitos.
    """
    if isinstance(valor, bool):
        raise TypeError(
            f"{nombre}: no se acepta bool; use int o float explícitamente."
        )
    if not isinstance(valor, (int, float)):
        raise TypeError(
            f"{nombre}: se esperaba int o float; se recibió {type(valor).__name__}."
        )
    resultado = float(valor)
    if not math.isfinite(resultado):
        raise ValueError(f"{nombre}: el valor debe ser finito (no inf ni nan).")
    return resultado


def _asegurar_resultado_finito(valor: float, operacion: str) -> float:
    """Comprueba que el resultado de la operación sea representable de forma finita."""
    if not math.isfinite(valor):
        raise OverflowError(
            f"{operacion}: el resultado excede el rango representable o no es finito."
        )
    return valor


def sumar(a: Any, b: Any) -> float:
    """Devuelve a + b. Valida operandos y desbordamiento del resultado."""
    x = _validar_operando(a, "a")
    y = _validar_operando(b, "b")
    return _asegurar_resultado_finito(x + y, "sumar")


def restar(a: Any, b: Any) -> float:
    """Devuelve a - b. Valida operandos y desbordamiento del resultado."""
    x = _validar_operando(a, "a")
    y = _validar_operando(b, "b")
    return _asegurar_resultado_finito(x - y, "restar")


def multiplicar(a: Any, b: Any) -> float:
    """Devuelve a * b. Valida operandos y desbordamiento del resultado."""
    x = _validar_operando(a, "a")
    y = _validar_operando(b, "b")
    return _asegurar_resultado_finito(x * y, "multiplicar")


def dividir(a: Any, b: Any) -> float:
    """
    Devuelve a / b. Valida operandos, división por cero y resultado finito.
    """
    x = _validar_operando(a, "a")
    y = _validar_operando(b, "b")
    if y == 0.0:
        raise ZeroDivisionError("dividir: el divisor no puede ser cero.")
    return _asegurar_resultado_finito(x / y, "dividir")


__all__ = ["PI", "dividir", "multiplicar", "restar", "sumar"]
