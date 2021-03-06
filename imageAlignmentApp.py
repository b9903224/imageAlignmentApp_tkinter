# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 23:29:18 2020

@author: b9903/mchsiaoj
"""

import tkinter as tk
from tkinter import filedialog
import tkinter.font as font
import os
import numpy as np
from PIL import Image, ImageTk
from utility.insertSignature import insertSignature
import scrollimage
import utility


featVer = 'dev'
kernelVer = 'dev'

padx = 0
pady = 0
pathEntryWidth=90
currentPath = os.getcwd()
imgShowSize=512
        
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().title("Image Alignment")
        self.grid()
#        self.pack()
        self.createWidgets()
        self.insertVersion('RD',1,1)
#        self.insertVersion('RU',1,1)
        
    def createWidgets(self):
        
        # bind method must has event as input: func(self,event)...
        self.callback_canvas_openPreImg = lambda event: self.loadImgFromEntry(self.entry_preImg, self.imgShowFrame.canvas_preImg, self.imgShowFrame.label_preImg)
        self.callback_canvas_openPostImg = lambda event: self.loadImgFromEntry(self.entry_postImg, self.imgShowFrame.canvas_postImg, self.imgShowFrame.label_postImg)
        
        self.label_intro = tk.Label(self)
        self.label_intro["text"] = """output file name e.g.:
            [xxx].png --> [xxx]_diff.png
            [xxx].png --> [xxx]_featureDemo.png"""
        self.label_intro.grid(row=0,column=1,columnspan=1)
        
        self.label_preImg = tk.Label(self)
        self.label_preImg["text"] = "Pre Img:"
        self.label_preImg.grid(row=1,column=0,padx=padx,pady=pady,sticky=tk.E)
        
        self.label_postImg = tk.Label(self)
        self.label_postImg["text"] = "Post Img:"
        self.label_postImg.grid(row=2,column=0,padx=padx,pady=pady,sticky=tk.E)
        
        self.label_outputPath = tk.Label(self)
        self.label_outputPath["text"] = "Output Path:"
        self.label_outputPath.grid(row=3,column=0,padx=padx,pady=pady,sticky=tk.E)
        
        self.entry_preImg = tk.Entry(self,width=pathEntryWidth)
        self.entry_preImg.grid(row=1,column=1,padx=padx,pady=pady)
        
        self.entry_postImg = tk.Entry(self,width=pathEntryWidth)
        self.entry_postImg.grid(row=2,column=1,padx=padx,pady=pady)
        
        self.entry_outputPath = tk.Entry(self,width=pathEntryWidth)
        self.entry_outputPath.grid(row=3,column=1,padx=padx,pady=pady)
        
        self.btn_outputPath = tk.Button(self)
        self.btn_outputPath["text"] = "Select Output Folder"
        self.btn_outputPath["command"] = lambda: self.loadDirectoryToEntry(self.entry_outputPath)
        self.btn_outputPath.grid(row=3,column=2,padx=padx,pady=pady)
        
        self.btn_copyPath_pre = tk.Button(self)
        self.btn_copyPath_pre["text"] = "Copy Path to Output (Pre)"
        self.btn_copyPath_pre["command"] = lambda: self.copyDirectoryToEntry(self.entry_preImg, self.entry_outputPath)
        self.btn_copyPath_pre.grid(row=1,column=2,padx=padx,pady=pady)
        
        self.btn_copyPath_post = tk.Button(self)
        self.btn_copyPath_post["text"] = "Copy Path to Output (Post)"
        self.btn_copyPath_post["command"] = lambda: self.copyDirectoryToEntry(self.entry_postImg, self.entry_outputPath)
        self.btn_copyPath_post.grid(row=2,column=2,padx=padx,pady=pady)
        
        self.createImgShowFrame()
        self.imgShowFrame.grid(row=5,column=0,columnspan=3,padx=padx,pady=pady)
        
        self.createAlignModeFrame()
        self.alignModeFrame.grid(row=4,column=0,padx=5,pady=5,columnspan=2,sticky='W')
        
        self.createManualAlignFrame()
        self.manualAlignFrame.grid(row=4,column=1,padx=15,pady=5,sticky='WN')
        
        self.btn_run = tk.Button(self,fg='white',bg='blue',activebackground='red',activeforeground='white',borderwidth=10)
        self.btn_run['text'] = 'Run'
        self.btn_run['font'] = font.Font(size=40, weight='bold')
        self.btn_run['command'] = self.run()
        self.btn_run.grid(row = 5,column=3,rowspan=1,padx=5,pady=5,sticky='EW')
        
    def createManualAlignFrame(self):
        entryWidth = 10
        manualAlignFrame = tk.LabelFrame(self,text='Manual Shift',labelanchor='nw',padx=5,pady=5)
        
        manualAlignFrame.label_shift_x = tk.Label(manualAlignFrame,text='X Shift: ')
        manualAlignFrame.entry_shift_x = tk.Entry(manualAlignFrame,width=entryWidth)
        manualAlignFrame.label_shift_y = tk.Label(manualAlignFrame,text='Y Shift: ')
        manualAlignFrame.entry_shift_y = tk.Entry(manualAlignFrame,width=entryWidth)
        
        manualAlignFrame.entry_shift_x.insert(0,'0')
        manualAlignFrame.entry_shift_y.insert(0,'0')
        
        manualAlignFrame.label_shift_x['state'] = 'disable'
        manualAlignFrame.entry_shift_x['state'] = 'disable'
        manualAlignFrame.label_shift_y['state'] = 'disable'
        manualAlignFrame.entry_shift_y['state'] = 'disable'
        
        manualAlignFrame.label_shift_x.grid(row=0,column=0,sticky='W')
        manualAlignFrame.entry_shift_x.grid(row=0,column=1)
        manualAlignFrame.label_shift_y.grid(row=1,column=0,sticky='W')
        manualAlignFrame.entry_shift_y.grid(row=1,column=1)
        
        self.manualAlignFrame = manualAlignFrame
        
    def createAlignModeFrame(self):
        alignModeFrame = tk.LabelFrame(self,text='Align Mode',padx=5,pady=5,labelanchor='nw')
        
        alignMode = tk.StringVar()
        alignMode.set('auto')
        
#        hitme = lambda : print('%s mode selected'%alignMode.get())
        disableManualAlignFrame = lambda : self.disableChildren(self.manualAlignFrame)
        enableManualAlignFrame = lambda : self.enableChildren(self.manualAlignFrame)
        
        alignModeFrame.radioBtn_auto = tk.Radiobutton(alignModeFrame,text='Auto',variable=alignMode,value='auto',command=disableManualAlignFrame)
        alignModeFrame.radioBtn_manual = tk.Radiobutton(alignModeFrame,text='Manual',variable=alignMode,value='manual',command=enableManualAlignFrame)
        
        alignModeFrame.radioBtn_auto.grid(row=0,column=0,sticky=tk.W)
        alignModeFrame.radioBtn_manual.grid(row=1,column=0,sticky=tk.W)

        alignModeFrame.alignMode = alignMode

        self.alignModeFrame = alignModeFrame
        
    def disableChildren(self,parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame','Labelframe'):
                child.configure(state='disable')
            else:
                self.disableChildren(child)

    def enableChildren(self,parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
#            print (wtype)
            if wtype not in ('Frame','Labelframe'):
                child.configure(state='normal')
            else:
                self.enableChildren(child)
                
    def run(self):
        pass
    
    def createImgShowFrame(self):
#        imgShowFrame = tk.Frame(self)
        imgShowFrame = tk.LabelFrame(self,text='Image',padx=5,pady=5,labelanchor='nw')
        
        textLoc = imgShowSize/2
        
        imgShowFrame.label_preImg = tk.Label(imgShowFrame)
        imgShowFrame.label_preImg['text'] = 'Pre Img'
        
        imgShowFrame.label_postImg = tk.Label(imgShowFrame)
        imgShowFrame.label_postImg['text'] = 'Post Img'
        
        imgShowFrame.canvas_preImg = tk.Canvas(imgShowFrame,width=imgShowSize,height=imgShowSize,bg='skyblue',highlightthickness=0)
        imgShowFrame.canvas_preImg.create_text(textLoc,textLoc,text='Select Pre Image (Click Me)',fill="darkblue",font="Times 20 italic bold")
        imgShowFrame.canvas_preImg.bind('<Button-1>',self.callback_canvas_openPreImg)
        
        imgShowFrame.canvas_postImg = tk.Canvas(imgShowFrame,width=imgShowSize,height=imgShowSize,bg='green',highlightthickness=0)
        imgShowFrame.canvas_postImg.create_text(textLoc,textLoc,text='Select Post Image (Click Me)',fill="darkblue",font="Times 20 italic bold")
        imgShowFrame.canvas_postImg.bind('<Button-1>',self.callback_canvas_openPostImg)
        
        imgShowFrame.label_preImg.grid(row=0,column=0)
        imgShowFrame.label_postImg.grid(row=0,column=1)
        imgShowFrame.canvas_preImg.grid(row=1,column=0)
        imgShowFrame.canvas_postImg.grid(row=1,column=1)
        
        self.imgShowFrame = imgShowFrame
        
    def loadImgFromEntry(self,entry,canvas,label, event=None):
#        print(event)
        fileName = self.loadFileNameToEntry(entry)
        self.loadImgToCanvas(fileName,canvas,label)
        
    def loadImgToCanvas(self,fileName,canvas,label):
        
        if not fileName:
            return
        img_ori = Image.open(fileName)
        img = ImageTk.PhotoImage(img_ori.resize((imgShowSize,imgShowSize)))
        canvas.create_image(0,0,anchor='nw',image=img)
        canvas.image=img
        canvas.img_ori = img_ori
        _, imgFileName = os.path.split(fileName)
        labelText = label['text']
        label_title = '[%s] %s, size: %g, %g, mode: %s'%(labelText,imgFileName, img_ori.height,img_ori.width,img_ori.mode)
        label.config(text=label_title)
        
    def loadFileNameToEntry(self, entry):
        fileName = filedialog.askopenfilename()
#        print(fileName)
        if fileName:
            entry.delete(0, tk.END)
            entry.insert(0, fileName)
            return fileName        
            
    def loadDirectoryToEntry(self, entry):
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)
            
    def copyDirectoryToEntry(self, srcEntry, destEtry):
        # copy src to dest
        srcPath = srcEntry.get()
        path, _ = os.path.split(srcPath)
        destEtry.delete(0, tk.END)
        destEtry.insert(0, path)
        
    def insertVersion(self,loc='RD',skipRow=0,skipCol=0):
#        signatureImg = Image.open('duck.jpg')
        rgb = self.winfo_rgb(self.cget('bg'))
        rgb = [_/255 for _ in rgb]
        fontSize = 10
        img = np.zeros(((fontSize+2)*3,150,3), 'uint8')
        img[..., 0] = rgb[0]*255
        img[..., 1] = rgb[1]*255
        img[..., 2] = rgb[2]*255
        img = insertSignature(img,featVer=featVer,kernelVer=kernelVer,fontSize=fontSize,loc=loc)
#        img = insertSignature(img,featVer=featVer,kernelVer=kernelVer,fontSize=fontSize,loc='RD')
#        utility.imshow(img, 'img')
        signatureImg_pillow = Image.fromarray(img)
        signatureImg = ImageTk.PhotoImage(signatureImg_pillow)
#        signatureImg = ImageTk.PhotoImage(Image.open('duck.jpg'))
        self.label_signature = tk.Label(self, image=signatureImg)
        self.label_signature.image = signatureImg
        self.label_signature.image_pillow = signatureImg_pillow
#        self.label_signature.bind('<Button-1>',lambda event: self.popupImageByLabel(self.label_signature.image_pillow,ratio=4))
#        self.label_signature.bind('<Button-1>',lambda event: self.popupScrollImage(self.label_signature.image))
        self.label_signature.bind('<Button-1>',lambda event: self.popupScrollImageWithRatio(self.label_signature.image_pillow,ratio=10))
        columnNum, rowNum = self.grid_size()
        if loc == 'RD':
            self.label_signature.grid(row=rowNum-1+skipCol,column=columnNum-1+skipRow,sticky='SE')
        elif loc == 'RU':
            self.label_signature.grid(row=0,column=columnNum-1+skipRow,sticky='NE')
            
    def popupScrollImageWithRatio(self,img,ratio):
        popupWin = tk.Toplevel()
        image_window = scrollimage.ScrollableImageWithRatio(popupWin, image=img, scrollbarwidth=20, width=512*3, height=512, ratio=ratio)
        image_window.pack()
    
    def popupScrollImage(self,img):
        popupWin = tk.Toplevel()
        image_window = scrollimage.ScrollableImage(popupWin, image=img, scrollbarwidth=6, width=200, height=200)
        image_window.pack()
    
    def popupImageByLabel(self,image_pillow,event=None,ratio=1):
        win = tk.Toplevel()
#        win.title('Version')
#        image_pillow = self.label_signature.image_pillow
#        ratio = 4
        width, height = image_pillow.width * ratio, image_pillow.height*ratio
        image_pillow = image_pillow.resize((width, height))
        img = ImageTk.PhotoImage(image_pillow)
        win.label = tk.Label(win,image=img)
        win.label.image = img
        win.label.bind('<Button-1>',lambda event: self.popupImageByLabel(image_pillow,ratio=2))
        win.label.back()



        
if __name__ == '__main__':
  root = tk.Tk()
  app = Application(root)
  app.mainloop()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  