from app.mapper.getmaxnumvaluemapper import Getmaxnumvaluemapper
import utils.mysqldb_utils
class Getmaxnumvaluedao :

	def getsysrecfldautorecordfieldauto(RECORD_ID, FIELD_ID) :
		returnVal = utils.mysqldb_utils.querySQL(Getmaxnumvaluemapper.getsysrecfldautorecordfieldauto(RECORD_ID, FIELD_ID),{"RECORD_ID":RECORD_ID,"FIELD_ID":FIELD_ID})
		return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
	
	
	def insertrecordfieldautointosysrecfldauto(BUSINESS_UNIT, RECORD_ID, FIELD_ID,FIRST_REG_DTM, FIRST_REG_ID, LAST_UPDATE_DTM, LAST_UPDATE_ID) :
		utils.mysqldb_utils.insertSQL(Getmaxnumvaluemapper.insertrecordfieldautointosysrecfldauto(BUSINESS_UNIT, RECORD_ID, FIELD_ID, FIRST_REG_DTM, FIRST_REG_ID, LAST_UPDATE_DTM, LAST_UPDATE_ID),{"BUSINESS_UNIT":BUSINESS_UNIT,"RECORD_ID":RECORD_ID,"FIELD_ID":FIELD_ID,"FIRST_REG_DTM":FIRST_REG_DTM,"FIRST_REG_ID":FIRST_REG_ID,"LAST_UPDATE_DTM":LAST_UPDATE_DTM,"LAST_UPDATE_ID":LAST_UPDATE_ID})
	
	
	def uptrecordfieldautotosysrecfldauto(NUM_VAR, LAST_UPDATE_DTM, LAST_UPDATE_ID, RECORD_ID, FIELD_ID) :
		utils.mysqldb_utils.updateSQL(Getmaxnumvaluemapper.uptrecordfieldautotosysrecfldauto(NUM_VAR, LAST_UPDATE_DTM, LAST_UPDATE_ID, RECORD_ID, FIELD_ID),{"NUM_VAR":NUM_VAR,"LAST_UPDATE_DTM":LAST_UPDATE_DTM,"LAST_UPDATE_ID":LAST_UPDATE_ID,"RECORD_ID":RECORD_ID,"FIELD_ID":FIELD_ID})
	
	
	def getlastnumfronusertablecontent(FIELD_ID, RECORD_ID, FIELD_IDS, headStr) :
		returnVal = utils.mysqldb_utils.querySQL(Getmaxnumvaluemapper.getlastnumfronusertablecontent(FIELD_ID, RECORD_ID, FIELD_IDS, headStr),{"FIELD_ID":FIELD_ID,"RECORD_ID":RECORD_ID,"FIELD_IDS":FIELD_IDS,"headStr":headStr})
		return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
	


