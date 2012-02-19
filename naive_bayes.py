from token import Token, TokenReader


if __name__ == '__main__':

    reader = TokenReader()
    tokens = reader.read_whitespaced_tokens("data/train_pos.txt")
    for token in tokens:
        token.print_tagged()
