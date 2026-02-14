from libqtile import bar, layout, widget, hook
from libqtile.config import Key, Group, Screen, Drag, Click
from libqtile.lazy import lazy
import os
import subprocess

mod = "mod4"
terminal = "kitty"
launcher = "rofi -show drun"

# Catppuccin Mocha
colors = {
    "base": "#1e1e2e",
    "surface": "#313244",
    "text": "#cdd6f4",
    "subtext": "#a6adc8",
    "accent": "#89b4fa",
}

# -------------------------
# AUTOSTART
# -------------------------
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])


# -------------------------
# KEYBINDS
# -------------------------
keys = [
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "d", lazy.spawn(launcher)),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),

    # Focus movement
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Resize
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),

    Key([mod], "space", lazy.layout.flip()),
    Key([mod], "n", lazy.layout.normalize()),
]

# -------------------------
# WORKSPACES
# -------------------------
groups = [Group(i) for i in ["1","2","3","4","5"]]

for group in groups:
    keys.extend([
        Key([mod], group.name, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], group.name, lazy.window.togroup(group.name)),
    ])

# -------------------------
# LAYOUTS (GAPS)
# -------------------------
layouts = [
    layout.MonadTall(
        border_focus=colors["accent"],
        border_normal=colors["surface"],
        border_width=2,
        margin=10,
    )
]

# -------------------------
# MOUSE
# -------------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# -------------------------
# WIDGET DEFAULTS
# -------------------------
widget_defaults = dict(
    font="Consolas",
    fontsize=13,
    padding=6,
    background=colors["base"],
    foreground=colors["text"],
)

extension_defaults = widget_defaults.copy()

# -------------------------
# BAR
# -------------------------
screens = [
    Screen(
        top=bar.Bar(
            [
                # Custom icon
                widget.TextBox(
                    text="◎",
                    fontsize=16,
                    padding=8,
                ),

                # Workspace indicator styled like Waybar
                widget.GroupBox(
                    font="Consolas",
                    fontsize=13,
                    margin_y=3,
                    margin_x=0,
                    padding_y=5,
                    padding_x=8,
                    borderwidth=2,

                    active=colors["text"],
                    inactive=colors["subtext"],

                    highlight_method="line",
                    highlight_color=[colors["accent"], colors["accent"]],
                    this_current_screen_border=colors["accent"],

                    background=colors["base"],
                ),

                widget.Spacer(),

                # Middle: Date
                widget.Clock(format="%A %d %B"),

                widget.Spacer(),

                # Right modules
                widget.CPU(format="{load_percent}%"),
                widget.Memory(format="{MemPercent}%"),
                widget.Volume(fmt="{}"),
                widget.Clock(format="%I:%M %p"),
            ],
            28,
            background=colors["base"],
        )
    )
]

floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"
