# 🔐 LLM Configuration Summary

> ⚠️ **This file contains references to credentials. Actual tokens go in `.env` only!**

## E2E Networks Inference Endpoints

All endpoints use **OpenAI-compatible API** format via vLLM.

### Authentication
- **Type:** Bearer token (JWT)
- **Token variable:** `E2E_API_TOKEN` (stored in `.env`)
- **Note:** Same token works for all 3 endpoints

---

## Models

### 1. Vision Model (Qwen)
| Property | Value |
|----------|-------|
| **Purpose** | Image understanding, OCR, chart analysis |
| **Model** | `Qwen/Qwen2.5-VL-7B-Instruct` |
| **Endpoint** | `https://infer.e2enetworks.net/project/p-6530/endpoint/is-8101/v1/` |
| **Env Variable** | `QWEN_BASE_URL` |

### 2. Reasoning Model (Mistral)
| Property | Value |
|----------|-------|
| **Purpose** | Agent reasoning, tool selection, planning |
| **Model** | `mistralai/Mistral-7B-v0.3` |
| **Endpoint** | `https://infer.e2enetworks.net/project/p-6530/endpoint/is-8105/v1/` |
| **Env Variable** | `MISTRAL_BASE_URL` |

### 3. Code Generation Model (DeepSeek)
| Property | Value |
|----------|-------|
| **Purpose** | Python code generation |
| **Model** | `deepseek-ai/deepseek-coder-7b-instruct-v1.5` |
| **Endpoint** | `https://infer.e2enetworks.net/project/p-6530/endpoint/is-8107/v1/` |
| **Env Variable** | `DEEPSEEK_BASE_URL` |

> **Note:** Using DeepSeek v1.5 (not v2) as v2 is unavailable on E2E Networks.

---

## .env.example Template

```bash
# E2E Networks LLM Configuration
E2E_API_TOKEN=your_jwt_token_here

# Model Endpoints
QWEN_BASE_URL=https://infer.e2enetworks.net/project/p-6530/endpoint/is-8101/v1/
QWEN_MODEL=Qwen/Qwen2.5-VL-7B-Instruct

MISTRAL_BASE_URL=https://infer.e2enetworks.net/project/p-6530/endpoint/is-8105/v1/
MISTRAL_MODEL=mistralai/Mistral-7B-v0.3

DEEPSEEK_BASE_URL=https://infer.e2enetworks.net/project/p-6530/endpoint/is-8107/v1/
DEEPSEEK_MODEL=deepseek-ai/deepseek-coder-7b-instruct-v1.5
```

---

## Usage Pattern

```python
import openai

# Configure client for a specific model
client = openai.OpenAI(
    api_key=os.getenv("E2E_API_TOKEN"),
    base_url=os.getenv("QWEN_BASE_URL"),
)

# Make request
response = client.chat.completions.create(
    model=os.getenv("QWEN_MODEL"),
    messages=[{"role": "user", "content": "..."}],
)
```

---

## Security Notes

1. **Never commit the actual token** — only `.env.example` with placeholders
2. `.env` is in `.gitignore`
3. Token expiry: Check JWT `exp` claim (currently set to ~1 year)
