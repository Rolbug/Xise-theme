import gi
import math
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk, Gio
import subprocess

properties = [
    {
        "type": "color",
        "name": "Background",
        "id": "base_color",
        "value": "#ffffff",
    },
    {
        "type": "color",
        "name": "Window Background",
        "id": "bg_color",
        "value": "#d8d8d8",
    },
    {
        "type": "color",
        "name": "Selected Items",
        "id": "accent_color",
        "value": "#97bf60",
    },
]

presets = [
    {
        "name": "Shiki Wise",
        "properties": {
            "base_color": "#ffffff",
            "bg_color": "#d8d8d8",
            "accent_color": "#97bf60"
        }
    }
]

def get_property(id):
    return next(x for x in properties if x["id"] == id)["value"]

def set_property(id, value):
    print(id)
    next(x for x in properties if x["id"] == id)["value"] = value
    print(next(x for x in properties if x["id"] == id))

def rgb_to_hex_string(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def gdk_color_to_hex_string(color):
    r = math.floor(color.red / 65535 * 255)
    g = math.floor(color.green / 65535 * 255)
    b = math.floor(color.blue / 65535 * 255)
    return rgb_to_hex_string(r, g, b)

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Xize Settings")
        self.set_border_width(10)

        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "Xize Settings"
        self.set_titlebar(headerbar)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        notebook = Gtk.Notebook()
        self.add(notebook)
        vbox.pack_start(notebook, True, True, 1)



        colors = Gtk.Grid()
        colors.set_border_width(10)
        colors.set_column_spacing(4)
        colors.set_row_spacing(4)
        notebook.append_page(colors, Gtk.Label(label="Colors"))

        widgets = Gtk.Grid()
        notebook.append_page(widgets, Gtk.Label(label="Widgets"))

        label = Gtk.Label(label="Background")
        label.set_selectable(True)
        label.set_hexpand(True)
        colors.attach(label, 1, 0, 1, 1)
        label = Gtk.Label(label="Foreground")
        label.set_selectable(True)
        label.set_hexpand(True)
        colors.attach(label, 2, 0, 1, 1)

        for i, property in enumerate(properties):
            label = Gtk.Label(label=property["name"])
            label.set_selectable(True)
            label.set_justify(Gtk.Justification.LEFT)
            label.set_halign(Gtk.Align.START)
            colors.attach(label, 0, i+1, 1, 1)
            if property["type"] == "color":
                input = Gtk.ColorButton()
                input.set_hexpand(True)

                colors.attach(input, 1, i+1, 1, 1)

                input.connect("color_set", lambda _, __, property=property: set_property(f"{property["id"]}", gdk_color_to_hex_string(_.get_color())), 1)



        confirm_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6, halign=Gtk.Align.END)
        vbox.pack_start(confirm_button_box, False, False, 0)

        ok_button = Gtk.Button(label="OK")
        confirm_button_box.pack_start(ok_button, False, False, 0)

        cancel_button = Gtk.Button(label="Cancel")
        confirm_button_box.pack_start(cancel_button, False, False, 0)

        self.button = Gtk.Button(label="Apply")
        self.button.connect("clicked", self.on_button_clicked)
        confirm_button_box.pack_start(self.button, False, False, 0)

    def on_button_clicked(self, widget):

        data = [f"$accent_color: {get_property("accent_color")};",
            f"$base_color: {get_property("base_color")};",
            f"$bg_color: {get_property("bg_color")};"]

        with open("./gtk-3.0/sass/_user-colors.scss", "w") as f:
            f.write("\n".join(data))
        subprocess.call("./parse-sass.sh", cwd="./gtk-3.0/")
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(Gio.File.new_for_path("./gtk-3.0/gtk.css"))
        screen = Gdk.Screen.get_default()
        style_context = self.get_style_context()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)



win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
