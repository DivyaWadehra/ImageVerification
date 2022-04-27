In this project, we will detect tampering of pan card using computer vision. 
This will help the different organizations in detecting whether the id of the pan card is original or not

STEPS:
1. Get images from user
2. Check for size and format of the image
3. Change shape and size of image according to the original image
4. convert the image to grayscale
5. find the similarity index of the images
6. finding the threshold of the image
7. find contour and grab those using imutils
8. Draw a bounding rectangle using these contour
9. plot difference, threshold, original and tampered image
10. compare all the images and check the similarity score to decide tampering