def generate_answer(query: str, context: str, language: str = 'es') -> str:
    import re
    sentences = re.split(r'(?<=[.!?])\s+', context)
    top = ' '.join(sentences[:3])[:800]
    if not top:
        top = 'No encontré información específica en la base. Describe con más detalle el problema.'
    if language.startswith('pt'):
        pre = 'Resumo técnico:'
    elif language.startswith('en'):
        pre = 'Technical summary:'
    else:
        pre = 'Resumen técnico:'
    return f"{pre} {top}"
