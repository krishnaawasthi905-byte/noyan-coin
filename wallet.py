import hashlib
import ecdsa
import os

def generate_wallet():
    # Generate private key
    private_key = os.urandom(32)
    
    # Generate public key from private key
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    public_key = signing_key.get_verifying_key()
    
    # Generate wallet address
    pub_hash = hashlib.sha256(public_key.to_string()).hexdigest()
    address = "NYN" + pub_hash[:32].upper()
    
    return {
        "private_key": private_key.hex(),
        "public_key": public_key.to_string().hex(),
        "address": address
    }

# Generate Aryan's founder wallet
wallet = generate_wallet()
print("=== NYN FOUNDER WALLET ===")
print(f"Address: {wallet['address']}")
print(f"Public Key: {wallet['public_key'][:32]}...")
print(f"Private Key: {wallet['private_key']}")
print("\n⚠️ SAVE YOUR PRIVATE KEY - NEVER SHARE IT")