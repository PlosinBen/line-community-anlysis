import re


class Rule:
    def __init__(self, msg_group: str, msg_type: str, regex: str):
        self.msg_group: str = msg_group
        self.msg_type: str = msg_type
        self.regex: str = regex
        self.match_groups: tuple | None = None

    def set_match_group(self, match_groups: tuple | None):
        self.match_groups = match_groups
        return self


class Rules:
    def __init__(self, rules: list[Rule] = ()):
        self.rules: list[Rule] = rules

    def match(self, msg: str) -> Rule | None:
        for rule in self.rules:
            result = re.match(rule.regex, msg)
            if result is not None:
                return rule.set_match_group(result.groups())

        return None
