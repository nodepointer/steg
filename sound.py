import wave

def encode_message_to_sound(input_audio, message, output_audio):
    # Open the input WAV file
    with wave.open(input_audio, 'rb') as audio:
        # Retrieve audio parameters and frames
        params, frames = audio.getparams(), bytearray(audio.readframes(audio.getnframes()))

    # Convert the message into binary format and append a terminator
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'

    # Check if the audio file has enough capacity to encode the message
    if len(binary_message) > len(frames):
        raise ValueError("Audio file too small for the message.")

    # Embed the binary message into the least significant bit (LSB) of audio frames
    for i, bit in enumerate(binary_message):
        frames[i] = (frames[i] & ~1) | int(bit)  # Modify LSB to match the message bit

    # Write the modified frames to the output WAV file
    with wave.open(output_audio, 'wb') as output:
        output.setparams(params)  # Use the same parameters as the input audio
        output.writeframes(frames)

    print(f"Message encoded in {output_audio}")

def decode_message_from_sound(input_audio):
    # Open the input WAV file
    with wave.open(input_audio, 'rb') as audio:
        # Read audio frames
        frames = bytearray(audio.readframes(audio.getnframes()))

    # Extract the LSBs of each frame to reconstruct the binary message
    binary_message = ''.join(str(frame & 1) for frame in frames)

    # Convert binary message back to text
    decoded_message = ''.join(
        chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)
    )

    # Stop decoding at the terminator (null character '\x00')
    return decoded_message.split('\x00', 1)[0]

def main():
    print("Audio Steganography - Encode and Decode Messages")
    choice = input("(1) Encode, (2) Decode: ")

    if choice == "1":
        encode_message_to_sound(
            input("Input WAV file: "),
            input("Message to encode: "),
            input("Output WAV file: ")
        )
    elif choice == "2":
        print("Decoded message:", decode_message_from_sound(input("Encoded WAV file: ")))
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()