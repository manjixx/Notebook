import numpy as np
from typing import List
import matplotlib.pyplot as plt
import matplotlib
import random
matplotlib.use('TkAgg')  # 或者 'TkAgg'，具体取决于你想保存图 or 弹窗展示图
# 设置matplotlib全局字体
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


# -------------------- 输入参数 --------------------
class Version:
    def __init__(self, vid: int, size_gb: float, deadline: int,
                 users: int, traffic_pattern: List[float]):
        self.id = vid
        self.size_gb = size_gb  # 安装包大小GB
        self.deadline = deadline  # 最晚发布日期（0-based）
        self.users = users  # 受影响用户数
        self.traffic_pattern = traffic_pattern  # 7天流量分布


VERSIONS = [
    Version(0, 2.5, 10, 1e6, [0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0]),
    Version(1, 1.8, 15, 8e5, [0.5, 0.3, 0.15, 0.05, 0.0, 0.0, 0.0]),
    Version(2, 3.0, 5, 1.2e6, [0.35, 0.35, 0.2, 0.1, 0.0, 0.0, 0.0]),
    Version(3, 1.2, 25, 5e5, [0.6, 0.25, 0.1, 0.05, 0.0, 0.0, 0.0]),
    Version(4, 2.0, 20, 9e5, [0.45, 0.35, 0.15, 0.05, 0.0, 0.0, 0.0]),
]

MONTH_DAYS = 30
NIGHT_HOURS = set(range(0, 8))  # 夜间时段
WEEKENDS = [6, 13, 20, 27]  # 周末日期
MIN_RELEASE_RATIO = 0.1  # 最小开放比例

# -------------------- 遗传算法参数 --------------------
POP_SIZE = 50
GEN_MAX = 200
MUTATE_PROB = 0.2
ELITE_RATE = 0.1


# -------------------- 核心数据结构 --------------------
class Chromosome:
    def __init__(self):
        self.genes = []  # [(release_day, is_night, ratio), ...]
        self.fitness = float('inf')

    def clone(self):
        c = Chromosome()
        c.genes = self.genes.copy()
        c.fitness = self.fitness
        return c


# -------------------- 费用计算引擎 --------------------
class CostCalculator:
    def __init__(self, versions: List[Version]):
        self.versions = versions
        self.hourly_bw = np.zeros(MONTH_DAYS * 24)  # 每小时带宽（GB）
        self.night_mask = np.array([h in NIGHT_HOURS for _ in range(MONTH_DAYS) for h in range(24)])

    def clear(self):
        self.hourly_bw.fill(0)

    def apply_release(self, version: Version, release_day: int,
                      is_night: bool, ratio: float):
        """应用单个版本的发布计划"""
        if release_day in WEEKENDS:
            raise ValueError("周末不能发布版本")

        total_traffic = version.size_gb * version.users * ratio
        start_hour = random.choice(list(NIGHT_HOURS)) if is_night else random.randint(8, 23)

        # 生成每小时流量分布
        for day_offset, pattern in enumerate(version.traffic_pattern):
            if pattern == 0:
                continue
            current_day = release_day + day_offset
            if current_day >= MONTH_DAYS:
                break
            # 按小时平均分配当日流量
            daily_traffic = total_traffic * pattern
            for h in range(24):
                hour_idx = current_day * 24 + h
                if hour_idx >= len(self.hourly_bw):
                    continue
                self.hourly_bw[hour_idx] += daily_traffic / 24

    def calculate_cost(self) -> float:
        """计算95峰值计费费用"""
        # 计算每小时的等效费用
        hour_cost = np.where(self.night_mask[:len(self.hourly_bw)],
                             self.hourly_bw * 0.5,  # 夜间半价
                             self.hourly_bw)

        # 取所有小时中前5%的最高值
        sorted_cost = np.sort(hour_cost)[::-1]
        peak_index = int(len(sorted_cost) * 0.05)
        return sorted_cost[peak_index] * 24 * 30  # 转换为月费用


# -------------------- 遗传算法实现 --------------------
class GAOptimizer:
    def __init__(self, versions: List[Version]):
        self.versions = versions
        self.calculator = CostCalculator(versions)

    def _init_population(self) -> List[Chromosome]:
        pop = []
        for _ in range(POP_SIZE):
            c = Chromosome()
            for ver in self.versions:
                # 生成可行解
                valid_days = [d for d in range(ver.deadline + 1) if d not in WEEKENDS]
                day = random.choice(valid_days) if valid_days else 0
                is_night = random.random() > 0.7  # 倾向夜间发布
                ratio = random.uniform(MIN_RELEASE_RATIO, 1.0)
                c.genes.append((day, is_night, ratio))
            pop.append(c)
        return pop

    def _evaluate(self, chrom: Chromosome) -> float:
        """计算适应度（费用）"""
        self.calculator.clear()
        try:
            for ver, (day, is_night, ratio) in zip(self.versions, chrom.genes):
                self.calculator.apply_release(ver, day, is_night, ratio)
            return self.calculator.calculate_cost()
        except ValueError:  # 非法解
            return float('inf')

    def _crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """两点交叉"""
        child = parent1.clone()
        idx = sorted(random.sample(range(len(self.versions)), 2))
        child.genes[idx[0]:idx[1]] = parent2.genes[idx[0]:idx[1]]
        return child

    def _mutate(self, chrom: Chromosome):
        """随机突变"""
        for i in range(len(chrom.genes)):
            if random.random() < MUTATE_PROB:
                ver = self.versions[i]
                valid_days = [d for d in range(ver.deadline + 1) if d not in WEEKENDS]
                new_day = random.choice(valid_days) if valid_days else 0
                new_night = not chrom.genes[i][1]
                new_ratio = np.clip(chrom.genes[i][2] + random.uniform(-0.2, 0.2),
                                    MIN_RELEASE_RATIO, 1.0)
                chrom.genes[i] = (new_day, new_night, new_ratio)

    def optimize(self) -> Chromosome:
        population = self._init_population()
        best_chrom = None

        for gen in range(GEN_MAX):
            # 评估适应度
            for chrom in population:
                if chrom.fitness == float('inf'):
                    chrom.fitness = self._evaluate(chrom)

            # 精英保留
            population.sort(key=lambda x: x.fitness)
            elites = population[:int(ELITE_RATE * POP_SIZE)]

            # 生成新一代
            new_pop = [c.clone() for c in elites]

            while len(new_pop) < POP_SIZE:
                # 轮盘赌选择
                parents = random.choices(
                    population=population[:int(POP_SIZE * 0.8)],  # 修正此处
                    weights=[1 / (c.fitness + 1e-6) for c in population[:int(POP_SIZE * 0.8)]],
                    k=2
                )
                child = self._crossover(parents[0], parents[1])
                self._mutate(child)
                new_pop.append(child)

            population = new_pop
            best_chrom = elites[0]
            print(f"Generation {gen}: Best Cost = {best_chrom.fitness:.2f}")

        return best_chrom


# -------------------- 结果可视化 --------------------
def visualize(chrom: Chromosome):
    calculator = CostCalculator(VERSIONS)
    for ver, (day, is_night, ratio) in zip(VERSIONS, chrom.genes):
        calculator.apply_release(ver, day, is_night, ratio)

    # 按天统计带宽费用
    daily_cost = []
    for d in range(MONTH_DAYS):
        day_hours = calculator.hourly_bw[d * 24:(d + 1) * 24]
        cost = sum(h * (0.5 if h in NIGHT_HOURS else 1) for h in day_hours)
        daily_cost.append(cost)

    plt.figure(figsize=(12, 6))
    plt.plot(daily_cost, label='每日带宽费用')
    plt.axhline(y=np.percentile(daily_cost, 95), color='r', linestyle='--',
                label='95计费峰值')
    plt.title("月度带宽费用分布（95峰值计费）")
    plt.xlabel("日期")
    plt.ylabel("等效费用")
    plt.legend()
    plt.grid()
    plt.show()


# -------------------- 执行优化 --------------------
if __name__ == "__main__":
    optimizer = GAOptimizer(VERSIONS)
    best_solution = optimizer.optimize()

    print("\n最优发布方案：")
    for ver, (day, is_night, ratio) in zip(VERSIONS, best_solution.genes):
        print(f"版本{ver.id}: 第{day}天{'夜间' if is_night else '白天'}发布，开放比例{ratio:.1%}")

    visualize(best_solution)
