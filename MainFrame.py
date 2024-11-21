import wx
import wx.html2 as webview
import plotly.graph_objs as go
import plotly.io as pio
from bs4 import BeautifulSoup

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        # Set up the main panel
        self.panel = wx.Panel(self)

        # Create a BoxSizer for horizontal layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Left panel for commands
        left_panel = wx.Panel(self.panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        combo_label = wx.StaticText(left_panel, label="Choose Option:")
        self.combo_box = wx.ComboBox(left_panel, choices=["Option 1", "Option 2", "Option 3"])
        left_sizer.Add(combo_label, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.combo_box, 0, wx.ALL | wx.EXPAND, 5)
        left_panel.SetSizer(left_sizer)

        # Right panel for Plotly plot
        right_panel = wx.Panel(self.panel)
        # Create a Plotly figure to display
        fig = go.Figure(data=go.Scatter(y=[2, 3, 1, 4, 5], mode='lines', name='Sample Line'))

        # Convert Plotly figure to HTML
        html_str = pio.to_html(fig, full_html=True)

        # Use WebView to display the HTML
        soup = BeautifulSoup(html_str, 'html.parser')
        body_content = soup.body.decode_contents()  # Extract inner HTML of the body tag
        self.web_view = webview.WebView.New(right_panel, backend=wx.html2.WebViewBackendEdge)
        self.web_view.SetPage(body_content, "about:blank")
        #self.web_view.LoadURL("http://www.google.com")
        # Sizer for right panel to hold the WebView
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(self.web_view, 1, wx.EXPAND)
        right_panel.SetSizer(right_sizer)

        # Add both left and right panels to the main sizer
        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 10)  # Left side with ComboBox
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 10)  # Right side with Plotly plot

        # Set main sizer
        self.panel.SetSizer(main_sizer)

        # Set frame size
        self.SetSize((800, 600))
        self.SetTitle("H2 Gui")