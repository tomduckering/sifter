import email.utils

from sieve.rules import base
import sieve.rules.string

# section 5.1
class SieveTestAddress(base.SieveTest):

    RULE_IDENTIFIER = 'ADDRESS'

    def __init__(self, arguments=None, tests=None):
        base.SieveTest.__init__(self, arguments, tests)
        self.validate_arguments_size(2, 6)
        self.validate_tests_size(0)
        self.match_type = self.comparator = self.address_part = None

        headers_idx = len(self.arguments) - 2
        keylist_idx = len(self.arguments) - 1
        if len(self.arguments) == 3:
            # TODO
            pass
        elif len(self.arguments) == 4:
            # TODO
            pass
        elif len(self.arguments) == 5:
            # TODO
            pass
        elif len(self.arguments) == 6:
            # TODO: allow arguments to come in any order
            self.validate_arg_is_tag(0, ('COMPARATOR',))
            self.validate_arg_is_comparator(1)
            self.comparator = self.arguments[1]
            self.validate_arg_is_address_part(2)
            self.address_part = self.arguments[2].tag
            self.validate_arg_is_match_type(3)
            self.match_type = self.arguments[3].tag

        self.validate_arg_is_stringlist(headers_idx)
        self.validate_arg_is_stringlist(keylist_idx)
        self.headers = self.arguments[headers_idx]
        self.keylist = self.arguments[keylist_idx]

    def evaluate(self, message, state):
        header_values = []
        for header in self.headers:
            # TODO: section 5.1: we should restrict the allowed headers to
            # those headers that contain an "address-list". this includes at
            # least: from, to, cc, bcc, sender, resent-from, resent-to.
            header_values.extend(message.get_all(header, []))
        addresses = []
        for address in email.utils.getaddresses(header_values):
            if address[1] != '':
                addresses.append(sieve.rules.string.address_part(address[1],
                    self.address_part))
        for address in addresses:
            for key in self.keylist:
                if sieve.rules.string.compare(address, key, state,
                        self.comparator, self.match_type):
                    return True
        return False
