import os
from PIL import Image
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
pattern = re.compile(r".*-nc\.(jpg|JPG|jpeg|JPEG|png|PNG|gif|GIF)$")


def fileList(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filter(lambda name: pattern.match(name), filenames):
            matches.append(os.path.join(root, filename))
    return matches


def getNewSize(img):
    (w, h) = img.size
    (nw, nh) = img.size
    if w > 1000:
        nw = 1000
        nh = int((1.0 * h / w) * nw)
    elif h > 1200:
        nh = 1200
        nw = int((1.0 * w / h) * nh)
    return (nw, nh)


def compressResizeImages(val):
    bytesSaved = 0
    files = fileList(inFolder)
    print(f"[COMPRESSOR] I found {len(files)} files to compress in total!")
    cur = 0
    for file in files:
        cur = 1
        print(
            f"[INFO] {str(cur).zfill(len(str(len(files))))}/{len(files)} Compressing image {os.path.basename(file)}"
        )
        imgFile = os.path.join(
            inFolder, file[file.find(inFolder):]
        )  # input image file path
        outImg = os.path.join(
            outFolder, file[file.find(inFolder):].replace("-nc", "")
        )  # output image file path
        oSize = os.path.getsize(imgFile)  # size of the original image
        inImg = Image.open(imgFile)
        size = getNewSize(inImg)
        inImg.thumbnail(size, Image.ANTIALIAS)  # resize the image
        inImg.save(outImg, "JPEG", quality=val)
        nSize = os.path.getsize(outImg)  # size of the new image
        bytesSaved = bytesSaved(oSize - nSize)
        print(
            f"[OK] {str(cur).zfill(len(str(len(files))))}/{len(files)} Image compressed!"
        )
    return bytesSaved


def main():
    quality = 100
    print(f"[COMPRESSOR] Quality of compression is {quality}%.")
    bytesSaved = compressResizeImages(quality)
    if not bytesSaved:
        bytesSaved = 0
    print(
        f"\n[SUCCESS] Compressing finished!\n[SUCCESS] Total MB saved - {round(bytesSaved/1024/1024, 2)}"
    )


inFolder = str(BASE_DIR / "static/img")
outFolder = str(BASE_DIR / "static/img-compressed")


if __name__ == "__main__":
    main()
