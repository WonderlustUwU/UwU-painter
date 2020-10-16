# coding=UTF-8
from tkinter import *
from tkinter.colorchooser import askcolor 
from functools import partial


class Paint(object):

    DEFAULT_COLOR = 'black'

    def __init__(self, partner):
        root.bind('<Control-z>', self.undo)
        
        self.titlebar = Frame(bg = 'azure3')
        self.titlebar.grid(row=0)
        
        self.title_button = Button(self.titlebar, text = 'UwU Painter', bg = 'azure3', font = 'fixedsys 12 ', activebackground = 'azure3', relief = SUNKEN, borderwidth=0, padx=11, width=165, anchor=W)
        self.title_button.grid(row=0, column=0, padx=0)        
        
        self.minimise_button = Button(self.titlebar, text = '—', bg = 'azure3', font = 'fixedsys 12 ', borderwidth=0, padx=6)
        self.minimise_button.grid(row=0, column=1, padx=0)              
        
        self.close_button = Button(self.titlebar, text = 'X', bg = 'firebrick', font = 'fixedsys 12 ', borderwidth=0, padx=7, command=root.destroy)
        self.close_button.grid(row=0, column=2, padx=0)               
        
        self.framer = Frame(bg = 'azure4')
        self.framer.grid(row=1) 
        
        self.topbar = Frame(self.framer, bg = 'azure4')
        self.topbar.grid(row=1, column = 0)        

        self.pen_button = Button(self.topbar, text = 'Paint Brush', bg = 'azure2', font = 'fixedsys 12 ', command=self.use_pen, relief = SUNKEN)
        self.pen_button.grid(row=0, column=0, padx=10)
        
        self.eraser_button = Button(self.topbar, text =  'Eraser', bg = 'azure2', font = 'fixedsys 12 ', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=1, padx=10)        

        self.color_button = Button(self.topbar, text = 'Color', bg = 'azure2', font = 'fixedsys 12 ', command=self.choose_color)
        self.color_button.grid(row=0, column=2, padx=10)
        
        self.help_button = Button(self.topbar, text = 'Help menu', bg = 'cornflower blue', font = 'fixedsys 12 ', command=self.help_me)
        self.help_button.grid(row=0, column=9, padx=10)        
        
        self.label = Label(self.topbar, bg = 'azure4', text = 'Brush size:', font = 'fixedsys 12 italic')
        self.label.grid(row=0, column=4, padx=10)
        
        self.color_display = Label(self.topbar, bg = 'black', text = '', font = 'fixedsys 12 italic', borderwidth = 3, relief = GROOVE, padx=13, pady=4)
        self.color_display.grid(row=0, column=3, padx=10)
        
        self.choose_size_button = Scale(self.topbar, from_=1, to=100, orient=HORIZONTAL, length=220, font = 'fixedsys 12 ', bg = 'azure4', borderwidth=0)
        self.choose_size_button.grid(row=0, column=5, columnspan=2, padx=10)
        self.choose_size_button.set(5)
        
        self.undo_button = Button(self.topbar, text =  'Undo', bg = 'azure2', font = 'fixedsys 12 ', command=self.undo)
        self.undo_button.grid(row=0, column=7, padx=10)            
                                    
        self.clear_button = Button(self.topbar, text='Clear', command=self.clear_canvas, font = 'fixedsys 12 ', bg = 'firebrick2')
        self.clear_button.grid(row=0, column=8, padx=10)

        self.c = Canvas(self.framer, bg='white', width=1400, height=700)
        self.c.grid(row=2, column = 0 ,columnspan=100)
        
        self.title_button.bind('<Button-1>', self.move_window)
        self.setup()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<Button-1>', self.dot)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.eraser_on = False
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
        self.color_display.configure(bg = str(self.color))
        self.activate_button(self.pen_button)
        
        
    def undo(self, *args):
        remove_line = int(self.c.find_all()[-1]) + 1
        if int(self.c.find_all()[-1])>20:
            for i in range(20):
                self.c.delete(remove_line-i)
        else:
            self.c.delete(remove_line-1)
    
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)
        
    def help_me(self):
        helper = Help(self)
        
    def dot(self,event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if event.x and event.y:
            self.c.create_line(event.x, event.y, event.x+1, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, joinstyle=ROUND, smooth=TRUE, splinesteps=1000)              
              
        
    def clear_canvas(self):
        self.c.delete("all")

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, joinstyle=ROUND, smooth=TRUE, splinesteps=1000)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None
        
    def move_window(self, partner):
        newindow_posx, newindow_posy = (root.winfo_pointerx()-root.winfo_rootx()), (root.winfo_pointery()-root.winfo_rooty())
        def move(self):
            newpointx, newpointy = root.winfo_pointerx(), root.winfo_pointery()
            root.geometry('1400x700+' + str(newpointx-newindow_posx) + '+' + str(newpointy-newindow_posy))
        self.title_button.bind('<B1-Motion>', move)
        
class Help:
    def __init__(self, partner): 
        self.helpbubble = Toplevel()
        self.helpbubble.geometry('300x400+200+200')
        self.helpbubble.overrideredirect(True)
        
        partner.help_button.config(state=DISABLED)
        self.helpbubble.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))
        
        self.helpbox = Frame(self.helpbubble)
        self.helpbox.grid(row=0)        
        
        self.titlebar = Frame(self.helpbox)
        self.titlebar.grid(row=0)

        self.title_button = Button(self.titlebar, text = 'Help menu', bg = 'azure3', font = 'fixedsys 12 ', activebackground = 'azure3', relief = SUNKEN, borderwidth=0, padx=11, width=31, anchor=W)
        self.title_button.grid(row=0, column=0, padx=0)        
        
        self.close_help = Button(self.titlebar, text = 'X', bg = 'firebrick', font = 'fixedsys 12 ', borderwidth=0, padx=7, command=partial(self.close_help, partner))
        self.close_help.grid(row=0, column=1, padx=0)
        
        self.title_button.bind('<Button-1>', self.move_window)
        
        self.help_explain= Label(self.helpbox, text = 'Welcome to the help menu <3 \n\n Paintbrush: actives the paint brush tool which will work with your selected color \n\n Eraser: activate the ersaer tool to remove parts of your drawing \n\n Color: allows you to pick a color from the color window and makes it your pantbrush colow while auto activating the paintbursh fuction \n\n Brush Size: selects the pixel width of the brush on you slider located to the riht of the label \n\n Undo: remove the last line drawn (it will delete less from detailed lines and more from less detailed lines \n\n Clear: erases the entire canvas )', bg = 'azure2', font = 'fixedsys 12 ', width=0, height=0, wrap = 300)
        self.help_explain.grid(row=1, column=0, padx=0)
        
    def move_window(self, partner):
        move_help = self.helpbubble
        newindow_posx, newindow_posy = (move_help.winfo_pointerx()-move_help.winfo_rootx()), (move_help.winfo_pointery()-move_help.winfo_rooty())
        def move(self):
            newpointx, newpointy = move_help.winfo_pointerx(), move_help.winfo_pointery()
            move_help.geometry('300x400+' + str(newpointx-newindow_posx) + '+' + str(newpointy-newindow_posy))
        self.title_button.bind('<B1-Motion>', move)   
         
    def close_help(self, partner):
        partner.help_button.config(state=NORMAL)
        self.helpbubble.destroy()
        
if __name__ == '__main__':
    root = Tk()
    root.title('UwU Painter')
    root.overrideredirect(True)  # turns off title bar
    root.geometry('1400x700+100+100')    
    UwU = Paint(root)
    root.mainloop()