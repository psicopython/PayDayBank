import os

os.system("""
    rm -rf migrations app/dbase.db
    flask db init && flask db migrate && flask db upgrade
""")
