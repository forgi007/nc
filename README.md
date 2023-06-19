DO NOT UES, NOT READY YET.

Scripts for Nextcloud Memories or Photos app, to help removing the duplicate files.

If you have a lot of (image) files with duplicates in several directories and you would like to organize it and remove duplicates, then I suggest this approach:
1., flatten directories, only keep directories which are similar to albums, e.g. 'backup_2001/holyday_italy/img_20010606.jpg' -> 'holyday_italy/img_20010606.jpg'. 
It is not a good idea to simply use `mv` to move the files and subdirectories, because you may overwrite some files. So, use `move_rename_dupes` to move files and directories, but rename files when yhey have the same name in source and destination directory
2., ...

Notes:
jdupes -jzrS /var/www/nextcloud/data/doro/files/ | tee dup.json
jdupes -uzrS /var/www/nextcloud/data/doro/files/ | tee uniq.json

filesize:
https://datagy.io/python-file-size/

file preview
https://www.w3schools.com/html/html_images.asp
https://pypi.org/project/preview-generator/
https://www.digitalocean.com/community/tutorials/python-simplehttpserver-http-server
https://gist.github.com/yukixz/5835965