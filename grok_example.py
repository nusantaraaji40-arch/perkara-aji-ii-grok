#!/usr/bin/env python3
"""Contoh pemakaian konektor Grok / xAI (custom.grok) — READ-ONLY secara default.

STATUS VERIFIKASI — JUJUR, 2026-11-07: GAGAL / BELUM TERBUKTI.
Perintah `models` (GET /v1/models ke api.x.ai) dijawab HTTP 400
`{"code": "invalid-argument", "error": "Incorrect API key provided"}`.
Artinya key yang tersimpan DITOLAK xAI — bukan key xAI yang valid. Perintah
yang sama tanpa kredensial dijawab 401, jadi kredensial memang terkirim dan
memang ditolak. Identitas pemilik key belum terbukti. JANGAN klaim konektor
ini bekerja sebelum `models` berhasil.
Perbaikan: buat key baru di https://console.x.ai/team/default/api-keys
(pastikan tim sudah top-up prepaid credits — xAI API tidak punya free tier),
lalu reconnect konektor custom.grok.

File ini TIDAK berisi API key/token/rahasia apa pun. Semua otentikasi
dilakukan oleh helper resmi di
~/workspace/custom-connectors/custom.grok/bin/grok.py yang memakai
surrogate dari secure storage. Helper memakai base OpenAI-compatible
https://api.x.ai/v1 dengan header `Authorization: Bearer <key>`.

PERHATIAN BIAYA: chat completion memakai kredit prepaid (berbayar per token,
tanpa free tier). Perintah `chat` di file ini HANYA jalan bila variabel
lingkungan GROK_ALLOW_SPEND=1 dipasang — tanpa itu perintah ditolak dengan
pesan. Jaga pesan tetap pendek.

Cara pakai:
    python3 grok_example.py                 # models (daftar model)
    python3 grok_example.py models          # sama
    python3 grok_example.py keyinfo         # info key (nama, ACL, blokir)
    python3 grok_example.py model grok-4.7  # baca satu model
    GROK_ALLOW_SPEND=1 python3 grok_example.py chat grok-4.7 "Halo, jawab dengan satu kalimat."
"""

import os
import subprocess
import sys

HELPER = os.environ.get("GROK_HELPER", "/home/hatch/workspace/custom-connectors/custom.grok/bin/grok.py")


def run(*args: str) -> int:
    """Jalankan helper grok.py dengan argumen dan teruskan outputnya."""
    cmd = ["python3", HELPER, *args]
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, text=True)
    return result.returncode


def main() -> int:
    args = sys.argv[1:] or ["models"]
    allowed = {"models", "keyinfo", "model", "chat"}
    if args[0] not in allowed:
        print(f"Perintah tidak diizinkan: {args[0]}", file=sys.stderr)
        print(f"Yang diizinkan: {sorted(allowed)}", file=sys.stderr)
        return 2
    if args[0] == "model" and len(args) < 2:
        print("Pemakaian: model <model_id>  (contoh: grok-4.7)", file=sys.stderr)
        print("Ambil model_id dari daftar `models` — jangan menebak id lama.",
              file=sys.stderr)
        return 2
    if args[0] == "chat":
        if os.environ.get("GROK_ALLOW_SPEND") != "1":
            print("DITOLAK: chat memakai kredit prepaid xAI (berbayar).",
                  file=sys.stderr)
            print("Bila memang mau mencoba, jalankan dengan:",
                  file=sys.stderr)
            print("  GROK_ALLOW_SPEND=1 python3 grok_example.py chat "
                  "<model_id> \"<pesan pendek>\"", file=sys.stderr)
            return 2
        if len(args) < 3:
            print("Pemakaian: chat <model_id> \"<pesan>\"", file=sys.stderr)
            return 2
        print("PERINGATAN: panggilan ini memakai kredit prepaid xAI.",
              file=sys.stderr)
    return run(*args)


if __name__ == "__main__":
    raise SystemExit(main())
