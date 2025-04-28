import numpy as np
from datetime import datetime, timedelta
from typing import List
import matplotlib.pyplot as plt
import matplotlib
import random
matplotlib.use('TkAgg')  # 或者 'TkAgg'，具体取决于你想保存图 or 弹窗展示图
# 设置matplotlib全局字体
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# -------------------- 系统配置 --------------------
BASE_DATE = datetime(2024, 5, 1)  # 假设当月从5月1日开始
MONTH_DAYS = 30
NIGHT_HOURS = set(range(0, 8))  # 夜间时段定义
WEEKEND_DAYS = [6, 13, 20, 27]  # 当月周末日期（0-based）


# -------------------- 版本数据类 --------------------
class Version:
    def __init__(self, vid: int, size_gb: float, deadline: datetime,
                 users: int, traffic_pattern: List[float], preset_time: datetime):
        """
        :param preset_time: 预设发布时间（datetime对象）
        :param deadline: 最晚发布时间（datetime对象）
        """
        self.id = vid
        self.size_gb = size_gb
        self.users = users
        self.traffic_pattern = traffic_pattern

        # 转换为相对于基准日期的偏移
        self.preset_day = (preset_time - BASE_DATE).days
        self.preset_min = (preset_time.hour * 60 + preset_time.minute)
        self.deadline_day = (deadline - BASE_DATE).days


# 测试数据（5个版本）
VERSIONS = [
    Version(0, 2.5, datetime(2024,5,10), 1e6, [0.4,0.3,0.2,0.1,0,0,0], datetime(2024,5,1,6,0)),
    Version(1, 1.8, datetime(2024,5,15), 8e5, [0.5,0.3,0.15,0.05,0,0,0], datetime(2024,5,3,0,0)),
    Version(2, 3.0, datetime(2024,5,5), 1.2e6, [0.35,0.35,0.2,0.1,0,0,0], datetime(2024,5,1,2,0)),
    Version(3, 1.2, datetime(2024,5,25), 5e5, [0.6,0.25,0.1,0.05,0,0,0], datetime(2024,5,4,0,0)),
    Version(4, 2.0, datetime(2024,5,20), 9e5, [0.45,0.35,0.15,0.05,0,0,0], datetime(2024,5,2,12,0)),
]

# -------------------- 遗传算法参数 --------------------
POP_SIZE = 100
GEN_MAX = 300
MUTATE_PROB = 0.25
ELITE_RATE = 0.15
MIN_RATIO = 0.1


# -------------------- 染色体结构 --------------------
class Chromosome:
    def __init__(self):
        self.genes = []  # [(release_day, is_night, ratio)]
        self.fitness = float('inf')

    def clone(self):
        c = Chromosome()
        c.genes = self.genes.copy()
        c.fitness = self.fitness
        return c


# -------------------- 成本计算引擎 --------------------
class CostCalculator:
    def __init__(self):
        self.hourly_bw = np.zeros(MONTH_DAYS * 24)
        self.night_mask = np.array([h in NIGHT_HOURS for _ in range(MONTH_DAYS) for h in range(24)])

    def _add_traffic(self, start_day: int, is_night: bool, daily_traffic: List[float]):
        """添加流量到小时级数组"""
        for day_offset, traffic in enumerate(daily_traffic):
            current_day = start_day + day_offset
            if current_day >= MONTH_DAYS:
                break

            # 确定小时分布
            if day_offset == 0:  # 发布当天
                if is_night:
                    hours = random.sample(NIGHT_HOURS, k=1)  # 随机选一个夜间小时
                else:
                    hours = random.sample(range(8, 24), k=1)
            else:  # 后续天平均分布
                hours = range(24)

            for h in hours:
                idx = current_day * 24 + h
                if idx < len(self.hourly_bw):
                    self.hourly_bw[idx] += traffic / len(hours)

    def calculate(self, plan: List[tuple]) -> float:
        """计算给定计划的费用"""
        self.hourly_bw.fill(0)
        for ver, (day, is_night, ratio) in plan:  # 正确解包结构
            total = ver.size_gb * ver.users * ratio
            daily_traffic = [total * p for p in ver.traffic_pattern]
            self._add_traffic(day, is_night, daily_traffic)

        # 计算95峰值
        hour_cost = np.where(self.night_mask, self.hourly_bw * 0.5, self.hourly_bw)
        sorted_cost = np.sort(hour_cost)[::-1]
        return sorted_cost[int(len(sorted_cost) * 0.05)] * 720

    def get_original_plan(self):
        """生成正确的原始计划数据结构"""
        return [
            (ver, (
                ver.preset_day,
                (ver.preset_min // 60) in NIGHT_HOURS,
                1.0
            )) for ver in VERSIONS
        ]

    def get_hourly_bandwidth(self, plan: List[tuple]) -> np.ndarray:
        """获取指定计划的小时级带宽数据"""
        self.hourly_bw.fill(0)
        for ver, (day, is_night, ratio) in plan:
            total = ver.size_gb * ver.users * ratio
            daily_traffic = [total * p for p in ver.traffic_pattern]
            self._add_traffic(day, is_night, daily_traffic)
        return self.hourly_bw.copy()  # 返回副本避免数据覆盖

# -------------------- 遗传算法核心 --------------------
class GAEngine:
    def __init__(self):
        self.calculator = CostCalculator()
        self.original_cost = self.calculator.calculate(
            self.calculator.get_original_plan())

    def _init_gene(self, ver: Version) -> tuple:
        valid_days = [d for d in range(ver.preset_day, ver.deadline_day + 1)
                      if d not in WEEKEND_DAYS]
        day = random.choice(valid_days) if valid_days else ver.preset_day
        is_night = random.random() > 0.6
        ratio = random.uniform(MIN_RATIO, 1.0)
        return (day, is_night, ratio)

    def _mutate_gene(self, gene: tuple, ver: Version) -> tuple:
        """基因变异"""
        day, is_night, ratio = gene
        # 调整日期
        if random.random() < 0.3:
            valid_days = [d for d in range(ver.preset_day, ver.deadline_day + 1)
                          if d not in WEEKEND_DAYS]
            day = random.choice(valid_days)
        # 调整时段
        if random.random() < 0.3:
            is_night = not is_night
        # 调整比例
        if random.random() < 0.3:
            ratio = np.clip(ratio + random.uniform(-0.15, 0.15), MIN_RATIO, 1.0)
        return (day, is_night, ratio)

    def optimize(self):
        # 初始化种群
        population = [Chromosome() for _ in range(POP_SIZE)]
        for c in population:
            c.genes = [self._init_gene(ver) for ver in VERSIONS]
            c.fitness = self.calculator.calculate(list(zip(VERSIONS, c.genes)))

        best = min(population, key=lambda x: x.fitness)

        for gen in range(GEN_MAX):
            # 选择
            sorted_pop = sorted(population, key=lambda x: x.fitness)
            elites = sorted_pop[:int(POP_SIZE * ELITE_RATE)]

            # 生成下一代
            new_pop = elites.copy()
            while len(new_pop) < POP_SIZE:
                # 轮盘赌选择
                p1, p2 = random.choices(
                    population=sorted_pop[:POP_SIZE // 2],
                    weights=[1 / (c.fitness + 1e-6) for c in sorted_pop[:POP_SIZE // 2]],
                    k=2
                )
                # 交叉
                child = p1.clone()
                cross_point = random.randint(1, len(VERSIONS) - 1)
                child.genes[cross_point:] = p2.genes[cross_point:]
                # 变异
                for i in range(len(child.genes)):
                    if random.random() < MUTATE_PROB:
                        child.genes[i] = self._mutate_gene(child.genes[i], VERSIONS[i])
                # 评估
                child.fitness = self.calculator.calculate(list(zip(VERSIONS, child.genes)))
                new_pop.append(child)

            population = new_pop
            current_best = min(population, key=lambda x: x.fitness)
            if current_best.fitness < best.fitness:
                best = current_best
            print(f"Gen {gen + 1}: Best {best.fitness:.2f} (Current {current_best.fitness:.2f})")

        return best


# -------------------- 结果可视化 --------------------
def format_time(day: int, is_night: bool) -> str:
    date = BASE_DATE + timedelta(days=day)
    if is_night:
        hour = random.choice(list(NIGHT_HOURS))
    else:
        hour = random.choice(list(set(range(24)) - NIGHT_HOURS))
    return date.replace(hour=hour, minute=0).strftime("%Y-%m-%d %H:%M")


def print_comparison(original_cost: float, optimized_plan: Chromosome):
    calc = CostCalculator()

    # 获取原始方案带宽数据
    original_plan = calc.get_original_plan()
    orig_bw = calc.get_hourly_bandwidth(original_plan)

    # 获取优化方案带宽数据
    optimized_plan_data = [(ver, gene) for ver, gene in zip(VERSIONS, optimized_plan.genes)]
    opt_bw = calc.get_hourly_bandwidth(optimized_plan_data)

    # 绘制对比图
    plt.figure(figsize=(15, 6))
    plt.plot(orig_bw, label='原始方案', alpha=0.7, color='blue')
    plt.plot(opt_bw, label='优化方案', alpha=0.7, color='orange')

    # 标注95峰值线
    for bw, color, label in [(orig_bw, 'blue', '原始峰值'), (opt_bw, 'orange', '优化峰值')]:
        peak_value = np.percentile(
            np.where(calc.night_mask, bw * 0.5, bw),
            95
        )
        plt.axhline(y=peak_value, color=color, linestyle='--', label=label)

    plt.title("带宽使用对比（原始方案 vs 优化方案）")
    plt.xlabel("小时（从月初开始）")
    plt.ylabel("等效带宽 (GB)")
    plt.legend()
    plt.grid(True)
    plt.show()

# -------------------- 主程序 --------------------
if __name__ == "__main__":
    engine = GAEngine()
    best_solution = engine.optimize()
    print_comparison(engine.original_cost, best_solution)
