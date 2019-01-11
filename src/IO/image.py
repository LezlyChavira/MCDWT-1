import cv2
import numpy as np
import os

class InputFileException(Exception):
    pass

def read(file_name):
    '''Read a 3-components image from disk. Each component stores
       integers between [0, 65535].

    Parameters
    ----------

        image : str.

            Path to the image in the file system, without extension.

    Returns
    -------

        [:,:,:].

            A color image, where each component is in the range [-32768, 32767].

    '''
    image = cv2.imread(file_name, -1)
    if image is None:
        raise InputFileException('{} not found'.format(file_name))
    else:
        if __debug__:
            print("image.py: read {}".format(file_name))
    buf = image.astype(np.float32)
    buf -= 32768.0
    #assert (np.amax(buf) < 65536), 'range overflow'
    #assert (np.amin(buf) >= 0), 'range underflow'
    return buf.astype(np.int16)

def write(image, file_name, bpc):
    '''Write a 3-components image to disk. Each component stores integers
       between [0, 65536].

    Parameters
    ----------

        image : [:,:,:].

            The color image to write, where each component is in the range [-32768, 32768].

        file_name : str.

            Path to the image in the file system, without extension.

    Returns
    -------

        None.
    '''

    image = image.astype(np.float32)
    image += 32768.0
    image = image.astype(np.uint16)
    #tmp = np.copy(image)
    #tmp += 32768

    #assert (np.amax(tmp) < 65536), '16 bit unsigned int range overflow'
    #assert (np.amin(tmp) >= 0), '16 bit unsigned int range underflow'

    #cv2.imwrite(file_name + "_LL.png", np.rint(tmp).astype(np.uint16))
    #file_name += "_LL.png"
    cv2.imwrite(file_name + ".png", np.rint(image).astype(bpc))
    os.rename(file_name + ".png", file_name)
    if __debug__:
        print("image.py: written {} using {}".format(file_name + ".png", bpc))

def write8(image, file_name):
    np.clip(image, 0, 255)
    write(image, file_name, np.uint8)

def write16(image, file_name):
    write(image, file_name, np.uint16)

if __name__ == "__main__":

    img = read("../../sequences/stockholm/000")
    write(img, "/tmp/000")
    print("generated /tmp/000")
