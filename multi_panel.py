# -*- coding: utf-8 -*-
import wx 
from wx.lib import scrolledpanel


class SettingsPanel(wx.Panel):
    def __init__(self, parent, title=""):
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (300, 300))
        self.title = title
        self.text = wx.TextCtrl(self, style = wx.TE_MULTILINE) 
        self.text.AppendText( "Current selection:" + self.title)

    def onPanelActivated(self):
        self.Show()

    def onPanelDeactivated(self):
        self.Hide()

    def isValid(self):
        return True


class Mywin(wx.Frame): 
    
    def __init__(self, parent, title, initialPanel=None): 
        super(Mywin, self).__init__(parent, title = title, size = (350,300))
        
        panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.HORIZONTAL) 

        self.languagesMap = {}
        self.languages = ['C', 'C++', 'Java', 'Python', 'Perl', 'JavaScript', 'PHP', 'VB.NET','C#']   
        self.lst = wx.ListBox(panel, size = (100,-1), style = wx.LB_SINGLE)

        self.container = scrolledpanel.ScrolledPanel(
			parent = panel,
			id = -1,
			style = wx.TAB_TRAVERSAL | wx.BORDER_THEME,
		)
        self.currentPanel = None

        # ----- initial multi-panel ----- 
        for language in self.languages:
            panel_of_language = SettingsPanel(parent=self.container, title=language)
            panel_of_language.Hide()
            self.languagesMap[language] = panel_of_language
            self.lst.Append((panel_of_language.title,))
        
        box.Add(self.lst, 0, wx.EXPAND) 
        box.Add(self.container, 1, wx.EXPAND)
        
        self.container.Layout()
        panel.SetSizer(box) 
        panel.Fit() 

        # -------- menubar --------
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY,  "Add Panels")
        self.Bind(wx.EVT_MENU, self.addNewPanel, switch_panels_menu_item)
        menubar.Append(fileMenu, 'Add')
        self.SetMenuBar(menubar)

        self.Centre() 
        self.lst.Bind(wx.EVT_LISTBOX, self.onPanelChange) 
        self.Show(True)  

    def onPanelChange(self, evt):
        newPanelID = self.languages.index(evt.GetEventObject().GetStringSelection())
        # newIndex = evt.GetIndex()
        self.doChange(newPanelID)

    def doChange(self, newPanelID):
		oldPanel = self.currentPanel

		self.container.Freeze()
		newPanel = self.getPanel(newPanelID)

		if oldPanel:
			oldPanel.onPanelDeactivated()
		self.currentPanel = newPanel
		newPanel.onPanelActivated()

		self.container.Layout()
		self.container.SetupScrolling()

		self.container.SetLabel(newPanel.title)
		self.container.Thaw()
    
    def getPanel(self, index):
        language = self.languages[index]
        panel = self.languagesMap[language]

        return panel

    def addNewPanel(self, event):
        # add new panel with input 
        dlg = wx.TextEntryDialog(self, 'Enter your new panel') 
		
        if dlg.ShowModal() == wx.ID_OK: 
            new_language = dlg.GetValue()
            new_panel = SettingsPanel(parent=self.container, title=new_language)
            new_panel.Hide()
            self.languagesMap[new_language] = new_panel
            self.languages.append(new_language)
            self.lst.Append((new_language,))
        dlg.Destroy() 
		
ex = wx.App() 
Mywin(None,'ListBox Demo') 
ex.MainLoop()