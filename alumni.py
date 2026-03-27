import os
import time
import urllib.request
import ssl
import random

def download_alumni_images():
    output_dir = 'alumni'
    
    # Create the alumni folder if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # SSL context to prevent certificate issues
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print("Starting download of 24 alumni images from thispersondoesnotexist.com...")

    for i in range(1, 25):
        filename = os.path.join(output_dir, f"alum{i}.jpg")
        
        # Adding a random query parameter to ensure we don't get a cached image from proxies/CDNs
        url = f"https://thispersondoesnotexist.com/?q={random.randint(1, 1000000)}"
        
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/jpeg'
            }
        )

        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                with open(filename, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"[{i}/24] Successfully saved -> {filename}")
        except Exception as e:
            print(f"[{i}/24] Failed to download: {e}")
            
        # Add a sleep interval so we don't overwhelm the server and get rate-limited
        time.sleep(1.5)

    print("Download complete!")

if __name__ == "__main__":
    download_alumni_images()
