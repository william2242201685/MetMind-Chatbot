# MetMind-Chatbot
Opening MetMind on google colab

1: Open https://colab.research.google.com/
3: Click on file
2: Click on open notebook
4: Click on upload
5: Upload the "metmind.ipynb" file

Uploading The Files
1: Click on the folder icon on the left side of the screen
2: Ignore the two generated folders



 

Uploading intents.json
1: Drag your downloaded intents.json under these generated folders[Into the empty space]
 



Uploading index.html

1: Right click in the empty space illustrated above and click new folder
2: Rename the folder to "templates"
3: Drag the index.html file into the newly created "templates" folder

Uploading pop.mp3 & styles.css
1: Once again, Right click in the empty space illustrated above and click new folder
2: Rename the folder to "static"

3: Drag the pop.mp3 file into the newly created "static" folder
4: Right click the newly created "static" folder and click new folder
5: Rename the folder to "css"
6: Drag the styles.css file into the newly created "css" folder


Uploading The Files: Confirmation

Your file storage should now look similar to this example
 

 
Running the code

1: Press "Runtime" on the top of the screen
2: Press run all
3: The code may time some time to compile. Please do not interrupt or close the program
4: Once the code is fully compiled then you will see this at the bottom of the screen[Scroll to the bottom]. You will need to click on the second link

 

Note 1 [resetting tensorflow graph error] 
If you are experiencing an error regarding resetting tensorflow graph then all you will need to do in order to fix this issue is:


Step 1: Press runtime [Located on the taskbar located at the top of the screen]
Step 2: Press restart and run all


Note 2 [Slow run/compile speed]
Some have informed me that they are experiencing issues regarding the run/compile speed of the code on google colab.


If you are experiencing any of these issues then you can easily combat against this by ensuring that you are running google colab via colabs GPU hardware accelerator:


Step 1: Press edit on the taskbar located near the top of the screen


 



Step 2: Press Notebook settings
Step 3: Click on the Hardware Accellerator Dropdown list and select GPU
Step 4: Press Save
 
NOTE 3: DO NOT CLOSE THE GOOGLE COLAB TAB WHILST THE CHATBOT IS RUNNING! THIS IS NEEDED FOR THE CHATBOTS FUNCTIONALITY


NOTE 4: Considering what browser you are using. Some web redirection functionalities may be blocked as a popup. Therefore, if you notice that a website should have opened [Indicated by the keyword "Redirect/Redirected" at the start of the message] then please click on the google colab tab and click on the pop-up blocked icon seen on the top left[As for google chrome] as to enable such pop ups in the future
