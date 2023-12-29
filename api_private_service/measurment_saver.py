import datetime
import mysql.connector
from .logger import get_logger
from flask import current_app

class MeasurmentSaver(object):
    
    def __init__(self):
        self.user = current_app.config['DB_USER']
        self.password = current_app.config['DB_PASSWORD']
        self.logger = get_logger()
        self.mydb = None

    def __enter__(self):
        try:
            self.mydb = mysql.connector.connect(host='localhost',
                                       user=self.user,
                                       password=self.password,
                                       database = 'monitor')
            self.logger.log_info('Connected to DB')
        except Exception as error:
            self.logger.log_error(str(error))     
        return self.save_temperature
 
    def __exit__(self, *args):
        if self.mydb == None:
            self.logger.log_error('Can not close connection to DB')
            return
        
        self.mydb.close() 
        self.logger.log_info('DB connection is closed')

    def save_temperature(self, sensor_id: int, temperature: float, humidity: float):
        date = datetime.datetime.now()
        self.logger.log_info('    date: {}'.format(date)) 
        m1 = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute=date.minute)
        self.logger.log_info(' M1 date: {} ({})'.format(m1, m1.timestamp()))
        m5 = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute= (date.minute // 5) * 5)
        self.logger.log_info(' M5 date: {} ({})'.format(m5, m5.timestamp()))
        m15 = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute= (date.minute // 15) * 15)
        self.logger.log_info('M15 date: {} ({})'.format(m15, m15.timestamp()))
        m30 = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=date.hour, minute= (date.minute // 30) * 30)
        self.logger.log_info('M30 date: {} ({})'.format(m30, m30.timestamp()))
        h1 = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=date.hour)
        self.logger.log_info(' H1 date: {} ({})'.format(h1, h1.timestamp()))
        h4 = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=(date.hour // 4) * 4)
        self.logger.log_info(' H4 date: {} ({})'.format(h4, h4.timestamp()))
        d1 = datetime.datetime(year=date.year, month=date.month, day=date.day)
        self.logger.log_info(' D1 date: {} ({})'.format(d1, d1.timestamp()))
        self.logger.log_info('Temperature: {}C, humidity: {}%'.format(temperature, humidity))

        if self.mydb == None:
            self.logger.log_error('Can not store to DB')
            return

        mycursor = self.mydb.cursor()

        sql = """INSERT INTO measurings 
                    (timestamp,
                    sensor_id,
                    m5,
                    m15,
                    m30,
                    h1,
                    h4,
                    d1,
                    temperature,
                    humidity) 
                VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s) 
                ON DUPLICATE KEY UPDATE temperature = %s, humidity = %s"""
        
        val = (m1.timestamp(), 
               sensor_id,
               m5.timestamp(),
               m15.timestamp(),
               m30.timestamp(),
               h1.timestamp(),
               h4.timestamp(),
               d1.timestamp(),
               temperature,
               humidity,
               temperature,
               humidity)
        
        mycursor.execute(sql, val)
        self.mydb.commit()

        self.logger.log_info('-------------------------------------------------------------------------')