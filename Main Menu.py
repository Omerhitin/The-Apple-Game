import pygame, sys
import ctypes
import runpy

class player:
    def __init__(self, name,score):
        self.score=score
        self.name=name
        
def get_scores_from_file(source): #Reading the score list text file into score_list array, which contains variables from the 'player' class
    file=open(source,'r')
    score_list=[]
    for line in file:
        elem=line.replace('\n','').split(',')
        score_list.append(player(elem[0],elem[1])) #Storing each name from the list and its score into player class variable
    file.close()
    return score_list

def draw_text (text,font,color,surface,x,y):
    textobj=font.render(text,1,color)
    textrect=textobj.get_rect()
    textrect.topleft=(x,y)
    surface.blit(textobj,textrect)
    
def Buttons(screen,font,width,height,click):
    mx, my = pygame.mouse.get_pos()  
    #Set buttons areas
    button_play_area = pygame.Rect(int(width/2)-int(width/11), 4*int(height/9),3*int(width/20) ,int(height/15))
    button_instructions_area = pygame.Rect(int(width/2)-int(width/11), 5*int(height/9),3*int(width/20) ,int(height/15))
    button_scores_area = pygame.Rect(int(width/2)-int(width/11), 6*int(height/9),3*int(width/20) ,int(height/15))
    
    #For each button we define a function that will be executed when the user clicks the button
    if button_play_area.collidepoint((mx, my)): 
        screen.blit(button_play_t,(int(width/2)-int(width/11), 4*int(height/9)))
        if click:
            sys.argv=['',english]
            runpy.run_path(path_name="Apple_game.py") #Running the actual game
    else:
        screen.blit(button_play,(int(width/2)-int(width/11), 4*int(height/9)))

    if button_instructions_area.collidepoint((mx, my)):
        screen.blit(button_instrucions_t,(int(width/2)-int(width/11), 5*int(height/9)))
        if click:
            Instructions()
    else:
        screen.blit(button_instrucions,(int(width/2)-int(width/11), 5*int(height/9)))

    if button_scores_area.collidepoint((mx, my)):
        screen.blit(button_scores_t,(int(width/2)-int(width/11), 6*int(height/9)))
        if click:
            scores(width,height)
    else:
        screen.blit(button_scores,(int(width/2)-int(width/11), 6*int(height/9)))
        
    return mx,my

def Instructions():
    running = True
    while running:
        screen.blit(instruc,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.update()     
        
def scores(width,height):
    first_place=pygame.image.load("./Files/winner.jpg")
    first_place=pygame.transform.scale(first_place, (int(sf_width/8),int(sf_height/3)))
    score_list=get_scores_from_file('./Files/score_list.txt')
    running = True
    rect = pygame.Rect(4*int(width/5)-int(width/13)-4, 2*int(height/5)-4,int(width/8)+8 ,int(height/3)+8)

    while running:
        screen.blit(scores_pic,(0,0))
        screen.blit(first_place,(4*int(width/5)-int(width/13),2*int(height/5)))
        
        if int(score_list[0].score)>0: #Printing the first place score if there is any
            pygame.draw.rect(screen, (0, 0, 0), rect,5)
            draw_text(score_list[0].score, font, (255, 198, 17), screen, 4*int(width/5)-int(sf_width/35),  2*int(height/5)+int(height/3))
        for i in range(5): #Printing the high scores table
            draw_text(str(i+1) + '. '+ score_list[i].name + ' - '+ score_list[i].score   ,
                      font2, (0, 0, 0), screen, int(width/10),  int(height/3) +(1.1*int(height/10)*i))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.update()
    
def load_photos():
    if english: #Loading the english version of the game photos
        #Set background image
        img=pygame.transform.scale(pygame.image.load("./Files/back_en.jpg"), (sf_width,sf_height))
        
        #Load and resize images
        instruc=pygame.transform.scale(pygame.image.load("./Files/instructions_en.jpg"), (sf_width,sf_height))
        scores_pic=pygame.transform.scale(pygame.image.load("./Files/scores_en.jpg"), (sf_width,sf_height))
        button_play=pygame.transform.scale(pygame.image.load("./Files/button play en.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_play_t=pygame.transform.scale(pygame.image.load("./Files/button play en t.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_instrucions=pygame.transform.scale(pygame.image.load("./Files/button inst en.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_instrucions_t=pygame.transform.scale(pygame.image.load("./Files/button inst en t.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_scores=pygame.transform.scale(pygame.image.load("./Files/button score en.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_scores_t=pygame.transform.scale(pygame.image.load("./Files/button score en t.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        lang=pygame.transform.scale(pygame.image.load("./Files/en to heb.jpg"), (int(sf_width/20),int(sf_height/15)))
        lang_t=pygame.transform.scale(pygame.image.load("./Files/en to heb t.jpg"), (int(sf_width/20),int(sf_height/15)))

    else: #Loading the hebrew version of the game photos
        #Set background image
        img=pygame.transform.scale(pygame.image.load("./Files/back.jpg"), (sf_width,sf_height))
        
        #Load and resize images
        instruc=pygame.transform.scale(pygame.image.load("./Files/instructions.jpg"), (sf_width,sf_height))
        scores_pic=pygame.transform.scale(pygame.image.load("./Files/scores.jpg"), (sf_width,sf_height))
        button_play=pygame.transform.scale(pygame.image.load("./Files/button play.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_play_t=pygame.transform.scale(pygame.image.load("./Files/button play t.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_instrucions=pygame.transform.scale(pygame.image.load("./Files/button inst.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_instrucions_t=pygame.transform.scale(pygame.image.load("./Files/button inst t.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_scores=pygame.transform.scale(pygame.image.load("./Files/button score.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        button_scores_t=pygame.transform.scale(pygame.image.load("./Files/button score t.jpg"), (3*int(sf_width/20),int(sf_height/15)))
        lang=pygame.transform.scale(pygame.image.load("./Files/heb to en.jpg"), (int(sf_width/20),int(sf_height/15)))
        lang_t=pygame.transform.scale(pygame.image.load("./Files/heb to en t.jpg"), (int(sf_width/20),int(sf_height/15)))
    return img,instruc,scores_pic,button_play,button_play_t,button_instrucions,button_instrucions_t,button_scores,button_scores_t,lang,lang_t

#Initialize game and display
pygame.init()
pygame.display.set_caption('The Rosh Hashana Game')
ctypes.windll.user32.SetProcessDPIAware()
resolution = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
screen=pygame.display.set_mode(resolution,pygame.FULLSCREEN)
window_size=pygame.display.get_surface().get_size() 
sf_width, sf_height = screen.get_size()
english=True

img,instruc,scores_pic,button_play,button_play_t,button_instrucions,button_instrucions_t,button_scores,button_scores_t,lang,lang_t=load_photos()
#Loading fonts
font = pygame.font.Font('./Files/dnk.ttf', int(sf_height/25))
font2= pygame.font.Font('./Files/dnk.ttf', int(sf_height/15))
    
""" Main Menu"""
    
click=False

while True:
    width, height =window_size[0],window_size[1]
    screen.blit(img,(0,0))
    
    mx,my=Buttons(screen,font,width,height,click)
    click = False
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

                    
    button_lang_area=pygame.Rect(10, 10,int(width/20) ,int(height/15)) #Set button area
    if button_lang_area.collidepoint((mx, my)): #When the user clicks, the game's language will be changed
        screen.blit(lang_t,(10, 10))
        if click:
            english=not(english)
            img,instruc,scores_pic,button_play,button_play_t,button_instrucions,button_instrucions_t,button_scores,button_scores_t,lang,lang_t=load_photos()
    else:
        screen.blit(lang,(10, 10))
    pygame.display.update() 
               












