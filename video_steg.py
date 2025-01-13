import wave
from moviepy import *

# This function will hide the message inside the audio file
def encode_message_to_sound(input_audio_path, message, output_audio_path):
    #o Open the audio file and read the frames
    with wave.open(input_audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = bytearray(audio.readframes(audio.getnframes()))

    # Convert the message to binary and add 8 0 bits to make the end
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'

    # If the message is longer than the number of audio frames, return error
    if len(binary_message) > len(frames):
        raise ValueError("The audio file is too small to hold the message.")

    # Replace the elast significant bit fo each frame with the message bits
    binary_index = 0
    for i in range(len(frames)):
        if binary_index < len(binary_message):
            frames[i] = (frames[i] & ~1) | int(binary_message[binary_index])
            binary_index += 1
        else:
            break

    # Save the encoded audio with the hidden message
    with wave.open(output_audio_path, 'wb') as output_audio:
        output_audio.setparams(params)
        output_audio.writeframes(frames)

    print(f"Message encoded and saved to {output_audio_path}")

# This function decodes the audio and gets the hidden message
def decode_message_from_sound(input_audio_path):
    # Open the audio and read all the frames
    with wave.open(input_audio_path, 'rb') as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))

    # Extract the LSBs of each frame to build the message
    binary_message = ''
    for frame in frames:
        binary_message += str(frame & 1)

    # Convert the binary message into characters
    decoded_message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if byte == '00000000': # Stop when we reach the end
            break
        decoded_message += chr(int(byte, 2)) # Convert binary back to character

    return decoded_message

# This function hides a message by encoding it into the audio track
def encode_message_to_video(input_video_path, message, output_video_path):
    # Extract audio from video
    input_audio_path = '/tmp/temp_audio.wav'
    video_clip = VideoFileClip(input_video_path)
    video_clip.audio.write_audiofile(input_audio_path, codec='pcm_s16le')

    # Send audio to the existing function
    encoded_audio_path = '/tmp/encoded_audio.wav'
    encode_message_to_sound(input_audio_path, message, encoded_audio_path)

    # Replace the original audio with the encoded one
    encoded_audio_clip = AudioFileClip(encoded_audio_path)
    final_video = video_clip.with_audio(encoded_audio_clip)

    # Save the final video with the hidden message
    final_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

    print(f"Video with encoded message saved to {output_video_path}")

# This function extracts the hidden message from the video's audio
def decode_message_from_video(input_video_path):
    # Extract the audio from the video
    input_audio_path = '/tmp/extracted_audio.wav'
    video_clip = VideoFileClip(input_video_path)
    video_clip.audio.write_audiofile(input_audio_path, codec='pcm_s16le')

    # Use the existing function to decode the audio
    decoded_message = decode_message_from_sound('/tmp/encoded_audio.wav')
    return decoded_message


def main():
    sub_choice = input("(1) Encode a message, (2) Decode a message: ")
    if sub_choice == "1":
        input_video_path = input("Enter the path to the input video file (MP4 format): ")
        message = input("Enter the message to encode: ")
        output_video_path = input("Enter the path for the output video file: ")
        try:
            encode_message_to_video(input_video_path, message, output_video_path)
        except Exception as e:
            print(f"Error: {e}")

    elif sub_choice == "2":
        input_video_path = input("Enter the path to the encoded video file (MP4 format): ")
        try:
            decoded_message = decode_message_from_video(input_video_path)
            print(f"Decoded message: {decoded_message}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()

