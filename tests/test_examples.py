import pytest
import json
from prooompt.datatypes import Template, Message
from prooompt.apply import apply_template
from prooompt.parse import parse

EXAMPLE_TEST_CASES = [
    "./examples/simple",
    "./examples/eval",
    "./examples/loop",
    "./examples/loop_outer",
]


@pytest.fixture(params=EXAMPLE_TEST_CASES)
def example(request):
    folder = request.param
    # load template.txt
    with open(f"{folder}/template.txt") as f:
        template_txt = f.read()
    # load template.json
    with open(f"{folder}/template.json") as f:
        template_json = json.load(f)
    # load inputs.json
    with open(f"{folder}/inputs.json") as f:
        inputs = json.load(f)
    # load messages.json
    with open(f"{folder}/messages.json") as f:
        messages = json.load(f)
    return template_txt, template_json, inputs, messages


def test_example_parse(example):
    template_txt_raw, template_json_raw, _, _ = example
    template_expected = Template.model_validate(template_json_raw)
    template_actual = parse(template_txt_raw)
    assert template_actual == template_expected


def test_example_apply(example):
    _, template_json_raw, inputs_raw, messages_raw = example

    # load template
    template = Template.model_validate(template_json_raw)
    assert template

    # load messages
    messages = [Message.model_validate(m) for m in messages_raw]

    # apply the inputs to the template
    output = apply_template(template, inputs_raw)
    assert output == messages
