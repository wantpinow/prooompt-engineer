import re
from pydantic import BaseModel


# Defining a simple token structure
class Token(BaseModel):
    type: str
    value: str


# Token definitions
TOKEN_REGEX = re.compile(
    r"""
    (\{\%\s*endmessage\s*\%\})|    # End of a message block
    (\{\%\s*message\s+[a-z]+\s*\%\})| # Start of a message block with role
    (\{\%\s*endfor\s*\%\})|        # End of a loop
    (\{\%\s*for\s+.+?\s+in\s+.+?\s*\%\})| # Start of a loop
    (\{\{.+?\}\})|                 # Expression
    (\{\%.*?\%\})|                 # Other tag (for future use)
    ([^{]+)                        # Text
    """,
    re.VERBOSE,
)

# Token types
TOKEN_TYPES = [
    ("ENDMESSAGE", "endmessage"),
    ("MESSAGE_START", "message"),
    ("ENDFOR", "endfor"),
    ("FOR", "for"),
    ("EXPRESSION", "expression"),
    ("TAG", "tag"),
    ("TEXT", "text"),
]


def tokenize(text) -> list[Token]:
    tokens = []
    for match in TOKEN_REGEX.finditer(text):
        match_groups = match.groups()
        for i, group in enumerate(match_groups):
            if group:
                # Determine the type based on which group matched
                token_type = TOKEN_TYPES[i][0]
                token_value = group
                if token_type != "TEXT":
                    token_value = token_value.strip()

                # Special handling for message and for tags to include additional info
                if token_type in ["MESSAGE_START", "FOR"]:
                    # Extracting role for MESSAGE_START or loop variables for FOR
                    token_value = re.sub(
                        r"^\{\%\s*|\s*\%\}$", "", token_value
                    )  # Remove the tag delimiter
                    if token_type == "MESSAGE_START":
                        token_value = token_value.split(" ")[1]

                if token_type == "EXPRESSION":
                    # remove the {{ and }} delimiters
                    token_value = token_value[2:-2].strip()

                tokens.append(Token(type=token_type, value=token_value))
                break
    # filter out text tokens that are empty
    tokens = [
        token
        for token in tokens
        if not (token.type == "TEXT" and token.value.strip() == "")
    ]
    return tokens
