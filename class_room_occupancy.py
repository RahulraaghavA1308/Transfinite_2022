from webbrowser import Grail
import torch
import pandas as pd
import numpy as np
import cv2 as cv
import time

def rescaleframe(frame, scale=0.75):#for images ,videos,live videos
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)

    return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

def draw_line_x(img,x_):
    cv.line(img,(0,x_),(924,x_),(0,0,200),thickness=2)

def draw_line_y(img,y_):
    cv.line(img,(y_,0),(y_,693),(0,0,200),thickness=2)


# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Images
while(True):
    cv.destroyAllWindows()
    img = r'D:\Rahul\Yolo v5\yolov5\Snap_1.jpg'  # or file, Path, PIL, OpenCV, numpy, list

    IMG = cv.imread(img)
    print(IMG.shape)
    x_ratio = IMG.shape[0]/693
    y_ratio = IMG.shape[1]/924

    # IMG = rescaleframe(IMG,0.1)


    IMG = cv.resize(IMG,(924,693),interpolation=cv.INTER_LINEAR)

    # cv.imshow('Original',IMG)
    print(IMG.shape)
    # Inference
    results = model(img)

    # Results
    # results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
    # results.show()

    df = results.pandas().xyxy[0]
    # print(df)
    df = df[(df['class']==0)]

    A = df.values.tolist()
    B = list()
    # print(A)
    if(len(A) == 0):
        print("No human is present")
    else:
        for x in A:
            # print(f'->{x[0]},{x[2]} ->{x[1]},{x[3]}')
            B.append([int((x[0] + x[2])*0.5*1/y_ratio),int((x[1] + x[3])*0.5*1/x_ratio)])

        # B has the list of center points of each and every person in the room
        print(B)

        for x in B:
            cv.rectangle(IMG,(x[0]-20,x[1]-20),(x[0]+20,x[1]+20),(255,0,0),thickness= 3)
            # cv.putText(IMG,f'({x[0]},{x[1]})',(x[0],x[1]),cv.FONT_HERSHEY_TRIPLEX,1.5,(0,200,200),thickness=1)

        row_1 = 300
        row_2 = 350
        row_3 = 400
        row_4 = 500

        # col_1 =

        # x_min and y_min are interchanged
        # [x_min,x_max,y_min,y_max]
        #         col 1                         2                 3
        GRIDS = [[0,row_1,0,924*1/3],[0,row_1,924*1/3,924*2/3],[0,row_1,924*2/3,924],
                [row_1,row_2,0,924*1/3],[row_1,row_2,924*1/3,924*2/3],[row_1,row_2,924*2/3,924],
                [row_2,row_3,0,924*1/3],[row_2,row_3,924*1/3,924*2/3],[row_2,row_3,924*2/3,924],
                [row_3,row_4,0,924*1/3],[row_3,row_4,924*1/3,924*2/3],[row_3,row_4,924*2/3,924]
        ]

        # cv.rectangle(IMG,(int(GRIDS[10][2]),int(GRIDS[10][0])),(int(GRIDS[10][3]),int(GRIDS[10][1])),(255,255,255),thickness=cv.FILLED)


        draw_line_x(IMG,300)
        draw_line_x(IMG,350)
        draw_line_x(IMG,400)
        draw_line_x(IMG,500)

        draw_line_y(IMG,int(924*1/3))
        draw_line_y(IMG,int(924*2/3))
        # draw_line_y(IMG,300)

        AMG = IMG.copy()
        RES = set()

        for x in B:
            for i,y in enumerate(GRIDS):
                if(x[0] > y[2] and x[0] < y[3] and x[1] > y[0] and x[1] < y[1]):
                    RES.add(i);

        print(" >---------> ")
        print(RES)
        # cv.rectangle(IMG,(int(GRIDS[10][2]),int(GRIDS[10][0])),(int(GRIDS[10][3]),int(GRIDS[10][1])),(255,255,255),thickness=cv.FILLED)

        for a in RES:
            IMG = cv.rectangle(IMG,(int(GRIDS[a][2]),int(GRIDS[a][0])),(int(GRIDS[a][3]),int(GRIDS[a][1])),(0,255,0),thickness= 10)

        # cv.imshow('before',rescaleframe(AMG,0.9))

        cv.imshow('Output',rescaleframe(IMG,1))

        cv.waitKey(2000)
            # if cv.waitKey(20) &0xFF==ord('d'):
            #     break;

    
    

