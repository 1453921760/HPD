import cv2

def show_img(url):
    img=cv2.imread(url)
    cv2.imshow("gg",img)
    cv2.waitKey(0)
    cv2.destroyWindow()

