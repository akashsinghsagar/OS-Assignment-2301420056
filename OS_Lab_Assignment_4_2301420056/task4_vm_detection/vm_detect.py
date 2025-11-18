#!/usr/bin/env python3
"""
Detect if the system is likely a Virtual Machine.
Heuristics:
- systemd-detect-virt (if available)
- /proc/cpuinfo 'hypervisor' flag
- DMI product_name (if readable)
- Common hypervisor strings in /sys/class/dmi/id/*
"""
import os, subprocess, re

def has_cmd(cmd):
    from shutil import which
    return which(cmd) is not None

def try_systemd_detect():
    if not has_cmd("systemd-detect-virt"):
        return None
    try:
        out = subprocess.check_output(["systemd-detect-virt","--quiet","--print"], stderr=subprocess.DEVNULL)
        kind = out.decode().strip()
        return kind if kind else "unknown"
    except subprocess.CalledProcessError:
        return None
    except Exception:
        return None

def cpuinfo_hypervisor_flag():
    try:
        with open("/proc/cpuinfo") as f:
            txt = f.read()
        return "hypervisor" in txt
    except Exception:
        return False

def read_first(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except Exception:
        return ""

def check_dmi_strings():
    candidates = [
        "/sys/class/dmi/id/product_name",
        "/sys/class/dmi/id/sys_vendor",
        "/sys/class/dmi/id/board_vendor",
        "/sys/class/dmi/id/product_version",
    ]
    val = " ".join(read_first(p) for p in candidates)
    return val

def main():
    verdicts = []
    kind = try_systemd_detect()
    if kind:
        verdicts.append(f"systemd-detect-virt: {kind}")

    hv = cpuinfo_hypervisor_flag()
    verdicts.append(f"/proc/cpuinfo has 'hypervisor' flag: {hv}")

    dmi = check_dmi_strings()
    verdicts.append("DMI strings: " + (dmi if dmi else "(unavailable)"))

    indicators = (dmi + " " + (kind or "")).lower()
    is_vm_guess = any(x in indicators for x in ["kvm","qemu","vmware","virtualbox","hyper-v","xen","parallels"]) or hv

    print("\n".join(verdicts))
    print(f"\nLikely running inside VM: {is_vm_guess}")

if __name__ == "__main__":
    main()
