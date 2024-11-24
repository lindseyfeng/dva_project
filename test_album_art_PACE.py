# generate_album_art.py

# Import necessary libraries
import os
import nltk
from transformers import pipeline
from better_profanity import profanity
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image


def install_nltk_data():
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)


def read_lyrics(file_path):
    """
    Reads lyrics from a text file.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lyrics = file.read()
        return lyrics
    else:
        print(f"File '{file_path}' not found.")
        return None


def summarize_text(text, device):
    """
    Summarizes the text using a transformer model.
    """
    summarizer = pipeline(
        "summarization", model="facebook/bart-large-cnn", device=device
    )
    input_length = len(text.split())
    if input_length < 50:
        max_len = min(50, int(input_length * 0.9))
        min_len = min(10, int(input_length * 0.5))
    else:
        max_len = min(130, int(input_length * 0.8))
        min_len = min(30, int(input_length * 0.5))

    # Summarize the text
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)[
        0
    ]["summary_text"]
    return summary


def clean_text(text):
    """
    Removes explicit language from the text.
    """
    profanity.load_censor_words()
    clean_text = profanity.censor(text)
    return clean_text


def generate_image(prompt, output_file="album_art.png"):
    """
    Generates an image based on the prompt using Stable Diffusion.
    """
    model_id = "runwayml/stable-diffusion-v1-5"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )
    pipe = pipe.to(device)
    if device == "cuda":
        with torch.autocast(device):
            image = pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]
    else:
        print("NOT CUDA")
        exit(0)

    # Save the image
    image.save(output_file)
    print(f"Album art saved as '{output_file}'")


def main():
    install_nltk_data()
    ################################################
    #
    #
    # 
    #
    #
    # Enter lyrics or prompt here to generate album art
    #
    #
    #
    #
    ################################################
    lyrics = "Can you hear the drums Fernando? \
                I remember long ago another starry night like this \
                In the firelight Fernando \
                You were humming to yourself and softly strumming your guitar \
                I could hear the distant drums \
                And sounds of bugle calls were coming from afar \
                They were closer now Fernando \
                Every hour every minute seemed to last eternally \
                I was so afraid Fernando \
                We were young and full of life and none of us prepared to die \
                And Im not ashamed to say \
                The roar of guns and cannons almost made me cry \
                There was something in the air that night \
                The stars were bright, Fernando \
                They were shining there for you and me \
                For liberty, Fernando \
                Though I never thought that we could lose \
                There's no regret \
                If I had to do the same again \
                I would, my friend, Fernando \
                If I had to do the same again \
                I would, my friend, Fernando" 

    print(f"Lyrics:\n{lyrics}\n")

    device = 0 if torch.cuda.is_available() else -1

    print("Summarizing lyrics...")
    summary = summarize_text(lyrics, device)
    print(f"\nSummary:\n{summary}\n")

    clean_summary = clean_text(summary)
    print(f"Clean Summary:\n{clean_summary}\n")

    image_prompt = f"An album cover art illustrating: {clean_summary}. Digital art."
    print(f"Image Prompt:\n{image_prompt}\n")

    print("Generating album art...")
    generate_image(image_prompt)


if __name__ == "__main__":#
    main()
