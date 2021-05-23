
# Create Executable:
    
## 1. Requirements:
> Install requirements: **pyinstaller**

- use :
  
    
    > pip install pyinstaller

- or :
  

    > cd $(current_floder)
    > pip install requirements.txt
## 2. Build
> Build **executable**
    
    > pyinstaller setup.spec

## 3. Play and share
> Two folders are created:
>           
>  -> `build/`
>
>  -> `dist/` 
> 
> > The folder `BeBarBall/` in `dist/` 
> > contains the executable `BeBarBall.exe` file.

1. Run `BeBarBall.exe` directly to play.

2. Pack the entire folder `BeBarBall/` 
and send it directly to the other computer
( **_NO_** Python needed) 