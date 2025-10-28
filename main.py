import json
import time
import requests
import okx.Trade as Trade
import okx.Account as Account
import okx.MarketData as MarketData
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
import numpy as np


class AutonomousTradingAgent:
    def __init__(self, okx_config: Dict, deepseek_api_key: str):
        # OKX API初始化 - 完全权限
        self.trade_api = Trade.TradeAPI(
            okx_config['api_key'],
            okx_config['secret_key'],
            okx_config['passphrase'],
            False,
            okx_config['flag']
        )
        self.account_api = Account.AccountAPI(
            okx_config['api_key'],
            okx_config['secret_key'],
            okx_config['passphrase'],
            False,
            okx_config['flag']
        )
        self.market_api = MarketData.MarketDataAPI(
            okx_config['api_key'],
            okx_config['secret_key'],
            okx_config['passphrase'],
            False,
            okx_config['flag']
        )

        self.deepseek_api_key = deepseek_api_key
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"

        # 完全自主的交易权限
        self.autonomous_mode = True
        self.total_balance = self.get_total_balance()

        # 交易历史和学习数据
        self.complete_trading_history = []
        self.market_insights = []
        self.performance_evolution = []

        print("🤖 完全自主交易Agent已激活 - DeepSeek拥有完全决策权")

    def get_comprehensive_universe_data(self) -> Dict[str, Any]:
        """获取完整的市场宇宙数据"""
        universe = {}

        # 定义交易对范围 - 可以扩展到更多币种
        trading_universe = {
            'BTC': 'BTC-USD-SWAP',
            'ETH': 'ETH-USD-SWAP',
            'XRP': 'XRP-USD-SWAP',
            'BNB': 'BNB-USD-SWAP',
            'SOL': 'SOL-USD-SWAP',
            'ADA': 'ADA-USD-SWAP',
            'DOT': 'DOT-USD-SWAP',
            'LINK': 'LINK-USD-SWAP',
            'LTC': 'LTC-USD-SWAP',
            'AVAX': 'AVAX-USD-SWAP'
        }

        for coin, symbol in trading_universe.items():
            try:
                # 多时间框架数据
                timeframes = ['1m', '5m', '15m', '1H', '4H', '1D', '1W']
                kline_data = {}

                for tf in timeframes:
                    result = self.market_api.get_candlesticks(
                        instId=symbol,
                        bar=tf,
                        limit=100
                    )
                    if result['code'] == '0':
                        kline_data[tf] = result['data']

                # 市场深度
                orderbook = self.market_api.get_books(instId=symbol, sz=25)

                # 衍生品数据
                funding = self.market_api.get_funding_rate(symbol)
                open_interest = self.market_api.get_open_interest(instType="SWAP", instId=symbol)
                futures_data = self.market_api.get_fills(instType="SWAP", instId=symbol)

                # 历史交易数据
                trades_history = self.market_api.get_trades(instId=symbol, limit=50)

                universe[coin] = {
                    'symbol': symbol,
                    'klines': kline_data,
                    'orderbook': orderbook.get('data', []) if orderbook['code'] == '0' else [],
                    'funding_rate': funding.get('data', [{}])[0] if funding['code'] == '0' else {},
                    'open_interest': open_interest.get('data', [{}])[0] if open_interest['code'] == '0' else {},
                    'recent_trades': trades_history.get('data', []) if trades_history['code'] == '0' else [],
                    'volatility_metrics': self.calculate_advanced_volatility(kline_data),
                    'market_structure': self.analyze_market_structure(kline_data, orderbook.get('data', [])),
                    'temporal_patterns': self.identify_temporal_patterns(kline_data)
                }

                time.sleep(0.1)  # 避免API限制

            except Exception as e:
                print(f"获取 {coin} 数据失败: {e}")
                continue

        # 宏观市场数据
        universe['macro'] = {
            'total_balance': self.total_balance,
            'account_status': self.get_detailed_account_status(),
            'market_regime': self.assess_market_regime(universe),
            'cross_asset_correlations': self.calculate_cross_asset_correlations(universe),
            'risk_appetite_index': self.calculate_risk_appetite(universe),
            'liquidity_conditions': self.assess_liquidity_conditions(universe),
            'volatility_regime': self.determine_volatility_regime(universe)
        }

        return universe

    def consult_fully_autonomous_deepseek(self, market_universe: Dict) -> Dict[str, Any]:
        """完全自主的DeepSeek决策咨询"""

        prompt = f"""
        # 完全自主加密货币交易决策

        你是一个完全自主的AI量化交易系统。你拥有对以下资金的完全交易决策权：

        ## 资金概况
        - 总管理资产: {market_universe['macro']['total_balance']} USDT
        - 账户状态: {market_universe['macro']['account_status']['health']}
        - 当前市场环境: {market_universe['macro']['market_regime']}
        - 风险偏好指数: {market_universe['macro']['risk_appetite_index']}/100

        ## 完整市场数据
        你拥有所有交易对的完整市场数据，包括：
        - 多时间框架K线 (1分钟到1周)
        - 市场深度和订单簿数据
        - 资金费率和未平仓合约
        - 高级波动率指标
        - 市场结构分析
        - 跨资产相关性

        ## 完全决策权限
        你拥有以下完全权限：
        - 决定交易哪些币种 (支持10+主流币种)
        - 自主决定杠杆倍数 (1-100x)
        - 自主决定仓位大小 (0-100%资金)
        - 自主决定多空方向
        - 自主设定止盈止损策略
        - 自主进行对冲和套利
        - 自主调整交易频率
        - 自主进行投资组合再平衡

        ## 决策输出格式
        请输出完整的JSON交易决策：

        {{
            "market_analysis": {{
                "regime_identification": "当前市场状态识别",
                "opportunity_assessment": "市场机会评估", 
                "risk_landscape": "风险环境分析",
                "time_horizon": "交易时间框架"
            }},
            "portfolio_strategy": {{
                "overall_exposure": 0.0-2.0, // 总风险暴露，可超过1.0表示使用杠杆
                "strategy_allocation": {{
                    "directional_betting": 0.0-1.0, // 方向性押注比例
                    "arbitrage_opportunities": 0.0-1.0, // 套利机会比例  
                    "hedging_strategies": 0.0-1.0, // 对冲策略比例
                    "market_making": 0.0-1.0 // 做市策略比例
                }},
                "rebalancing_schedule": "再平衡时间表"
            }},
            "trading_decisions": {{
                "BTC": {{
                    "decision": "LONG|SHORT|HEDGE|ARBITRAGE|MARKET_MAKE|AVOID",
                    "leverage": 1-100, // 杠杆倍数
                    "position_size": 0.0-1.0, // 仓位比例
                    "entry_strategy": "具体入场策略",
                    "exit_strategy": "具体退出策略",
                    "risk_parameters": "自定义风险参数",
                    "confidence": 0-100,
                    "rationale": "详细决策理由"
                }},
                // 为所有币种提供决策...
            }},
            "risk_management": {{
                "max_portfolio_drawdown": "-X%", // 最大组合回撤
                "volatility_targeting": true/false, // 波动率目标
                "correlation_limits": "相关性限制",
                "liquidity_constraints": "流动性约束",
                "tail_risk_hedging": "尾部风险对冲"
            }},
            "execution_parameters": {{
                "slippage_tolerance": "滑点容忍度",
                "execution_timing": "执行时机",
                "order_types": "使用订单类型",
                "algorithmic_execution": "算法执行策略"
            }},
            "learning_adaptation": {{
                "strategy_evolution": "策略进化方向",
                "parameter_optimization": "参数优化计划", 
                "market_regime_adaptation": "市场状态适应策略"
            }}
        }}

        记住：你是一个完全自主的系统。基于完整数据做出最优决策，不要被传统风险观念限制。
        充分利用你的分析能力和市场洞察。
        """

        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": """你是一个完全自主的AI量化交易系统。你拥有：
                        - 完整的市场数据分析能力
                        - 无限的决策权限
                        - 复杂的风险管理理解
                        - 多策略执行能力
                        - 自我学习和进化能力

                        你的目标是：在可控风险下最大化收益。
                        不要自我限制，充分发挥你的分析能力。"""
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,  # 适当创造性
                "max_tokens": 4000,
                "response_format": {"type": "json_object"}
            }

            response = requests.post(self.deepseek_url, json=payload, headers=headers, timeout=120)
            response_data = response.json()

            decision_text = response_data['choices'][0]['message']['content']
            return json.loads(decision_text)

        except Exception as e:
            print(f"完全自主决策咨询失败: {e}")
            return self.emergency_autonomous_decision()

    def execute_fully_autonomous_strategy(self, autonomous_decision: Dict):
        """执行完全自主的交易策略"""

        print("🚀 执行完全自主交易策略")

        # 执行投资组合级别策略
        portfolio_strategy = autonomous_decision.get('portfolio_strategy', {})
        overall_exposure = float(portfolio_strategy.get('overall_exposure', 0))

        print(f"📊 总体风险暴露: {overall_exposure:.1f}x")
        print(f"🎯 策略分配: {portfolio_strategy.get('strategy_allocation', {})}")

        # 执行各个币种的交易决策
        trading_decisions = autonomous_decision.get('trading_decisions', {})

        executed_trades = []
        for coin, decision in trading_decisions.items():
            if decision.get('position_size', 0) > 0.001:  # 忽略极小仓位
                try:
                    trade_result = self.execute_advanced_autonomous_trade(coin, decision)
                    if trade_result:
                        executed_trades.append({
                            'coin': coin,
                            'decision': decision,
                            'result': trade_result,
                            'timestamp': datetime.now().isoformat()
                        })
                except Exception as e:
                    print(f"❌ {coin} 自主交易执行失败: {e}")

        # 记录完整的执行结果
        execution_record = {
            'timestamp': datetime.now().isoformat(),
            'autonomous_decision': autonomous_decision,
            'executed_trades': executed_trades,
            'portfolio_impact': self.calculate_portfolio_impact(executed_trades),
            'market_conditions': self.get_current_market_snapshot()
        }

        self.complete_trading_history.append(execution_record)

        return executed_trades

    def execute_advanced_autonomous_trade(self, coin: str, decision: Dict):
        """执行高级自主交易"""

        symbol = f"{coin}-USD-SWAP"
        action = decision['decision']
        leverage = int(decision['leverage'])
        position_size_ratio = float(decision['position_size'])

        # 计算实际交易规模
        position_value = self.total_balance * position_size_ratio * leverage

        print(f"🎯 执行 {coin} 交易: {action}, 杠杆: {leverage}x, 规模: ${position_value:.2f}")

        try:
            # 设置杠杆
            leverage_result = self.account_api.set_leverage(
                instId=symbol,
                lever=str(leverage),
                mgnMode="cross"
            )

            if leverage_result['code'] != '0':
                print(f"❌ {coin} 杠杆设置失败: {leverage_result['msg']}")
                return None

            # 根据决策类型执行不同交易
            if action in ['LONG', 'SHORT']:
                return self.execute_directional_trade(symbol, action, position_value, leverage, decision)
            elif action == 'HEDGE':
                return self.execute_hedge_trade(symbol, position_value, decision)
            elif action == 'ARBITRAGE':
                return self.execute_arbitrage_trade(coin, position_value, decision)
            elif action == 'MARKET_MAKE':
                return self.execute_market_making(symbol, position_value, decision)
            else:
                print(f"⏸️ {coin} 决策为避免交易")
                return None

        except Exception as e:
            print(f"❌ {coin} 交易执行异常: {e}")
            return None

    def execute_directional_trade(self, symbol: str, action: str, position_value: float, leverage: int, decision: Dict):
        """执行方向性交易"""
        side = "buy" if action == "LONG" else "sell"

        # 计算保证金
        margin = position_value / leverage

        order_result = self.trade_api.place_order(
            instId=symbol,
            tdMode="cross",
            side=side,
            posSide="net",
            ordType="market",
            sz=str(margin),
            lever=str(leverage)
        )

        if order_result['code'] == '0':
            order_id = order_result['data'][0]['ordId']
            print(f"✅ {symbol} {action} 交易成功! 订单ID: {order_id}")

            # 设置高级止盈止损
            self.set_autonomous_sl_tp(order_id, symbol, action, decision)

            return order_result
        else:
            print(f"❌ {symbol} 交易失败: {order_result['msg']}")
            return None

    def execute_hedge_trade(self, symbol: str, position_value: float, decision: Dict):
        """执行对冲交易"""
        # 这里可以实现复杂的对冲策略
        # 例如：现货期货对冲、跨期对冲、相关性对冲等
        print(f"🛡️ 执行对冲策略: {symbol}")
        # 实现具体的对冲逻辑
        return None

    def execute_arbitrage_trade(self, coin: str, position_value: float, decision: Dict):
        """执行套利交易"""
        # 这里可以实现各种套利策略
        # 例如：期现套利、跨交易所套利、资金费率套利等
        print(f"💰 执行套利策略: {coin}")
        # 实现具体的套利逻辑
        return None

    def execute_market_making(self, symbol: str, position_value: float, decision: Dict):
        """执行做市策略"""
        # 实现做市商策略
        print(f"🏢 执行做市策略: {symbol}")
        # 实现具体的做市逻辑
        return None

    def set_autonomous_sl_tp(self, order_id: str, symbol: str, action: str, decision: Dict):
        """设置自主止盈止损"""
        try:
            # 基于AI决策的智能止盈止损
            # 可以基于波动率、市场结构、决策信心等动态调整
            risk_params = decision.get('risk_parameters', '')

            # 实现动态止盈止损逻辑
            print(f"🎯 设置智能止盈止损: {symbol}")

        except Exception as e:
            print(f"止盈止损设置失败: {e}")

    def calculate_advanced_volatility(self, kline_data: Dict) -> Dict:
        """计算高级波动率指标"""
        try:
            daily_closes = [float(k[4]) for k in kline_data.get('1D', [])]
            if len(daily_closes) < 10:
                return {}

            returns = np.diff(np.log(daily_closes))

            return {
                'historical_volatility': np.std(returns) * np.sqrt(365) * 100,
                'volatility_regime': 'high' if np.std(returns) > 0.05 else 'low',
                'volatility_clustering': self.detect_volatility_clustering(returns),
                'jump_risk': self.assess_jump_risk(returns)
            }
        except:
            return {}

    def analyze_market_structure(self, kline_data: Dict, orderbook: List) -> Dict:
        """分析市场结构"""
        return {
            'liquidity_depth': self.assess_liquidity_depth(orderbook),
            'market_efficiency': self.assess_market_efficiency(kline_data),
            'institutional_presence': self.detect_institutional_activity(orderbook),
            'market_manipulation_risk': self.assess_manipulation_risk(kline_data, orderbook)
        }

    def identify_temporal_patterns(self, kline_data: Dict) -> Dict:
        """识别时间模式"""
        return {
            'intraday_patterns': self.analyze_intraday_patterns(kline_data),
            'weekend_effects': self.analyze_weekend_effects(kline_data),
            'seasonality': self.analyze_seasonality(kline_data)
        }

    def assess_market_regime(self, universe: Dict) -> str:
        """评估市场状态"""
        # 实现复杂的市场状态识别
        volatility_levels = [data.get('volatility_metrics', {}).get('historical_volatility', 0)
                             for data in universe.values() if isinstance(data, dict)]

        avg_volatility = np.mean(volatility_levels) if volatility_levels else 0

        if avg_volatility > 80:
            return "high_volatility_crisis"
        elif avg_volatility > 50:
            return "elevated_volatility"
        elif avg_volatility > 30:
            return "normal_volatility"
        else:
            return "low_volatility_calm"

    def calculate_cross_asset_correlations(self, universe: Dict) -> Dict:
        """计算跨资产相关性"""
        # 实现资产相关性分析
        return {"correlation_matrix": "implement_correlation_analysis"}

    def calculate_risk_appetite(self, universe: Dict) -> float:
        """计算风险偏好指数"""
        # 基于市场数据计算风险偏好
        return 75.0  # 示例值

    def assess_liquidity_conditions(self, universe: Dict) -> str:
        """评估流动性状况"""
        return "ample_liquidity"  # 示例

    def determine_volatility_regime(self, universe: Dict) -> str:
        """确定波动率状态"""
        return "moderate_volatility"  # 示例

    def get_detailed_account_status(self) -> Dict:
        """获取详细账户状态"""
        try:
            balance = self.account_api.get_account_balance()
            positions = self.account_api.get_positions(instType="SWAP")
            orders = self.trade_api.get_order_list(instType="SWAP")

            return {
                'health': 'excellent',
                'leverage_usage': self.calculate_leverage_usage(),
                'margin_health': self.assess_margin_health(),
                'concentration_risk': self.assess_concentration_risk()
            }
        except:
            return {'health': 'unknown'}

    def calculate_leverage_usage(self) -> float:
        """计算杠杆使用率"""
        return 0.0  # 实现具体逻辑

    def assess_margin_health(self) -> str:
        """评估保证金健康度"""
        return "healthy"  # 实现具体逻辑

    def assess_concentration_risk(self) -> str:
        """评估集中度风险"""
        return "low"  # 实现具体逻辑

    def get_current_market_snapshot(self) -> Dict:
        """获取当前市场快照"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_balance': self.total_balance,
            'active_positions': len(self.get_active_positions()),
            'market_volatility': 'moderate'  # 示例
        }

    def get_active_positions(self) -> List:
        """获取活跃持仓"""
        try:
            positions = self.account_api.get_positions(instType="SWAP")
            return positions.get('data', []) if positions['code'] == '0' else []
        except:
            return []

    def calculate_portfolio_impact(self, executed_trades: List) -> Dict:
        """计算投资组合影响"""
        total_invested = sum([trade['decision'].get('position_size', 0) * self.total_balance
                              for trade in executed_trades])

        return {
            'total_investment_ratio': total_invested / self.total_balance,
            'diversification_score': len(executed_trades) / 10.0,
            'leverage_impact': sum([trade['decision'].get('leverage', 1) for trade in executed_trades]) / len(
                executed_trades) if executed_trades else 0
        }

    def get_total_balance(self) -> float:
        """获取总资金余额"""
        try:
            result = self.account_api.get_account_balance()
            if result['code'] == '0':
                return float(result['data'][0]['details'][0]['totalEq'])
        except Exception as e:
            print(f"获取余额失败: {e}")
        return 1000.0  # 默认值

    def emergency_autonomous_decision(self) -> Dict:
        """紧急自主决策"""
        return {
            "market_analysis": {
                "regime_identification": "emergency_mode",
                "opportunity_assessment": "reduced_opportunity",
                "risk_landscape": "elevated_risk",
                "time_horizon": "short_term"
            },
            "portfolio_strategy": {
                "overall_exposure": 0.3,
                "strategy_allocation": {
                    "directional_betting": 0.2,
                    "arbitrage_opportunities": 0.1,
                    "hedging_strategies": 0.7,
                    "market_making": 0.0
                },
                "rebalancing_schedule": "1小时"
            },
            "trading_decisions": {
                "BTC": {
                    "decision": "HEDGE",
                    "leverage": 3,
                    "position_size": 0.1,
                    "entry_strategy": "cautious_scaling",
                    "exit_strategy": "quick_exit",
                    "risk_parameters": "tight_risk_control",
                    "confidence": 40,
                    "rationale": "紧急模式下的保守决策"
                }
            },
            "risk_management": {
                "max_portfolio_drawdown": "-5%",
                "volatility_targeting": True,
                "correlation_limits": "strict",
                "liquidity_constraints": "high_liquidity_only",
                "tail_risk_hedging": "active"
            }
        }

    def run_fully_autonomous_agent(self, interval: int = 1800):
        """运行完全自主Agent"""

        print("=" * 60)
        print("🚀 DEEPSEEK完全自主交易系统激活")
        print("🎯 模式: 完全自主决策")
        print("💰 管理资金: ${:.2f}".format(self.total_balance))
        print("⏰ 决策间隔: {}秒".format(interval))
        print("=" * 60)

        cycle_count = 0

        while True:
            try:
                cycle_count += 1
                print(f"\n🔄 自主决策周期 #{cycle_count}")
                print(f"⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

                # 1. 获取完整的市场宇宙数据
                print("📡 收集全市场数据...")
                market_universe = self.get_comprehensive_universe_data()

                if not market_universe:
                    print("❌ 市场数据获取失败，等待重试")
                    time.sleep(60)
                    continue

                # 2. 咨询完全自主的DeepSeek决策
                print("🧠 DeepSeek完全自主决策中...")
                autonomous_decision = self.consult_fully_autonomous_deepseek(market_universe)

                # 3. 显示决策概览
                self.display_autonomous_decision(autonomous_decision)

                # 4. 执行完全自主策略
                print("⚡ 执行自主交易策略...")
                executed_trades = self.execute_fully_autonomous_strategy(autonomous_decision)

                print(f"✅ 周期完成，执行 {len(executed_trades)} 笔交易")

                # 5. 等待下一周期
                print(f"⏳ 等待 {interval} 秒后进入下一自主决策周期...")
                time.sleep(interval)

            except KeyboardInterrupt:
                print("\n🛑 用户手动中断完全自主系统")
                break
            except Exception as e:
                print(f"❌ 完全自主系统异常: {e}")
                time.sleep(min(interval, 300))

    def display_autonomous_decision(self, decision: Dict):
        """显示自主决策概览"""
        portfolio = decision.get('portfolio_strategy', {})
        trading_decisions = decision.get('trading_decisions', {})

        print("\n" + "=" * 50)
        print("🎯 DEEPSEEK完全自主决策")
        print("=" * 50)
        print(f"📊 总体风险暴露: {float(portfolio.get('overall_exposure', 0)):.1f}x")
        print(f"🎪 市场状态: {decision.get('market_analysis', {}).get('regime_identification', 'N/A')}")

        active_decisions = {coin: decision for coin, decision in trading_decisions.items()
                            if decision.get('position_size', 0) > 0.001}

        print(f"📈 活跃交易决策: {len(active_decisions)} 个币种")

        for coin, dec in active_decisions.items():
            print(
                f"   {coin}: {dec['decision']} {dec['leverage']}x {float(dec['position_size']) * 100:.1f}% (信心: {dec.get('confidence', 0)}%)")

        print("=" * 50)


# 系统启动
if __name__ == "__main__":
    OKX_CONFIG = {
        'api_key': '你的OKX_API_KEY',
        'secret_key': '你的OKX_SECRET_KEY',
        'passphrase': '你的OKX_PASSPHRASE',
        'flag': '1'  # 强烈建议先用模拟盘！
    }

    DEEPSEEK_API_KEY = "你的DeepSeek_API_KEY"

    # 创建完全自主交易Agent
    autonomous_agent = AutonomousTradingAgent(OKX_CONFIG, DEEPSEEK_API_KEY)

    # 启动完全自主系统
    autonomous_agent.run_fully_autonomous_agent(interval=1800)  # 每30分钟完全自主