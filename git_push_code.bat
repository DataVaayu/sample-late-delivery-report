 
@echo on
set datetime=%date% %time%

git add .
git commit -m "%datetime%"
git push origin main --force
