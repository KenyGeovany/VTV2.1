from PIL import Image, ImageTk


def read_image(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.Resampling.LANCZOS))


def center_window(window, app_width, app_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - app_width) / 2)
    y = int((screen_height - app_height) / 2)
    return window.geometry(f"{app_width}x{app_height}+{x}+{y}")
