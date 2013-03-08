import model
import sys


if __name__ == '__main__':
    modelfilename = sys.argv[1]
    model = model.get_model(modelfilename)
    tagfilename = sys.argv[2]
    with open(tagfilename, "r") as f:
        for line in f:
            if line.strip() == "":
                print ""
                continue
            word = vword = line.strip()
            if word not in model.vocabulary:
                vword = "_RARE_"
            tag = ""
            p_max = 0
            for t in model.tags:
                p = model.tag_word_prob.get((t, vword), 0)
                if p > p_max:
                    tag = t
                    p_max = p
            print word + " " + tag
    print "*" in model.tags
