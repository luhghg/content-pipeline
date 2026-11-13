from app.models.db_models import ContentItem, Status
import pytest
from app.LLM.LLM_functions import transition


def test_transition():
    content = ContentItem(status=Status.APPROVED)
    with pytest.raises(ValueError):
        transition(item=content, new_status=Status.GENERATING)
