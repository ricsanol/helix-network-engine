from __future__ import annotations

from helix.models.precheck_result import PreCheckResult


def should_approve(precheck_result: PreCheckResult) -> bool:
    """
    Regra central:
    Se o pre-check foi sucesso, pode aplicar.
    """
    return precheck_result.success


def build_decision_reason(precheck_result: PreCheckResult) -> str:
    """
    Gera motivo padronizado da decisão.
    """
    if precheck_result.success:
        return "pre-check aprovado"

    reasons = []

    if precheck_result.errors:
        reasons.extend(precheck_result.errors)

    for item in precheck_result.items:
        if not item.passed and item.severity.upper() == "ERROR":
            reasons.append(f"{item.name}: {item.message}")

    if not reasons:
        return "pre-check falhou (motivo não identificado)"

    return "; ".join(reasons)