#  coding=UTF-8
from tkinter import *
from tkinter.colorchooser import askcolor
from functools import partial
from PIL import ImageGrab
import os


class Paint(object):

    DEFAULT_COLOR = 'black'

    def __init__(self, partner):
        root.bind('<Control-z>', self.undo)

        self.titlebar = Frame(bg='azure3')
        self.titlebar.grid(row=0)

        self.title_button = Button(self.titlebar, text='UwU Painter',
                                   bg='azure3', font='fixedsys 12 ',
                                   activebackground='azure3',
                                   relief=SUNKEN, borderwidth=0, padx=11,
                                   width=165, anchor=W)
        self.title_button.grid(row=0, column=0, padx=0)

        self.minimise_button = Button(self.titlebar, text='—',
                                      bg='azure3', font='fixedsys 12 ',
                                      borderwidth=0, padx=6,
                                      command=self.minimise)
        self.minimise_button.grid(row=0, column=1, padx=0)

        self.close_button = Button(self.titlebar, text='X',
                                   bg='firebrick', font='fixedsys 12 ',
                                   borderwidth=0, padx=7,
                                   command=root.destroy)
        self.close_button.grid(row=0, column=2, padx=0)

        self.framer = Frame(bg='azure4')
        self.framer.grid(row=1)

        self.topbar = Frame(self.framer, bg='azure4')
        self.topbar.grid(row=1, column=0)

        self.pen_button = Button(self.topbar, text='Paint Brush',
                                 bg='azure2', font='fixedsys 12 ',
                                 command=self.use_pen, relief=SUNKEN)
        self.pen_button.grid(row=0, column=0, padx=10)

        self.eraser_button = Button(self.topbar, text='Eraser',
                                    bg='azure2', font='fixedsys 12 ',
                                    command=self.use_eraser)
        self.eraser_button.grid(row=0, column=1, padx=10)

        self.color_button = Button(self.topbar, text='Color',
                                   bg='azure2', font='fixedsys 12 ',
                                   command=self.choose_color)
        self.color_button.grid(row=0, column=2, padx=10)

        self.help_button = Button(self.topbar, text='Help menu',
                                  bg='cornflower blue',
                                  font='fixedsys 12 ',
                                  command=self.help_me)
        self.help_button.grid(row=0, column=9, padx=10)

        self.label = Label(self.topbar, bg='azure4', text='Brush size:',
                           font='fixedsys 12 italic')
        self.label.grid(row=0, column=4, padx=10)

        self.color_display = Label(self.topbar, bg='black', text='',
                                   font='fixedsys 12 italic',
                                   borderwidth=3,
                                   relief=GROOVE, padx=13, pady=4)
        self.color_display.grid(row=0, column=3, padx=10)

        self.choose_size_button = Scale(self.topbar, from_=1, to=100,
                                        orient=HORIZONTAL, length=220,
                                        font='fixedsys 12 ',
                                        bg='azure4', borderwidth=0)
        self.choose_size_button.grid(row=0, column=5, columnspan=2, padx=10)
        self.choose_size_button.set(5)

        self.undo_button = Button(self.topbar, text='Undo',
                                  bg='azure2', font='fixedsys 12 ',
                                  command=self.undo)
        self.undo_button.grid(row=0, column=7, padx=10)

        self.clear_button = Button(self.topbar, text='Clear',
                                   command=self.clear_canvas,
                                   font='fixedsys 12 ', bg='firebrick2')
        self.clear_button.grid(row=0, column=8, padx=10)

        self.save_button = Button(self.topbar, text='Save',
                                  command=self.save_file, font='fixedsys 12 ',
                                  bg='springgreen3')
        self.save_button.grid(row=0, column=10, padx=10)

        self.c = Canvas(self.framer, bg='white', width=1400, height=700)
        self.c.grid(row=2, column=0, columnspan=100)

        self.title_button.bind('<Button-1>', self.move_window)
        self.titlebar.bind("<Map>", self.mapped)
        # Show window when icon pressed in taskbar
        call_icon = Icon(self)
        self.setup()
        # runs setup function

        # buttons for diff options, its in the name

    def minimise(self):
        root.update_idletasks()
        root.overrideredirect(False)
        root.state('withdraw')
        # minimise window using pseudo window

    def mapped(self, parent):
        root.update_idletasks()
        root.overrideredirect(True)
        root.state('normal')
        # maximises window using pseudo window

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
        # uses the old cursor position and new cursor position
        # to make a line when mouse 1 is pressed

    def use_pen(self):
        self.eraser_on = False
        self.activate_button(self.pen_button)
        # activates paintbrush tool

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
        self.color_display.configure(bg=str(self.color))
        self.activate_button(self.pen_button)
        # activates the inbuilt color chooser based on your os

    def save_file(self):
        x = root.winfo_rootx()
        y = root.winfo_rooty() + self.c.winfo_y() + 22
        x1 = x + self.c.winfo_width() - 4
        y1 = y + self.c.winfo_height() - self.c.winfo_y() - 26
        filename_list = []
        for i in os.listdir('.'):
            if '.png' in i:
                filename_list.append(i)
        num_img = len(filename_list)
        ImageGrab.grab().crop((x, y, x1, y1)).save(
            'UwU_image(' + str(num_img) + ').png')
        # crops screenshot to fit the canvas and saving the file to
        # same location as UwU painter

    def undo(self, *args):
        remove_line = int(self.c.find_all()[-1]) + 1
        if int(self.c.find_all()[-1]) > 20:
            for i in range(20):
                self.c.delete(remove_line - i)
        else:
            self.c.delete(remove_line - 1)
        # deletes the last 20 inputs unless belwow 20 inputs where it deletes 1

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)
        # Pseudo eraser that uses white paint

    def help_me(self):
        helper = Help(self)
        # opens help menu (second window that has shows button usage)

    def dot(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if event.x and event.y:
            self.c.create_line(event.x, event.y, event.x + 1, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, joinstyle=ROUND,
                               smooth=TRUE, splinesteps=1000)
        # creates a dot on click, this is becasue the main
        # paintbrush can only create lines and not dots

    def clear_canvas(self):
        self.c.delete("all")
        # clears canvas

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode
        # changes appearance for buttons and whne selected and unselected

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, joinstyle=ROUND,
                               smooth=TRUE, splinesteps=1000)
        self.old_x = event.x
        self.old_y = event.y
        # continuation of paint with finer details added (rounded edges)

    def reset(self, event):
        self.old_x, self.old_y = None, None
        # refreshes to change new position to old position

    def move_window(self, partner):
        newindow_posx = (root.winfo_pointerx() - root.winfo_rootx())
        newindow_posy = (root.winfo_pointery() - root.winfo_rooty())

        def move(self):
            newpointx = root.winfo_pointerx()
            newpointy = root.winfo_pointery()
            root.geometry('1400x700+' + str(newpointx -
                                            newindow_posx) + '+' + str(
                                                newpointy - newindow_posy))
        self.title_button.bind('<B1-Motion>', move)
        #  uses screen distance to move the window by minusing the distance
        #  between screen edge and window edge to
        #  calculate the postiton of window


class Help:
    def __init__(self, partner):
        self.helpbubble = Toplevel()
        self.helpbubble.geometry('300x435+200+200')
        self.helpbubble.overrideredirect(True)
        self.helpbubble.attributes('-topmost', True)

        partner.help_button.config(state=DISABLED)
        self.helpbubble.protocol('WM_DELETE_WINDOW',
                                 partial(self.close_help, partner))

        self.helpbox = Frame(self.helpbubble)
        self.helpbox.grid(row=0)

        self.titlebar = Frame(self.helpbox)
        self.titlebar.grid(row=0)

        self.title_button = Button(self.titlebar, text='Help menu',
                                   bg='azure3', font='fixedsys 12 ',
                                   activebackground='azure3',
                                   relief=SUNKEN,
                                   borderwidth=0, padx=11, width=31, anchor=W)
        self.title_button.grid(row=0, column=0, padx=0)

        self.close_help = Button(self.titlebar, text='X',
                                 bg='firebrick', font='fixedsys 12 ',
                                 borderwidth=0, padx=7,
                                 command=partial(self.close_help, partner))
        self.close_help.grid(row=0, column=1, padx=0)

        self.title_button.bind('<Button-1>', self.move_help)

        self.help_explain = Label(self.helpbox,
                                  text='Welcome to the help menu <3 \n\n Paint'
                                  'brush: actives the paint brush tool which w'
                                  'ill work with your selected color \n\n Eras'
                                  'er: activate the eraser tool to remove part'
                                  's of your drawing \n\n Color: allows you to'
                                  ' pick a color from the color window and mak'
                                  'es it your pantbrush colow while auto activ'
                                  'ating the paintbursh fuction \n\n Brush Siz'
                                  'e: selects the pixel width of the brush on '
                                  'you slider located to the riht of the label'
                                  ' \n\n Undo: remove the last line drawn (it '
                                  'will delete less from detailed lines and mo'
                                  're from less detailed lines \n\n Clear: era'
                                  'ses the entire canvas \n\n Save: saves the '
                                  'file to the same location as UwU painter',
                                  bg='azure2',
                                  font='fixedsys 12 ',
                                  width=0, height=0,
                                  wrap=300)
        self.help_explain.grid(row=1, column=0, padx=0)
        # help window with close buttons and move widow

    def move_help(self, partner):
        helproot = self.helpbubble
        newindow_posx = (helproot.winfo_pointerx() - helproot.winfo_rootx())
        newindow_posy = (helproot.winfo_pointery() - helproot.winfo_rooty())

        def move(self):
            newpointx = helproot.winfo_pointerx()
            newpointy = helproot.winfo_pointery()
            helproot.geometry(
                '300x435+' + str(
                    newpointx - newindow_posx) + '+' + str(
                    newpointy - newindow_posy))
        self.title_button.bind('<B1-Motion>', move)
        # same move window but adapted to work with the help menu

    def close_help(self, partner):
        partner.help_button.config(state=NORMAL)
        self.helpbubble.destroy()
        # closes the help window


class Icon:  # adds an icon into the taskbar so if the window is not focusd on
    # it can be accessed easily
    def __init__(self, partner):
        self.icon = Toplevel()
        root.title('UwU painter')
        self.icon.geometry('1x1+-100+-100')
        self.icon.attributes('-alpha', 0)
        self.minimise()
        self.icon.bind("<Map>", self.mapped)
        self.icon.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        exit()

    def minimise(self):
        root.update_idletasks()
        self.icon.update_idletasks()
        self.icon.state('iconic')

    def mapped(self, parent):
        self.icon.update_idletasks()
        root.state('normal')
        root.attributes('-topmost', True)
        root.attributes('-topmost', False)
        self.minimise()


if __name__ == '__main__':
    root = Tk()
    root.title('UwU Painter')
    root.overrideredirect(True)  # turns off title bar
    root.geometry('1400x700+100+100')
    UwU = Paint(root)
    root.mainloop()
    # runs prog while stating window geometry

