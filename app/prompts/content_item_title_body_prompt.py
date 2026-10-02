from app.models.db_models import ContentType

def title_body_prompt(title: str, content_type: ContentType, prompt_hint: str | None) -> str:
    if prompt_hint is not  None:
        with_prompt = f"and additional information {prompt_hint},"
    else:
        with_prompt = ''

    return f"Write a {content_type.value} on the topic {title}, {with_prompt} and return that in JSON format like that: {{\"title\": text, \"body\": text}}"
