import os  
from PIL import Image  
  
# Get the Image Size  
def get_size_format(b, factor=1024, suffix="B"):  
    """ 
    Scale bytes to its proper byte format 
    e.g: 
        1253656 => '1.20MB' 
        1253656678 => '1.17GB' 
    """  
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:  
        if b < factor:  
            return f"{b:.2f}{unit}{suffix}"  
        b /= factor  
    return f"{b:.2f}Y{suffix}"  
  
# Untuk mengompres gambar yang diberikan 
def compress_given_img(image_name, new_size_ratio=0.9, quality=90, image_width=None, height_width=None, to_jpg=True):  
    # memuat gambar yang diunggah ke memori 
    img = Image.open(image_name)  
    # mencetak bentuk gambar asli 
    print("[*] Image size:", img.size)  
    # mendapatkan ukuran gambar asli dalam byte 
    image_size = os.path.getsize(image_name)  
    # mencetak ukuran sebelum kompresi/pengubahan ukuran  
    print("[*] Size before compression:", get_size_format(image_size))  
    if new_size_ratio < 1.0:  
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)  
        # print bentuk gambar baru  
        print("New image shape:", img.size)  
    elif image_width and height_width:  
        # jika image_width dan height_width disetel, ubah ukurannya  
        img = img.resize((image_width, height_width), Image.ANTIALIAS)  
        # print bentuk gambar baru 
        print("New image shape:", img.size)  
    # pisahkan nama file dan ekstensi 
    filename, ext = os.path.splitext(image_name)  
    # buat nama file baru dengan menambahkan _compressed ke nama file asli  
    if to_jpg:  
        # ubah ekstensi ke JPEG  
        new_filename = f"{filename}_compressed.jpg"  
    else:  
        # mempertahankan ekstensi yang sama dari gambar aslinya  
        new_filename = f"{filename}_compressed{ext}"  
    try:  
        # simpan gambar dengan kualitas yang sesuai dan optimalkan setel ke True  
        img.save(new_filename, quality=quality, optimize=True)  
    except OSError:  
        # konversikan gambar ke mode RGB terlebih dahulu  
        img = img.convert("RGB")  
        # simpan gambar dengan kualitas yang sesuai dan optimalkan setel ke True  
        img.save(new_filename, quality=quality, optimize=True)  
    print(" New file saved:", new_filename)  
    # dapatkan ukuran gambar baru dalam byte 
    new_image_size = os.path.getsize(new_filename)  
    # cetak ukuran baru dalam format yang baik
    print("Size after compression:", get_size_format(new_image_size))  
    # menghitung byte penghematan  
    saving_diff = new_image_size - image_size  
    # cetak persentase tabungan  
    print(f" Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")  
  
if __name__ == "__main__":  
    import argparse  
    parser = argparse.ArgumentParser(description="Python script to compress and resize image")  
    parser.add_argument("image", help="Given image to compress and/or resize")  
    parser.add_argument("-j", "--to-jpg", action="store_true", help="Converting image to JPEG")  
    parser.add_argument("-q", "--quality", type=int, help="Quality start from 0 (worst) to max 95 (best). The standard is 90", default=90)  
    parser.add_argument("-r", "--resize-ratio", type=float, help="Changing ratio from 0 to 1, setting 0,5 will multiply the image width and height by 0,5. The standard is 1.0", default=1.0)  
    parser.add_argument("-w", "--width", type=int, help="new image width, make sure to set it with parameter `height`")  
    parser.add_argument("-hh", "--height", type=int, help="new height for image, make sure to set it with parameter `width`")  
    args = parser.parse_args()  
    # print the passed arguments  
    print("="*50)  
    print("Image:", args.image)  
    print("To JPEG:", args.to_jpg)  
    print("Quality:", args.quality)  
    print("Resizing ratio:", args.resize_ratio)  
    if args.width and args.height:  
        print("Width:", args.width)  
        print("Height:", args.height)  
    print("="*50)  
    # compress the image  
    compress_given_img(args.image, args.resize_ratio, args.quality, args.width, args.height, args.to_jpg)