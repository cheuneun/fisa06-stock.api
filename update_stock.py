import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# 로컬 테스트용 (GitHub Actions에서는 Secret 설정이 우선됨)
load_dotenv()

# Alpha Vantage API 설정
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SYMBOL = "AAPL"  # 원하는 주식 심볼 (애플: AAPL, 테슬라: TSLA, 삼성전자: 005930.KS)
URL = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={SYMBOL}&apikey={API_KEY}"

README_PATH = "README.md"

def get_stock_data():
    """Alpha Vantage API를 호출하여 주식 데이터를 가져옴"""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        # API 응답에서 핵심 데이터 추출
        quote = data.get("Global Quote", {})
        
        if not quote:
            return "주식 데이터를 찾을 수 없습니다. (API 호출 한도 초과일 수 있음)"
            
        price = quote.get("05. price", "0")
        change_percent = quote.get("10. change percent", "0%")
        high = quote.get("03. high", "0")
        low = quote.get("04. low", "0")
        
        return {
            "symbol": SYMBOL,
            "price": float(price),
            "change": change_percent,
            "high": high,
            "low": low
        }
    return None

def update_readme():
    """README.md 파일을 주식 정보로 업데이트"""
    stock = get_stock_data()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(stock, dict):
        stock_info = f"📈 **{stock['symbol']}** | 현재가: **${stock['price']:.2f}** ({stock['change']})"
        extra_info = f"- 오늘의 고가: ${stock['high']} / 저가: ${stock['low']}"
    else:
        stock_info = "데이터를 가져오는 중 오류가 발생했습니다."
        extra_info = ""

    readme_content = f"""
# 💹 실시간 주식 대시보드

이 리포지토리는 Alpha Vantage API와 GitHub Actions를 사용하여 주가 정보를 자동으로 업데이트합니다.

## 실시간 종목 정보
> {stock_info}
{extra_info}

---
⏳ **최종 업데이트 시간:** {now} (KST/UTC)  
*본 데이터는 Alpha Vantage를 통해 제공됩니다.*
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()