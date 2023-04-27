import mysql.connector

def getConnection():
    dbConnection = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    passwd="password",
    database="brain_tumour_database",
     
    )
    return dbConnection

def insertPatient(patient):
    dbConnection = getConnection()
    mycursor = dbConnection.cursor()
    sql = "INSERT INTO patient  VALUES (DEFAULT,%s, %s,%s)"
    val = (patient['patientName'], patient['age'],patient['gender'])
    mycursor.execute(sql, val)
    id = mycursor.lastrowid
    dbConnection.commit()
    
    return str(id)

def insertScanImage(scanImage):
    dbConnection = getConnection()
    mycursor = dbConnection.cursor()
    sql = "INSERT INTO scan_image  VALUES (DEFAULT,%s, %s,DEFAULT,%s)"
    isTumour=0
    if scanImage["isTumour"]=="Its a tumour":
        isTumour=1
    val = (int(scanImage["patientId"]),isTumour,float(scanImage["predictionPercentage"]))
    mycursor.execute(sql, val)
    id = mycursor.lastrowid
    dbConnection.commit()
    return str(id)

def getScanResults(patientId):
    dbConnection = getConnection()
    mycursor = dbConnection.cursor()
    sql = "SELECT * FROM scan_image WHERE patient_id="+str(patientId)
    mycursor.execute(sql)
    scanImages = mycursor.fetchall()
    dbConnection.commit()
    return scanImages

def getPatient(patientId):
    dbConnection = getConnection()
    mycursor = dbConnection.cursor()
    sql = "SELECT * FROM patient WHERE id="+str(patientId)
    mycursor.execute(sql)
    patient = mycursor.fetchone()
    if patient is None:
        return {"patientId":"null"}
    patient= {"patientId":patient[0],"patientName":patient[1],"age":patient[2],"gender":patient[3]}
    dbConnection.commit()
    return patient




