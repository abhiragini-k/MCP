"""
Pendle Finance API Client
High-performance client with caching and batch operations 
"""
import asyncio
import json
import time
from datetime import datetime
from typing import Any, Optional, List, Dict
import httpx
from functools import lru_cache

# Configuration
PENDLE_API_BASE = "https://api-v2.pendle.finance/core"
PENDLE_SDK_BASE = "https://api-v2.pendle.finance/sdk"
PENDLE_CONVERT_BASE = "https://api-v2.pendle.finance/convert"
PENDLE_LIMIT_ORDER_BASE = "https://api-v2.pendle.finance/limit-order"

SUPPORTED_CHAINS = {
    "ethereum": 1,
    "arbitrum": 42161,
    "optimism": 10,
    "bsc": 56,
    "mantle": 5000
}

class OptimizedPendleClient:
    """High-performance client with caching and batch operations"""
    
    def __init__(self):
        self.base_url = PENDLE_API_BASE
        self.sdk_url = PENDLE_SDK_BASE
        self.convert_url = PENDLE_CONVERT_BASE
        self.limit_order_url = PENDLE_LIMIT_ORDER_BASE
        
        # Optimized HTTP client with connection pooling
        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
        
        # Simple in-memory cache
        self._cache = {}
        self._cache_ttl = 60  # 60 seconds cache
    
    def _get_cache_key(self, endpoint: str, params: dict) -> str:
        """Generate cache key"""
        return f"{endpoint}:{json.dumps(params, sort_keys=True)}"
    
    def _get_cached(self, key: str) -> Optional[dict]:
        """Get from cache if valid"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self._cache_ttl:
                return data
        return None
    
    def _set_cache(self, key: str, data: dict):
        """Set cache"""
        self._cache[key] = (data, time.time())
    
    async def close(self):
        await self.client.aclose()
    
    def get_chain_name(self, chain_id: int) -> str:
        chains = {
            1: "Ethereum",
            42161: "Arbitrum",
            10: "Optimism",
            56: "BSC",
            5000: "Mantle"
        }
        return chains.get(chain_id, f"Chain {chain_id}")
    
    async def _fetch_with_cache(self, endpoint: str, params: dict = None) -> dict:
        """Fetch with caching support"""
        if params is None:
            params = {}
        
        cache_key = self._get_cache_key(endpoint, params)
        cached = self._get_cached(cache_key)
        
        if cached:
            return cached
        
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        
        self._set_cache(cache_key, data)
        return data
    
    # ========== HOSTED SDK FUNCTIONS ==========
    
    async def convert_swap(self, chain_id: int, market_address: str, 
                          receiver: str, token_in: str, token_out: str,
                          amount_in: str, slippage: float = 0.005) -> dict:
        """Swap tokens using Pendle Hosted SDK Convert API"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/swap"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "tokenIn": token_in,
                "tokenOut": token_out,
                "amountIn": amount_in,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountOut": data.get("amountOut"),
            "priceImpact": f"{data.get('priceImpact', 0) * 100:.4f}%",
            "minAmountOut": data.get("minAmountOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_add_liquidity(self, chain_id: int, market_address: str,
                                   receiver: str, token_in: str, amount_in: str,
                                   slippage: float = 0.005) -> dict:
        """Add liquidity using Hosted SDK"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/add-liquidity"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "tokenIn": token_in,
                "amountIn": amount_in,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountLpOut": data.get("amountLpOut"),
            "priceImpact": f"{data.get('priceImpact', 0) * 100:.4f}%",
            "minLpOut": data.get("minLpOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_add_liquidity_zpi(self, chain_id: int, market_address: str,
                                       receiver: str, token_in: str, amount_in: str,
                                       slippage: float = 0.005) -> dict:
        """Add liquidity with Zero Price Impact (ZPI)"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/add-liquidity-zpi"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "tokenIn": token_in,
                "amountIn": amount_in,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountLpOut": data.get("amountLpOut"),
            "priceImpact": "~0% (ZPI)",
            "gas": data.get("gas"),
        }
    
    async def convert_remove_liquidity(self, chain_id: int, market_address: str,
                                      receiver: str, amount_lp: str, token_out: str,
                                      slippage: float = 0.005) -> dict:
        """Remove liquidity using Hosted SDK"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/remove-liquidity"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "amountLp": amount_lp,
                "tokenOut": token_out,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountTokenOut": data.get("amountOut"),
            "priceImpact": f"{data.get('priceImpact', 0) * 100:.4f}%",
            "minTokenOut": data.get("minOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_mint_pt_yt(self, chain_id: int, market_address: str,
                                receiver: str, token_in: str, amount_in: str,
                                slippage: float = 0.005) -> dict:
        """Mint PT & YT tokens"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/mint"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "tokenIn": token_in,
                "amountIn": amount_in,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountPtOut": data.get("amountPtOut"),
            "amountYtOut": data.get("amountYtOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_redeem_pt_yt(self, chain_id: int, market_address: str,
                                  receiver: str, amount_pt: str, token_out: str,
                                  slippage: float = 0.005) -> dict:
        """Redeem PT & YT tokens"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/redeem"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "amountPt": amount_pt,
                "tokenOut": token_out,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountTokenOut": data.get("amountOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_mint_sy(self, chain_id: int, sy_address: str,
                             receiver: str, token_in: str, amount_in: str,
                             slippage: float = 0.005) -> dict:
        """Mint SY tokens"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/sy/{sy_address}/mint"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "tokenIn": token_in,
                "amountIn": amount_in,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountSyOut": data.get("amountSyOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_redeem_sy(self, chain_id: int, sy_address: str,
                               receiver: str, amount_sy: str, token_out: str,
                               slippage: float = 0.005) -> dict:
        """Redeem SY tokens"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/sy/{sy_address}/redeem"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "amountSy": amount_sy,
                "tokenOut": token_out,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountTokenOut": data.get("amountOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_rollover_pt(self, chain_id: int, from_market: str, to_market: str,
                                 receiver: str, amount_pt: str, slippage: float = 0.005) -> dict:
        """Roll over PT from one market to another"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/rollover"
        
        response = await self.client.post(
            endpoint,
            json={
                "fromMarket": from_market,
                "toMarket": to_market,
                "receiver": receiver,
                "amountPt": amount_pt,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountPtOut": data.get("amountPtOut"),
            "priceImpact": f"{data.get('priceImpact', 0) * 100:.4f}%",
            "gas": data.get("gas"),
        }
    
    async def convert_add_liquidity_dual(self, chain_id: int, market_address: str,
                                        receiver: str, amount_token: str, amount_pt: str,
                                        slippage: float = 0.005) -> dict:
        """Add dual-sided liquidity (token + PT)"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/add-liquidity-dual"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "amountToken": amount_token,
                "amountPt": amount_pt,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountLpOut": data.get("amountLpOut"),
            "priceImpact": f"{data.get('priceImpact', 0) * 100:.4f}%",
            "gas": data.get("gas"),
        }
    
    async def convert_remove_liquidity_dual(self, chain_id: int, market_address: str,
                                           receiver: str, amount_lp: str,
                                           slippage: float = 0.005) -> dict:
        """Remove liquidity to both token and PT"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/markets/{market_address}/remove-liquidity-dual"
        
        response = await self.client.post(
            endpoint,
            json={
                "receiver": receiver,
                "amountLp": amount_lp,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountTokenOut": data.get("amountTokenOut"),
            "amountPtOut": data.get("amountPtOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_transfer_liquidity(self, chain_id: int, from_market: str,
                                        to_market: str, receiver: str, amount_lp: str,
                                        slippage: float = 0.005) -> dict:
        """Transfer liquidity between markets"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/transfer-liquidity"
        
        response = await self.client.post(
            endpoint,
            json={
                "fromMarket": from_market,
                "toMarket": to_market,
                "receiver": receiver,
                "amountLp": amount_lp,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountLpOut": data.get("amountLpOut"),
            "gas": data.get("gas"),
        }
    
    async def convert_transfer_liquidity_zpi(self, chain_id: int, from_market: str,
                                            to_market: str, receiver: str, amount_lp: str,
                                            slippage: float = 0.005) -> dict:
        """Transfer liquidity with Zero Price Impact"""
        endpoint = f"{self.convert_url}/v1/{chain_id}/transfer-liquidity-zpi"
        
        response = await self.client.post(
            endpoint,
            json={
                "fromMarket": from_market,
                "toMarket": to_market,
                "receiver": receiver,
                "amountLp": amount_lp,
                "slippage": slippage,
            }
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "transaction": {
                "to": data.get("to"),
                "data": data.get("data"),
                "value": data.get("value"),
            },
            "amountLpOut": data.get("amountLpOut"),
            "priceImpact": "~0% (ZPI)",
            "gas": data.get("gas"),
        }
    
    # ========== OPTIMIZED API FUNCTIONS ==========
    
    async def get_markets_batch(self, chain_ids: List[int], limit: int = 20) -> dict:
        """Batch fetch markets from multiple chains"""
        tasks = [
            self._fetch_with_cache(
                f"{self.base_url}/v1/{chain_id}/markets",
                {"limit": limit, "order_by": "liquidity:desc"}
            )
            for chain_id in chain_ids
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_markets = []
        for chain_id, result in zip(chain_ids, results):
            if isinstance(result, Exception):
                continue
            markets = result.get("results", result) if isinstance(result, dict) else result
            for m in markets[:limit]:
                all_markets.append({
                    "address": m.get("address"),
                    "name": m.get("name") or m.get("symbol"),
                    "chain": self.get_chain_name(chain_id),
                    "chainId": chain_id,
                    "impliedAPY": f"{m.get('impliedApy', 0) * 100:.2f}%",
                    "lpAPY": f"{m.get('aggregatedApy', 0) * 100:.2f}%",
                    "liquidity": f"${m.get('liquidity', 0) / 1e6:.2f}M",
                })
        
        return {"markets": all_markets, "totalChains": len(chain_ids)}
    
    async def get_best_opportunities(self, chain_id: int, min_liquidity: float = 100000) -> dict:
        """Find best yield opportunities with filters"""
        data = await self._fetch_with_cache(
            f"{self.base_url}/v1/{chain_id}/markets",
            {"limit": 100, "order_by": "apy:desc"}
        )
        
        markets = data.get("results", data) if isinstance(data, dict) else data
        
        # Filter by liquidity and sort by APY
        filtered = [
            m for m in markets 
            if m.get("liquidity", 0) >= min_liquidity
        ]
        
        opportunities = []
        for m in filtered[:15]:
            days_to_maturity = int((m.get("expiry", 0) * 1000 - datetime.now().timestamp() * 1000) / (1000 * 60 * 60 * 24))
            
            opportunities.append({
                "market": m.get("name"),
                "address": m.get("address"),
                "apy": f"{m.get('aggregatedApy', 0) * 100:.2f}%",
                "impliedAPY": f"{m.get('impliedApy', 0) * 100:.2f}%",
                "liquidity": f"${m.get('liquidity', 0) / 1e6:.2f}M",
                "daysToMaturity": days_to_maturity,
                "volume24h": f"${m.get('volume24h', 0) / 1e6:.2f}M",
                "riskScore": "Low" if days_to_maturity > 90 else "Medium" if days_to_maturity > 30 else "High",
            })
        
        return {"opportunities": opportunities, "count": len(opportunities)}
    
    async def get_market_depth(self, market_address: str, chain_id: int) -> dict:
        """Get market depth and liquidity distribution"""
        data = await self._fetch_with_cache(
            f"{self.base_url}/v1/{chain_id}/markets/{market_address}"
        )
        
        return {
            "marketAddress": market_address,
            "totalLiquidity": f"${data.get('liquidity', 0) / 1e6:.2f}M",
            "ptReserves": data.get("pt", {}).get("totalSupply"),
            "syReserves": data.get("sy", {}).get("totalSupply"),
            "utilizationRate": f"{data.get('utilizationRate', 0) * 100:.2f}%",
            "depth": {
                "buy1Percent": data.get("depth", {}).get("buy1pct"),
                "sell1Percent": data.get("depth", {}).get("sell1pct"),
            },
        }
    
    async def simulate_strategy(self, market_address: str, chain_id: int,
                               investment: float, strategy: str) -> dict:
        """Simulate investment strategies"""
        data = await self._fetch_with_cache(
            f"{self.base_url}/v1/{chain_id}/markets/{market_address}"
        )
        
        days_to_maturity = int((data.get("expiry", 0) * 1000 - datetime.now().timestamp() * 1000) / (1000 * 60 * 60 * 24))
        
        scenarios = {
            "optimistic": 1.2,
            "expected": 1.0,
            "pessimistic": 0.8,
        }
        
        results = {}
        
        if strategy == "PT":
            base_return = investment * (data.get("impliedApy", 0) * (days_to_maturity / 365))
            for scenario, multiplier in scenarios.items():
                results[scenario] = {
                    "finalValue": investment + (base_return * multiplier),
                    "profit": base_return * multiplier,
                    "apy": f"{data.get('impliedApy', 0) * 100 * multiplier:.2f}%",
                }
        elif strategy == "YT":
            base_return = investment * (data.get("ytApy", 0) * (days_to_maturity / 365))
            for scenario, multiplier in scenarios.items():
                results[scenario] = {
                    "finalValue": investment + (base_return * multiplier),
                    "profit": base_return * multiplier,
                    "apy": f"{data.get('ytApy', 0) * 100 * multiplier:.2f}%",
                }
        elif strategy == "LP":
            base_return = investment * (data.get('aggregatedApy', 0) * (days_to_maturity / 365))
            for scenario, multiplier in scenarios.items():
                results[scenario] = {
                    "finalValue": investment + (base_return * multiplier),
                    "profit": base_return * multiplier,
                    "apy": f"{data.get('aggregatedApy', 0) * 100 * multiplier:.2f}%",
                }
        
        return {
            "strategy": strategy,
            "investment": f"${investment:,.2f}",
            "daysToMaturity": days_to_maturity,
            "scenarios": results,
        }
    
    async def get_trending_markets(self, chain_id: int, period: str = "24h") -> dict:
        """Get trending markets by volume growth"""
        data = await self._fetch_with_cache(
            f"{self.base_url}/v1/{chain_id}/trending",
            {"period": period}
        )
        
        return {
            "period": period,
            "trending": data.get("markets", [])[:10],
        }
    
    async def get_protocol_revenue(self, chain_id: Optional[int] = None) -> dict:
        """Get protocol revenue statistics"""
        endpoint = f"{self.base_url}/v1/{chain_id}/revenue" if chain_id else f"{self.base_url}/v1/revenue"
        
        data = await self._fetch_with_cache(endpoint, {})
        
        return {
            "totalRevenue": f"${data.get('total', 0) / 1e6:.2f}M",
            "revenue24h": f"${data.get('24h', 0) / 1e3:.2f}K",
            "revenue7d": f"${data.get('7d', 0) / 1e6:.2f}M",
            "revenueByChain": data.get("byChain", {}),
        }


# Initialize client
pendle_api = OptimizedPendleClient()
