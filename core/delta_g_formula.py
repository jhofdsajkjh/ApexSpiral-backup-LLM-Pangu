import math
import logging

logging.basicConfig(level=logging.INFO)


class DeltaGUnified:
    """APEX ΔG 统一公式 - LLM抗幻觉核心引擎"""
    LAMBDA = 1.5
    TAU = 0.32
    DELTA_B = 0.18

    def __init__(self):
        pass

    @staticmethod
    def shannon_entropy(prob_list: list[float]) -> float:
        """
        计算香农信息熵
        H = -Σ p(x) * log2(p(x))
        """
        entropy = 0.0
        for p in prob_list:
            if p > 0:
                entropy -= p * math.log2(p)
        return round(entropy, 4)

    @staticmethod
    def shannon_channel_capacity(bandwidth: float, snr: float) -> float:
        """
        香农信道容量
        C = B * log2(1 + SNR)
        """
        return round(bandwidth * math.log2(1 + snr), 4)

    @staticmethod
    def code_redundancy(avg_len: float, entropy: float) -> float:
        """
        代码冗余度
        R = L_avg / H
        """
        if entropy == 0:
            return 0.0
        return round(avg_len / entropy, 4)

    def calc_total_delta_g(self, H: float, F: float, L: float, N: float, C: float,
                          Omega: float, grad_E: float, Gamma: float, avg_code_len: float,
                          Psi: float, Theta: float) -> float:
        """
        统一ΔG公式计算

        参数:
            H: 信息熵 (0-8 bits)
            F: 事实性因子 (0-1)
            L: 上下文长度 (tokens)
            N: 噪声干扰 (0-1)
            C: 通道容量 (bits)
            Omega: 语义覆盖度 (0-1)
            grad_E: 能量梯度 (0-1)
            Gamma: 压缩效率 (0-1)
            avg_code_len: 平均编码长度
            Psi: 协议合规度 (0-1)
            Theta: 逻辑一致性 (0-1)

        返回:
            ΔG_total: 系统总偏离度
        """
        term1 = self.LAMBDA * H
        term2 = self.LAMBDA * (1 - F) + math.exp(-self.TAU * L) + self.DELTA_B
        term3 = self.LAMBDA * (N / C if C != 0 else 1.0)
        term4 = self.LAMBDA * (1 - Omega) * grad_E
        red = self.code_redundancy(avg_code_len, H)
        term5 = self.LAMBDA * (1 - Gamma) * red
        term6 = self.LAMBDA * (1 - Psi) * self.TAU
        term7 = self.LAMBDA * (1 - Theta) * H
        total = term1 + term2 + term3 + term4 + term5 + term6 + term7
        return round(total, 4)

    def judge_system_state(self, dg_total: float) -> str:
        """
        判断系统状态并返回应对策略

        阈值:
            ≤ 2.10: 健康稳态
            2.10 - 4.0: 轻度偏离 → 自动局部修复
            > 4.0: 严重越界 → 触发全量重启自愈
        """
        if dg_total <= 2.10:
            return "steady_健康稳态"
        elif 2.10 < dg_total <= 4.0:
            return "mild_轻度偏离_自动局部修复"
        else:
            return "critical_严重越界_触发全量重启自愈"


# 便捷函数
def quick_calc(H: float, F: float, L: float, N: float = 0.0, C: float = 1.0,
               Omega: float = 1.0, grad_E: float = 0.0, Gamma: float = 1.0,
               avg_code_len: float = 1.0, Psi: float = 1.0, Theta: float = 1.0) -> tuple[float, str]:
    """
    快速计算ΔG并返回状态判断

    示例:
        >>> dg, state = quick_calc(H=2.0, F=0.9, L=100)
        >>> print(f"ΔG={dg}, 状态={state}")
    """
    engine = DeltaGUnified()
    dg = engine.calc_total_delta_g(H, F, L, N, C, Omega, grad_E, Gamma, avg_code_len, Psi, Theta)
    state = engine.judge_system_state(dg)
    return dg, state


if __name__ == "__main__":
    # 示例
    engine = DeltaGUnified()

    # 测试1: 健康状态
    dg1 = engine.calc_total_delta_g(H=1.5, F=0.95, L=50, N=0.1, C=8.0,
                                     Omega=0.9, grad_E=0.2, Gamma=0.85,
                                     avg_code_len=2.0, Psi=0.9, Theta=0.95)
    print(f"测试1 ΔG={dg1}, 状态={engine.judge_system_state(dg1)}")

    # 测试2: 轻度偏离
    dg2 = engine.calc_total_delta_g(H=4.0, F=0.7, L=500, N=0.4, C=4.0,
                                     Omega=0.6, grad_E=0.5, Gamma=0.6,
                                     avg_code_len=3.5, Psi=0.7, Theta=0.65)
    print(f"测试2 ΔG={dg2}, 状态={engine.judge_system_state(dg2)}")

    # 测试3: 严重越界
    dg3 = engine.calc_total_delta_g(H=7.5, F=0.3, L=2000, N=0.8, C=2.0,
                                     Omega=0.3, grad_E=0.9, Gamma=0.3,
                                     avg_code_len=6.0, Psi=0.4, Theta=0.3)
    print(f"测试3 ΔG={dg3}, 状态={engine.judge_system_state(dg3)}")

    # 香农熵测试
    probs = [0.25, 0.25, 0.25, 0.25]
    print(f"均匀分布熵: {DeltaGUnified.shannon_entropy(probs)}")

    probs2 = [0.5, 0.25, 0.125, 0.125]
    print(f"非均匀分布熵: {DeltaGUnified.shannon_entropy(probs2)}")
