@echo off

md ##temp
copy *.png ##temp >nul
pushd ##temp
md blur
md mask
md out

for %%f in (*.png) do (
  echo %%~nxf
  magick convert "%%~nxf" -alpha extract "mask/%%~nxf"
  magick convert "%%~nxf" ^( +clone -blur 1x1 ^) -compose DstOver -composite "blur/%%~nxf"
  magick convert "blur/%%~nxf" "mask/%%~nxf" -alpha off -compose copy-opacity -composite "out/%%~nxf"
)

popd
move ##temp\out\* .
rd /s /q ##temp