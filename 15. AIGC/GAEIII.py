import random
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
import csv

matplotlib.use("TkAgg")

HOLIDAYS = [datetime(2024, 5, 1), datetime(2024, 5, 3), datetime(2024, 5, 10)]  # 节假日示例


class Version:
    def __init__(self, vid, batch_size, users, size_gb, start_time, end_time, period, traffic_pattern):
        self.vid = vid
        self.batch_size = batch_size
        self.users = users
        self.size_gb = size_gb
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.traffic_pattern = traffic_pattern

    def calculate_traffic(self, release_dates, proportions):
        traffic = np.zeros(31)  # 存储每日流量（5月1日=索引0）
        for i, date in enumerate(release_dates):
            # 处理跨月流量影响
            start_offset = max((datetime(2024, 5, 1) - date).days, 0)
            for j in range(start_offset, len(self.traffic_pattern)):
                current_day = date + timedelta(days=j)
                if current_day.month == 5:  # 只统计5月流量
                    day_index = current_day.day - 1
                    if 0 <= day_index < 31:
                        traffic[day_index] += (
                                self.users * proportions[i]
                                * self.size_gb
                                * self.traffic_pattern[j]
                        )
        return traffic

    @classmethod
    def from_csv_row(cls, row):
        """从CSV行创建Version对象"""
        return cls(
            vid=int(row['vid']),
            batch_size=int(row['batch_size']),
            users=int(float(row['users'])),
            size_gb=float(row['size_gb']),
            start_time=datetime.strptime(row['start_time'], "%Y-%m-%d"),
            end_time=datetime.strptime(row['end_time'], "%Y-%m-%d"),
            period=int(row['period']),
            traffic_pattern=list(map(float, row['traffic_pattern'].split(',')))
        )


class GeneticOptimizer:
    def __init__(self, versions, pop_size=50, generations=200, mutation_rate=0.1, crossover_rate=0.8):
        self.versions = versions
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.history = []  # 新增：用于记录各代最佳流量分布

    def initialize_population(self):
        population = []
        for _ in range(self.pop_size):
            individual = []
            for version in self.versions:
                release_dates = self.generate_valid_dates(version)
                proportions = self.generate_valid_proportions(version)
                individual.append((release_dates, proportions))
            population.append(individual)
        return population

    def generate_valid_proportions(self, version):
        """生成满足业务约束的发布比例"""
        while True:
            # 初始比例<=1%
            p1 = min(random.uniform(0, 0.011), 0.01)
            remaining = 1 - p1
            max_other = remaining / (version.batch_size - 1)

            # 其他比例在±10%范围内波动
            other_props = []
            for _ in range(version.batch_size - 1):
                prop = random.uniform(max_other * 0.9, max_other * 1.1)
                other_props.append(prop)

            # 归一化处理
            total_other = sum(other_props)
            if total_other == 0:
                continue
            scale = remaining / total_other
            other_props = [p * scale for p in other_props]

            # 最终检查
            if all(p <= max_other * 1.1 for p in other_props) and \
                    abs(sum([p1] + other_props) - 1) < 1e-6:
                return [p1] + other_props



    def generate_valid_dates(self, version):
        # 调整开始日期（最多推迟3天）
        start_candidates = [version.start_time + timedelta(days=i) for i in range(4)]
        valid_starts = [d for d in start_candidates if d.weekday() < 5 and d not in HOLIDAYS]
        adjusted_start = valid_starts[0] if valid_starts else version.start_time

        # 调整结束日期（最多延后5天）
        end_candidates = [version.end_time + timedelta(days=i) for i in range(6)]
        valid_ends = [d for d in end_candidates if d.weekday() < 5 and d not in HOLIDAYS]
        adjusted_end = valid_ends[-1] if valid_ends else version.end_time

        # 生成所有合法日期
        current_date = adjusted_start
        legal_dates = []
        while current_date <= adjusted_end:
            if current_date.weekday() < 5 and current_date not in HOLIDAYS:
                legal_dates.append(current_date)
            current_date += timedelta(days=1)

        # 均匀选择批次日期
        if len(legal_dates) < version.batch_size:
            return legal_dates[:version.batch_size]  # 处理边界情况

        step = max(1, len(legal_dates) // (version.batch_size - 1))
        selected = []
        for i in range(version.batch_size):
            idx = min(i * step, len(legal_dates) - 1)
            selected.append(legal_dates[idx])
        return selected

    def fitness(self, individual):
        """改进的适应度函数，考虑多种分布特性"""
        total_traffic = np.zeros(31)
        for i, (release_dates, proportions) in enumerate(individual):
            traffic = self.versions[i].calculate_traffic(release_dates, proportions)
            total_traffic += traffic

        mean = np.mean(total_traffic)
        deviations = total_traffic - mean

        # 核心改进：多维度评估分布质量
        metrics = {
            'std': np.std(total_traffic),  # 标准差
            'mad': np.mean(np.abs(deviations)),  # 平均绝对偏差
            'max_dev': np.max(np.abs(deviations)),  # 最大绝对偏差
            'overflow': np.sum(np.where(deviations > 0, deviations ** 2, 0)),  # 正向偏离惩罚
            'underflow': np.sum(np.where(deviations < 0, deviations ** 2, 0))  # 负向偏离惩罚
        }

        # 组合权重（可调整）
        return (
                0.4 * metrics['std']
                + 0.3 * metrics['mad']
                + 0.2 * metrics['max_dev']
                + 0.1 * (metrics['overflow'] + metrics['underflow'])
        )
    def selection(self, population):
        fitness_scores = [self.fitness(ind) for ind in population]
        return random.choices(population, weights=[1 / (f + 1e-9) for f in fitness_scores], k=self.pop_size)

    def crossover(self, parent1, parent2):
        return [random.choice([v1, v2]) if random.random() < self.crossover_rate else v1
                for v1, v2 in zip(parent1, parent2)]

    # def mutate(self, individual):
    #     for i in range(len(individual)):
    #         if random.random() < self.mutation_rate:
    #             version = self.versions[i]
    #             release_dates, proportions = individual[i]
    #             new_p1 = random.uniform(0, 0.01)
    #             new_proportions = [new_p1] + [(1 - new_p1) / (version.batch_size - 1)] * (version.batch_size - 1)
    #             individual[i] = (release_dates, new_proportions)
    #     return individual

    def mutate(self, individual):
        """增强型变异操作"""
        for idx in range(len(individual)):
            if random.random() < self.mutation_rate:
                # 深拷贝当前版本参数
                version = self.versions[idx]
                original_dates, original_props = individual[idx]

                # 变异策略选择（50%概率变异日期，50%变异比例）
                if random.random() < 0.5:
                    # 变异发布日期（保持批次数量不变）
                    new_dates = self.mutate_dates(original_dates.copy(), version)
                    individual[idx] = (new_dates, original_props.copy())
                else:
                    # 变异发布比例
                    new_props = self.mutate_proportions(original_props.copy(), version)
                    individual[idx] = (original_dates.copy(), new_props)
        return individual

    def mutate_dates(self, dates, version):
        """日期变异策略"""
        # 随机选择要变异的批次（至少变异1个）
        mutate_indices = random.sample(
            range(len(dates)),
            k=random.randint(1, len(dates)))

        for i in mutate_indices:
        # 允许前后调整1-3天
            delta = random.choice([-3, -2, -1, 1, 2, 3])
        new_date = dates[i] + timedelta(days=delta)

        # 确保新日期合法
        while True:
            # 调整到最近的工作日
            if new_date.weekday() < 5 and new_date not in HOLIDAYS:
                break
            new_date += timedelta(days=1)

            # 保证日期顺序
        if i > 0 and new_date < dates[i - 1]:
            new_date = dates[i - 1] + timedelta(days=1)
        if i < len(dates) - 1 and new_date > dates[i + 1]:
            new_date = dates[i + 1] - timedelta(days=1)

        dates[i] = new_date
        return dates

    def mutate_proportions(self, props, version):
        """带约束的比例变异"""
        new_props = props.copy()
        idx = random.randint(0, len(props) - 1)

        if idx == 0:  # 变异初始比例
            delta = random.uniform(-0.005, 0.005)
            new_props[0] = np.clip(new_props[0] + delta, 0, 0.01)
        else:  # 变异其他比例
            max_val = (1 - new_props[0]) / (version.batch_size - 1) * 1.1
            delta = random.uniform(-max_val * 0.1, max_val * 0.1)
            new_props[idx] = np.clip(new_props[idx] + delta, 0, max_val)

        # 归一化处理
        total = sum(new_props)
        new_props = [p / total for p in new_props]
        return new_props

    def optimize(self):
        population = self.initialize_population()
        best_fitness = float('inf')
        best_individual = population[0].copy()  # 深拷贝初始个体
        self.history = [self.calculate_total_traffic(best_individual)]

        for gen in range(self.generations):
            # 选择
            selected = self.selection(population)

            # 交叉和变异
            offspring = []
            for i in range(0, self.pop_size, 2):
                if i + 1 < len(selected):
                    child = self.crossover(selected[i], selected[i + 1])
                    offspring.append(self.mutate(child))

            # 新一代种群
            population = sorted(population + offspring, key=self.fitness)[:self.pop_size]

            # 更新最佳个体
            current_best = population[0]
            current_fitness = self.fitness(current_best)
            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_individual = current_best.copy()

            # 记录历史流量（深拷贝）
            current_traffic = self.calculate_total_traffic(current_best)
            self.history.append(current_traffic.copy())

            print(f"Generation {gen + 1}: Fitness={current_fitness:.2f} Traffic={current_traffic[:5]}...")
            # 保存结果
        self.save_to_csv(best_individual)
        print(f"优化方案已保存到 optimized_schedule.csv")
        self.visualize_optimization_process()
        return best_individual



        # self.visualize_traffic(best_individual)
        # return best_individual

    def calculate_total_traffic(self, individual):
        """计算单个个体的总流量"""
        total_traffic = np.zeros(31)
        for i, (release_dates, proportions) in enumerate(individual):
            traffic = self.versions[i].calculate_traffic(release_dates, proportions)
            total_traffic += traffic
        return total_traffic

    def visualize_optimization_process(self):
        """可视化整个优化过程"""
        fig, ax = plt.subplots(figsize=(14, 8))

        cmap = plt.get_cmap('viridis')
        for idx, traffic in enumerate(self.history):
            alpha = 0.2 + 0.6 * (idx / len(self.history))
            color = cmap(idx / len(self.history))
            ax.plot(traffic, color=color, alpha=alpha, lw=0.8)

        ax.plot(self.history[0], color='black', linestyle='--', lw=1.5, label='Initial')
        ax.plot(self.history[-1], color='red', lw=2.5, label='Optimized')

        final_mean = np.mean(self.history[-1])
        ax.axhline(final_mean, color='blue', linestyle=':', lw=2, label='Final Mean')
        ax.fill_between(range(31),
                        final_mean * 0.95,
                        final_mean * 1.05,
                        color='gray', alpha=0.1,
                        label='±5% Range')

        sm = plt.cm.ScalarMappable(cmap=cmap,
                                   norm=plt.Normalize(0, len(self.history)))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, pad=0.02)
        cbar.set_label('Generation Progress')

        ax.set_title("Optimization Process Visualization")
        ax.set_xlabel("Day of Month")
        ax.set_ylabel("Traffic Volume (GB)")
        ax.legend(loc='upper right')
        ax.grid(True)
        plt.show()

    def visualize_traffic(self, best_individual):
        total_traffic = np.zeros(31)
        for i, (release_dates, proportions) in enumerate(best_individual):
            traffic = self.versions[i].calculate_traffic(release_dates, proportions)
            total_traffic += traffic

        plt.figure(figsize=(12, 6))

        # 绘制主要图形
        plt.plot(total_traffic, marker='o', label="Optimized Traffic")
        mean_line = np.mean(total_traffic)
        plt.axhline(mean_line, color='r', linestyle='--', label="Average")

        # 添加统计标注
        plt.text(31.5, mean_line,
                 f"Mean: {mean_line:.2f} GB\nStd: {np.std(total_traffic):.2f}\nMax Dev: {np.max(np.abs(total_traffic - mean_line)):.2f}",
                 verticalalignment='center')

        # 设置置信区间（±10%）
        plt.fill_between(range(31),
                         mean_line * 0.9,
                         mean_line * 1.1,
                         color='green', alpha=0.1,
                         label="±10% Range")

        plt.title("Traffic Distribution with Enhanced Mean Proximity")
        plt.xlabel("Day of Month")
        plt.ylabel("Traffic (GB)")
        plt.legend()
        plt.grid(True)
        plt.xlim(0, 30)
        plt.show()

    def save_to_csv(self, individual, filename="optimized_schedule_detail.csv"):
        """增强版CSV保存功能"""
        # 生成日期范围（5月1日-31日）
        date_range = [datetime(2024, 5, 1) + timedelta(days=i) for i in range(31)]
        date_headers = [d.strftime("%m/%d") for d in date_range]

        with open(filename, 'w', newline='') as csvfile:
            # 定义CSV结构
            writer = csv.writer(csvfile)

            # 第一部分：总体统计
            writer.writerow(["【方案摘要】"])
            writer.writerow([
                "生成时间", datetime.now().strftime("%Y-%m-%d %H:%M"),
                "版本数量", len(individual),
                "总流量(GB)", np.sum(self.calculate_total_traffic(individual)),
                "流量标准差", np.std(self.calculate_total_traffic(individual))
            ])

            # 第二部分：每日总流量
            writer.writerow([])
            writer.writerow(["【每日总流量(GB)】"] + date_headers)
            total_traffic = self.calculate_total_traffic(individual)
            writer.writerow(["Total"] + [f"{v:.2f}" for v in total_traffic])

            # 第三部分：各版本详细信息
            writer.writerow([])
            writer.writerow(["【版本详情】"])
            headers = [
                          "VersionID", "Batch", "ReleaseDate", "Proportion",
                          "Users", "SizeGB", "StartDate", "EndDate"
                      ] + date_headers
            writer.writerow(headers)

            for vid, (dates, props) in enumerate(individual):
                version = self.versions[vid]
                traffic_matrix = np.zeros((len(dates), 31))  # 每个批次的每日流量

                for batch_idx in range(len(dates)):
                    # 计算单个批次的流量分布
                    single_batch_props = [0.0] * len(dates)
                    single_batch_props[batch_idx] = 1.0
                    traffic = version.calculate_traffic([dates[batch_idx]], [1.0])

                    # 写入行数据
                    row = [
                              vid + 1,  # VersionID从1开始
                              batch_idx + 1,  # Batch编号
                              dates[batch_idx].strftime("%Y-%m-%d"),
                              f"{props[batch_idx]:.6f}",
                              f"{version.users:,}",
                              f"{version.size_gb:.1f}GB",
                              version.start_time.strftime("%Y-%m-%d"),
                              version.end_time.strftime("%Y-%m-%d")
                          ] + [f"{v:.2f}" for v in traffic]

                    writer.writerow(row)
                    traffic_matrix[batch_idx] = traffic

                # 添加版本汇总行
                writer.writerow([
                                    f"Version {vid + 1} Total", "", "", "", "", "", "", ""
                                ] + [f"{np.sum(traffic_matrix[:, d]):.2f}" for d in range(31)])

            # 第四部分：统计指标
            writer.writerow([])
            writer.writerow(["【统计指标】"])
            writer.writerow([
                "指标", "值", "出现日期", "说明"
            ])
            stats = {
                "最高流量日": (np.max(total_traffic), np.argmax(total_traffic)),
                "最低流量日": (np.min(total_traffic), np.argmin(total_traffic)),
                "平均流量": (np.mean(total_traffic), -1),
                "超过均值天数": (np.sum(total_traffic > np.mean(total_traffic)), -1)
            }
            for k, (v, d) in stats.items():
                writer.writerow([
                    k,
                    f"{v:.2f}GB",
                    f"5月{d + 1}" if d != -1 else "N/A",
                    self._get_stat_description(k)  # 添加说明文本
                ])

    def _get_stat_description(self, key):
        """生成统计指标的解读说明"""
        desc = {
            "最高流量日": "建议检查该日期是否存在多个版本叠加发布",
            "最低流量日": "可能需要调整该日期附近的发布计划",
            "平均流量": "理想状态应保持每日流量在此值±10%范围内",
            "超过均值天数": "值越小表示流量分布越均衡"
        }
        return desc.get(key, "")

    @classmethod
    def load_from_csv(cls, filename):
        versions = []
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 转换CSV行数据为对象
                versions.append(Version.from_csv_row(row))
        return cls(versions)

def generate_test_versions(num_versions=5, include_cross_month=True, seed=None):
    """
    生成多版本测试数据生成器

    参数：
    num_versions: 生成版本数量
    include_cross_month: 是否包含跨月版本
    seed: 随机种子

    返回：Version对象列表
    """
    if seed:
        random.seed(seed)
        np.random.seed(seed)

    versions = []

    # 基础参数范围
    param_ranges = {
        'users': (8e5, 1.2e7),  # 用户数量范围
        'size_gb': (1.5, 5.0),  # 包大小范围
        'period': (10, 21),  # 发布周期范围
        'batch_size': (5, 10)  # 批次数范围
    }

    # 流量模式模板
    traffic_templates = [
        # 指数衰减型
        lambda: [0.4 * (0.6 ** i) for i in range(15)],
        # 阶梯下降型
        lambda: [0.4, 0.3, 0.2, 0.1] + [0.05] * 11,
        # 均匀分布型
        lambda: [1 / 15] * 15,
        # 前载集中型
        lambda: [0.6, 0.3, 0.1] + [0] * 12
    ]

    for vid in range(num_versions):
        # 随机生成基础参数
        params = {
            'vid': vid,
            'batch_size': random.randint(*param_ranges['batch_size']),
            'users': int(random.uniform(*param_ranges['users'])),
            'size_gb': round(random.uniform(*param_ranges['size_gb']), 1),
            'period': random.randint(*param_ranges['period'])
        }

        # 生成流量模式（标准化）
        template = random.choice(traffic_templates)
        traffic_pattern = template()
        traffic_pattern = [p / sum(traffic_pattern) for p in traffic_pattern]

        # 生成时间范围
        if include_cross_month and vid == 0:  # 第一个版本作为跨月版本
            start = datetime(2024, 4, 28) + timedelta(days=random.randint(0, 3))
            end = start + timedelta(days=random.randint(7, 14))
        else:
            start = datetime(2024, 5, 1) + timedelta(days=random.randint(0, 3))
            end = start + timedelta(days=random.randint(10, params['period'] + 5))

        # 调整合法开始日期
        while start.weekday() >= 5 or start in HOLIDAYS:
            start += timedelta(days=1)

        versions.append(
            Version(
                vid=params['vid'],
                batch_size=params['batch_size'],
                users=params['users'],
                size_gb=params['size_gb'],
                start_time=start,
                end_time=end,
                period=params['period'],
                traffic_pattern=traffic_pattern
            )
        )

    return versions


# 测试数据（包含跨月版本）
if __name__ == "__main__":
    # 生成可重复的测试数据
    test_versions = generate_test_versions(
        num_versions=100,
        include_cross_month=True,
        seed=42  # 固定种子保证可重复性
    )

    # 打印生成的测试数据
    print("Generated Test Versions:")
    for idx, v in enumerate(test_versions):
        print(f"\nVersion {idx}:")
        print(f"VID: {v.vid}")
        print(f"Users: {v.users:,}")
        print(f"Size: {v.size_gb}GB")
        print(f"Batch Size: {v.batch_size}")
        print(f"Start: {v.start_time.strftime('%Y-%m-%d')}")
        print(f"End: {v.end_time.strftime('%Y-%m-%d')}")
        print(f"Traffic Pattern: {[round(p, 3) for p in v.traffic_pattern[:5]]}...")

    optimizer = GeneticOptimizer(test_versions, pop_size=100, generations=300)
    best = optimizer.optimize()

    # 输出方案细节
    print("\nOptimized Plan:")
    for vid, (dates, props) in enumerate(best):
        print(f"\nVersion {vid}:")
        print(f"Release Dates: {[d.strftime('%m/%d') for d in dates]}")
        print(f"Proportions: {[round(p, 4) for p in props]}")
    print("\nNote: The traffic visualization shows the combined effect of all versions")
