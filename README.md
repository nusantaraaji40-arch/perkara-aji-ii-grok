# Contoh Konektor Grok / xAI — PERKARA AJI II

Contoh pemakaian konektor Grok (custom.grok) dari workspace Muse, khusus operasi **read-only** secara default. Repo ini bagian dari proyek PERKARA AJI II — agen AI yang membuat video YouTube 8 menit dari foto presenter.

## Isi repo

| File | Konektor | Perintah |
|---|---|---|
| `grok_example.py` | custom.grok | `models`, `keyinfo`, `model`, `chat` (chat berbayar, lihat di bawah) |

## Cara pakai

```bash
python3 grok_example.py                 # models — daftar model yang bisa dipanggil key
python3 grok_example.py keyinfo         # info key (nama, ACL, status blokir)
python3 grok_example.py model grok-4.7  # baca satu model (ambil id dari `models`, jangan menebak)
```

Syarat: helper konektor harus ada di mesinmu, yaitu `~/workspace/custom-connectors/custom.grok/bin/grok.py`. Kalau helper-mu ada di tempat lain, atur lewat environment variable:

```bash
GROK_HELPER=/path/ke/grok.py python3 grok_example.py
```

## Perhatian biaya

API xAI **berbayar per token dan tanpa free tier** (tim harus top-up prepaid credits di console.x.ai). Perintah `chat` hanya jalan bila `GROK_ALLOW_SPEND=1` dipasang — tanpa itu ditolak. Jaga pesan tetap pendek.

```bash
GROK_ALLOW_SPEND=1 python3 grok_example.py chat grok-4.7 "Halo, jawab dengan satu kalimat."
```

## Tanpa secret

File-file di repo ini **tidak berisi API key, token, atau rahasia apa pun**. Semua otentikasi dilakukan helper konektor, yang memakai surrogate dari secure storage Muse. Key xAI dibuat di `console.x.ai/team/default/api-keys`, diawali `xai-`, dan hanya ditampilkan sekali saat dibuat. Jangan pernah menaruh key di file, di `.env`, atau di commit.

## Status verifikasi — jujur (2026-11-07)

Konektor Grok **belum terbukti bekerja** pada 2026-11-07: `GET /v1/models` dijawab HTTP 400 `{"code": "invalid-argument", "error": "Incorrect API key provided"}`. Panggilan yang sama tanpa kredensial dijawab 401 "No credentials presented" — jadi kredensial memang terkirim dan memang ditolak xAI sebagai key yang salah.

Perbaikan: buat key baru di `console.x.ai/team/default/api-keys` (pastikan tim sudah top-up prepaid credits), lalu reconnect. **Update 2026-11-07 ~03:01:** link reconnect sudah dikirim — status di atas bisa berubah begitu reconnect diisi. Jangan klaim konektor ini bekerja sebelum `models` berhasil.

Key yang sama ini juga bisa dipakai di Cursor (Settings → Models → OpenAI API Key + Override OpenAI Base URL `https://api.x.ai/v1`, tambah model `grok-code-fast-1` atau `grok-4.7`).

## Repo terkait (hasil screening)

Repo open source terbaik untuk memakai Grok API dari code sendiri (bukan bagian repo ini, lisensinya masing-masing):

- **xai-sdk-python** — https://github.com/xai-org/xai-sdk-python — SDK Python resmi xAI (gRPC), lisensi Apache-2.0. Paling cocok: ada video gen `grok-imagine-video` (image-to-video, durasi 10 detik, keyframes first/last frame) — jalur paling langsung mengubah foto presenter jadi klip 10 detik.
- **xai-cookbook** — https://github.com/xai-org/xai-cookbook — contoh nyata pemakaian API Grok, lisensi kustom gaya MIT (Beta Testing License, © X.AI LLC). Paling dekat dengan pipeline ini: contoh `photo-to-talking-character` (foto → karakter bicara), `storyboard-to-film`, `grok-shorts`, `photo-to-time-lapse`, `video-dubbing`.
- **grok-build** — https://github.com/xai-org/grok-build — coding agent harness + TUI dari xAI, lisensi Apache-2.0. Bukan untuk video; berguna mengotomasi pengerjaan repo `perkara-aji-ii-agent`.

Catatan biaya: semua pemakaian di atas berbayar per token/video — hitung biaya per episode sebelum dipakai produksi.

## Lisensi

Code contoh di repo ini berlisensi **MIT** (lihat `LICENSE`). Dependensi/repo terkait di atas punya lisensinya sendiri-sendiri — periksa sebelum memakai.
