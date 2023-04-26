
class Mempool:
    def __init__(self):
        self.mempool = []

    def add_to_mempool(self, transaction):
        exists = False
        for tx in self.mempool:
            if (tx.signature == transaction.signature):
                exists = True
        if not exists:
            self.mempool.append(transaction)
