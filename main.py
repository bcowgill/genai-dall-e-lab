#import our libraries
import os
import openai
from PIL import Image,ImageOps,ImageFilter
from io import BytesIO
import requests

URL="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.wallpapersden.com%2Fimage%2Fdownload%2Fforest-house-covered-in-snow-4k_bGdnaGuUmZqaraWkpJRqZmetamZn.jpg&f=1&nofb=1&ipt=9792dce97e24b7f28d8e9013a22b18ad9bd36059d5675ac60f769dbfdfec09ee&ipo=images"
URL2="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.wallpapersden.com%2Fimage%2Fdownload%2Fforest-snow-trail_ZmtpbWWUmZqaraWkpJRqZmetamZn.jpg&f=1&nofb=1&ipt=afd6ac5c167d5ed11c160c36b1585db1508da98fbdf8f656a489ddfefe45b5f9&ipo=images"

# Set API key and prompt
openai.api_key = os.getenv('OPENAI_KEY')

def fileList():
    # Get the current directory
  current_directory = os.getcwd()
  # Get all files in the current directory
  files = os.listdir(current_directory)
  # Print all files (not directories)
  print("The current files in your directory: ")
  for file in files:
      if os.path.isfile(file):
          print(file)

def main():
    while True:
      try:
        print("\n1. Generate an image with DALL-E")
        print("2. Create variations of an image")
        print("3. Resize an image")
        print("4. Add a filter to your image")
        print("5. Show available image files")
        print("0. Exit")
        
        option = input("Choose an option: ")

        if option == "1":
            prompt = input("Enter the prompt for DALL-E: ")
            # Generate the image with DALL-E
            generate_image(prompt)
        elif option == "2":
            image_path = input("Enter the path of the image: ")
            # Open the image file
            create_variations(image_path)
        elif option=="3":
          image_path = input("Enter the path of the image you want resized: ")
          # run resize function
          re_size(image_path)
        elif option=="4":
          image_path = input("Enter the path of the image you want to add a filter to: ")
          # run filter function
          filters(image_path)
        elif option=="5":
          # Show the files available
          fileList()
        elif option == "0":
            print("Exiting the program...")
            break
        else:
            print("Invalid option. Please enter a valid number.")
      except Exception as exc:
        print(f"Error: {exc}")

def generate_image(prompt1):
    # Generate the image with DALL-E
    print(f"Generating an image for the prompt: {prompt1}")
    # Call DALL-E API here
    try:
      response = openai.Image.create(
        prompt=prompt1,
        n=1,
        size="256x256"
      )
      image_url = response['data'][0]['url']
    except Exception as exc:
      #print(f"generate: {exc}")
      image_url = URL
    img_data = requests.get(image_url).content
    with open('image_created.png', 'wb') as handler:
      handler.write(img_data)
    img=Image.open('image_created.png')
    print(f"Your image was generated under the `image_created.png` file name. {img}")
    return img

def create_variations(img):
    # Create variations of an image using PIL
    print("Creating variations of the image...")
    # Call DALL-E API here
    try:
      image_data=open(img, "rb")
      response = openai.Image.create_variation(
        image=image_data,
        n=1,
        size="256x256"
      )
      image_url = response['data'][0]['url']
    except Exception as exc:
      #print(f"ERR2 {exc}")
      image_url = URL2
    img_data = requests.get(image_url).content
    with open('image_var.png', 'wb') as handler:
      handler.write(img_data)
    img=Image.open('image_var.png')
    print(f"Your image was generated under the `image_var.png` file name. {img}")

def re_size(image_path):
## Open an image file
    with Image.open(image_path) as img:
        # Ask the user to choose a dimension
        print("Choose a dimension for resizing the image:")
        print("1. 256x256")
        print("2. 512x512")
        print("3. 1024x1024")
        option = input("Enter your option: ")
        if option == "1":
            target_size = (256, 256)
        elif option == "2":
            target_size = (512, 512)
        elif option == "3":
            target_size = (1024, 1024)
        else:
            print("Invalid option. Using default size 256x256.")
            target_size = (256, 256)

        # Resize the image
        resized_img = img.resize(target_size)

        # Save the resized image
        resized_img.save('resized_image.png')
        print("Your given image was resized and saved under `resized_image.png` ")

def filters(image_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Ask the user to choose a filter
        print("Choose a filter to apply on the image:")
        print("1. Contour")
        print("2. Edge Enhance")
        print("3. Find Edges")
        print("4. Gaussian Blur")
        option = input("Enter your option: ")

        if option == "1":
            filtered_img = img.filter(ImageFilter.CONTOUR)
        elif option == "2":
            filtered_img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif option == "3":
            filtered_img = img.filter(ImageFilter.FIND_EDGES)
        elif option == "4":
            filtered_img = img.filter(ImageFilter.GaussianBlur(radius=5))
        else:
            print("Invalid option. Applying Contour filter by default.")
            filtered_img = img.filter(ImageFilter.CONTOUR)
        
        # Save the filtered image
        filtered_img.save('filtered_image.png')
        print("Filter applied successfully, 'filtered_image.png' created.")


if __name__ == "__main__":
    main()

