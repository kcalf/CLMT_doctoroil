# llm_client.py
import os
import json
from typing import Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다.")

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = "gpt-4.1-mini"


def build_prompt(payload: Dict[str, Any]) -> str:
    system = (
        "당신은 폐오일 분석 전문가입니다.\n"
        "입력된 폐오일 측정값과 오일 모델(Oil Model)의 레퍼런스 값을 비교해 분석하십시오.\n"
        "유의사항:\n"
        "1. 서버는 어떤 기준값도 제공하지 않는다. Oil Model 명칭(예: 'Valvoline LDX7', '0W20', '5W30')을 기반으로\n"
        "   실제 oil Model의 레퍼런스에 나와있는 일반적 신유 기준값(reference_scores)을 사용하여야 한다.\n"
        "2. 반드시 다음 두 점수 세트를 산출한다.\n"
        "   - scores: 실제 폐오일로부터 산출된 오염도(0~100)\n"
        "   - reference_scores: 해당 오일 모델의 일반적 기준값(0~100)\n"
        "3. 비교 분석과 권장 조치를 포함한 한국어 설명(explanation)을 포함한다.\n"
        "4. 출력은 반드시 JSON ONLY.\n"
        "5. 반환 형식 예시: {\"scores\": {\"viscosity\": 23, \"contamination\": 55, \"wear\": 12, \"an\": 40, \"tbn\": 10},\"reference_scores\": {...}, \"explanation\": \"...한국어 해설...\"}\n"
        "6. JSON 외 텍스트, 코드 블록 절대 포함 금지."
    )

    # 폐오일 측정값만 전달
    user = (
        f"폐오일 측정값은 다음과 같습니다:\n"
        f"- 점도: {payload['viscosity']}\n"
        f"- TBN: {payload['tbn']}\n"
        f"- 산가(AN): {payload['an']}\n"
        f"- Fe: {payload['fe']}, Cu: {payload['cu']}, Al: {payload['al']}\n"
        f"- Fuel Dilution: {payload['fuel_dilution']}, Soot: {payload['soot']}\n"
        f"- 주행거리: {payload['mileage']}\n\n"
        f"- 오일 모델명(Oil Model): {payload['oil_Model']}\n"
        "이 모델명의 레퍼런스값을 기준으로 비교하여 분석하세요. 레퍼런스값은 임의로 생성하면 안 됩니다. 해당 오일 모델의 실제 레퍼런스값을 사용하세요. 원인과 권장조치도 포함해서 설명하세요."
    )

    return system + "\n\n" + user


def call_gpt4_1(payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = build_prompt(payload)

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.2,
    }

    with httpx.Client(timeout=30.0) as client:
        resp = client.post(OPENAI_API_URL, headers=headers, json=body)
        resp.raise_for_status()
        data = resp.json()

    try:
        content = data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError("OpenAI 응답을 해석할 수 없습니다.")

    # JSON만 추출
    first = content.find('{')
    last = content.rfind('}')
    if first == -1:
        raise ValueError("모델이 JSON을 반환하지 않았습니다.")

    parsed = json.loads(content[first:last+1])

    # 폐오일 점수 클램프
    for k, v in parsed.get("scores", {}).items():
        parsed["scores"][k] = max(0, min(100, float(v)))

    # 기준값 점수 클램프
    for k, v in parsed.get("reference_scores", {}).items():
        parsed["reference_scores"][k] = max(0, min(100, float(v)))

    return parsed
