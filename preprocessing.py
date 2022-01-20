import cv2
import math
import numpy as np

def resize_image(res,img_path,img_name):
    """Resize images over 2500 px in both sides.
    
    Args:
        img_path: Path to drug image.
        img_name: Image file name.

    Returns:
        r_img: Resized image.
    """
    # Read image file
    img = cv2.imread('{}\{}'.format(img_path,img_name))

    # Resize image if both sides greater than selected resolution
    if (img.shape[1] > res) and (img.shape[0] > res):
        if img.shape[1] > img.shape[0]:
            diff = int(img.shape[1]/res)
        else:
            diff = int(img.shape[0]/res)

        dim = (int(img.shape[1]/diff), int(img.shape[0]/diff))
        print('Image dimensions: ', dim)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    return(img)

def get_contours(img):
    """Get array of contours around drug pack.
    
    Args:
        img: Drug original or resized image.

    Returns:
        contours: Image contour arrays.
    """
    # Convert color to gray
    # cvt_color = cv2.cvtColor(img,cv2.COLOR_BGR2Lab)

    # Get edges
    # edged = cv2.Canny(cvt_color, 10, 550,L2gradient=True)
    edged = cv2.Canny(img, 10, 550,L2gradient=True)

    # Find and draw external countors
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

    return(contours)

def draw_rectangle(img,contours):
    """Get array of rectangle around drug pack.
    
    Args:
        contours: Drug contour array.

    Returns:
        points: rectangle contour array.
    """
    # Get longest contour
    max_contour = max(contours, key=len)

    # Get minimum rectangle area and get its points
    rect = cv2.minAreaRect(max_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    points = box.tolist()
    # cv2.drawContours(img,[box],0,(0,255,0),2)

    return(points)
    
def warp(img,points):
    """Warp current drug image.
    
    Args:
        img: Current drug image.
        points: Rectangle contour points.

    Returns:
        warp_image: final warped image.
    """
    # Getting hypotenuse for each rectangle size to provide new image dims
    x = int(math.sqrt(((abs(points[0][0]-points[1][0])**2))+((abs(points[0][1]-points[1][1])**2))))
    y = int(math.sqrt(((abs(points[1][0]-points[2][0])**2))+((abs(points[1][1]-points[2][1])**2))))

    pts1 = np.float32([points[2], points[3], points[1], points[0]])
    pts2 = np.float32([[0, 0], [x, 0], [0, y], [x, y]])
      
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    wrap_img = cv2.warpPerspective(img, matrix, (x, y))

    return (wrap_img)

