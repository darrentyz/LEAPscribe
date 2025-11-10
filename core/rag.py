import os, faiss, numpy as np
from typing import List, Dict
from core.llm import embed
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

INDEX_PATH = "data/index.faiss"
META_PATH  = "data/meta.npy"

def _load_index():
    if not os.path.exists(INDEX_PATH):
        return None, []
    index = faiss.read_index(INDEX_PATH)
    meta  = np.load(META_PATH, allow_pickle=True).tolist()
    return index, meta

def _save_index(index, meta):
    os.makedirs("data", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    np.save(META_PATH, np.array(meta, dtype=object), allow_pickle=True)

def chunk(text, size=800, overlap=120):
    toks = text.split()
    out=[]
    i=0
    while i<len(toks):
        out.append(" ".join(toks[i:i+size]))
        i += size-overlap
    return out

def extract_text(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()
    try:
        if name.endswith(".pdf"):
            text_parts = []
            reader = PdfReader(BytesIO(file_bytes))
            if reader.is_encrypted:
                try: reader.decrypt("")
                except Exception: pass
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
            return "\n".join(text_parts).strip()
        elif name.endswith(".docx"):
            doc = Document(BytesIO(file_bytes))
            return "\n".join(p.text for p in doc.paragraphs if p.text).strip()
        else:
            return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return file_bytes.decode("utf-8", errors="ignore")

def upsert_documents(docs: List[Dict]):
    texts = [d["text"] for d in docs]
    metas = [d["meta"] for d in docs]
    chunks, meta_chunks = [], []
    for t, m in zip(texts, metas):
        for c in chunk(t):
            if c and c.strip():
                chunks.append(c); meta_chunks.append(m)

    if not chunks:
        return
    vecs = np.array(embed(chunks), dtype="float32")
    index, meta = _load_index()
    if index is None:
        index = faiss.IndexFlatIP(vecs.shape[1])
    faiss.normalize_L2(vecs)
    index.add(vecs)
    meta.extend([{"text": c, **mc} for c, mc in zip(chunks, meta_chunks)])
    _save_index(index, meta)

def query(q: str, k=6):
    index, meta = _load_index()
    if index is None:
        return []
    qv = np.array(embed(q)[0], dtype="float32")
    faiss.normalize_L2(qv.reshape(1,-1))
    D, I = index.search(qv.reshape(1,-1), k)
    return [meta[i] for i in I[0] if i < len(meta)]
