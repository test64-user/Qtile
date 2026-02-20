# Qtile Configuration File
# X11 Session Configuration with Catppuccin Theme

import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# ===== KEYBINDINGS =====
mod = "mod4"  # Super/Windows key
terminal = "kitty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    
    # Move windows between left/right columns or move up/down in current stack
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Grow windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    
    # Terminal
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    
    # Toggle between different layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    
    # Window controls
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    
    # Qtile controls
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    # Application launcher (rofi)
    Key([mod], "space", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key([mod], "p", lazy.spawn("rofi -show run"), desc="Launch rofi run"),
    
    # Volume controls
    Key([], "F11", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Increase volume"),
    Key([], "F10", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Decrease volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Increase volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute audio"),
    
    # Brightness controls
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%"), desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-"), desc="Decrease brightness"),
    
    # Screenshot
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take screenshot"),
]

# ===== CATPPUCCIN MOCHA COLORS =====
catppuccin = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",
    "overlay2": "#9399b2",
    "overlay1": "#7f849c",
    "overlay0": "#6c7086",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
}

# ===== GROUPS/WORKSPACES =====
groups = [
    Group("www"),
    Group("term"),
    Group("code"),
    Group("music"),
    Group("etc"),
]

# Map number keys to workspace names
group_keys = ["1", "2", "3", "4", "5"]

for i, group in enumerate(groups):
    keys.extend(
        [
            # Switch to workspace using number keys
            Key([mod], group_keys[i], lazy.group[group.name].toscreen(), desc=f"Switch to group {group.name}"),
            # Move window to workspace using number keys
            Key([mod, "shift"], group_keys[i], lazy.window.togroup(group.name, switch_group=True), desc=f"Move focused window to group {group.name}"),
        ]
    )

# ===== LAYOUTS =====
layout_theme = {
    "border_width": 2,
    "margin": 8,  # Gaps between windows
    "border_focus": catppuccin["mauve"],
    "border_normal": catppuccin["surface0"],
    "border_on_single": True,  # Always show borders even for single window
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
]

# ===== WIDGETS =====
widget_defaults = dict(
    font="Consolas",
    fontsize=13,
    padding=8,
    background=catppuccin["base"],
    foreground=catppuccin["text"],
)
extension_defaults = widget_defaults.copy()

def create_widgets():
    """Create the widgets for the bar"""
    return [
        # Left side - Custom icon and workspaces
        widget.TextBox(
            text="🐧",
            fontsize=18,
            foreground=catppuccin["blue"],
            padding=10,
            mouse_callbacks={"Button1": lazy.spawn("rofi -show drun")},
        ),
        widget.Sep(
            linewidth=0,
            padding=6,
        ),
        widget.GroupBox(
            font="Consolas",
            fontsize=13,
            margin_y=3,
            margin_x=0,
            padding_y=6,
            padding_x=8,
            borderwidth=3,
            active=catppuccin["text"],
            inactive=catppuccin["surface2"],
            rounded=True,
            highlight_color=catppuccin["mauve"],  # Violet background
            highlight_method="block",
            this_current_screen_border=catppuccin["mauve"],
            this_screen_border=catppuccin["surface1"],
            other_current_screen_border=catppuccin["mauve"],
            other_screen_border=catppuccin["surface0"],
            foreground=catppuccin["text"],
            background=catppuccin["base"],
            urgent_alert_method="block",
            urgent_border=catppuccin["red"],
            disable_drag=True,
        ),
        widget.Spacer(),
        
        # Middle - Date
        widget.TextBox(
            text="📆",
            foreground=catppuccin["text"],
            fontsize=16,
            padding=5,
        ),
        widget.Clock(
            format="%d %B %A",  # 12 February Wednesday
            foreground=catppuccin["text"],
            fontsize=13,
        ),
        
        widget.Spacer(),
        
        # Right side - System info
        widget.TextBox(
            text="💻",
            foreground=catppuccin["blue"],
            fontsize=16,
            padding=0,
        ),
        widget.CPU(
            format="{load_percent}%",
            foreground=catppuccin["text"],
            update_interval=2,
            padding=5,
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=catppuccin["surface1"],
        ),
        widget.TextBox(
            text="🧠",
            foreground=catppuccin["green"],
            fontsize=16,
            padding=0,
        ),
        widget.Memory(
            format="{MemPercent}%",
            foreground=catppuccin["text"],
            update_interval=2,
            padding=5,
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=catppuccin["surface1"],
        ),
        widget.TextBox(
            text="🔊",
            foreground=catppuccin["yellow"],
            fontsize=16,
            padding=0,
        ),
        widget.Volume(
            foreground=catppuccin["text"],
            padding=5,
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=catppuccin["surface1"],
        ),
        widget.TextBox(
            text="⏱️",
            foreground=catppuccin["text"],
            fontsize=16,
            padding=0,
        ),
        widget.Clock(
            format="%I:%M %p",  # 01:10 PM
            foreground=catppuccin["text"],
            fontsize=13,
            padding=5,
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=catppuccin["surface1"],
        ),
        # Systray (only shows when relevant)
        widget.Systray(
            padding=5,
        ),
        widget.Sep(
            linewidth=0,
            padding=5,
        ),
    ]

# ===== SCREENS =====
screens = [
    Screen(
        top=bar.Bar(
            create_widgets(),
            36,  # Bar height (increased from 30)
            background=catppuccin["base"],
            opacity=0.95,
        ),
    ),
]

# ===== MOUSE BINDINGS =====
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# ===== FLOATING WINDOWS =====
floating_layout = layout.Floating(
    float_rules=[
        # Default floating rules
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
        Match(wm_class="Nitrogen"),  # Nitrogen (wallpaper setter)
        Match(wm_class="Pavucontrol"),  # PulseAudio volume control
        Match(wm_class="Arandr"),  # Screen layout editor
    ],
    **layout_theme,
)

# ===== GENERAL SETTINGS =====
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"

# ===== STARTUP APPLICATIONS =====
@hook.subscribe.startup_once
def autostart():
    """Run autostart script"""
    home = os.path.expanduser("~")
    
    # Merge .Xresources
    subprocess.run([f"{home}/.fehbg"])
    subprocess.run(["xrdb", "-merge", f"{home}/.Xresources"])
    
    # Set cursor theme and size
    subprocess.run(["xsetroot", "-cursor_name", "left_ptr"])
    subprocess.Popen([
        "xsetroot", "-xcf", 
        "/usr/share/icons/Adwaita/cursors/left_ptr", "16"
    ])
    
    # You can add more startup applications here
    # Examples:
    # subprocess.Popen(["picom", "-b"])  # Compositor
    # subprocess.Popen(["nitrogen", "--restore"])  # Wallpaper
    # subprocess.Popen(["nm-applet"])  # Network manager
    # subprocess.Popen(["volumeicon"])  # Volume icon
