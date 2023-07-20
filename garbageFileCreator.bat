echo off


echo "This is a grabage text file">grabagetxtfile.txt

timeout /t 3

call git_push_code.bat

del grabagetxtfile.txt

call git_push_code.bat