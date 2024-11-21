import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


class MainFrame(wx.Frame):
    def __init__(self, parent, title = "H2 Gui"):
        super().__init__(parent, title=title, size=(1200, 800))

        # Panel
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)

        # Left-side controls (dropdown menus)
        control_panel = wx.Panel(panel)
        control_sizer = wx.BoxSizer(wx.VERTICAL)
        control_panel.SetSizer(control_sizer)

        self.axis_labels = ["p", "Tu", "phi", "egr"]

        self.xaxis_choice = wx.Choice(control_panel, choices=self.axis_labels)
        self.yaxis_choice = wx.Choice(control_panel, choices=self.axis_labels)
        self.zaxis_choice = wx.Choice(control_panel, choices=self.axis_labels)

        self.xaxis_choice.SetSelection(3)  # Default selection
        self.yaxis_choice.SetSelection(1)
        self.zaxis_choice.SetSelection(2)

        control_sizer.Add(wx.StaticText(control_panel, label="X Axis"), 0, wx.ALL, 5)
        control_sizer.Add(self.xaxis_choice, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(wx.StaticText(control_panel, label="Y Axis"), 0, wx.ALL, 5)
        control_sizer.Add(self.yaxis_choice, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(wx.StaticText(control_panel, label="Z Axis"), 0, wx.ALL, 5)
        control_sizer.Add(self.zaxis_choice, 0, wx.ALL | wx.EXPAND, 5)

        update_button = wx.Button(control_panel, label="Update Graph")
        update_button.Bind(wx.EVT_BUTTON, self.update_graph)
        control_sizer.Add(update_button, 0, wx.ALL | wx.CENTER, 10)

        # Right-side graph (Matplotlib canvas)
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(panel, -1, self.figure)

        # Add panels to sizer
        sizer.Add(control_panel, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 10)

        # Load data and initialize graph
        self.data = pd.read_csv("tempTable.csv")
        self.data["lambda"] = 1.0 / self.data["phi"]
        self.tooltip = wx.ToolTip("")
        self.tooltip.Enable(False)  # Start with tooltips disabled
        self.SetToolTip(self.tooltip)

        # Bind mouse motion event for interactivity
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

        self.update_graph(None)

    def update_graph(self, event):
        self.ax = self.figure.add_subplot(projection='3d')
        self.figure.clear()
        self.ax = self.figure.add_subplot(111, projection='3d')

        # Extract axis selections
        xaxis = self.xaxis_choice.GetSelection()
        yaxis = self.yaxis_choice.GetSelection()
        zaxis = self.zaxis_choice.GetSelection()

        # Get unused axis for slicing
        waxis = [i for i in range(len(self.axis_labels)) if i not in [xaxis, yaxis, zaxis]][0]
        isoID = 0
        axis = self.axis_labels

        # Process data
        ranges = {a: np.unique(self.data[a].to_numpy()) for a in axis}
        subData = self.data.loc[self.data[axis[waxis]] == ranges[axis[waxis]][isoID]]
        where = np.invert(subData["completed"].to_numpy())

        # Plot data
        self.points = subData[where]  # Save for hover functionality
        self.scatter = self.ax.scatter(
            self.points[axis[xaxis]],
            self.points[axis[yaxis]],
            self.points[axis[zaxis]],
            alpha=1
        )

        # Set axis limits and ticks
        self.ax.set_xlim([ranges[axis[xaxis]].min(), ranges[axis[xaxis]].max()])
        self.ax.set_ylim([ranges[axis[yaxis]].min(), ranges[axis[yaxis]].max()])
        self.ax.set_zlim([ranges[axis[zaxis]].min(), ranges[axis[zaxis]].max()])

        self.ax.set_xticks(np.linspace(ranges[axis[xaxis]].min(), ranges[axis[xaxis]].max(), 5))
        self.ax.set_yticks(np.linspace(ranges[axis[yaxis]].min(), ranges[axis[yaxis]].max(), 5))
        self.ax.set_zticks(np.linspace(ranges[axis[zaxis]].min(), ranges[axis[zaxis]].max(), 5))

        self.ax.set_xlabel(axis[xaxis], labelpad=20)
        self.ax.set_ylabel(axis[yaxis], labelpad=20)
        self.ax.set_zlabel(axis[zaxis], labelpad=20)

        self.canvas.draw()

    def on_hover(self, event):
        if event.inaxes == self.ax:
            # Get the mouse position in data coordinates
            x, y, z = event.xdata, event.ydata, event.zdata

            if x is None or y is None or z is None:
                self.tooltip.Enable(False)
                return

            # Check proximity to points
            distances = np.sqrt(
                (self.points[self.axis_labels[0]] - x) ** 2 +
                (self.points[self.axis_labels[1]] - y) ** 2 +
                (self.points[self.axis_labels[2]] - z) ** 2
            )
            min_idx = distances.idxmin()

            # Set tooltip if close enough
            if distances[min_idx] < 0.5:  # Adjust tolerance as needed
                row = self.points.iloc[min_idx]
                info = (
                    f"p: {row['p']:.2f}\n"
                    f"Tu: {row['Tu']:.2f}\n"
                    f"phi: {row['phi']:.2f}\n"
                    f"egr: {row['egr']:.2f}"
                )
                self.tooltip.SetTip(info)
                self.tooltip.Enable(True)
            else:
                self.tooltip.Enable(False)
