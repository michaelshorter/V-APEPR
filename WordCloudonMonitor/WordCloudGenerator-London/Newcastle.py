from wordcloud import WordCloud
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import requests

dirname = os.path.dirname(__file__)
content_path = os.path.join(dirname, 'AzureSpeechCC/content.txt')
wordcloud_image_name = 'wordcloud-newcastle.png'
partner_wordcloud_image_name = 'wordcloud-london.png'
partner_wordcloud_image_path = os.path.join(dirname, partner_wordcloud_image_name)
wordcloud_image_path = os.path.join(dirname, wordcloud_image_name)
upload_url = 'https://connected-display.herokuapp.com/upload'
image_request_url = 'https://connected-display.herokuapp.com/uploads'
generation_interval = 120
dither_image_what_path = os.path.join(dirname, 'dither-image-what.py')

#change the value in return to set the single color need, in hsl format.
def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return "black" 

def generate_wordcloud_from_file(file_path):
    print("Reading " + file_path + "...")
    # read text from file and store in a variable
    with open(file_path, 'r') as file:
        data = file.read()

    print("Generating wordcloud...")
    # create wordcloud using data
    wordcloud = WordCloud(
        background_color="white", height=300, width=400,
        include_numbers = True, min_word_length=5, # minimum length of word
        max_words = 15, margin = 4 # margin between words
    ).generate(data)

    default_colors = wordcloud.to_array()

    plt.imshow(wordcloud.recolor(color_func=grey_color_func), interpolation="bilinear")

    plt.axis("off")
    plt.savefig(wordcloud_image_path)
    #plt.savefig('/home/pi/latestWordCloud.png')
    #plt.show()

    # 

def main():
    while True:
        try:
            # Generate wordcloud from content file
            generate_wordcloud_from_file(content_path)

            image = open(wordcloud_image_path, "rb")
            # Upload wordcloud image to server
            post_response = requests.post(upload_url, files = {"image": (wordcloud_image_name, image, 'image/png')})

            if post_response.ok:
                print("Upload successful")
                print(post_response.status_code)
                print(post_response.text)
            else:
                print("Error uploading image")
                print(post_response.status_code)

            # Get list of images from server and check if partner wordcloud is on there.
            get_response = requests.get(image_request_url)
            images_on_server = get_response.json()
            print(images_on_server)
            # Check if my partner's image is on the server
            if partner_wordcloud_image_name in images_on_server:
                print("Partner image found on server")
                # Download image
                partner_image = requests.get(image_request_url + "/" + partner_wordcloud_image_name).content
                with open(partner_wordcloud_image_path, 'wb') as handler:
                    handler.write(partner_image)
                print("Writing image to e-ink display...")
                os.system("python3 " + dither_image_what_path + " --colour 'red' --image '" + partner_wordcloud_image_path + "'")
            else:
                print("Partner image not found on server")

            # Write image to e-ink display
            #print("Writing image to e-ink display...")
            #os.system("python3 " + dither_image_what_path + " --colour 'red' --image '" + wordcloud_image_path + "'")

        except ValueError as e:
            print("Warning: Not enough words to generate wordcloud from!")
        # Sleep
        print("Sleeping...")
        time.sleep(generation_interval)

if __name__ == "__main__":
    main()
