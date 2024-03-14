# applying inputs to a template
from prooompt.datatypes import (
    Template,
    TemplateMessage,
    TemplateEval,
    TemplateLoop,
    TemplateText,
    Message,
    TemplateItemUnion,
)


def apply_template(template: Template, inputs: dict) -> list[Message]:
    messages: list[Message] = []
    for item in template.items:
        if isinstance(item, TemplateMessage):
            message_content = get_message_content(item.template, inputs)
            messages.append(Message(role=item.role, content=message_content))
        if isinstance(item, TemplateText):
            raise ValueError("Text items are not allowed at the top level")
        if isinstance(item, TemplateEval):
            raise ValueError("Eval items are not allowed at the top level")
        if isinstance(item, TemplateLoop):
            if item.iterable not in inputs:
                raise ValueError(f"Loop iterable {item.iterable} not in inputs")
            for iterator in inputs[item.iterable]:
                sub_messages = apply_template(
                    Template(items=item.template),
                    {
                        **inputs,
                        item.iterator: iterator,
                    },
                )
                messages.extend(sub_messages)
    return messages


def get_message_content(template: list[TemplateItemUnion], inputs: dict) -> Message:
    content = ""
    for item in template:
        if isinstance(item, TemplateMessage):
            raise NotImplementedError("Nested messages are not supported")
        if isinstance(item, TemplateText):
            content += item.content
        if isinstance(item, TemplateEval):
            content += str(eval(item.value, inputs))
        if isinstance(item, TemplateLoop):
            if item.iterable not in inputs:
                raise ValueError(f"Loop iterable {item.iterable} not in inputs")
            for iterator in inputs[item.iterable]:
                sub_content = get_message_content(
                    item.template,
                    {
                        **inputs,
                        item.iterator: iterator,
                    },
                )
                content += sub_content
    return content
