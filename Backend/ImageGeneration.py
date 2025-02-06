import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
import matplotlib.pyplot as plt

# Function to open generated images
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            continue

        try:
            img = Image.open(image_path)
            print(f"Opening Image: {image_path}")
            plt.imshow(img)
            plt.axis('off')  # Hide axes
            plt.show()
            sleep(1)
        except Exception as e:
            print(f"Error opening {image_path}: {e}")

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Function to query the Hugging Face API asynchronously
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return None

# Function to generate images
async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    
    # Gather all generated image bytes
    image_bytes_list = await asyncio.gather(*tasks)

    # Save images to the "Data" directory
    os.makedirs("Data", exist_ok=True)
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = os.path.join("Data", f"{prompt.replace(' ', '_')}{i + 1}.jpg")
            print(f"Saving image to: {file_path}")  # Debug statement
            with open(file_path, "wb") as f:
                f.write(image_bytes)

    print("Image generation completed.")

# Function to monitor the ImageGeneration.data file
def monitor_image_generation():
    while True:
        try:
            with open(r"Frontend/Files/ImageGeneration.data", "r") as f:
                data = f.read()
            print(f"Read from ImageGeneration.data: {data}")  # Debug statement

            prompt, status = data.split(",")
            
            if status == "True":
                print("Generating Images...")
                asyncio.run(generate_images(prompt=prompt))
                open_images(prompt)

                # Reset the ImageGeneration.data file
                with open(r"Frontend/Files/ImageGeneration.data", "w") as f:
                    f.write("False,False")
                break
            else:
                sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            sleep(1)

if __name__ == "__main__":
    monitor_image_generation()