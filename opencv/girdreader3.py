from scipy import ndimage
import cv2
import numpy as np
import pandas as pd

img = cv2.imread("grid1red.png")

blue = np.array([200, 70, 60])
red = np.array([30, 20, 220])

# isblue = cv2.inRange(img, blue, blue+20)
isred = cv2.inRange(img, red, red+20) > 0

labels, count = ndimage.label(~isred)

loc = np.where(labels >= 2) #label 1 is the border

# to get the location, we need to sort the block along yaxis and xaxis
df = pd.DataFrame({"y":loc[0], "x":loc[1], "label":labels[loc], "isred":isred[loc]})

grid = df.groupby("label").mean().sort_values("y")

def f(df):
    return df.sort_values("x").reset_index(drop=True)
res = grid.groupby((grid.y.diff().fillna(0) > 10).cumsum()).apply(f)

print((res.isred.unstack(1) > 0).astype(np.uint8))
