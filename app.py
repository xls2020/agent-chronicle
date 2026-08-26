"""Agent Chronicle — 极简 WebUI 入口 (FastAPI, 单文件后端)

功能:
  1. 展示小说全文
  2. 展示脱敏样本
  3. 展示对照关系 (mapping)
  4. 配置页: 接入任意 LLM 的 API (保存到本地 config, 不提交)

依赖: fastapi + uvicorn (见 requirements.txt)
运行: python app.py  ->  http://localhost:8000
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
CHRONICLES = ROOT / "chronicles"
SAMPLES = ROOT / "samples"
WEBUI = ROOT / "src" / "webui"
CONFIG_FILE = ROOT / "webui_config.json"  # local-only, gitignored

app = FastAPI(title="Agent Chronicle", version="0.1")


def _read(path: Path, default=""):
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8", errors="replace")


@app.get("/", response_class=HTMLResponse)
def index():
    return _read(WEBUI / "index.html", "<h1>Agent Chronicle</h1>")


@app.get("/api/chronicles")
def list_chronicles():
    files = sorted(CHRONICLES.glob("*.md"))
    return [{"name": f.stem, "title": f.stem, "path": f.name} for f in files if f.name != "README.md"]


@app.get("/api/chronicle/{name}")
def get_chronicle(name: str):
    # safe path: only allow .md under chronicles/; accept name with or
    # without the ".md" extension (the list endpoint returns the bare stem).
    candidates = [name] if name.endswith(".md") else [name, name + ".md"]
    for cand in candidates:
        safe = (CHRONICLES / cand).resolve()
        if safe.is_relative_to(CHRONICLES.resolve()) and safe.suffix == ".md" and safe.exists():
            return {"name": name, "content": safe.read_text(encoding="utf-8", errors="replace")}
    return JSONResponse({"error": "not found"}, status_code=404)


@app.get("/api/events")
def get_events():
    events = []
    p = SAMPLES / "desensitized_events.jsonl"
    if p.exists():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return events


@app.get("/api/mapping")
def get_mapping():
    m = json.loads(_read(SAMPLES / "mapping.json", "{}"))
    return m


@app.get("/api/config")
def get_config():
    cfg = json.loads(_read(CONFIG_FILE, "{}"))
    return cfg


@app.post("/api/config")
async def save_config(req: dict):
    # store LLM config locally; never commit
    CONFIG_FILE.write_text(json.dumps(req, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True}


@app.get("/api/health")
def health():
    return {"status": "ok", "chronicles": len(list(CHRONICLES.glob("*.md")))}


# static frontend
app.mount("/static", StaticFiles(directory=str(WEBUI)), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
