from flask import Flask, render_template, request, redirect, url_for
import requests, json, os, csv
from werkzeug.utils import secure_filename
from database import OracleDB

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


#############################################

# MAIN

@app.route("/", methods= ['GET','POST'])
@app.route("/main", methods= ['GET','POST'])
def main():

    if request.method == 'POST':


        file = request.files['datafile']
        if file: 
            filename = secure_filename(file.filename)
            print("filename:", filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("filepath:", file_path)
            file.save(file_path)

            data = []
            with open(file_path) as file_object:
                reader_obj = csv.reader(file_object)

                #skip the first row
                next(reader_obj)

                for row in reader_obj:
                    #print(row)
                    data.append(row)
                
                if data:

                    with OracleDB().get_connection() as connection:

                        truncate_statement = '''
                        
                        TRUNCATE TABLE masy3540_co_stock
                        
                        ''' 

                        insert_statement = '''
                        
                        INSERT INTO masy3540_co_stock
                        (
                            DT,
                            OPEN,
                            HIGH,
                            LOW,
                            CLOSE,
                            VOLUME,
                            DIVIDENDS,
                            STOCK_SPLIT
                        ) VALUES (
                            :DT,
                            :OPEN,
                            :HIGH,
                            :LOW,
                            :CLOSE,
                            :VOLUME,
                            :DIVIDENDS,
                            :STOCK_SPLIT
                        )
                        
                        '''                    

                        cursor = connection.cursor()
                        cursor.execute(truncate_statement)
                        cursor.executemany(insert_statement, data)
                        connection.commit()

                return redirect(url_for('main'))
    

    elif request.method == 'GET':

        with OracleDB().get_connection() as connection:

            graph_query = '''
                SELECT DT,CLOSE FROM masy3540_co_stock
            '''
            
            cursor = connection.cursor()
            cursor.execute(graph_query)
            graph_data = cursor.fetchall()

            labels = [row[0] for row in graph_data]
            values = [row[1] for row in graph_data]

            query = '''
                SELECT * FROM masy3540_co_stock
            '''
            
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall() #gets all records
            #print(len(data))
 
        return render_template("main.html", title="Main", data=data, labels=labels, values=values)
    
#############################################

# ADD


@app.route("/add", methods= ['GET','POST'])
def add():

    print("in add:", request.method)

    if request.method == 'GET':
        
        return render_template("add.html", title="Add")
    
    elif request.method == 'POST':

        with OracleDB().get_connection() as connection:
            cursor = connection.cursor()
        
            insert_statement= """
                INSERT INTO masy3540_co_stock
                        (
                            DT,
                            OPEN,
                            HIGH,
                            LOW,
                            CLOSE,
                            VOLUME
                        ) VALUES (
                            :DT,
                            :OPEN,
                            :HIGH,
                            :LOW,
                            :CLOSE,
                            :VOLUME
                        )
                    """
            
            DT = request.form.get("date")
            open = request.form.get("open")
            high = request.form.get("high")
            low = request.form.get("low")
            close = request.form.get("close")
            volume = request.form.get("volume")
            #print(insert_statement)
            #print(date, open, high, low, close, volumn, dividends, stock_split)

            cursor.execute(insert_statement, DT=DT,open=open,high=high,low=low,close=close,volume=volume) 
            connection.commit()
            return redirect('/main')


#############################################

# EDIT

@app.route("/edit/<id>", methods= ['GET','POST'])
def edit(id):

    print("in edit:", request.method)
    print("date:", id)
    data = None
    if request.method == 'GET':
        with OracleDB().get_connection() as connection:
            query = '''
                SELECT * FROM masy3540_co_stock WHERE DT = :DT
            '''
            
            cursor = connection.cursor()
            cursor.execute(query, DT=id)
            data = cursor.fetchone()
            return render_template("edit.html", title="Edit", data=data)
    
    elif request.method == 'POST':
        open = request.form.get("open")
        high = request.form.get("high")
        low = request.form.get("low")
        close = request.form.get("close")
        volume = request.form.get("volume")

        with OracleDB().get_connection() as connection:
            query = '''
                UPDATE masy3540_co_stock
                SET
                    DT = :DT,
                    OPEN = :OPEN,
                    HIGH = :HIGH,
                    LOW = :LOW,
                    CLOSE = :CLOSE,
                    VOLUME = :VOLUME
                WHERE DT = :DT
            '''
            
            cursor = connection.cursor()
            cursor.execute(query, DT=id,open=open,high=high,low=low,close=close,volume=volume)
            connection.commit()
            return redirect(url_for('main'))

#############################################

# DELETE

@app.route("/delete/<id>", methods= ['GET','POST'])
def delete(id):

    print("in delete:", request.method)
    print("date:", id)
    data = None
    if request.method == 'GET':
        with OracleDB().get_connection() as connection:
            query = '''
                SELECT * FROM masy3540_co_stock WHERE DT = :DT
            '''
            
            cursor = connection.cursor()
            cursor.execute(query, DT=id)
            data = cursor.fetchone()
            return render_template("delete.html", title="Delete", data=data)
    
    elif request.method == 'POST':

        with OracleDB().get_connection() as connection:
            query = '''

                DELETE FROM masy3540_co_stock

                WHERE DT = :DT
               
            '''
            
            cursor = connection.cursor()
            cursor.execute(query, DT=id)
            connection.commit()
            return redirect(url_for('main'))


##############################################

# DOWNLOAD

@app.route("/download", methods= ['GET','POST'])
def download():

    if request.method == 'GET':

        with OracleDB().get_connection() as connection:

            header_query = '''
                SELECT column_name
                FROM USER_TAB_COLUMNS
                WHERE table_name = 'MASY3540_CO_STOCK'
            '''

            row_query = '''
                SELECT *
                FROM MASY3540_CO_STOCK
            '''
            
            cursor = connection.cursor()
            cursor.execute(header_query)
            headers = cursor.fetchall()

            cursor.execute(row_query)
            rows = cursor.fetchall() 

            with open('stocks.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(headers)

                # write multiple rows
                writer.writerows(rows)
 
            return redirect(url_for('main'))






##############################################

if __name__ == "__main__":
    print("do something")
    app.run(debug=True)

