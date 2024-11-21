import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
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
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.status_bar = self.CreateStatusBar()

        self.update_graph(None)

    def on_mouse_move(self, event):
        if event.inaxes != self.ax:
            return

        # Get the mouse coordinates (in axes' data space)
        mouse_x, mouse_y = event.xdata, event.ydata
        min_distance = float('inf')
        closest_point = None

        # Find the closest data point to the mouse position
        for xi, yi, zi in zip(self.x, self.y, self.z):
            distance = np.sqrt((mouse_x - xi) ** 2 + (mouse_y - yi) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_point = (xi, yi, zi)

        # Update the status bar with the closest point value
        if closest_point:
            self.status_bar.SetStatusText(f"Closest point: {closest_point}")

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
        self.x = self.points[axis[xaxis]]
        self.y = self.points[axis[yaxis]]
        self.z = self.points[axis[zaxis]]
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
            # Get the 3D data points
            x_data = self.points[self.axis_labels[3]].to_numpy()
            y_data = self.points[self.axis_labels[1]].to_numpy()
            z_data = self.points[self.axis_labels[2]].to_numpy()
            print("Test")

            # Transform the 3D data to 2D screen coordinates
            # We need to convert data coordinates to display coordinates using ax.transData
            transformed_points = [self.ax.transData.transform([x, y]) for x, y in zip(x_data, y_data)]

            # Extract the 2D screen coordinates
            screen_x = [point[0] for point in transformed_points]
            screen_y = [point[1] for point in transformed_points]

            # Compare mouse position to projected points
            mouse_x, mouse_y = event.x, event.y
            print((
                    f"Mouse x: {mouse_x:.2f}\n"
                    f"Mouse y: {mouse_y:.2f}\n"
                ))
            distances = np.sqrt((np.array(screen_x) - mouse_x) ** 2 + (np.array(screen_y) - mouse_y) ** 2)
            min_idx = np.argmin(distances)
            print(f"p: {x_data[min_idx]:.2f}\n"
                    f"Tu: {y_data[min_idx]:.2f}\n"
                    f"phi: {z_data[min_idx]:.2f}\n")
            # Set tooltip if close enough
            if distances[min_idx] < 10:  # Adjust tolerance as needed
                info = (
                    f"p: {x_data[min_idx]:.2f}\n"
                    f"Tu: {y_data[min_idx]:.2f}\n"
                    f"phi: {z_data[min_idx]:.2f}\n"
                )
                self.tooltip.SetTip(info)
                self.tooltip.Enable(True)
            else:
                self.tooltip.Enable(False)