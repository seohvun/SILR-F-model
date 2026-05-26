import modmodelfinal as md
import matplotlib.pyplot as plt
import numpy as np

res = []
wall = [0, 2, 5, 8, 9]
for i in wall:
        res.append(md.main(i))

plt.scatter(wall, res)

plt.legend()
plt.grid(True, linestyle=':')

plt.tight_layout()

z = np.polyfit(wall, res, 1)  # 계산기 돌리기
p = np.poly1d(z)             # 선으로 변신
plt.plot(wall, p(wall), "r--",label=f'Trendline: y={z[0]:.2f}x+{z[1]:.2f}') # 그리기!
plt.xlabel('Wall Intensity (W)')
plt.ylabel('Result (L/I Ratio or Bias)')
plt.show()