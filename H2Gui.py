import wx

from MainFrame import MainFrame


class H2Gui(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.frame.Show()
        return True


# Run the application
if __name__ == "__main__":
    app = H2Gui()
    app.MainLoop()
