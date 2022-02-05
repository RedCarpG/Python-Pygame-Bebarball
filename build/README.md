
# Create Executable

## 1. Requirements

Install dependency modules :

use :

    > pip install -r .\build\requirements.txt

or install manually :

    > pip install pyinstaller

## 2. Build

Build **executable**

    > pyinstaller .\build\setup.spec

- or :

Run directly `build.bat`, which does the same thing.

## 3. Play and share

Two folders will be created:

> -> `build/setup`
>
> -> `dist/`

The folder `BeBarBall/` in `dist/` contains the executable `BeBarBall.exe` file.

1. Run `BeBarBall.exe` directly to play.

2. Pack the entire folder `BeBarBall/` 
and send it directly to the other computer
( **_NO_** Python needed) 