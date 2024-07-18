## Installation 

Follow these insturctions to setup your own instance of the app:

### 1: Clone the repo

```sh
git clone https://github.com/im-ukr/SmartStay
```

### 2: Cd to the folder

Open terminal/cmd/powershell and change directory/folder to the cloned folder. 

The command for the same would be

```sh
cd Location\ To/SmartStay
```

### 3: Install the PIP packages/dependencies

After you cd into the repo folder, ensure you see the following cmd/terminal prompt

```sh
Something.../SmartStay $
```

If not, repeat the previous step.

After this, run the following command in cmd/terminal:

```sh
pip install -r requirements.txt
```

### 4: Setup the database

To create the database from the MySQL schema, either:

1: Copy-paste the contents of [sql/hms.sql](sql/hms.sql) directly into the MySQL command line, or

2: Use the command to do it automatically (from cmd)

```sh
get-content sql/hms.sql | mysql -u<username> -p<password>
```

This will create and setup the database.

(**<u>Note</u>**: Don't **include the "<>" angular brackets** in the command, and replace the `<username>` and `<password>` with the credentials created in MySQL

### 5: Add database credentials to the app

Start by renaming the `.example.env` file just `.env`, and then replacing the `Your-Username` and `Your-Password` values with the MySQL credentials.

### 6: Installing Fonts

In order to make the app's gui look good, you will have to install the Montserrat font. From the `assets` folder, install all three fonts (with `.ttf` format) by double clicking them.

### 7: It's done 🎉 | Run the app

Run `main.py` file with python 3 and you should see the login window, if you have followed each step correctly.

The default username and password are `username` and `password` respectively.
