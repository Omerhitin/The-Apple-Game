import cv2
import numpy as np
import copy
import pygame
import random
import sys

class player:
    def __init__(self, name,score):
        self.score=score
        self.name=name

    
"""Image processing and filtering function, and display related functions:"""

def top_bar(back):
    cv2.putText(back, str(parameters['points']+parameters['round']),(10,apple_length+5),cv2.FONT_HERSHEY_SIMPLEX,
                1.2,(0,0,240),2,cv2.LINE_AA) #Writing the score
    cv2.putText(back, str(parameters['losses']),(210,apple_length+5),cv2.FONT_HERSHEY_SIMPLEX,
                1.2,(0,0,240),2,cv2.LINE_AA) #Writing the losses
    #Pasting the red apple and the rotten apple
    back=paste_apple(apple_BW,apple_color,back,(90,5))           
    frames['screen']=paste_apple(apple_rot_BW,apple_color_rot,back,(250,5))           

def get_apple (file_name):
    apple_color=cv2.imread(file_name,1)
    apple_BW=cv2.imread(file_name,0)
    _,thresh= cv2.threshold(apple_BW,253,255,cv2.THRESH_TOZERO) # Threshing the image
    kernel_grad=np.ones((4,4),np.uint8)
    gradient=cv2.morphologyEx(thresh,cv2.MORPH_GRADIENT,kernel_grad) #Getting only the noise around the shape
    apple_BW=cv2.bitwise_or(thresh,gradient) #Cleaning the noise
    return apple_color,cv2.bitwise_not(apple_BW)

def paste_apple (img_BW,img_color,background,coordinate):
    img_BW=cv2.resize(img_BW,(apple_length,apple_length))
    img_color=cv2.resize(img_color,(apple_length,apple_length))
    img_color=cv2.bitwise_and(img_color,img_color,mask=img_BW) #Cropping the apple
    (x,y)=coordinate

    #Creating mask 
    ones=255*np.ones(np.shape(background)[:2],np.uint8)
    ones[y:y+apple_length,x:x+apple_length]=cv2.bitwise_not(img_BW)
 
    #Pasting the colored apple on the frame, using the mask
    background=cv2.bitwise_and(background,background,mask=ones)
    zeros=np.zeros(np.shape(background),np.uint8)
    zeros[y:y+apple_length,x:x+apple_length]=img_color
    background=cv2.add(background,zeros)
    
    #Removing the noise around the apple
    background[y:y+apple_length,x:x+apple_length]=cv2.medianBlur(background[y:y+apple_length,x:x+apple_length],3)
    return background

def get_coordinates (half):
    x=random.randint(0,int(width)-apple_length) 
    y=random.randint(10,half*(int(height)-apple_length))
    return (x,y)

def activate_camera (cap,points):
    ret,frame=cap.read()
    if points<9: #At the first 10 points of every round, the display will be straight (like looking in the mirror
    #Beyond the 10 first points, the display will be flipped (right is left and left is right)
        frame=cv2.flip(frame,1)
    return frame

def creatediff (next_frame,prev_frame,kernel):
    #Changing to grayscale:
    prev_frame=cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY) 
    next_frame=cv2.cvtColor(next_frame,cv2.COLOR_BGR2GRAY)
    diff=cv2.absdiff(next_frame,prev_frame)    #Computing the absolute value of difference between the frames
    #Some refining
    _,diff=cv2.threshold(diff,50,255,cv2.THRESH_BINARY)
    diff=cv2.medianBlur(diff,3)
    diff=cv2.Canny(diff,100,255)
    diff=cv2.dilate(diff,kernel,iterations=1)
    return diff

def paste_message (img,color,background,coordinate,scale):
    _,thresh= cv2.threshold(img,50,255,cv2.THRESH_BINARY)
    img=cv2.medianBlur(thresh,5)
    height,width=int(np.shape(background)[0]/scale[1]), 2*int(np.shape(background)[1]/scale[0])
    img=cv2.resize(img, (width,height))
    color=cv2.resize(color, (width,height))
    (x,y)=coordinate
    ones=255*np.ones(np.shape(background)[:2],np.uint8)
    ones[:height,x:x+width]=cv2.bitwise_not(img)
    background=cv2.bitwise_and(background,background,mask=ones)
    img=cv2.bitwise_and(color,color,mask=img)
    kernel=np.ones((2,2),np.uint8)
    background[:height,x:x+width]=cv2.add(background[:height,x:x+width],img)
  
    background[:height,x:x+width]=cv2.erode(background[:height,x:x+width],kernel,iterations=1)
    background[:height,x:x+width]=cv2.bilateralFilter(background[:height,x:x+width],9,75,75)
    return background

def first_screen_message():
    if english: #Print english message to screen
        cv2.putText(frames['screen'], "Your score is in the top 5 high scores!",(0,int(height/10)),cv2.FONT_HERSHEY_SIMPLEX,1.1,(0,0,240),2,cv2.LINE_AA) #Writing the score
        cv2.putText(frames['screen'], "Please type your name:",(30,2*int(height/10)),cv2.FONT_HERSHEY_SIMPLEX,1.1,(0,0,240),2,cv2.LINE_AA) #Writing the score
        cv2.putText(frames['screen'], "When finished, press Enter",(30,3*int(height/10)),cv2.FONT_HERSHEY_SIMPLEX,1.1,(0,0,240),2,cv2.LINE_AA) #Writing the score
    else: #Print hebrew message to screen
        frames['screen']=paste_message (cv2.imread("./Files/Enter name.jpg",0),cv2.imread("./Files/Enter name.jpg",1),frames['screen'],(0,0),(2,2.5))

def second_screen_message():
    if english: #Print english message to screen
        cv2.putText(frames['screen'], "You have broke a record!",(0,int(height/15)),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,240),2,cv2.LINE_AA) #Writing the score
        cv2.putText(frames['screen'], "Let's take a photo of you!",(0,2*int(height/15)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,240),2,cv2.LINE_AA) #Writing the score
        cv2.putText(frames['screen'], "Please stand in the red frame",(0,3*int(height/15)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,240),2,cv2.LINE_AA) #Writing the score
        cv2.putText(frames['screen'], "When ready, touch the apple and wait 3 seconds",(0,4*int(height/15)),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,240),2,cv2.LINE_AA) #Writing the score
    else: #Print hebrew message to screen
        frames['screen']=paste_message (cv2.imread("./Files/broke record.jpg",0),cv2.imread("./Files/broke record.jpg",1),frames['screen'],(0,0),(2,3))

"""Actual game related functions:"""

"""
    The game is built of 4 stages, switching between them every 5 points periodically.
    At the first 20 points, there are no rotten apples, so the user can't get negative points.
    After the user scores 20 points, rotten apples start to pop every 3-10 seconds (chosen randomly) for 1-3 seconds (also chosen randomly).
    As opposed to the regular-red-apples, the rotten apples will pop only at the top half of the screen,
    in order to prevent the user to touch them by mistake with his upper half of the body.
    Time counting is done by counting down the frame number that was randomly picked.
    """
    
def run_levels():
    if parameters['round']!=0: #If we have passed the first 20 points, rotten apples start to pop 
        times['pop_time']-=1 #Counting down
        if times['pop_time']<=0: #if countdown is over
            frames['apple_color'],frames['apple_BW']=apple_color_rot,apple_rot_BW #Placing the rotten apple instead 
            parameters['half']=0.5 #Placing rotten apples only in the top half
            times['duration']-=1 #Counting down
            if times['duration'] <=0:
                reset_times_and_apples() #if count down is over, the code gets placing red apples, and get new randomly times
   
    if parameters['points']<=4: #points<=4
        level_0()
    
    elif ( parameters['points']>4) & ( parameters['points']<=9): #4<points<=9
        level_1()
        
    elif  parameters['points']>9:
        if ( parameters['points']>9) & ( parameters['points']<=14):#9<points<=14
            level_0()
    
        elif  parameters['points']>14:#14<points<=19
            level_1()
    """
    After every 20 points the user wins, the code restarts the "points" variable
    so it will return to the first level, and saves those 20 points in the "round" variable
    """
    if  parameters['points']==20: #after the user won 20 points, 
        parameters['round']+=20
        parameters['points']=0
            
    top_bar(frames['screen']) #Updates the top bar, showing the points

def level_0 ():
    sum=np.sum(frames['diff'][parameters['cor'][1]:parameters['cor'][1]+apple_length,
                           parameters['cor'][0]:parameters['cor'][0]+apple_length]) #Calculate the sum of activated pixels within the ROI containing the apple
    if sum>100: # if pixel is activated:
        if parameters['half']==1: #if half=1 then the player touched an apple.So we play score sound, and raise his points by 1
            score_sound.play()
            parameters['points']+=1
        else: #if half is not 1, then it's 0.5, thus the user touched a rotten apple. So we play the loss sound, raise his loss points by 1,
        #and set 'duration' to zero, so the rotten apple will be replaced by a regular apple.
           parameters['losses']+=1
           loss_sound.play()
           times['duration']=0
    
        parameters['cor']=get_coordinates(parameters['half']) # Generating new random coordinate
        
    frames['screen']=paste_apple(frames['apple_BW'],frames['apple_color'],frames['screen'],
                             parameters['cor']) #Pasting the apple on the frame
    return 

def level_1 ():
    seconds_passed=(1/fps)*parameters['frame_count']
    position_changing_time=60/(parameters['round']+20) #With every round the apple position at this level is changing faster
    if(seconds_passed)%(position_changing_time)==0: #The apple coordinate will be changed randomly according to the apple position changing time
        parameters['cor']=get_coordinates(parameters['half']) # Generating new random coordinate
    return level_0()

def reset_times_and_apples():
    frames['apple_color'],frames['apple_BW']=apple_color,apple_BW
    times['pop_time']=random.randrange(fps*3,fps*10,fps)
    times['duration']=random.randrange(fps,fps*3,fps)
    parameters['half']=1 #placing apples anywhere

def check_score_in_highscore(score_list,score): #This function checks if the user's score between the 5 high scores in the score list.
    # If it is - the fucntion return its position. If not - it returns -1. Either way, it returns the most updated list.
    np_score=np.array(score_list)
    mask=[int(np_score[i].score) >= score for i in range(5)]  
    i=len( np_score[mask])

    if i<5: 
         np_score[i+1:]= np_score[i:len( np_score)-1] #Shifting the scores one place to the right
         np_score[i]=player(0,str(score)) #Inserting the player's score
         return np_score.tolist(),i
    return np_score.tolist(),-1


""" I/O related functions:"""
def get_scores_from_file(source): #Reading the score list text file into score_list array, which contains variables from the 'player' class
    file=open(source,'r')
    score_list=[]
    for line in file:
        elem=line.replace('\n','').split(',') 
        score_list.append(player(elem[0],elem[1])) #Storing each name from the list and its score into player class variable
    file.close()
    return sorted(score_list,key=lambda x:x.score,reverse=True)

def update_list(target,score_list): #Updating the score list
    file=open(target,'w')
    for i in range(4):
        file.write(score_list[i].name +","+score_list[i].score+'\n')
    file.write(score_list[4].name +","+score_list[4].score)
    file.close()
    return
        

""" Main Function:"""
try: #If the game is not activated using the menu.py file, an error would arise, so we handle this
    english=sys.argv[1]
except IndexError:
    english=True #English is the default language incase of an error
    
#Starting the video and setting the window size
cap = cv2.VideoCapture(0)
cv2.namedWindow("Apple_game", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Apple_game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#Initialize Parameters:
fps= cap.get(cv2.CAP_PROP_FPS)
num=fps*4 ;i=4 ;flag=0 ;game_over_waiting_time=5*fps ;scale=20 ;name=""
kernel=np.ones((5,5),np.uint8)

#Get first frame, pictures and score list
prev_frame = activate_camera(cap,0)
apple_color,apple_BW=get_apple('./Files/apple.jpg') #Returning the B_W apple and color apple
apple_color_rot,apple_rot_BW=get_apple('./Files/rotten.jpg') #Returning the B_W rotten apple and colored rotten apple
(height,width)=prev_frame.shape[:2]
apple_length=int(height/scale) # The apple's width and height
score_list=get_scores_from_file('./Files/score_list.txt') #Loading the score file

#Music initialization:
pygame.mixer.init()
score_sound=pygame.mixer.Sound('./Files/score2.wav')
loss_sound=pygame.mixer.Sound('./Files/loss.wav')
backmus=pygame.mixer.Sound('./Files/bashanah.wav')
backmus.play(loops=-1)

#Initializing dictionaries
parameters={'frame_count':1,'points':0,'cor':get_coordinates(1),'round':0,'half':1,'losses':0}
frames={'screen':0,'diff':0,'next_frame':0,'apple_BW':apple_BW,'apple_color':apple_color}
times={'pop_time':random.randrange(fps*3,fps*10,fps),'duration':random.randrange(fps,fps*3,fps)}


while(cap.isOpened()):
    parameters['frame_count']+=1 
    frames['next_frame']=activate_camera(cap,parameters['points']) # Catch next frame
    frames['diff']=creatediff(frames['next_frame'],prev_frame,kernel) # Create the difference frame
    frames['screen']=copy.deepcopy(frames['next_frame']) #Copying the frame
    if parameters['losses'] < 3:
        run_levels()
        
    elif parameters['losses']==3:
        cv2.putText(frames['screen'], "Game Over!",(int(width/2)-4*int(width/9),int(height/2)),cv2.FONT_HERSHEY_SIMPLEX,
            3,(0,0,240),7,cv2.LINE_AA) 
        game_over_waiting_time-=1 #Count down in order to present the 'game over' message for 5 seconds
        if game_over_waiting_time==0:
            parameters['losses']=4
            score_list,score_index=check_score_in_highscore(score_list,parameters['points']+parameters['round'])
   
    key = cv2.waitKey(30) & 0xff
    if key == 27: #ESC key
        break       
            
    if parameters['losses']==4:
        if score_index==-1: #If the score is not between the top 5 scores - the game is over
            break
        if flag==0: #The score is among the top 5 scores, thus we save the player's name
            if len(name)<20:
                if key==8 and (len(name)>0):
                    name=name[:(len(name)-1)]
                if (key>=32 and key<=122):
                    name+=(chr(key))
            first_screen_message()
            cv2.putText(frames['screen'], name,(0,int(4.5*height/10)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,240),2,cv2.LINE_AA) #Writing the score
            if key==13: #Enter key
                score_list[score_index].name=name
                update_list('./Files/score_list.txt',score_list)
                flag=1
            
        elif flag==1:
            if score_index==0:
                second_screen_message()
                cv2.rectangle(frames['screen'],(int(width/3),int(height/3)),(2*int(width/3),height),(0,0,240),2)
                frames['screen']=paste_apple(apple_BW,apple_color,frames['screen'],
                                 (2*int(width/3)+50,int(height/3)+20))
                sum=np.sum(frames['diff'][int(height/3)-10:int(height/3)-10+apple_length,2*int(width/3)+50:2*int(width/3)+50+apple_length]) #Calculate the sum of activated pixels
                if sum>100: # if pixel is activated, we raise a flag
                    flag=2
            else:
                break
        
        elif flag==2:
            cv2.rectangle(frames['screen'],(int(width/3),int(height/3)),(2*int(width/3),height),(0,0,240),2)
            if (i>0) and num==fps*i:
                i-=1
            if i==0:
                window=frames['screen'][int(height/3)+2:height-2,int(width/3)+2:2*int(width/3)-2]
                cv2.imwrite('./Files/winner.jpg',window)
                break
            cv2.putText(frames['screen'], str(i),(int(width/2),130),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,240),2,cv2.LINE_AA) #Writing the score
            num-=1 
            
    cv2.imshow("Apple_game",frames['screen'])
    prev_frame=copy.deepcopy(frames['next_frame']) 

pygame.mixer.quit()
cap.release()
cv2.destroyAllWindows()