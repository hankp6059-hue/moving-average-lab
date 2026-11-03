import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

# 1. 读图，换成你的手机夜景照片也可以，记得转灰度
img = cv2.imread('my_photo.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError('请把 my_photo.jpg 放在同一目录，或换成你的图片路径')

# 2. 加高斯噪声 sigma=25
np.random.seed(0)
noise = np.random.normal(0, 25, img.shape)
noisy = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)

# 3. 三种降噪
gauss = cv2.GaussianBlur(noisy, (5, 5), 1.0)
median = cv2.medianBlur(noisy, 5)
bilateral = cv2.bilateralFilter(noisy, 9, 75, 75)

# 4. 输出指标
methods = [('Noisy', noisy), ('Gaussian', gauss), ('Median', median), ('Bilateral', bilateral)]
print('| 方法 | PSNR/dB | SSIM |')
print('|---|---:|---:|')
for name, out in methods:
    p = psnr(img, out, data_range=255)
    s = ssim(img, out, data_range=255)
    print(f'| {name} | {p:.2f} | {s:.3f} |')

# 5. 保存五连对比图
h, w = img.shape
canvas = np.zeros((h, w * 5), dtype=np.uint8)
for i, im in enumerate([img, noisy, gauss, median, bilateral]):
    canvas[:, i*w:(i+1)*w] = im
cv2.imwrite('comparison.png', canvas)
for n, im in [('noisy',noisy),('gauss',gauss),('median',median),('bilateral',bilateral)]:
    cv2.imwrite(f'out_{n}.png', im)
print('已保存 comparison.png')
