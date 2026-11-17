#!/usr/bin/env python3
"""
Environment Diagnostic and Verification Test
AI Tools for Research - Post Mid-Sem Assignment
Student: Sujal Rajesh Ghagare (MSE2026015)
"""

import sys
import os
import platform
import json

def run_diagnostics():
    print("=" * 60)
    print("  RESEARCH ENVIRONMENT DIAGNOSTIC & VERIFICATION TEST")
    print("=" * 60)
    
    # 1. System Platform
    print(f"[1] Operating System: {platform.system()} {platform.release()} (Architecture: {platform.machine()})")
    print(f"[2] Python Version:   {sys.version.split()[0]} ({sys.executable})")
    
    # 2. Check Required Packages
    required_pkgs = ['numpy', 'pandas', 'matplotlib', 'scipy']
    all_ok = True
    print("\n[3] Library Compatibility & Import Verification:")
    for pkg in required_pkgs:
        try:
            mod = __import__(pkg)
            version = getattr(mod, '__version__', 'unknown')
            print(f"    - {pkg:<12} : INSTALLED (version {version})")
        except ImportError as e:
            print(f"    - {pkg:<12} : FAILED ({e})")
            all_ok = False
            
    # 3. Random Seed Control Check
    print("\n[4] Deterministic Seed Control Test:")
    import numpy as np
    np.random.seed(42)
    sample_a = np.random.rand(3)
    np.random.seed(42)
    sample_b = np.random.rand(3)
    seed_match = np.allclose(sample_a, sample_b)
    print(f"    - Seed Determinism: {'PASSED (Deterministic outputs verified)' if seed_match else 'FAILED'}")
    
    # 4. Directory Structure Check
    print("\n[5] Project Repository Directory Structure Check:")
    dirs = ['configs', 'data', 'notebooks', 'src', 'scripts', 'results', 'results/figures', 'paper', 'paper/figures', 'prompts']
    for d in dirs:
        exists = os.path.isdir(d)
        print(f"    - Directory {d:<18} : {'EXISTS' if exists else 'MISSING'}")
        if not exists:
            all_ok = False
            
    # 5. Configuration File Check
    print("\n[6] Configuration File Test:")
    cfg_path = os.path.join('configs', 'config.json')
    if os.path.isfile(cfg_path):
        with open(cfg_path, 'r') as f:
            cfg = json.load(f)
        print(f"    - {cfg_path} : VALID JSON (Project: {cfg.get('project_name')})")
    else:
        print(f"    - {cfg_path} : NOT FOUND")
        all_ok = False

    print("\n" + "=" * 60)
    if all_ok and seed_match:
        print("  VERIFICATION RESULT: ALL CHECKS PASSED (STATUS: READY)")
    else:
        print("  VERIFICATION RESULT: ISSUES DETECTED")
    print("=" * 60)
    return all_ok and seed_match

if __name__ == '__main__':
    success = run_diagnostics()
    sys.exit(0 if success else 1)
