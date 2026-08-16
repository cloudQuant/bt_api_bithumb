# bt_api_bithumb

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bithumb.svg)](https://pypi.org/project/bt_api_bithumb/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bithumb.svg)](https://pypi.org/project/bt_api_bithumb/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bithumb/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bithumb/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bithumb/badge/?version=latest)](https://bt-api-bithumb.readthedocs.io/)

---

<!-- English -->
# bt_api_bithumb

> **Bithumb exchange plugin for bt_api** — Unified REST API for **Spot** trading with support for **KRW**, **USDT**, **USD**, **BTC**, and **ETH** trading pairs.

`bt_api_bithumb` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **Bithumb** exchange. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure.

Bithumb is one of **South Korea's largest cryptocurrency exchanges**, offering trading in KRW, USDT, USD, BTC, and ETH pairs.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bithumb.readthedocs.io/ |
| Chinese Docs | https://bt-api-bithumb.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bithumb |
| PyPI | https://pypi.org/project/bt_api_bithumb/ |
| Issues | https://github.com/cloudQuant/bt_api_bithumb/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### 1 Asset Type

| Asset Type | Code | REST | Description |
|---|---|---|---|
| Spot | `BITHUMB___SPOT` | ✅ | Spot trading with KRW, USDT, USD, BTC, ETH pairs |

### REST API

- **Market Data** — Ticker, order book depth, k-lines, recent trades
- **Account** — Balance, account info
- **Trading** — Place orders, cancel orders, query order status, open orders

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITHUMB___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BITHUMB___SPOT", "BTCUSDT")
balance = api.get_balance("BITHUMB___SPOT")
order = api.make_order(exchange_name="BITHUMB___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### Unified Data Containers

All exchange responses normalized to bt_api_base container types:

- `TickContainer` — 24hr rolling ticker
- `OrderBookContainer` — Order book depth
- `BarContainer` — K-line/candlestick
- `TradeContainer` — Individual trades
- `OrderContainer` — Order status and fills
- `AccountBalanceContainer` — Asset balances

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bithumb
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bithumb
cd bt_api_bithumb
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `httpx` for HTTP client

---

## Quick Start

### 1. Install

```bash
pip install bt_api_bithumb
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BITHUMB___SPOT", "BTCUSDT")
print(f"BTCUSDT price: {ticker}")
```

### 3. Place an order (requires API key)

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITHUMB___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BITHUMB___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"Order placed: {order}")
```

### 4. bt_api Plugin Integration

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITHUMB___SPOT": {"api_key": "key", "secret": "secret"}
})

# REST calls
ticker = api.get_tick("BITHUMB___SPOT", "BTCUSDT")
balance = api.get_balance("BITHUMB___SPOT")
order = api.make_order(exchange_name="BITHUMB___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

---

## Architecture

```
bt_api_bithumb/
├── plugin.py                     # register_plugin() — bt_api plugin entry point
├── registry_registration.py      # register_bithumb() — feeds / exchange_data registration
├── exchange_data/
│   └── __init__.py             # BithumbExchangeData (base) + BithumbExchangeDataSpot
├── feeds/
│   ├── live_bithumb/
│   │   ├── spot.py             # BithumbRequestDataSpot — SPOT feed
│   │   └── request_base.py     # BithumbRequestData — base request class
│   └── __init__.py
├── containers/                   # Normalized data containers
├── errors/
│   └── __init__.py
└── __init__.py
```

---

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_tick` | 24hr rolling ticker |
| | `get_depth` | Order book depth |
| | `get_kline` | K-line/candlestick |
| | `get_exchange_info` | Exchange configuration |
| **Account** | `get_balance` | Asset balances |
| | `get_account` | Full account info |
| **Trading** | `make_order` | LIMIT orders |
| | `cancel_order` | Cancel order by ID |
| | `query_order` | Query order status |
| | `get_open_orders` | All open orders |

---

## Supported Bithumb Symbols

Bithumb trading pairs are supported in multiple quote currencies:

- **USDT pairs**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT` ...
- **USD pairs**: `BTCUSD`, `ETHUSD` ...
- **BTC pairs**: `ETHBTC`, `XRPBTC` ...
- **ETH pairs**: `XRPETH` ...
- **KRW pairs**: `BTCKRW`, `ETHKRW`, `SOLKRW` ...

---

## Error Handling

All Bithumb API errors are translated to bt_api_base `ApiError` subclasses.

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-bithumb.readthedocs.io/ |
| **中文** | https://bt-api-bithumb.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bithumb/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 Bithumb 交易所插件** — 为**现货**交易提供统一的 REST API，支持 **KRW**、**USDT**、**USD**、**BTC** 和 **ETH** 交易对。

`bt_api_bithumb` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，连接 **Bithumb** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。

Bithumb 是 **韩国最大的加密货币交易所** 之一，提供 KRW、USDT、USD、BTC 和 ETH 交易对。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bithumb.readthedocs.io/ |
| 中文文档 | https://bt-api-bithumb.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bithumb |
| PyPI | https://pypi.org/project/bt_api_bithumb/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bithumb/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 1 种资产类型

| 资产类型 | 代码 | REST | 说明 |
|---|---|---|---|
| 现货 | `BITHUMB___SPOT` | ✅ | 现货交易，支持 KRW、USDT、USD、BTC、ETH 交易对 |

### REST API

- **行情数据** — 行情、订单簿深度、K线、近期成交
- **账户** — 余额、账户信息
- **交易** — 下单、撤单、查询订单状态、挂单列表

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITHUMB___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BITHUMB___SPOT", "BTCUSDT")
balance = api.get_balance("BITHUMB___SPOT")
order = api.make_order(exchange_name="BITHUMB___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### 统一数据容器

所有交易所响应规范化为 bt_api_base 容器类型：

- `TickContainer` — 24小时滚动行情
- `OrderBookContainer` — 订单簿深度
- `BarContainer` — K线/蜡烛图
- `TradeContainer` — 逐笔成交
- `OrderContainer` — 订单状态和成交
- `AccountBalanceContainer` — 资产余额

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bithumb
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bithumb
cd bt_api_bithumb
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `httpx` HTTP 客户端

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_bithumb
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BITHUMB___SPOT", "BTCUSDT")
print(f"BTCUSDT 价格: {ticker}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITHUMB___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BITHUMB___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"订单已下单: {order}")
```

### 4. bt_api 插件集成

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITHUMB___SPOT": {"api_key": "key", "secret": "secret"}
})

# REST 调用
ticker = api.get_tick("BITHUMB___SPOT", "BTCUSDT")
balance = api.get_balance("BITHUMB___SPOT")
order = api.make_order(exchange_name="BITHUMB___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

---

## 架构

```
bt_api_bithumb/
├── plugin.py                     # register_plugin() — bt_api 插件入口
├── registry_registration.py     # register_bithumb() — feeds / exchange_data 注册
├── exchange_data/
│   └── __init__.py             # BithumbExchangeData（基类）+ BithumbExchangeDataSpot
├── feeds/
│   ├── live_bithumb/
│   │   ├── spot.py             # BithumbRequestDataSpot — SPOT feed
│   │   └── request_base.py    # BithumbRequestData — 请求基类
│   └── __init__.py
├── containers/                   # 规范化数据容器
├── errors/
│   └── __init__.py
└── __init__.py
```

---

## 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **行情数据** | `get_tick` | 24小时滚动行情 |
| | `get_depth` | 订单簿深度 |
| | `get_kline` | K线/蜡烛图 |
| | `get_exchange_info` | 交易所配置 |
| **账户** | `get_balance` | 资产余额 |
| | `get_account` | 完整账户信息 |
| **交易** | `make_order` | 限价单 |
| | `cancel_order` | 按 ID 撤单 |
| | `query_order` | 查询订单状态 |
| | `get_open_orders` | 所有挂单 |

---

## 支持的 Bithumb 交易对

支持多种计价货币的 Bithumb 交易对：

- **USDT 交易对**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT` ...
- **USD 交易对**: `BTCUSD`, `ETHUSD` ...
- **BTC 交易对**: `ETHBTC`, `XRPBTC` ...
- **ETH 交易对**: `XRPETH` ...
- **KRW 交易对**: `BTCKRW`, `ETHKRW`, `SOLKRW` ...

---

## 错误处理

所有 Bithumb API 错误均翻译为 bt_api_base `ApiError` 子类。

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-bithumb.readthedocs.io/ |
| **中文文档** | https://bt-api-bithumb.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bithumb/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com
