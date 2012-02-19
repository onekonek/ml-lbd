tag_names = ["POS", "CHK"]

class Token():

    def __init__(self):
        self.tags = {}
        self.string = ""

    def print_tagged(self):
        tag_string = '\t'.join("{0} = {1:<4}".format(
            name, self.tags[name] if name in self.tags else "") 
            for name in tag_names)
        print("{0:<20}\t{1}".format(self.string, tag_string))

class TokenReader():

    def read_whitespaced_tokens(self, filename, tag_order = [0, 1]):
        """Reads tokens from a whitespace-separated file and returns a list.

        The file contains word<whitespace>tag1<TAB>tag2...
        The tag_order[i, j...] parameter defines that at column i(j..)
        tag 0(1...) (see tag_names) is present.
        TODO(elmar): Better to use tuples here.
        
        """
        tokens_file = open(filename, "r")
        tokens = []
        for line in tokens_file:
            # Skip empty lines.
            if line.strip() == "":
                continue
            token = Token()
            cols = line.strip().split()
            token.string = cols[0]
            # Insert the tags.
            for tag_name_idx, idx in enumerate(tag_order):
                # Check if the tag is present.
                if idx + 1< len(cols):
                    token.tags[tag_names[tag_name_idx]] = cols[idx + 1]
            tokens.append(token)
        tokens_file.close()
        return tokens

if __name__ == '__main__':
    print("This is module %s"%(__name__))
    exit(1)
