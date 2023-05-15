#Tạo thư viện cho các lệnh 
import pygame                                                           #pip install pygame
import os                                                               #os giúp load file từ folder khác
import random 
#Khởi tạo module cho game
pygame.init()
#Khai báo chiều rộng và chiều cao của màn hình
WIDTH = 500
HEIGHT = 600
# Khởi tạo màu sắc
white=(255,255,255)
black=(0,0,0)
red=(255, 0, 0)
#Tạo cửa sổ 
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Doodle Jump (Space Version)')
gameIcon = pygame.image.load(os.path.join("images","logo.png"))
pygame.display.set_icon(gameIcon)


fps = 60
font = pygame.font.Font('freesansbold.ttf',16)
timer = pygame.time.Clock()

#Đặt tọa độ cho người chơi và platform
playerx = 190
playery = 380
platform = [[200,525,70,10], [350, 400, 70, 10], [180,300,70,10], 
            [50, 180, 70, 10], [160,50,70,10]]
#Tạo biến
score = 0
high_score = 0
GO = False
jump = False
y_change = 0
x_change = 0
player_speed = 3
super_jump = 2
jump_last = 0
#Thêm hình ảnh của người chơi, UFO và background 
player = pygame.transform.scale((pygame.image.load 
                                 ((os.path.join("images","player.png")))), (90, 90))
ufo = pygame.transform.scale((pygame.image.load 
                                 ((os.path.join("images","ufo.png")))), (90, 90))
ufo_x=random.randint(0,WIDTH)
ufo_y=0
bg=pygame.image.load(os.path.join("images","bg.jpg"))
bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))
bgy=0



#Hàm kiểm tra va chạm
def check_collision(rect_list, j):
    global playerx
    global playery
    global y_change
    for i in range (len(rect_list)):
        if rect_list[i].colliderect([playerx, playery + 60, 60, 30
                                     ]) and jump == False and y_change > 0:
            j = True
    return j
#Hàm va chạm với UFO
def collision(x1,y1,w1,h1 , x2,y2,w2,h2):
    if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
        return True
    return False
#Hàm làm background đi xuống
def movebg():
    global bgy
    screen.blit(bg,(0,bgy))
    screen.blit(bg,(0,bgy-HEIGHT))
    bgy+=1
    if bgy==+HEIGHT:
        bgy=0
    screen.blit(player,(playerx,playery))
#Hàm cập nhật và làm người chơi nhảy liên tục
def update_player(y_pos):
    global jump 
    global y_change
    jump_height = 10
    gravity = .4
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos
#Hàm tạo ra các platform ngẫu nhiên
def update_platform(my_list, y_pos, change):
    global score
    if y_pos < 250 and change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= change
    else:
        pass 
    for item in range(len(my_list)):
        if my_list[item][1] > 600:
            my_list[item] = [random.randint(10, 320), random.randint
                             (-50, -10), 70, 10]
            score += 1
    return my_list






run = True
while run == True:
    
    timer.tick(fps)
    movebg()
    blocks=[]
    #Hiển thị điểm số
    score_text = font.render('Score: ' + str(score), True, white)
    screen.blit(score_text, (380, 20))
    AJ_text = font.render('Air Jump: ' + str(super_jump), True, white)
    screen.blit(AJ_text, (10, 20))
    #Hiển thị thông báo sau khi chết
    if GO:
        GO_text = font.render('Game Over!', True, red)
        screen.blit(GO_text, (200, 200))
        AJ_text = font.render('Air Jump restar', True, red)
        screen.blit(AJ_text, (185, 220))
        tutorial_text = font.render('Press SPACE to play again', True, red)
        screen.blit(tutorial_text, (145, 240))


    #vẽ platform
    for i in range(len(platform)):
        block=pygame.draw.rect(screen,black,platform[i], 0, 3)
        blocks.append(block)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #Khởi tạo các sự kiện nhấn phím
        if event.type == pygame.KEYDOWN:
            #Nếu chết thì phím SPACE dùng để reset
            if event.key == pygame.K_SPACE and GO:
                GO = False
                score = 0
                playerx = 190
                playery = 380   
                super_jump = 2
                jump_last = 0
                platform = [[200,525,70,10], [350, 400, 70, 10], [180,300,70,10], 
                            [50, 180, 70, 10], [160,50,70,10]]
            #Nếu không chết thì phím SPACE dùng để Air Jump
            if event.key == pygame.K_SPACE and not GO and super_jump > 0:
                super_jump -= 1
                y_change = -15
            #Dùng để duy chuyển sang trái
            if event.key == pygame.K_a:
                x_change = -player_speed
            #Dùng để duy chuyển sang phải
            if event.key == pygame.K_d:
                x_change = player_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change = 0
            if event.key == pygame.K_d:
                x_change = 0

        

    #Kiểm tra người chơi và chạm với block
    jump = check_collision(blocks, jump)
    playerx += x_change
    #Đặt lại vị trí người chơi sau khi chết
    if playery < 500:
        playery = update_player(playery)  
    else:
        GO = True
        y_change = 0
        x_change  = 0
    #Hiện platform ngẩu nhiên
    platform = update_platform(platform, playery, y_change)

    
    if x_change < 0:
        player = pygame.transform.scale((pygame.image.load (os.path.join("images","player.png"))), (90, 90))
    elif x_change > 0:
        player = pygame.transform.scale((pygame.image.load (os.path.join("images","player2.png"))), (90, 90))


    #Khi đủ 10 điểm sẽ được cộng thêm 1 lần Air Jump
    if score - jump_last > 10:
        jump_last = score 
        super_jump += 1

    #Khi đủ điểm UFO sẽ xuất hiện
    if score>5:
        screen.blit(ufo,(ufo_x,ufo_y))
        ufo_y-=1
        if score > 10: 
            ufo_y-=5
        if score > 50: 
            ufo_y-=10
        if score > 100: 
            ufo_y-=20
        if ufo_y <0 :
            ufo_y=random.randint(HEIGHT,HEIGHT+100)
            ufo_x=random.randint(0,WIDTH)

        #Xữ lý va chạm với UFO
        if collision(playerx,playery,90,90,ufo_x,ufo_y,90,90):
            GO=True
            y_change=0
            x_change=0
            playerx=190
            playery=380
            super_jump=2
            jump_last=0
            platform=[[200,525,70,10],[350,400,70,10],[180,300,70,10]
                      ,[50,180,70,10],[160,50,70,10]]
            score=0

    pygame.display.flip()
pygame.quit()


