rem 環境変数 ANACONDA_ROOT: C:\Users\ユーザー\Anaconda3
pushd SerialController
call %ANACONDA_ROOT%\Scripts\activate.bat
call activate PokeCon
python Window.py
popd
