import cv2 


def localMeanStd(image, winSize):
    # winSize: a tuple (width, height) which is size of small windows
    #
    # This function calculates the local mean of an image by
    # spliting it into blocks, then calculating the local mean
    # of each blocks's vertex. Finally, using bilinear interpolation
    # (for decreasing the computational time)
    # to get the remaining pixels's value.
    lmimage = image.copy().astype('float64')  # local mean image
    lsdimage = image.copy().astype('float64')  # local standard deviation image
    row, col = lmimage.shape
    winWidth, winHeight = winSize
    hfw = (winWidth - 1) / 2  # half size of window's width
    hfh = (winHeight - 1) / 2  # half size of window's height

    # calculate local mean for each vertex of all windows
    for j in range(0, col, winWidth):
        left = j
        right = j + winWidth - 1

        for i in range(0, row, winHeight):
            top = i
            bottom = i + winHeight - 1

            # calculate the mean and standard deviation of vertices
            # top-left
            lmimage[top, left], lsdimage[top, left] = cv2.meanStdDev(
                image[(top - hfh):(top + hfh), (left - hfw):(left + hfw)])
            # top-right
            lmimage[top, right], lsdimage[top, right] = cv2.meanStdDev(
                image[(top - hfh):(top + hfh), (right - hfw):(right + hfw)])
            # bottom-left
            lmimage[bottom, left], lsdimage[bottom, left] = cv2.meanStdDev(
                image[(bottom - hfh):(bottom + hfh), (left - hfw):(left + hfw)])
            # bottom-right
            lmimage[bottom, right], lsdimage[bottom, right] = cv2.meanStdDev(
                image[(bottom - hfh):(bottom + hfh), (right - hfw):(right + hfw)])

    # using bilinear interpolation for remaining pixels
    for j in range(0, col, winWidth):
        left = j
        right = j + winWidth - 1
        for i in range(0, row, winHeight):
            top = i
            bottom = i + winHeight - 1

            meanA, sdA = lmimage[top, left], lsdimage[top, left]
            meanB, sdB = lmimage[top, right], lsdimage[top, right]
            meanC, sdC = lmimage[bottom, left], lsdimage[bottom, left]
            meanD, sdD = lmimage[bottom, right], lsdimage[bottom, right]

            for px in range(j, j + winWidth):
                cx = (px - j) / (winWidth * 1.0)
                for py in range(i, i + winHeight):
                    cy = (py - i) / (winHeight * 1.0)
                    lmimage[py, px] = (
                        1 - cy) * ((1 - cx) * meanA + cx * meanB) + cy * ((1 - cx) * meanC + cx * meanD)
                    lsdimage[py, px] = (
                        1 - cy) * ((1 - cx) * sdA + cx * sdB) + cy * ((1 - cx) * sdC + cx * sdD)

    return lmimage, lsdimage

