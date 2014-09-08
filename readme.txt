Evette is a FREE application covered by the terms of the GNU General Public Licence designed to save Animal Clinics and Vet Surgeries time, effort, paperwork and money.

GNU Public Licence - http://www.gnu.org/philosophy/free-sw.html

--Requirements--

python (I have been using version 2.5 for my testing)
python-mysqldb
python-wxgtk (I have been using version 2.8 for my testing)

mysql-server

--Installation--

Once all the required packages are installed, simply run linux-install.sh from the command line, you will be prompted for the root password (so that the necessary files can be copied to /usr/local/lib). Once the installation is complete you can delete the installation folder.

You should now be able to run evette by typing evette into the command line.

Note:
The default settings assume that you have a local mysql server running on port 3306 with user root and no password (this is how mysql server is setup by default so you needn't change these settings unless you really want to). If evette cannot connect to your mysql server on startup, it will ask you for it's ip, username and password.

If evette starts successfully you will be prompted for a username and password, the default username is "user" and the password is "letmein". Once you have successfully logged in, it is advisable to go straight to the help section to find out how to create new users.