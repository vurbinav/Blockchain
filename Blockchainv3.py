import datetime # show timestamp of block when created
import hashlib # used to hash the blocks
import json # used to encode block before hashing them
import time

# Define Transaction class
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

# Build Blockchain
class Blockchain:
    def __init__(self):
        # Initializes Blockchain
        self.chain = []
        # We use '0' because we are going to use SHA256 which only accepts Strings with ' '
        self.create_block(proof=1, prev_hash='0')

    # Defines new created block
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash,
                 'transactions': []}  # Add transactions field
        # Calculate hash of the block
        block['hash'] = self.hash(block)
        # Join to chain
        self.chain.append(block)
        return block

    # Return prev block
    def get_prev_block(self):
        return self.chain[-1]

    def proof_work(self, prev_proof):
        new_proof = 1
        check_proof = False

        # When we find solution proof becomes True
        while check_proof is False:
            # Hashes the operation into SHA256
            hash_operation = hashlib.sha256(str(new_proof ** 2 - prev_proof ** 2).encode()).hexdigest()
            # Checks first 4 characters for hash operation to be 0000
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                # goes to the next new_proof value to check
                new_proof += 1
        return new_proof

    # Makes sure all blocks have the correct proof_work
    # Makes sure the prev_hash of each block is the same as prev_hash of all blocks
    def hash(self, block):
        # Encodes block in SHA256
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def valid_chain(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            # Makes sure proof starts with 0000
            hash_operation = hashlib.sha256(str(proof ** 2 - prev_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True


# Function to add a transaction to the blockchain
def add_transaction_to_blockchain(transaction, blockchain):
    latest_block = blockchain.get_prev_block()
    if len(latest_block['transactions']) >= 2:
        new_proof = blockchain.proof_work(latest_block['proof'])
        new_block = blockchain.create_block(new_proof, latest_block['hash'])
    latest_block['transactions'].append(vars(transaction))

# Function to corrupt the blockchain by modifying a block
def corrupt_blockchain(blockchain, index):
    if index >= len(blockchain.chain):
        print("Invalid block index.")
        return
    block_to_corrupt = blockchain.chain[index]
    block_to_corrupt['transactions'] = [{'corrupted': True}]
    block_to_corrupt['hash'] = blockchain.hash(block_to_corrupt)


# Interactability with the blockchain
if __name__ == '__main__':
    blockchain = Blockchain()

    while True:
        print("\n1. Add a transaction")
        print("2. Display all blocks")
        print("3. Corrupt the Blockchain")
        print("4. Check Blockchain validity")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            sender = input("Enter sender name: ")
            recipient = input("Enter recipient name: ")
            amount = input("Enter amount: ")
            transaction = Transaction(sender, recipient, amount)
            add_transaction_to_blockchain(transaction, blockchain)
            print("Transaction added!")
        elif choice == '2':
            for block in blockchain.chain:
                print("Block #" + str(block['index']))
                print("Timestamp: " + block['timestamp'])
                print("Proof: " + str(block['proof']))  # Convert proof to string for concatenation
                print("Previous Hash: " + block['prev_hash'])
                print("\n")
        elif choice == '3':
            index = int(input("Enter the index of the block to corrupt: "))
            corrupt_blockchain(blockchain, index)
            print(f"Blockchain corrupted at block index {index}!")
        elif choice == '4':
            valid = blockchain.valid_chain(blockchain.chain)
            print("Blockchain valid!" if valid else "Blockchain compromised!")
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")