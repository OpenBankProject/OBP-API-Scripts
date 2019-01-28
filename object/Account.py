class Account:
    def __init__(self, id, bank, label, number, type,
                 balance, IBAN, owners, generate_public_view,
                 generate_accountants_view, generate_auditors_view):
        self.id = id
        self.bank= bank
        self.label = label
        self.number = number
        self.type = type
        self.balance = balance
        self.IBAN = IBAN
        self.owners = owners
        self.generate_public_view = generate_public_view
        self.generate_accountants_view = generate_accountants_view
        self.generate_auditors_view = generate_auditors_view