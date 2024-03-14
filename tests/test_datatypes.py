import pytest
import json

from prooompt.datatypes import (
    Template,
    TemplateItem,
    TemplateMessage,
    TemplateEval,
    TemplateLoop,
    TemplateText,
    Message,
)


@pytest.fixture
def text_item_input():
    return {"type": "text", "content": "foobar"}


@pytest.fixture
def eval_item_input():
    return {"type": "eval", "value": "foobar"}


@pytest.fixture
def loop_item_input(
    text_item_input,
    eval_item_input,
):
    return {
        "type": "loop",
        "iterator": "foo",
        "iterable": "bar",
        "template": [
            text_item_input,
            eval_item_input,
        ],
    }


@pytest.fixture
def message_item_input(
    text_item_input,
    eval_item_input,
):
    return {
        "type": "message",
        "role": "user",
        "template": [
            text_item_input,
            eval_item_input,
        ],
    }


@pytest.fixture
def template_input(
    text_item_input, eval_item_input, loop_item_input, message_item_input
):
    return {
        "items": [
            text_item_input,
            eval_item_input,
            loop_item_input,
            message_item_input,
        ],
    }


def test_load_text_template(text_item_input):
    text_item = TemplateItem.validate_json(json.dumps(text_item_input))
    assert text_item
    assert isinstance(text_item, TemplateText)


def test_load_eval_template(eval_item_input):
    eval_item = TemplateItem.validate_json(json.dumps(eval_item_input))
    assert eval_item
    assert isinstance(eval_item, TemplateEval)


def test_load_loop_template(loop_item_input):
    loop_item = TemplateLoop.model_validate(loop_item_input)
    assert loop_item
    assert isinstance(loop_item, TemplateLoop)
    assert isinstance(loop_item.template[0], TemplateText)
    assert isinstance(loop_item.template[1], TemplateEval)


def test_load_message_template(message_item_input):
    message_item = TemplateMessage.model_validate(message_item_input)
    assert message_item
    assert isinstance(message_item, TemplateMessage)
    assert isinstance(message_item.template[0], TemplateText)
    assert isinstance(message_item.template[1], TemplateEval)


def test_load_template(template_input):
    template = Template.model_validate(template_input)
    assert template
    assert isinstance(template, Template)
    assert isinstance(template.items[0], TemplateText)
    assert isinstance(template.items[1], TemplateEval)
    assert isinstance(template.items[2], TemplateLoop)
    assert isinstance(template.items[3], TemplateMessage)
    assert isinstance(template.items[3].template[0], TemplateText)
    assert isinstance(template.items[3].template[1], TemplateEval)
