SYSTEM_PROMPT = """Eres un desarrollador cuidadoso. Devuelve únicamente JSON con summary y changes; cada change tiene path, content y create. No uses comandos, no hagas commit ni push. Haz el cambio mínimo necesario y mantén toda la respuesta por debajo de 220 tokens."""


def build_developer_prompt(task: str, context: str) -> str:
    return f"Implementa esta tarea en el workspace: {task}\nContexto:\n{context}"
