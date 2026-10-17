from multiprocessing import BoundedSemaphore
from os import path
from pathlib import Path

import anthropic
import base64

client = anthropic.Anthropic()
PROMPTS_DIR = Path(__file__).parent / "prompts"

def detect_media_type(data: bytes) -> str:
    if data.startswith(b"\x89PNG"):
        return "image/png"
    if data.startswith(b"\xff\xd8"):
        return "image/jpeg"
    if data.startswith(b"%PDF"):
        return "application/pdf"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("Nepodporovaný formát souboru")

def load_prompt(version: str) -> str:
    return (PROMPTS_DIR / f"{version}.md").read_text(encoding="utf-8")

def extract(file_path: str, prompt_version: str, model: str = "claude-haiku-5-5") -> dict:
    raw = Path(file_path).read_bytes()
    media_type = detect_media_type(raw)
    block_type = "document" if media_type == "application/pdf" else "image"

    system = load_prompt(prompt_version)
    data = base64.standard_b64encode(raw).decode("utf-8")

    response = client.messages.create(
        model = model,
        max_tokens=4096,
        system=system,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": block_type,
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": data
                        },
                    },
                    {
                      "type": "text",
                      "text": "Extract the data from this invoice."
                    },
                ],
            },
        ],
    )

    if response.stop_reason == "max_tokens":
        raise RuntimeError("Odpověd byla useknutá.")

    text = "".join(b.text for b in response.content if b.type == "text")

    return {
        "raw_text": text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.input_tokens,
    }
