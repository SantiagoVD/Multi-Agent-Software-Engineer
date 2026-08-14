SYSTEM_PROMPT = """Eres un revisor de código. Evalúa seguridad, regresiones y cumplimiento. Devuelve ReviewResult y no modifiques archivos."""


def build_review_prompt(task: str, context: str) -> str:
    return f"Revisa los cambios para esta tarea: {task}\n{context}"
