#!/usr/bin/env python3
"""
Script simple pour télécharger GPT-OSS-20B
Usage: python download_simple.py
"""

import os
from pathlib import Path

def download_model():
    print("🚀 Téléchargement de GPT-OSS-20B...")
    
    try:
        from huggingface_hub import snapshot_download
        
        # Configuration
        model_name = "openai/gpt-oss-20b"
        local_dir = "./models/gpt-oss-20b"
        
        # Création du dossier
        Path(local_dir).mkdir(parents=True, exist_ok=True)
        
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