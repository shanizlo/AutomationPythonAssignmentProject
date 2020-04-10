from json import loads

"""
JSON parser for common operations such as checking for a value existence.
"""
class JsonParser(object):
    def __init__(self, json):
        self.json = loads(json)

    def has_value(self, value):
        # Helper method to search (recursively) inside values list.
        def has_value_aux(values, value):
            for child in values:
                # If the child is a dict, call self recursively and keep looking on the dict values.
                if type(child) is dict:
                    if has_value_aux(child.values(), value):
                        return True
                # If the child is a dict, call self recursively and keep looking on the dict values.
                elif type(child) is list:
                    if has_value_aux(child, value):
                        return True
                # Not a dict nor a list - can compare values and return True on success.
                elif child == value:
                    return True
            return False

        return has_value_aux(self.json.values(), value)
