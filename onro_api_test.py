from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def encrypt_with_public_key(public_key_str: str, plaintext: str) -> str:
    # Load the public key from the string
    public_key = serialization.load_pem_public_key(public_key_str.encode())

    # Encrypt the plaintext
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Encode the ciphertext as a Base64 string
    return base64.b64encode(ciphertext).decode()


def decrypt_with_private_key(private_key_str: str, ciphertext_str: str) -> str:
    # Decode the Base64 string to get the binary ciphertext
    ciphertext = base64.b64decode(ciphertext_str)

    # Load the private key from the string
    private_key = serialization.load_pem_private_key(private_key_str.encode(), password=None)

    # Decrypt the ciphertext
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()
# Example usage
public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqXpA8/Y9GLRkQIUBvQJq
yt4hfQP9xuTyDvzs0KmoOR3ud+OYT/VymQcdujzGJbF5VygzRduM4qm6feFUHnJ2
lGaQqRwmZvpeBwB1Lwj2jT+5PrVQ+tNapSahH5h3enoYGnZU4qD1gdLkw5ef1fiq
qpFMTni3eojChuGudUveiT1LaSPH8GdQuFOFszRXUqHVZXZNU8+aL/m/F6mgyUMe
bP9YS6YJ/BCj/NOrg8hIezRi//058/XU4GQ2hETz/3tkyaWVXiV1lKvAg2tL7JL/
uPwrIupFntnLwhLWvSSjtKhsqNuStW3J0gqnxOmMMt8PqahdV6S/lGy+3WPVFMca
0wIDAQAB
-----END PUBLIC KEY-----"""

private_key = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCpekDz9j0YtGRA
hQG9AmrK3iF9A/3G5PIO/OzQqag5He5345hP9XKZBx26PMYlsXlXKDNF24ziqbp9
4VQecnaUZpCpHCZm+l4HAHUvCPaNP7k+tVD601qlJqEfmHd6ehgadlTioPWB0uTD
l5/V+KqqkUxOeLd6iMKG4a51S96JPUtpI8fwZ1C4U4WzNFdSodVldk1Tz5ov+b8X
qaDJQx5s/1hLpgn8EKP806uDyEh7NGL//Tnz9dTgZDaERPP/e2TJpZVeJXWUq8CD
a0vskv+4/Csi6kWe2cvCEta9JKO0qGyo25K1bcnSCqfE6Ywy3w+pqF1XpL+UbL7d
Y9UUxxrTAgMBAAECggEAO2lipMOBNoxiiqW17ssOofCN/9Pq3pM68hsjb6DSGrfN
9dRg/ELYuiGe/783XVZiabXrh4VIVdtXR7K6uPO6cxqjgs0d/0KsvLqh2evD9s9M
gtmwOkXmhHfOyxM5a0Oq+HfcGRiBCFJkpNaeDzYdqi7Gd8nk1D1mKD+sV21R5Xz2
8OdIYlBnuFI1ZkgJ/aUn55Kcpwg7AdQp6gFXcQHsrs3SmcCre+PFr7ycaB5ivB7N
UdYtqB6FGN7pEeY800Jd483XYMWDj7iGjbMGECadG/PyHJn6gcx9McDFJOqFv8pE
3i2hGTg2e/B9nMrhtp0P3ggJACx3solhmn6oQoWUQQKBgQDoJqOaPq8ksnYGZYpe
9WbI6nVVjK1y+Wvd/IEKOVquwyddLw4/c9SbY+uIuxZfR0yTtNWTHOCESD034R0d
jw04r/Pjhsuz7A/k56jNm80dqcTrDe1Ls9dKNXoTU53DchbnDlDpfp/GMCIjkdWe
iLvXJAOphnBWE6aVdtyWTbv/QQKBgQC641xvTrT6q0IopWFzKrO5f2H5eE+FRjgV
LKk4mMBR7SbRM+xEfrGESDrMC8KZUe3pPO5fTkO6Sl1LTUTmr3aFqgkEyXCmtQmi
L+hnYbgc/MHWiXZ3AP0uDEsh9leM/fe4xwvE94V47OH/TrZHW8iz2t69QLjcwLor
pxkNJUHpEwKBgEbZa/qqAMfBUzXWjWk3mbvdmhuWyGSbbGkeI7+cC2nkk0HkF4QT
9KHL19ktx8EiQGOfv8KbAIY+ibhhEoKv4sgXIuagf9CUTbF9Zc4CK5JO+pMF+BKv
exfhxDTbwv0f949ilhz8kQRqMjEK09gDQNiC3D9DkUsjyiY5VU7lwGdBAoGBAK/d
GfOoRggItoYXMn+0dFGffCvMuk/4xveuAkO/AmNV3gxJZxEBg7yuV54BhwrOHSo5
azsGJBeeuPIOcUL/ZHHdkwUNJlPJ0pnrqS/3tdCZTTK8Ql0z8guuB9mavcJwjvcz
X3DnV5N2niipAkBeL5yH3siKqisZtVc0tA85uy8/AoGBALcdiqpj926Lb2TLuQ18
uP4JprDwP+HhFK6SE5PlNGDzG6yEe7ADHMp8b5HFRkqApkzByHs00iUXcaSVYLni
BMAxbEkBRQS4Pb5NTuiBTn9IugzGmAvNc8cVAomy2qvxJmobp3HA0Fttgkuc/RX/
1/wIbwq6M8yYpST5qDJdJzDk
-----END PRIVATE KEY-----"""

message = "xyz"

# Encrypt
ciphertext = encrypt_with_public_key(public_key, message)
print("Encrypted:", ciphertext)

# Decrypt
decrypted_message = decrypt_with_private_key(private_key, ciphertext)
print("Decrypted:", decrypted_message)
