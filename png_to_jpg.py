import os
from PIL import Image
import subprocess

in_dir = "output"
out_dir = "out2"

def main1():
    for filename in os.listdir(in_dir):
        f = os.path.join(in_dir, filename)
        if os.path.isfile(f):
            nom = f.split("/")[-1].split(".")[0]
            print("\033[31m", f, "\033[0m In production with command ", ['ffmpeg', '-i', f, 'out2'+nom+'.jpg'])
            # i = Image.open(f)
            # print('out2/'+nom+'.jpg')
            # i.save('out2/'+nom+'.webp')#, optimize=True, quality=20)
            out = subprocess.Popen(['convert', f, 'out2/'+nom+'.heic'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout,stderr = out.communicate()
            print(stdout)
            print(f, "end")


if __name__ == "__main__":
    main1()

