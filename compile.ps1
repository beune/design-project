.\venv\Scripts\activate
Set-Location -Path src\client\frontend
npm install
npm run build
Set-Location -Path ..
python -m eel controller.py web --onefile
Write-Output "Done"
