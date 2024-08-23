"""py-webview
    inputs:
        trigger: a boolean toggle should do
        points: a random data set i'm only using for this example
        html_path: path to your html file (theoretically, you should be able to build out an entire dashboard here)"""


__author__ = "sandy"


import Rhino
import System
import Eto.Drawing as drawing
import Eto.Forms as forms
import json

class SampleEtoWebViewDialog(forms.Dialog[bool]):

    def __init__(self, points, html_path):
        super().__init__()
        self.Title = 'Point Plot'
        self.Padding = drawing.Padding(10)
        self.Resizable = False  

        # convert guids to point3d
        points_coords = []
        for point in points:
            points_coords.append([point.X, point.Y])

        # load html content
        try:
            with open(html_path, 'r') as file:
                html_template = file.read()
        except Exception as e:
            Rhino.RhinoApp.WriteLine(f"Error loading HTML file: {e}")
            return

        # pass data into html
        points_json = json.dumps(points_coords)
        html_content = html_template.replace('{{points}}', points_json) # you COULD also theoretically replace this section with a string containing the entire html code if for some reason, you want to do that and then call it later using the LoadHtml method

        # create webview control
        self.m_webview = forms.WebView()
        self.m_webview.Size = drawing.Size(620, 620)  # set webview size

        # load html content
        self.m_webview.LoadHtml(html_content)

        # create layout
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        layout.AddRow(self.m_webview)

        # create dialog content
        self.Content = layout
        self.ClientSize = drawing.Size(640, 640)  # create dialog size

# webview
def DisplayWebView(points, html_path):
    dialog = SampleEtoWebViewDialog(points, html_path)
    dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

# call display
if trigger:
    DisplayWebView(points, html_path)
