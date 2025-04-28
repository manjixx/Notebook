import numpy as np
import heapq
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
import random
matplotlib.use('TkAgg')  # 或者 'TkAgg'，具体取决于你想保存图 or 弹窗展示图
# 设置matplotlib全局字体
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


# -------------------- 输入参数 ----------------------
# 每个版本包含：
# - 大小（GB）
# - 流量曲线（发布后每天的总流量比例）
# - 初始优先级（值越小越优先）
# - 截止天（必须在这天及之前发布）
versions = [
    {"id": 0, "size": 2.5, "flow_curve": [0.4, 0.3, 0.2, 0.1], "priority": 1, "deadline": 10},
    {"id": 1, "size": 1.8, "flow_curve": [0.5, 0.3, 0.15, 0.05], "priority": 2, "deadline": 15},
    {"id": 2, "size": 3.0, "flow_curve": [0.35, 0.35, 0.2, 0.1], "priority": 0, "deadline": 5},
    {"id": 3, "size": 1.2, "flow_curve": [0.6, 0.25, 0.1, 0.05], "priority": 3, "deadline": 25},
    {"id": 4, "size": 2.0, "flow_curve": [0.45, 0.35, 0.15, 0.05], "priority": 2, "deadline": 20},
]

num_days = 30  # 规划未来30天
max_release_per_day = 2  # 每天最多发2个版本
num_simulations = 100  # 多次模拟，选最好的一组计划
weekend_days = [6, 13, 20, 27]  # 周末日期（不允许发布）

# 惩罚权重
weight_peak = 1.0  # 峰值惩罚
weight_var = 0.5  # 波动惩罚
weight_deadline_penalty = 5.0  # 超过截止日的惩罚分


# -------------------- 辅助函数 ----------------------

def estimate_bandwidth(releases, d):
    """计算白天和夜间的带宽消耗"""
    day_bw, night_bw = 0.0, 0.0
    for (release_day, is_night, version) in releases:
        offset = d - release_day
        if 0 <= offset < len(version["flow_curve"]):
            flow = version["flow_curve"][offset] * version["size"]
            if offset == 0:  # 发布当天流量全部分配到对应时段
                if is_night:
                    night_bw += flow
                else:
                    day_bw += flow
            else:  # 后续天流量平均分配到白天和夜间
                day_bw += flow * 0.5
                night_bw += flow * 0.5
    return day_bw, night_bw


def dynamic_priority(version, current_day):
    """动态优先级调整"""
    days_left = max(version["deadline"] - current_day, 0) + 1
    return version["priority"] - 10.0 / days_left  # 值越小越优先


def score_release_candidate(releases, version, day, is_night):
    """评估候选发布计划的得分"""
    temp_releases = releases + [(day, is_night, version)]
    daily_cost_bw = []
    for d in range(num_days):
        day_bw, night_bw = estimate_bandwidth(temp_releases, d)
        cost_bw = max(day_bw, night_bw * 0.5)  # 夜间半价折算
        daily_cost_bw.append(cost_bw)

    # 计算95峰值
    sorted_bw = sorted(daily_cost_bw, reverse=True)
    peak_index = int(0.05 * num_days)
    peak_bw = sorted_bw[peak_index] if peak_index < num_days else sorted_bw[-1]

    # 波动性和截止日惩罚
    variance = np.var(daily_cost_bw)
    deadline_penalty = (day > version["deadline"]) * (day - version["deadline"]) * weight_deadline_penalty
    return weight_peak * peak_bw + weight_var * variance + deadline_penalty


def total_score(releases):
    """计算总得分"""
    daily_cost_bw = []
    for d in range(num_days):
        day_bw, night_bw = estimate_bandwidth(releases, d)
        daily_cost_bw.append(max(day_bw, night_bw * 0.5))

    sorted_bw = sorted(daily_cost_bw, reverse=True)
    peak_index = int(0.05 * num_days)
    peak_bw = sorted_bw[peak_index] if peak_index < num_days else sorted_bw[-1]

    deadline_penalty = sum(
        (day > v["deadline"]) * (day - v["deadline"]) * weight_deadline_penalty
        for (day, _, v) in releases
    )
    variance = np.var(daily_cost_bw)
    return weight_peak * peak_bw + weight_var * variance + deadline_penalty


# -------------------- 主调度逻辑 ----------------------

def schedule_versions(versions, num_days, max_release_per_day, randomize=False):
    releases = []  # (发布日, 是否夜间, 版本)
    pending = versions.copy()
    day_count = defaultdict(int)

    while pending:
        candidates = []
        for ver in pending:
            # 允许在截止日+5天内安排
            max_day = min(ver["deadline"] + 5, num_days - 1)
            for day in range(0, max_day + 1):
                if day in weekend_days or day_count[day] >= max_release_per_day:
                    continue  # 跳过周末和已满的天
                for is_night in [False, True]:  # 考虑白天和夜间发布
                    # 计算优先级和得分
                    dyn_prio = dynamic_priority(ver, day)
                    score = score_release_candidate(releases, ver, day, is_night)
                    # 添加随机扰动避免局部最优
                    candidates.append((
                        score,
                        dyn_prio,
                        random.random() if randomize else 0,
                        day, is_night, ver
                    ))

        if not candidates:
            raise RuntimeError("无法安排所有版本，请检查约束条件")

        # 选择最优候选（得分最低）
        candidates.sort()
        best = candidates[0]
        _, _, _, day, is_night, ver = best

        releases.append((day, is_night, ver))
        pending.remove(ver)
        day_count[day] += 1

    return releases


# -------------------- 模拟退火优化 ----------------------

def simulate(versions, num_simulations):
    best_plan = None
    best_score = float('inf')
    for _ in range(num_simulations):
        plan = schedule_versions(versions, num_days, max_release_per_day, randomize=True)
        current_score = total_score(plan)
        if current_score < best_score:
            best_score = current_score
            best_plan = plan
    return best_plan


# -------------------- 可视化 ----------------------

def plot_bandwidth(releases):
    days = list(range(num_days))
    day_bw = [estimate_bandwidth(releases, d)[0] for d in days]
    night_bw = [estimate_bandwidth(releases, d)[1] * 0.5 for d in days]  # 夜间半价
    cost_bw = [max(db, nb) for db, nb in zip(day_bw, night_bw)]

    plt.figure(figsize=(12, 6))
    plt.plot(days, day_bw, label='白天带宽 (全价)', marker='o')
    plt.plot(days, night_bw, label='夜间带宽 (半价)', marker='x')
    plt.plot(days, cost_bw, label='计费带宽', linestyle='--', color='red')

    # 标注周末
    for wd in weekend_days:
        plt.axvline(x=wd, color='gray', linestyle=':', alpha=0.5)

    plt.title("每日带宽使用及计费带宽（95峰值计费）")
    plt.xlabel("天数")
    plt.ylabel("等效带宽 (GB)")
    plt.legend()
    plt.grid(True)
    plt.show()


# -------------------- 运行 ----------------------

if __name__ == "__main__":
    final_plan = simulate(versions, num_simulations)

    print("最优发布计划：")
    plan_dict = defaultdict(list)
    for day, is_night, ver in final_plan:
        plan_dict[day].append(f"版本{ver['id']}（{'夜间' if is_night else '白天'}）")

    for day in sorted(plan_dict):
        print(f"第{day}天：{plan_dict[day]}")

    print("\n总得分:", total_score(final_plan))
    plot_bandwidth(final_plan)
