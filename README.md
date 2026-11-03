# denoise-experiment：自摄照片的传统降噪对比

秦靖涵 · 中山大学物理系 大一 · 2026年10月

**在线网页：** https://hankp6059-hue.github.io/moving-average-lab/ 。可以在浏览器里实时调参数、拖动对比降噪前后的照片，也能换成你自己的照片。

## 实验 1：三种传统滤波对比
- 图像：本人手机拍摄的美人蕉照片 `my_photo.jpg`，转灰度（960×1282）
- 加噪：高斯噪声 σ=25，`np.random.seed(0)`
- 方法：高斯滤波 5×5（σ=1.0）、中值滤波 5×5、双边滤波（d=9, σColor=75, σSpace=75）
- 指标：PSNR、SSIM（scikit-image）；另按 Sobel 梯度划分细节区（梯度最大的 20% 像素）和平坦区（梯度最小的 50%），分别计算 PSNR

| 方法 | PSNR/dB | SSIM | 细节区 PSNR/dB | 平坦区 PSNR/dB |
|---|---:|---:|---:|---:|
| 加噪图 | 20.26 | 0.322 | 20.22 | 20.29 |
| 高斯滤波 | 29.98 | 0.781 | 28.37 | 30.71 |
| 中值滤波 | 29.56 | 0.785 | 27.03 | 31.13 |
| 双边滤波 | 29.90 | 0.821 | 26.85 | 32.35 |

结论：双边滤波 SSIM 最高、画面最干净，但细节区 PSNR 最低（26.85 dB，高斯 28.37 dB）——看起来干净不等于细节真实。

## 文件

| 文件 | 说明 |
| --- | --- |
| `index.html` | 互动网页，纯前端、无第三方库 |
| `canna_gray.png` | 实验用的灰度原图（与 `cv2.imread(..., IMREAD_GRAYSCALE)` 结果逐像素相同），网页用它保证结果可复现 |
| `my_photo.jpg` | 彩色原片 |
| `denoise_experiment.py` | 原实验代码 |
| `results/` | Python 输出的降噪结果图和指标表 `metrics.csv` |

## 网页与 Python 的一致性

网页按原实验的算法在浏览器里重新实现了一遍，默认参数下与 Python 结果对照：

- 噪声：实现了 numpy 旧版随机数（MT19937 + 极坐标法），种子为 0 时与 `np.random.seed(0)` 生成的加噪图逐像素相同
- 高斯滤波、中值滤波：按 OpenCV 的 8 位定点算法实现，与 `results/` 中的输出逐像素相同
- 双边滤波：122 万个像素中有 24 个差 1（浮点运算顺序不同）
- 四项指标与上表完全一致

## 复现

```bash
pip install -r requirements.txt
python denoise_experiment.py
```

运行环境：Python 3.13、OpenCV 5.0、scikit-image 0.26。

本地打开网页需要通过本地服务器（直接双击 `index.html` 时浏览器会拦截读取图片）：

```bash
python -m http.server
```

然后访问 http://localhost:8000 。
