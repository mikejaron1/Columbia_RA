import psycopg2

##index dun bradstreet number, country code, year, state, and county
## state = dstateab, duns = duns number, dnatlcod = NATIONAL CODES, dcountyc = DUN AND BRADSTREET COUNTY CODE

con = psycopg2.connect(database='dun_bradstreet')
cur = con.cursor() 

cur.execute('CREATE INDEX main_index ON main (year, dstateab, duns, dnatlcod, dcountyc);')
con.commit()
print('Finished')












