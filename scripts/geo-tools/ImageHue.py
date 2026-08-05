"""
Calculates the luminance values of an image at specified points.

Inputs:
    image_path: String (item access, string)
    points: List of Points (list access, pt)

Outputs:
    values: List of Numbers (The luminance values at each point)
"""

try:
    ghenv.Component.Name = "ImageHue"
    ghenv.Component.NickName = "IH"
    ghenv.Component.Description = "Calculates the luminance values of an image at specified points."
except NameError:
    pass

import System.Drawing as sd

def get_image_values(img_path, pts):
    if not img_path or not pts:
        return []
        
    try:
        bmp = sd.Bitmap(img_path)
    except Exception as e:
        print("Error loading image: " + str(e))
        return []
        
    w = bmp.Width - 1
    h = bmp.Height - 1
    
    min_x = min([p.X for p in pts])
    max_x = max([p.X for p in pts])
    min_y = min([p.Y for p in pts])
    max_y = max([p.Y for p in pts])
    
    range_x = max_x - min_x
    range_y = max_y - min_y
    
    if range_x == 0: range_x = 1.0
    if range_y == 0: range_y = 1.0

    out_values = []
    
    for pt in pts:
        norm_x = (pt.X - min_x) / range_x
        norm_y = (pt.Y - min_y) / range_y
        
        px = int(norm_x * w)
        py = int((1.0 - norm_y) * h)
        
        px = max(0, min(px, w))
        py = max(0, min(py, h))
        
        color = bmp.GetPixel(px, py)
        
        luminance = (0.299 * color.R + 0.587 * color.G + 0.114 * color.B) / 255.0
        out_values.append(luminance)
        
    bmp.Dispose() 
    
    return out_values

if 'image_path' in globals() and 'points' in globals():
    values = get_image_values(image_path, points)
