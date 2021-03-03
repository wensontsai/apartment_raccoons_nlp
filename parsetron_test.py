# !pip install parsetron
# python2 parsetron_test.py
## ONLY RUNS FOR PYTHON 2 ##

from parsetron import Set, Regex, Optional, OneOrMore, Grammar, RobustParser
import string


class LightGrammar(Grammar):

    action = Set(['change', 'flash', 'set', 'blink'])
    light = Set(['top', 'middle', 'bottom'])
    color = Regex(r'(red|yellow|blue|orange|purple|...)')
    times = Set(['once', 'twice', 'three times']) | Regex(r'\d+ times')
    one_parse = action + light + Optional(times) + color
    GOAL = OneOrMore(one_parse)

    @staticmethod
    def test():
        parser = RobustParser((LightGrammar()))
        sents = [
            "set my top light to red",
            "set my top light to red and change middle light to yellow",
            "set my top light to red and change middle light to yellow and "
            "flash bottom light twice in blue"
        ]
        for sent in sents:
            tree, result = parser.parse(sent)
            assert result.one_parse[0].color == 'red'

            print '"%s"' % sent
            print "parse tree:"
            print tree
            print "parse result:"
            print result
            print


class QuestionGrammar(Grammar):

    search = Set(["revenue numbers", "revenues", "revenue", "sales", "sales numbers", "same store sales"])
    direction = Set(["increase", "decrease", "change"])
    company = Set(["Amazon", "LinkedIn", "Microsoft", "Apple"])
    duration = Set(["last quarter", "this quarter", "from last quarter to this quarter", "from last to this quarter",
                    "from last quarter"])
    parse_rule_0 = search + company
    parse_rule_1 = search + company + duration
    parse_rule_2 = search + direction + company + duration
    parser_rule_3 = search + direction + duration + company
    GOAL = OneOrMore(parse_rule_0 | parse_rule_1 | parse_rule_2 | parser_rule_3)

    @staticmethod
    def test():
        parser = RobustParser((QuestionGrammar()))
        sents = [
            "what was the revenue for Amazon last quarter?",
            "did revenue numbers change for Amazon from last quarter to this quarter?",
            "how much did same store sales increase for Apple last quarter?"
        ]
        for sent in sents:
            tree, result = parser.parse(sent)
            assert result.one_parse[0].color == 'red'

            print '"%s"' % sent
            print "parse tree:"
            print tree
            print "parse result:"
            print result
            print


def clean_sent(sent):
    return sent.strip(string.punctuation)


parser = RobustParser(QuestionGrammar())
sents = ["what were the revenue and same store sales numbers for Amazon from last quarter?"]
for sent in sents:
    sent = clean_sent(sent)
    tree, result = parser.parse(sent)
    print '"%s"' % sent
    print "parse result:"
    if result is not None:
        for key, vals in result.items():
            for val in vals:
                if key != "GOAL":
                    direction = val.get("direction", None)
                    search = val.get("search", None)
                    company = val.get("company", None)
                    duration = val.get("duration", None)

                    print "Search - %s" % search
                    print "Direction - %s" % direction
                    print "Company - %s" % company
                    print "Duration - %s" % duration


