@echo off
setlocal

set hspath=%CD%
set osupath="%hspath%\..\"


if exist "%hspath%\%1" (
cd %osupath%
del "drum-*.wav"
del "normal-*.wav"
del "soft-*.wav"

echo Deleted previous hitsounds!

echo Hitsounds folder "%1" found!
cd "%hspath%\%1"
dir
xcopy * %osupath%
echo Copied successfully
) else (
echo Hitsounds folder not found. Check your input!
)