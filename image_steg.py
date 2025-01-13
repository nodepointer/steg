from cryptosteganography import CryptoSteganography

def encode(image_path, message, output_path, key):
    stego = CryptoSteganography(key)
    stego.hide(image_path, output_path, message)
    print(f"Message encoded and saved to {output_path}")

def decode(image_path, key):
    stego = CryptoSteganography(key)
    message = stego.retrieve(image_path)
    return message

if __name__ == "__main__":
    choice = input("Choose an option: (1) Encode, (2) Decode: ")
    key = input("Enter encryption key: ")

    if choice == "1":
        try:
            encode(input("Input image path: "), input("Message to encode: "), input("Output image path: "), key)
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "2":
        try:
            decoded_message = decode(input("Encoded image path: "), key)
            print(f"Decoded message: {decoded_message}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice.")
