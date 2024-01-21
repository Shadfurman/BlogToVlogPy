from openai import OpenAI
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import requests
import os
import time
import pygame
import sys

# OPENAI_API_KEY=your api key here

client = OpenAI()
pygame.init()

RENDER_VIDEO = True
PLAY_SOUND = True
SHOW_IMAGES = True
SKIP_TO_SHOW_GENERATED_IMAGES = True
SKIP_TO_PLAY_GENERATED_AUDIO = True
# UPLOAD_TO_YOUTUBE = True
# UPLOAD_TO_RUMBLE = True
# UPLOAD_TO_TWITTER = True

paragraph_delineator = "\n\n"
text_file = "input.txt"
speech_file_path = "./audio/"
image_file_path = "./images/"

screen_width = 1792     # OpenAI will only generate a limited set of image dimentions
screen_height = 1024    # 1024x1024, 1024x1792 or 1792x1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(text_file)


with open(text_file, 'r') as file:
    file_contents = file.read()

paragraphs = [paragraph.strip() for paragraph in file_contents.split(paragraph_delineator) if paragraph.strip()]

# Create the directory if it doesn't exist
if not os.path.exists(speech_file_path):
    os.makedirs(speech_file_path)
if not os.path.exists(image_file_path):
    os.makedirs(image_file_path)

def check_for_text(image_url):
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "If this image contains clear and obvious non-diegetic text that is easily legible and identifiable, respond with [```yes]. If the image contains no text, or diegetic text that is very small, consists of single letters, or is not easily legible and identifiable, respond with [```no]"},
            {
            "type": "image_url",
            "image_url": {
                "url": image_url,
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )
    reply = response.choices[0].message.content
    print(reply)
    if "```yes" in str(reply):
        print ("Text found in image.\n" + str(reply) + "\n" + image_url)
        return True
    else:
        if "```no" in str(reply):
            return False
        
def text_to_speech(text, voice):
    while True:
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            print(text)
            print("-----")
            return(response)
            break
        except Exception as e:
            if '429' in str(e):
                print("Rate limit reached. Waiting to retry...")
                time.sleep(30)  # Adjust the sleep time if necessary
            else:
                raise  # Re-raise the exception if it's not a rate limit issue

def generate_related_image(text):
    print(text + "\n\n")
    print("Generating image prompt...\n\n")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert image prompt generator. You generate image prompts that never generate text in the image by descibing in vivid visual detail. You avoid words that could be misinterpreted as containing text, such as signs, blueprints, diagram, testing, computation, equation, calculation, numbers, etc."},
            {"role": "user", "content": "Can you please generate a prompt for an awe inspiring image somewhat related to the following\n(Only the prompt and nothing else)\n" + text},
        ]
    )
    image_prompt = response.choices[0].message.content
    print(image_prompt + "\n")

    while True:
        try:
            response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1792x1024",
            quality="standard",
            n=1,
            )
            is_text_present = check_for_text(response.data[0].url)
            if is_text_present == False: break
        except Exception as e:
            if '400' in str(e):
                print(e)
            else:
                raise

    return(response.data[0].url)



clips = []

for i, paragraph in enumerate(paragraphs):
    speech_file = f"{speech_file_path}{i}.mp3"
    image_file = f"{image_file_path}{i}.png"

    if os.path.exists(speech_file):
        print(f"File {speech_file} already exists. Skipping...")
    else:
        speech_response = text_to_speech(paragraph, "alloy")
        speech_response.stream_to_file(speech_file)
        if (SKIP_TO_PLAY_GENERATED_AUDIO):
            PLAY_SOUND = True

    if os.path.exists(image_file):
        print(f"File {image_file} already exists. Skipping...")    
    else:
        image_url = generate_related_image(paragraph)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_file, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded to {image_file}")
            if (SKIP_TO_SHOW_GENERATED_IMAGES):
                SHOW_IMAGES = True
        else:
            print(f"Error downloading image: {response.status_code}")
    
    audio_clip = AudioFileClip(speech_file)
    image_clip = ImageClip(image_file, duration=audio_clip.duration)
    image_clip = image_clip.set_audio(audio_clip)
    clips.append(image_clip)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Toggle with the space bar
                SHOW_IMAGES = not SHOW_IMAGES
                PLAY_SOUND = not PLAY_SOUND
    
    if (PLAY_SOUND == True):
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.load(speech_file)
        pygame.mixer.music.play()
    if (SHOW_IMAGES == True):
        image = pygame.image.load(image_file)
        screen.blit(image, (0, 0))
        pygame.display.flip()

if (RENDER_VIDEO == True):
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile("final_video.mp4", fps=24)