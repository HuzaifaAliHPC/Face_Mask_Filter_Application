# Import required modules
import cv2
import numpy as np
import sys

# Take selfie
## Start camera
cam = cv2.VideoCapture(0)
if not (cam.isOpened()):
    print("Unable to start camera... Exitting...")
    sys.exit()

## Capture frame
while 1:
    ret, frame = cam.read()
    if ret == False:
        print("Unable to read frame from camera...")
        sys.exit()
    ## Display the selfie
    cv2.imshow("Frame",frame)
    ## Press c to capture selfie
    if cv2.waitKey(20) == ord('c'):
        break

cam.release()

# Read mask image
#The cv2.IMREAD_UNCHANGED flag is used to read the image as is, without any conversions. 
mask = cv2.imread("mask.png",cv2.IMREAD_UNCHANGED) 
## Resize mask
mask = cv2.resize(mask, None, fx=0.2, fy=0.2)
## Obtain alpha channel of mask
alpha = mask[:,:,3]
## Convert alpha to 3-channel
alpha = cv2.cvtColor(alpha,cv2.COLOR_GRAY2BGR)
## Convert mask to 3-channel
mask = mask[:,:,:3]

cv2.destroyAllWindows()

# Mouse callback function
def mouseCallbackFunction(event, x, y, flags, param):
    global frame
    # Reset image
    frame = frameCopy.copy()
    # Apply mask on image
    frame = applyMask(frame,x,y)
    # Display mask on image
    cv2.imshow("Image with mask",frame)

# Apply mask
def applyMask(frame,x,y):
    # Width and height of mask
    height, width, _ = mask.shape
    # Select the affected region in image
    region = frame[y-height//2:y+height//2+1, x-width//2:x+width//2]
    # Convert region to float datatype
    region = region.astype('float')
    # Apply mask to the affected region
    try:
        region = cv2.add(cv2.multiply(alpha,mask),
                cv2.multiply(1-alpha,region))
    except:
        pass
    # Convert region back to uint8
    region = region.astype(np.uint8)
    # Replace region in image
    frame[y-height//2:y+height//2+1, x-width//2:x+width//2] = region
    return frame

cv2.namedWindow("Image with mask")

# Create a copy of frame
frameCopy = frame.copy()
# Convert alpha and mask to float
alpha = alpha.astype('float')
mask = mask.astype('float')
# Scale down alpha to 0 to 1 range
alpha = alpha/255.0

cv2.setMouseCallback("Image with mask",mouseCallbackFunction)
cv2.imshow("Image with mask",frame)

k = cv2.waitKey(0)

if k == ord('s'):
    cv2.imwrite("Image_with_maks.png",frame)

cv2.destroyAllWindows()
