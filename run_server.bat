@echo off
title Miniature Galaxy - 微缩银河
echo ============================================================
echo   微缩银河 · Miniature Galaxy (Three.js 3D Particle Universe)
echo   正在启动本地宇宙服务器并自动打开浏览器...
echo ============================================================
start http://localhost:8088/index.html
python -m http.server 8088
pause
