import cv2
import numpy as np
import os
if __debug__:
    import time

class InputFileException(Exception):
    pass

def readL(file_name):
    fn = file_name + "_LL"
    LL = cv2.imread(fn, -1)
    if LL is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        assert (np.amin(LL) >= 0), "underflow error"
        assert (np.amax(LL) < 65536), str(np.amax(LL)) + " -> overflow error"
        if __debug__:
            print("pyramid: read {}".format(fn))
    #return LL.astype(np.float64)
    LL = LL.astype(np.float32)
    LL -= 32768.0
    LL = LL.astype(np.int16)
    #return LL.astype(np.uint16)
    return LL

def readH(file_name):
    fn = file_name + "_LH"
    LH = cv2.imread(fn, -1)
#    for y in range(50):
#        for x in range(50):
#            print(LH[y+50,x+50,0], end=' ')

    if LH is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        assert (np.amin(LH) >= 0), "underflow error"
        assert (np.amax(LH) < 65536), "overflow error"
        LH = LH.astype(np.float32)
        LH -= 32768.0
        LH = LH.astype(np.int16)
        if __debug__:
            print("pyramid: read {}".format(fn))

#    for y in range(50):
#        for x in range(50):
#            print(LH[y+50,x+50,0], end='*')

    fn = file_name + "_HL"
    HL = cv2.imread(fn, -1)
    if HL is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        assert (np.amin(HL) >= 0), "underflow error"
        assert (np.amax(HL) < 65536), "overflow error"
        HL = HL.astype(np.float32)
        HL -= 32768.0
        HL = HL.astype(np.int16)
        if __debug__:
            print("pyramid: read {}".format(fn))

    fn = file_name + "_HH"
    HH = cv2.imread(fn, -1)
    if HH is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        assert (np.amin(HH) >= 0), "underflow error"
        assert (np.amax(HH) < 65536), "overflow error"
        HH = HH.astype(np.float32)
        HH -= 32768.0
        HH = HH.astype(np.int16)
        if __debug__:
            print("pyramid: read {}".format(fn))
    return LH.astype(np.float64), HL.astype(np.float64), HH.astype(np.float64)

def read(file_name):
    '''Read a pyramid from disk.

    Parameters
    ----------

        image : str.

            Pyramid in the file system, without extension.

    Returns
    -------

        (L, H) where L = [:,:,:] and H = (LH, HL, HH),
        where LH, HL, HH = [:,:,:].

            A color pyramid.

    '''

    #fn = file_name + "_LL"
    #LL = cv2.imread(fn, -1).astype(np.float64)
    #if LL is None:
    #    raise InputFileException('{} not found'.format(fn))
    #else:
    #    if __debug__:
    #        print("pyramid: read {}".format(fn))
    LL = readL(file_name)
    #LL -= 32768

    LH, HL, HH = readH(file_name)
    return (LL, (LH, HL, HH))

def writeH(H, file_name):
#    for y in range(50):
#        for x in range(50):
#            print(H[0][y+50,x+50,0], end=' ')
    LH = H[0].astype(np.float32)
    LH += 32768.0
    #LH = np.rint(LH).astype(np.uint16)
    LH = LH.astype(np.uint16)
#    for y in range(50):
#        for x in range(50):
#            print(LH[y+50,x+50,0], end=' ')
    assert (np.amax(LH) < 65536), 'range overflow'
    assert (np.amin(LH) >= 0), 'range underflow'
    cv2.imwrite(file_name + "_LH.png", LH)
    os.rename(file_name + "_LH.png", file_name + "_LH")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_LH"))

#    HL = H[1] + 32768.0
#    HL = np.rint(HL).astype(np.uint16)
    HL = H[1].astype(np.float32)
    HL += 32768.0
    HL = HL.astype(np.uint16)
    assert (np.amax(HL) < 65536), 'range overflow'
    assert (np.amin(HL) >= 0), 'range underflow'
    cv2.imwrite(file_name + "_HL.png", HL)
    os.rename(file_name + "_HL.png", file_name + "_HL")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_HL"))

#    HH = H[2] + 32768.0
#    HH = np.rint(HH).astype(np.uint16)
    HH = H[2].astype(np.float32)
    HH += 32768.0
    HH = HH.astype(np.uint16)
    assert (np.amax(HH) < 65536), 'range overflow'
    assert (np.amin(HH) >= 0), 'range underflow'
    cv2.imwrite(file_name + "_HH.png", HH)
    os.rename(file_name + "_HH.png", file_name + "_HH")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_HH"))

def write(pyramid, file_name):
    '''Write a pyramid to disk.

    Parameters
    ----------

        L : [:,:,:].

            A LL subband.

        H : (LH, HL, HH), where LH, HL, HH = [:,:,:].

            H subbands.

        file_name : str.

            Pyramid in the file system.

    Returns
    -------

        None.

    '''

    #file_name = '{}L{:03d}.png'.format(path, number)
    #print(np.min(pyramid[0]))
    #LL = pyramid[0] + 32768
    #LL = pyramid[0]
    #print(np.min(LL))
    #print(np.max(LL))

    #LL = np.rint(pyramid[0]).astype(np.uint16)
    #LL = pyramid[0].astype(np.uint16)
    LL = pyramid[0].astype(np.float32)
    LL += 32768.0
    LL = LL.astype(np.uint16)
    if __debug__:
        cv2.imshow("LL pyramid", LL)
        while cv2.waitKey(1) & 0xFF != ord('q'):
            time.sleep(0.1)
    assert (np.amax(LL) < 65536), 'range overflow'
    assert (np.amin(LL) >= 0), 'range underflow'
    cv2.imwrite(file_name + "_LL.png", LL)
    os.rename(file_name + "_LL.png", file_name + "_LL")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_LL"))
    #y = pyramid[0].shape[0]
    #x = pyramid[0].shape[1]
    #buf = np.full((y*2, x*2, 3), 32768, np.uint16)
    #buf[0:y,x:x*2,:] = np.round(pyramid[1][0] + 128)
    #buf[y:y*2,0:x,:] = np.round(pyramid[1][1] + 128)
    #buf[y:y*2,x:x*2,:] = np.round(pyramid[1][2] + 128)
    #LH = pyramid[1][0] + 32768

    writeH(pyramid[1], file_name)
    #LH = pyramid[1][0]

    #assert (np.amax(LH) < 65536), 'range overflow'
    #assert (np.amin(LH) >= 0), 'range underflow'

    #LH = np.rint(LH).astype(np.uint16)
    #LH = np.rint(LH).astype(np.int16)
    #cv2.imwrite(file_name + "_LH.png", LH)
    #os.rename(file_name + "_LH.png", file_name + "_LH")
    #if __debug__:
    #    print("pyramid: written {}".format(file_name + "_LH"))

    #buf[0:y,x:x*2,:] = np.rint(LH).astype('uint16')

    #HL = pyramid[1][1] + 32768
    #HL = pyramid[1][1]
    
    #assert (np.amax(HL) < 65536), 'range overflow'
    #assert (np.amin(HL) >= 0), 'range underflow'

    #HL = np.rint(HL).astype(np.uint16)
    #HL = np.rint(HL).astype(np.int16)
    #cv2.imwrite(file_name + "_HL.png", HL)
    #os.rename(file_name + "_HL.png", file_name + "_HL")
    #if __debug__:
    #    print("pyramid: written {}".format(file_name + "_HL"))

    #buf[y:y*2,0:x,:]= np.rint(HL).astype('uint16')

    #HH = pyramid[1][2] + 32768
    #HH = pyramid[1][2]

    #assert (np.amax(HH) < 65536), 'range overflow'
    #assert (np.amin(HH) >= 0), 'range underflow'

    #HH = np.rint(HH).astype(np.uint16)
    #HH = np.rint(HH).astype(np.int16)
    #cv2.imwrite(file_name + "_HH.png", HH)
    #os.rename(file_name + "_HH.png", file_name + "_HH")
    #if __debug__:
    #    print("pyramid: written {}".format(file_name + "_HH"))

    #buf[y:y*2,x:x*2,:] = np.rint(HH).astype('uint16')
    #file_name = '{}H{:03d}.png'.format(path, number)

    #cv2.imwrite(file_name, buf)

if __name__ == "__main__":

    import os
    os.system("cp ../../sequences/stockholm/000 /tmp/_LL")
    os.system("cp ../../sequences/stockholm/001 /tmp/_LH")
    os.system("cp ../../sequences/stockholm/002 /tmp/_HL")
    os.system("cp ../../sequences/stockholm/004 /tmp/_HH")
    pyr = read("/tmp/")
    write(pyr, "/tmp/out")
    print("generated pyramid /tmp/out")
