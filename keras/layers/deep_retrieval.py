import numpy as np


# def get_rmac_region_coordinates(H, W, L):
def rmac_regions(H, W, L):
    # Almost verbatim from Tolias et al Matlab implementation.
    # Could be heavily pythonized, but really not worth it...
    # Desired overlap of neighboring regions
    ovr = 0.4
    # Possible regions for the long dimension
    steps = np.array((2, 3, 4, 5, 6, 7), dtype=np.float32)
    w = np.minimum(H, W)

    b = (np.maximum(H, W) - w) / (steps - 1)
    # steps(idx) regions for long dimension. The +1 comes from Matlab
    # 1-indexing...
    idx = np.argmin(np.abs(((w**2 - w * b) / w**2) - ovr)) + 1

    # Region overplus per dimension
    Wd = 0
    Hd = 0
    if H < W:
        Wd = idx
    elif H > W:
        Hd = idx

    regions_xywh = []
    for l in range(1, L+1):
        wl = np.floor(2 * w / (l + 1))
        wl2 = np.floor(wl / 2 - 1)
        # Center coordinates
        if l + Wd - 1 > 0:
            b = (W - wl) / (l + Wd - 1)
        else:
            b = 0
        cenW = np.floor(wl2 + b * np.arange(l - 1 + Wd + 1)) - wl2
        # Center coordinates
        if l + Hd - 1 > 0:
            b = (H - wl) / (l + Hd - 1)
        else:
            b = 0
        cenH = np.floor(wl2 + b * np.arange(l - 1 + Hd + 1)) - wl2

        for i_ in cenH:
            for j_ in cenW:
                regions_xywh.append([j_, i_, wl, wl])

    # Round the regions. Careful with the borders!
    for i in range(len(regions_xywh)):
        for j in range(4):
            regions_xywh[i][j] = int(round(regions_xywh[i][j]))
        if regions_xywh[i][0] + regions_xywh[i][2] > W:
            regions_xywh[i][0] -= ((regions_xywh[i][0] +
                                    regions_xywh[i][2]) - W)
        if regions_xywh[i][1] + regions_xywh[i][3] > H:
            regions_xywh[i][1] -= ((regions_xywh[i][1] +
                                    regions_xywh[i][3]) - H)
    return np.array(regions_xywh).astype(np.int32)
