.\venv\Scripts\activate
Set-Location -Path src\client\frontend
npm install
npm run build
Set-Location -Path ..
python -m eel app.py web --onefile
Write-Output "Done"
