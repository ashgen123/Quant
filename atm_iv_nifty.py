#!/usr/bin/python
import os
import mibian
import MySQLdb
import scipy as sp
import numpy as np
import pandas as pd
import pylab as plt
import datetime as dt;
import pdb
dbuser=os.environ['dbuser']
dbhost=os.environ['dbhost']
dbpass=os.environ['dbpass']
dbdatabase=os.environ['dbdatabase']

def execute_sql_query(sql):
	global dbuser,dbhost,dbpass,dbdatabase;
	# Open database connection
	db = MySQLdb.connect(dbhost,dbuser,dbpass,dbdatabase)

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute(sql)

	# Fetch a single row using fetchone() method.
	data = cursor.fetchall()

	return data

def atm_iv():
	sql="""select opt_close,strike,type,timestamp,fut_close,expiry from

	(

	 select o.close as opt_close,o.strike as strike,o.option_type as type,o.timestamp as timestamp,m.close as fut_close,o.time_to_expiry as expiry from

	 (

	  select close,strike,option_type,timestamp,datediff(expiry,timestamp)/365 as time_to_expiry from nse.nse_opt where symbol='NIFTY' and datediff(expiry,timestamp)<30

	 ) o,

	 (

	  select close,timestamp from nse.nse_fut where symbol='NIFTY' and datediff(expiry,timestamp)<30

	 )m

	 where o.timestamp=m.timestamp 

	) d

	where

	(strike %100 =0) and

	(

	 (strike > (fut_close) and strike < (fut_close+100) and type='CE') 

	 or

	 (strike < (fut_close) and strike > (fut_close-100) and type='PE') 

	)

	order by timestamp,type,strike"""

	data=execute_sql_query(sql)
	calliv=[]
	putiv=[]
	calldates=[]
	putdates=[]
	#Data will be in the follwing format(close,strike,type,date,fut_close,expiry in years)
	for i in range(0,len(data)-1):
		opt_type=data[i][2]
		price=data[i][0]
		strike=data[i][1]
		timestamp=data[i][3]
		underlying=data[i][4]
		expiry=data[i][5]	
		if (expiry*365)<1:
			continue
		if (opt_type=="CE"):
			c= mibian.BS([underlying,strike,10,expiry*365], callPrice=price)
		        calliv.append(c.impliedVolatility)
			calldates.append(timestamp)
	        else:
			p= mibian.BS([underlying,strike,10,expiry*365], putPrice=price)
			putiv.append(p.impliedVolatility)
			putdates.append(timestamp)
	pdb.set_trace()
	put=pd.Series(putiv,putdates)
	call=pd.Series(calliv,calldates)
	return call,put

if __name__ == '__main__':
	[call,put]=atm_iv()
	print call,put
