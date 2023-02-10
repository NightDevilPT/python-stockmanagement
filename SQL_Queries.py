import sqlite3 as SQL
from tkinter import messagebox


######===========[ Create Table Start ]==========#####
def Create_Table(database_name=None,table_name=None,heading=(),data_types=(),primary_key=None):
    try:
        sql = SQL.connect(database_name)
        sql_cur = sql.cursor()

        columns = ""
        for i in heading:
            if heading.index(i)==len(heading)-1:
                if primary_key==i:
                    columns = columns + i + " " + data_types[heading.index(i)] + " Primary key"
                else:
                    columns = columns + i + " " + data_types[heading.index(i)]
            else:
                if primary_key==i:
                    columns = columns + i + " " + data_types[heading.index(i)] + " Primary key,"
                else:
                    columns = columns + i + " " + data_types[heading.index(i)] + ','

        query = f"create table if not exists {table_name}({columns})"
        sql_cur.execute(query)
        sql.close()
    except Exception as e:
        print(e,"insert")
        messagebox.showerror("",f"{e}")
######===========[ Create Table End ]==========#####


def Update_Data(database_name="",table_name="",update_column="",update_value=(),key_column="",key_value=""):
    try:
        sql = SQL.connect(database_name)
        sql_cur = sql.cursor()

        qry = f"update {table_name} set {update_column} where ({key_column}='{key_value}')"
        sql_cur.execute(qry,update_value)
        
        sql.commit()
        sql.close()
        return True
    except Exception as e:
        print(e)
        return False


def Insert_Data(database_name="",table_name="",columns="",values=[]):

    try:
        sql = SQL.connect(database_name)
        sql_cur = sql.cursor()
        
        bind_q=""

        for i in values:
            if values.index(i)==len(values)-1:
                bind_q = bind_q + "?"
            else:
                bind_q = bind_q + "?,"

        qry = f"INSERT INTO {table_name}({columns})VALUES({bind_q})"
        sql_cur.execute(qry,values)

        sql.commit()
        sql.close()
        return True
    except Exception as e:
        print(e)
        messagebox.showerror("",f"{e}{table_name}")
        return False

######===========[ Delete Data Start ]==========#####
def Delete_Data(database_name="",table_name="",key_value=None,key_column=None):
    try:
        sql = SQL.connect(database_name)
        sqlcur = sql.cursor()

        qry = f"delete from {table_name} where {key_column}='{key_value}'"
        sqlcur.execute(qry)

        sql.commit()
        sql.close()
        return True
    except Exception as e:
        print(e)
        return False
    pass
######===========[ Delete Data End ]==========#####

def Select_All_Data(database_name="",table_name=""):
    try:
        sql = SQL.connect(database_name)
        sql_cur = sql.cursor()
        
        qry = f"SELECT * FROM {table_name}"
        sql_cur.execute(qry)
        data = sql_cur.fetchall()

        sql.close()
        return data
    except Exception as e:
        print(e)
        return False


def Select_Data_Using_Like(database_name=None,Table_Name=None,Select_data="*",ID="",Values=""):
    try:
        sql = SQL.connect(database_name)
        sql_cur = sql.cursor()

        qry = f"select {Select_data} from {Table_Name} where {ID} Like '{Values}%'"
        sql_cur.execute(qry)
        data = sql_cur.fetchall()

        sql.close()
        return data
    except Exception as e:
        return []


def Select_Specified_Data(database_name="",table_name="",select_data="*",key_columns="",key_values=()):
    try:
        sql = SQL.connect(database_name)
        sql_cur = sql.cursor()
        
        qry = f"SELECT {select_data} FROM {table_name} where ({key_columns})"
        sql_cur.execute(qry,key_values)
        data = sql_cur.fetchall()

        sql.close()
        return data
    except Exception as e:
        print(e)
        return False