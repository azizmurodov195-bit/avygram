import os, re, subprocess, json, urllib.request

# 1. Обновляем версию до 1.1.3 и увеличиваем APP_VERSION_CODE в gradle.properties
with open("gradle.properties", "r") as f:
    lines = f.readlines()

out = []
for l in lines:
    if l.startswith("APP_VERSION_NAME="):
        out.append("APP_VERSION_NAME=1.1.3\n")
    elif l.startswith("APP_VERSION_CODE="):
        v = int(l.strip().split("=")[1]) + 1
        out.append(f"APP_VERSION_CODE={v}\n")
    else:
        out.append(l)

with open("gradle.properties", "w") as f:
    f.writelines(out)

print("VERSION_UPDATED_TO_1.1.3")
