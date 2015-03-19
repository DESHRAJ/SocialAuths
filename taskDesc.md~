For people who want to work on creating web-pages , building the API etc, the task would be along the following lines:

We have a train - a - class page on cloudcv.org that takes training images for new categories like "coke cans, cakes , pastries" whatever , and train a classifier which modifies the default caffe model (that consist of just the 1000 imagenet categories) to add these new categories to this default model. This new model can then be used to classify a new test image.
Now this was all background,

The task is 
When the user visits the site, you should create a unique job for this user, for that visit. The task will require multiple requests to the server and you should have a way of figuring out which requests belong to which user. 
The fist part is giving training images for each category.
1. The user will type a category name  and you should query google images/ flicker/ imgur etc with this name and pick top 20 images from the search result.
2. Send these images to the server and store these images in the following format: 

/jobid/train / category_name / images. 
/jobid/test/
/jobid/util/

So if a user search for "Cats" and "Dogs" , you will have something like 
 /jobid/train/cats/ image1.jpg etc
 /jobid/train/dogs/ image1.jpg etc
/jobid/test/
/jobid/util/

Please note that you should create a test folder and util folder automatically. 

Then you should allow user to upload test images. To make things not difficult, you can accept a public dropbox url and download these images on the server and save it inside the test folder. 

Then the user can press "train a class" button to train a model. 
Then the user can press "test a model" button to test a model.

Once the user presses test a model, it should show each test image and its corresponding classification result. 

For doing all this, you will need to install "Caffe" on your system. 

We will be providing you with the relavant python code to train and test a classifier. 

Good luck. I am hoping to see some amazing work related to this.  

Let me know if you face issues and people at the gitter room are turning out to be very helpful. :)

Thanks
Harsh
