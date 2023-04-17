from PIL import Image, ImageEnhance
import os


def split_string(string, max_chars_per_line):
    words = string.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) > max_chars_per_line:
            lines.append(current_line.strip())
            current_line = ""
        current_line += " " + word
    if current_line:
        lines.append(current_line.strip())

    # Re-combine lines to achieve even distribution of words
    num_lines = len(lines)
    if num_lines > 1:
        total_words = len(words)
        ideal_words_per_line = (total_words + num_lines - 1) // num_lines
        excess_words = total_words - ideal_words_per_line * (num_lines - 1)

        even_lines = []
        i = 0
        while i < num_lines - 1:
            line_words = words[:ideal_words_per_line]
            if excess_words > 0:
                line_words.append(words[ideal_words_per_line])
                excess_words -= 1
                words.pop(ideal_words_per_line)
            even_lines.append(" ".join(line_words))
            words = words[ideal_words_per_line:]
            i += 1
        even_lines.append(" ".join(words))
        return "\n".join(even_lines)
    else:
        return lines[0]



def darken_images(images_folder, output_folder):
    # Set desired darkness
    dark = 0.5

    # Loop through all the images in the directory
    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Open the image
            filepath = os.path.join(images_folder, filename)
            img = Image.open(filepath)

            # Create an enhancer object for the image
            enhancer = ImageEnhance.Brightness(img)

            # Reduce the brightness by a factor of 'dark'
            dark_img = enhancer.enhance(dark)

            # Save the cropped image
            dark_img.save(f"{output_folder}/{filename}")


def cut_images(images_folder, output_folder):
    # Set the target size
    target_size = (1080, 1350)

    # Loop through all the images in the directory
    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Open the image
            filepath = os.path.join(images_folder, filename)
            img = Image.open(filepath)

            # Get the size of the image
            width, height = img.size

            # Calculate the coordinates for cropping
            left = (width - target_size[0]) // 2
            top = (height - target_size[1]) // 2
            right = left + target_size[0]
            bottom = top + target_size[1]

            # Crop the image
            img = img.crop((left, top, right, bottom))

            # Save the cropped image
            img.save(f"{output_folder}/{filename}")


def create_new_topic_dirs(topic, project_dir):
    # /customers/___
    if not os.path.exists(f"{project_dir}/customers/{topic}"):
        os.makedirs(f"{project_dir}/customers/{topic}")
    # /sources/images/___
    if not os.path.exists(f"{project_dir}/sources/images/{topic}"):
        os.makedirs(f"{project_dir}/sources/images/{topic}")