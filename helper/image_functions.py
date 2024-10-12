from PIL import Image, ImageColor

def generate_pixel_art(input_image_path, output_image_path, output_size=(32, 64), upscale_factor=10, bgcolor='black'):
    # Open the input image and convert to RGB
    input_image = Image.open(input_image_path).convert('RGB')
    input_width, input_height = input_image.size

    # Desired output dimensions
    output_width, output_height = output_size

    # Calculate aspect ratios
    input_aspect = input_width / input_height
    output_aspect = output_width / output_height

    # Determine the scaling factors and padding
    if input_aspect < output_aspect:
        # Image is wider than output aspect ratio
        scale = output_height / input_height
        scaled_width = int(input_width * scale)
        scaled_height = output_height
        pad_left = (output_width - scaled_width) // 2
        pad_top = 0
    else:
        # Image is taller than output aspect ratio
        scale = output_width / input_width
        scaled_width = output_width
        scaled_height = int(input_height * scale)
        pad_left = 0
        pad_top = (output_height - scaled_height) // 2

    # Create a new image with the desired output size and background color
    if bgcolor.startswith('#'):
        bgcolor = bgcolor.lstrip('#')
        bgcolor = tuple(int(bgcolor[i:i+2], 16) for i in (0, 2, 4))
    else:
        bgcolor = ImageColor.getrgb(bgcolor)

    pixel_art_image = Image.new('RGB', (output_width, output_height), bgcolor)

    for y_out in range(output_height):
        for x_out in range(output_width):
            # Map output pixel to scaled image coordinates
            x_in_scaled = (x_out - pad_left + 0.5) / scale
            y_in_scaled = (y_out - pad_top + 0.5) / scale

            # Map to original image coordinates
            x_in = x_in_scaled
            y_in = y_in_scaled

            if 0 <= x_in < input_width and 0 <= y_in < input_height:
                x_in = int(x_in)
                y_in = int(y_in)
                color = input_image.getpixel((x_in, y_in))
            else:
                # Outside the image bounds, use background color
                color = bgcolor

            pixel_art_image.putpixel((x_out, y_out), color)

    # Save the pixel art image
    pixel_art_image.save(output_image_path)
    print(f"Pixel art image saved as {output_image_path}")

    # Optional: Upscale the pixel art image for better visibility
    upscaled_image = pixel_art_image.resize(
        (output_width * upscale_factor, output_height * upscale_factor),
        Image.NEAREST
    )
    upscaled_output_path = 'upscaled_' + output_image_path
    upscaled_image.save(upscaled_output_path)
    print(f"Upscaled pixel art image saved as {upscaled_output_path}")

# Example usage:
generate_pixel_art('sonic.png', 'output.png', output_size=(64, 32))
