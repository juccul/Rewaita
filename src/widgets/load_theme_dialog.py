import gi, os, gettext
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
from .theme_page import create_color_thumbnail_button, load_colors_from_css

_ = gettext.gettext

class LoadThemeDialog(Adw.Window):
    def __init__(self, parent, on_load_callback):
        super().__init__(modal=True, transient_for=parent)
        self.set_default_size(800, 600)
        self.set_title(_("Load Theme"))

        self.on_load_callback = on_load_callback
        self.parent_window = parent

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(box)

        header = Adw.HeaderBar()
        box.append(header)

        # Tabs for Light / Dark
        stack = Adw.ViewStack()
        switcher_bar = Adw.ViewSwitcher(stack=stack, policy=Adw.ViewSwitcherPolicy.WIDE)

        box.append(switcher_bar)
        box.append(stack)

        for theme_type in ["light", "dark"]:
            scrolled = Gtk.ScrolledWindow()
            flowbox = Gtk.FlowBox(
                column_spacing=12,
                row_spacing=12,
                max_children_per_line=3,
                homogeneous=True,
                margin_start=12,
                margin_end=12,
                margin_top=12,
                margin_bottom=12,
                selection_mode=Gtk.SelectionMode.NONE
            )

            themes_dir = os.path.join(parent.data_dir, theme_type)
            if os.path.exists(themes_dir):
                themes = sorted(os.listdir(themes_dir))
                for theme in themes:
                    if not theme.endswith(".css"): continue

                    theme_path = os.path.join(themes_dir, theme)
                    colors = load_colors_from_css(theme_path)
                    name = os.path.splitext(theme)[0]

                    btn = create_color_thumbnail_button(colors, name, _("Preview"))
                    btn.connect("clicked", self.on_theme_clicked, theme_path, name, theme_type)

                    flowbox.append(btn)

            scrolled.set_child(flowbox)
            page = stack.add_titled(scrolled, theme_type, theme_type.capitalize())
            page.set_icon_name("weather-clear-symbolic" if theme_type == "light" else "weather-clear-night-symbolic")

    def on_theme_clicked(self, btn, path, name, theme_type):
        self.on_load_callback(path, name, theme_type)
        self.close()
