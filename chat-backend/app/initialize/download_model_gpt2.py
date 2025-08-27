#!/usr/bin/env python3
"""
Script simple pour télécharger GPT-2
Usage: python download_model_gpt2.py
"""

import os
from pathlib import Path

def download_model():
    print("🚀 Téléchargement de GPT-2...")

    try:
        from huggingface_hub import snapshot_download
        
        # Configuration
        model_name = "gpt2"
        # 🔹 Chemin relatif depuis la racine du projet
        base_dir = Path(__file__).resolve().parent.parent / "llms_models"
        local_dir = base_dir / "gpt-2"
        
        # Création du dossier
        local_dir.mkdir(parents=True, exist_ok=True)
        
        # Téléchargement
        print(f"📁 Téléchargement dans: {local_dir}")
        print("⏳ Patientez...")

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
