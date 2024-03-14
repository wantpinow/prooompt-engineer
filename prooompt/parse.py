import re
from prooompt.tokenize import Token, tokenize
from prooompt.datatypes import (
    Template,
    TemplateItemUnion,
    TemplateMessage,
    MessageRole,
    TemplateText,
    TemplateEval,
    TemplateLoop,
)


def parse(raw_template: str) -> Template:
    tokens = tokenize(raw_template)
    return parse_tokens(tokens)


def parse_tokens(tokens: list[Token]) -> Template:
    items = parse_template_items(tokens, top_level=True)
    return Template(items=items)


def parse_template_items(
    tokens: list[Token], top_level: bool = True
) -> list[TemplateItemUnion]:
    token_types = [token.type for token in tokens]
    parsed = []
    token_idx = 0
    while token_idx < len(tokens):
        token = tokens[token_idx]

        if token.type == "MESSAGE_START":
            # Extract the role from the message start token
            role = token.value

            # Get the tokens between the message start and endmessage tokens
            message_end_idx = token_types[token_idx:].index("ENDMESSAGE")
            message_tokens = tokens[token_idx + 1 : token_idx + message_end_idx]

            # Parse the message tokens
            message_template = parse_template_items(message_tokens, top_level=False)

            # Remove leading and trailing whitespace from the first and last text tokens
            if isinstance(message_template[0], TemplateText):
                message_template[0].content = message_template[0].content.lstrip()
            if isinstance(message_template[-1], TemplateText):
                message_template[-1].content = message_template[-1].content.rstrip()

            # Add the new message to the parsed list
            message = TemplateMessage(role=MessageRole(role), template=message_template)
            parsed.append(message)
            token_idx += message_end_idx
            continue

        elif token.type == "FOR":
            for_loop_depth = 1
            for_loop_tokens = []

            # regex: get the iterator and the iterable
            # format: for x in y

            iterator, iterable = re.search(
                r"for\s+(.+?)\s+in\s+(.+)", token.value
            ).groups()

            for token in tokens[token_idx + 1 :]:
                if token.type == "FOR":
                    for_loop_depth += 1
                elif token.type == "ENDFOR":
                    for_loop_depth -= 1
                    if for_loop_depth == 0:
                        break
                for_loop_tokens.append(token)
            for_loop_template = parse_template_items(for_loop_tokens, top_level=False)
            parsed.append(
                TemplateLoop(
                    template=for_loop_template, iterator=iterator, iterable=iterable
                )
            )
            token_idx += len(for_loop_tokens) + 1
            continue

        elif token.type == "EXPRESSION" and not top_level:
            parsed.append(TemplateEval(value=token.value))

        elif token.type == "TEXT" and not top_level:
            parsed.append(TemplateText(content=token.value))

        token_idx += 1

    return parsed
