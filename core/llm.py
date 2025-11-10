import os, time, base64
from typing import List, Union
import streamlit as st
from openai import OpenAI, OpenAIError
try:
    from openai import APIStatusError
except Exception:
    APIStatusError = Exception

_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not _API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing. Add it in Streamlit → Settings → Secrets.")

CHAT_MODEL = st.secrets.get("CHAT_MODEL", "gpt-4o-mini")
EMBED_MODEL = st.secrets.get("EMBEDDING_MODEL", "text-embedding-3-small")
IMAGE_MODEL = st.secrets.get("IMAGE_MODEL", "gpt-image-1")

client = OpenAI(api_key=_API_KEY)

def chat(messages, model: str = CHAT_MODEL):
    try:
        resp = client.chat.completions.create(model=model, messages=messages)
        return resp.choices[0].message.content
    except APIStatusError as e:
        status = getattr(e, "status_code", "unknown")
        body = getattr(getattr(e, "response", None), "text", "") or str(e)
        raise RuntimeError(f"Chat API error [{status}]: {body[:400]}")
    except OpenAIError as e:
        raise RuntimeError(f"Chat API error: {getattr(e, 'message', str(e))}")

def embed(texts: Union[str, List[str]], model: str = EMBED_MODEL, batch_size: int = 16):
    if isinstance(texts, str):
        texts = [texts]
    clean: List[str] = [t if (t and t.strip()) else " " for t in texts]
    out: List[List[float]] = []
    i = 0
    while i < len(clean):
        batch = clean[i : i + batch_size]
        try:
            resp = client.embeddings.create(model=model, input=batch)
            out.extend([d.embedding for d in resp.data])
            i += batch_size
        except APIStatusError as e:
            status = getattr(e, "status_code", "unknown")
            body = getattr(getattr(e, "response", None), "text", "") or str(e)
            hint = ""
            if status == 401:
                hint = " (Check OPENAI_API_KEY in Secrets; ensure org access.)"
            elif status == 404:
                hint = " (Embedding model not enabled; override EMBEDDING_MODEL in Secrets.)"
            elif status == 429:
                hint = " (Rate limit; retry or reduce batch_size.)"
            raise RuntimeError(f"Embeddings API error [{status}]: {body[:400]}{hint}")
        except OpenAIError as e:
            if "rate" in str(e).lower():
                time.sleep(2.0); continue
            raise RuntimeError(f"Embeddings API error: {getattr(e, 'message', str(e))}")
    return out

def generate_image(prompt: str, size: str = "1024x1024") -> bytes:
    try:
        resp = client.images.generate(model=IMAGE_MODEL, prompt=prompt, size=size)
        b64 = resp.data[0].b64_json
        import base64 as _b64
        return _b64.b64decode(b64)
    except Exception as e:
        raise RuntimeError(f"Image generation error: {e}")
