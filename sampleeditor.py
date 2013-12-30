#!/usr/bin/env python
import wx, os
ID_TEXT=1000

ID_NEW=100
ID_OPEN=101
ID_SAVE=102
ID_SAVEAS=103
ID_QUIT=104

ID_UNDO=200
ID_REDO=201
ID_CUT=202
ID_COPY=203
ID_PASTE=204
ID_DELETE=205
ID_SELECT_ALL=206

ID_VIEW_STATUSBAR=300

ID_ABOUT=400

ID_T_NEW=1
ID_T_OPEN=2
ID_T_SAVE=3
ID_T_UNDO=4
ID_T_REDO=5
ID_T_CUT=6
ID_T_COPY=7
ID_T_PASTE=8
class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size = (800,600))

        # variables
        self.modify = False
        self.undos=[]
        self.redos=[]

        self.text = wx.TextCtrl(self, ID_TEXT, style=wx.TE_MULTILINE)
        self.text.Bind(wx.EVT_TEXT, self.OnTextChanged, id=ID_TEXT)
        self.text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.backuptext = self.text.GetValue()
        self.statusbar = self.CreateStatusBar() #Create the statusbar

        # Setting up the "File" menu
        filemenu= wx.Menu()
        tempitem=wx.MenuItem(filemenu, ID_NEW, "&New"," Create a new document")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/document-new.png'))
        filemenu.AppendItem(tempitem)
        tempitem=wx.MenuItem(filemenu, ID_OPEN, "&Open"," Open a file")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/document-open.png'))
        filemenu.AppendItem(tempitem)
        tempitem=wx.MenuItem(filemenu, ID_SAVE, "&Save"," Save the current file")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/document-save.png'))
        filemenu.AppendItem(tempitem)
        tempitem=wx.MenuItem(filemenu, ID_SAVEAS, "Save &As..."," Save the current file with a different name")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/document-save-as.png'))
        filemenu.AppendItem(tempitem)

        filemenu.AppendSeparator()

        tempitem=wx.MenuItem(filemenu, ID_QUIT,"&Quit"," Quit the program")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/application-exit.png'))
        filemenu.AppendItem(tempitem)

        #Creating the "Edit" menu
        editmenu=wx.Menu()
        tempitem=wx.MenuItem(editmenu, ID_UNDO,"&Undo","Undo the last action")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/edit-undo.png'))
        editmenu.AppendItem(tempitem)

        tempitem=wx.MenuItem(editmenu, ID_REDO,"&Redo","Redo the last undone action")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/edit-redo.png'))
        editmenu.AppendItem(tempitem)

        editmenu.AppendSeparator()

        tempitem=wx.MenuItem(editmenu, ID_CUT,"Cu&t","Cut the selection")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/gnome/16x16/actions/edit-cut.png'))
        editmenu.AppendItem(tempitem)

        tempitem=wx.MenuItem(editmenu, ID_COPY,"&Copy","Copy the selection")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/gnome/16x16/actions/edit-copy.png'))
        editmenu.AppendItem(tempitem)

        tempitem=wx.MenuItem(editmenu, ID_PASTE,"&Paste","Paste the clipboard")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/gnome/16x16/actions/edit-paste.png'))
        editmenu.AppendItem(tempitem)

        tempitem=wx.MenuItem(editmenu, ID_DELETE,"&Delete","Delete the selected text")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/gnome/16x16/actions/edit-delete.png'))
        editmenu.AppendItem(tempitem)

        editmenu.AppendSeparator()

        tempitem=wx.MenuItem(editmenu, ID_SELECT_ALL,"Select &All","Select the entire document")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/gnome/16x16/actions/edit-select-all.png'))
        editmenu.AppendItem(tempitem)

        # Setting up the "View" menu
        viewmenu=wx.Menu()
        self.statusbaritem=wx.MenuItem(viewmenu, ID_VIEW_STATUSBAR,"&Statusbar","Show or hide the statusbar in the current window")
        self.statusbaritem.SetCheckable(True)

        viewmenu.AppendItem(self.statusbaritem)
        self.statusbaritem.Check()
        
        # Setting up the "Help" menu
        helpmenu=wx.Menu()
        tempitem=wx.MenuItem(helpmenu, ID_ABOUT, "&About"," About this application")
        tempitem.SetBitmap(wx.Bitmap('/usr/share/icons/Human/16x16/actions/gtk-about.png'))
        helpmenu.AppendItem(tempitem)
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(editmenu, "&Edit") # Adding the "editmenu" to the MenuBar
        menuBar.Append(viewmenu, "&View") # Adding the "viewmenu" to the MenuBar
        menuBar.Append(helpmenu, "&Help") # Adding the "helpmenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        wx.EVT_MENU(self, ID_NEW, self.OnNew)
        wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, ID_SAVEAS, self.OnSaveAs)
        wx.EVT_MENU(self, ID_QUIT, self.OnQuit)

        wx.EVT_MENU(self, ID_UNDO, self.OnUndo)
        wx.EVT_MENU(self, ID_REDO, self.OnRedo)
        wx.EVT_MENU(self, ID_CUT, self.OnCut)
        wx.EVT_MENU(self, ID_COPY, self.OnCopy)
        wx.EVT_MENU(self, ID_PASTE, self.OnPaste)
        wx.EVT_MENU(self, ID_DELETE, self.OnDelete)
        wx.EVT_MENU(self, ID_SELECT_ALL, self.OnSelectAll)

        wx.EVT_MENU(self, ID_VIEW_STATUSBAR, self.ToggleStatusBar)

        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)

        #Make the toolbar
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)
        toolbar.AddSimpleTool(ID_T_NEW, wx.Image('/usr/share/icons/Human/24x24/actions/document-new.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Create a new document', '')
        toolbar.AddSimpleTool(ID_T_OPEN, wx.Image('/usr/share/icons/Human/24x24/actions/document-open.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Open a file', '')
        toolbar.AddSimpleTool(ID_T_SAVE, wx.Image('/usr/share/icons/Human/24x24/actions/document-save.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Save the current file', '')
        toolbar.AddSeparator()
        toolbar.AddSimpleTool(ID_T_UNDO, wx.Image('/usr/share/icons/Human/24x24/actions/edit-undo.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Undo the last action', '')
        toolbar.AddSimpleTool(ID_T_REDO, wx.Image('/usr/share/icons/Human/24x24/actions/edit-redo.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Redo the last undone action', '')
        toolbar.AddSeparator()
        toolbar.AddSimpleTool(ID_T_CUT, wx.Image('/usr/share/icons/gnome/24x24/actions/edit-cut.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Cut the selection', '')
        toolbar.AddSimpleTool(ID_T_COPY, wx.Image('/usr/share/icons/gnome/24x24/actions/edit-copy.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Copy the selection', '')
        toolbar.AddSimpleTool(ID_T_PASTE, wx.Image('/usr/share/icons/gnome/24x24/actions/edit-paste.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Paste the clipboard', '')
        self.Bind(wx.EVT_TOOL, self.OnNew, id=ID_T_NEW)
        self.Bind(wx.EVT_TOOL, self.OnOpen, id=ID_T_OPEN)
        self.Bind(wx.EVT_TOOL, self.OnSave, id=ID_T_SAVE)

        self.Bind(wx.EVT_TOOL, self.OnUndo, id=ID_T_UNDO)
        self.Bind(wx.EVT_TOOL, self.OnRedo, id=ID_T_REDO)
        self.Bind(wx.EVT_TOOL, self.OnCut, id=ID_T_CUT)
        self.Bind(wx.EVT_TOOL, self.OnCopy, id=ID_T_COPY)
        self.Bind(wx.EVT_TOOL, self.OnPaste, id=ID_T_PASTE)
        self.SetToolBar(toolbar)
        self.Show(True)
    def OnNew(self, e):
        self.filename, self.dirname = 'New File',''
        self.text.Clear()
        self.SetTitle("IsMEdit - "+self.filename)
    def OnOpen(self, e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=open(os.path.join(self.dirname,self.filename),'r')
            self.text.SetValue(f.read())
            f.close()
            self.SetTitle("IsMEdit - "+self.filename)
        dlg.Destroy()
    def OnSaveAs(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=open(os.path.join(self.dirname,self.filename),'w')
            f.write(self.text.GetValue().encode('utf8'))
            f.close()
        dlg.Destroy()
        self.SetTitle("IsMEdit - "+self.filename)
    def OnSave(self, e):
        try:
            f=open(os.path.join(self.dirname,self.filename),'w')
            f.write(self.text.GetValue().encode('utf8'))
        except AttributeError: self.OnSaveAs(e)
    def OnQuit(self, e):
        if self.modify:
            dlg = wx.MessageDialog(self, 'Save before exiting?', '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL |  wx.ICON_QUESTION)
            val = dlg.ShowModal()
            if val == wx.ID_YES:
                self.OnSave(e)
                self.Destroy()
            elif val == wx.ID_CANCEL:
                dlg.Destroy()
            else:
                self.Destroy()
        else:
            self.Destroy()
    def OnUndo(self, e):
        place=self.text.GetInsertionPoint()
        self.redos.append(self.text.GetValue())
        self.text.SetValue(self.undos[len(self.undos)-1])
        self.text.SetInsertionPoint(place)
        self.undos=self.undos[:-1]
        if len(self.redos) >= 30: self.redos=self.redos[1:]
    def OnRedo(self, e):
        place=self.text.GetInsertionPoint()
        self.text.SetValue(self.redos[len(self.redos)-1])
        self.text.SetInsertionPoint(place)
        self.redos=self.redos[:-1]
    def OnCut(self, e):
        self.text.Cut()
    def OnCopy(self, e):
        self.text.Copy()
    def OnPaste(self, e):
        self.text.Paste()
    def OnDelete(self, e):
        frm, to = self.text.GetSelection()
        self.text.Remove(frm, to)
    def OnSelectAll(self, e):
        self.text.SelectAll()
    def ToggleStatusBar(self, e):
        if self.statusbar.IsShown():
            self.statusbar.Hide()
            self.statusbaritem.Check(False)
        else:
            self.statusbar.Show()
            self.statusbaritem.Check()

    def OnAbout(self,e):
        d= wx.MessageDialog(self, "(I)an's (M)ini (Edit)or\nA simple editor written in wxPython","About IsMEdit", wx.OK) # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.
    def OnTextChanged(self, e):
        self.modify=True
        e.Skip()
    def OnKeyDown(self, e):
        keycode = e.GetKeyCode()
        self.undos.append(self.text.GetValue())
        if len(self.undos) >= 30: self.undos=self.undos[1:]
        e.Skip()

app = wx.PySimpleApp()
frame = MainWindow(None, -1, "IsMEdit - New File")
frame.SetIcon(wx.Icon('/usr/share/icons/gnome/16x16/apps/accessories-text-editor.png', wx.BITMAP_TYPE_PNG))
app.MainLoop()  
