#!/usr/bin/env python3
"""
Script simple pour télécharger GPT-OSS-20B
Usage: python download_models_oss.py
"""

from pathlib import Path

def download_model():
    print("🚀 Téléchargement de GPT-OSS-20B...")

    try:
        from huggingface_hub import snapshot_download

        # Nom du modèle
        model_name = "openai/gpt-oss-20b"

        # 🔹 Chemin relatif depuis la racine du projet
        base_dir = Path(__file__).resolve().parent.parent / "llms_models"
        local_dir = base_dir / "gpt-oss-20b"

        # Création du dossier si nécessaire
        local_dir.mkdir(parents=True, exist_ok=True)

        # Téléchargement
        print(f"📁 Téléchargement dans: {local_dir}")
        print("⏳ Patientez... (peut prendre plusieurs heures)")

        snapshot_download(
            repo_id=model_name,
            local_dir=local_dir,
            resume_download=True,
            ignore_patterns=[
                "*.msgpack", "*.h5", "*.ot", "*.tflite",
                "rust_model.ot", "tf_model.h5"
            ]
        )

        print("✅ Téléchargement terminé!")
        print(f"📍 Modèle disponible dans: {local_dir}")

    except ImportError:
        print("❌ Installez d'abord: pip install huggingface_hub")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    download_model()
