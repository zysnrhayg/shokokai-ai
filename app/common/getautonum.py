from app.dao.getmaxnumvaluedao import Getmaxnumvaluedao
from app.dto.getmaxnumvalueentity import GetMaxNumValueEntity
import utils.date_util
from flask import session 
import utils.string_util
import utils.string_const
import utils.dbconstant
import utils.config 
class GetAutonum :
	def getMaxNumValue(self,RecordID,FieldID) :                                                                                         
		returnVal = None                                                                                                                    
		alData = []                                                                              
		numVarData = None
		alRowData = []                                                                                                         
		sb = ""                                                                                                       
		headChar = ""                                                                                                                      
		maxNumVar = 1                                                                                                                         
		curNum = ""                                                                                                                        
		dataType = ""                                                                                                                      
		dataLen = ""                                                                                                                       
		userValue = ""                                                                                                                     
		tmpValue = ""                                                                                                                      
		dateFormatPattern = ""                                                                                                            
		dateString = ""                                                                                                                   
		alDataMap = {}
		try :                                                                                                                                       
			alData = alDataMap[RecordID+FieldID]                                                                                                 
			iNumLen = 0                                                                                                                   
			if alData != None  and len(alData)>0 :                                                                                          
				alRowData = alData[0]                                                                                                 
		                                                                                                                              
				numVarData = self.getsysrecfldautorecordfieldauto(RecordID, FieldID)                                                                           
				if numVarData != None and len(numVarData) > 0 :                                                                       
					curNum = utils.string_util.changeNullToBlank(numVarData[0][0])                                                   
				else :                                                                                                                   
					self.insertrecordfieldautointosysrecfldauto(RecordID, FieldID)                                                                          
					curNum = "0"                                                                                                      
		                                                                                                                              
				#データ長さ                                                                                                               
				dataLen = utils.string_util.changeNullToBlank( alRowData[4])                                                              
				#頭文字                                                                                                                  
				headChar = utils.string_util.changeNullToBlank( alRowData[0])                                                              
		                                                                                                                              
				if len(utils.string_util.ChangeIntToString(utils.string_util.parseInt(curNum) + 1)) > utils.string_util.changeStringToInt(dataLen) :      
					curNum = "0"                                                                                                      
				#最大番号                                                                                                                 
				#番号の長さ                                                                                                               
				if utils.string_util.isNullOrBlank(alRowData[2]) :                                                                          
					iNumLen = utils.string_util.parseInt(dataLen)                                                                            
				else :                                                                                                                   
					iNumLen = utils.string_util.parseInt(utils.string_util.changeNullToBlank(alRowData[2]))                                     
				#データタイプ                                                                                                             
				dataType = utils.string_util.changeNullToBlank( alRowData[3])                                                                
                                                                                                                                            
				#ユーザーテーブル自動採番値を取得                                                                                         
				userValue = utils.string_util.changeNullToBlank(self.getlastnumfronusertablecontent(headChar, FieldID, RecordID))                                        
		                                                                                                                              
				if (dataType == utils.dbconstant.MYSQL_DATA_TYPE_INT                                                                        
						or dataType==utils.dbconstant.MYSQL_DATA_TYPE_UNDEFINED                                               
						or dataType==utils.dbconstant.MYSQL_DATA_TYPE_DOUBLE                                                     
						or dataType==utils.dbconstant.MYSQL_DATA_TYPE_DATE                                                       
						or dataType==utils.dbconstant.MYSQL_DATA_TYPE_DATETIME                                                 
						or dataType==utils.dbconstant.MYSQL_DATA_TYPE_TIME                                                       
						or dataType==utils.dbconstant.MYSQL_DATA_TYPE_BOOLEAN):                                                  
					pass                                                   
		                                                                                                                              
				#特殊採番ルール対応                                                                                                       
				tmpValue = headChar                                                                                                       
				start = tmpValue.find("[")                                                                                                            
				end = tmpValue.find("]")                                                                                                             
				while start > -1 and end  > -1 :                                   
					if start > -1 and end > -1 and start < end :                                                                       
						dateFormatPattern = tmpValu[start + 1, end]                                                    
						dateString = utils.date_util.getPatternDate(dateFormatPattern)                                                  
				headChar = tmpValue                                                                                                       
		                                                                                                                              
				#フィールド定義の最大値                                                                                                   
				if utils.string_util.isNullOrBlank(curNum) == False :                                                                                     
					maxNumVar = utils.string_util.parseInt(curNum) + 1                                                                      
				                                                                                                                    
                                                                                                                                            
				#ユーザー値の頭文字を削除                                                                                                 
				userValue = userValue.replace(headChar, utils.string_const.STRING_OF_BLANK)                                                 
		                                                                                                                              
				#比較し、最大値を利用                                                                                                     
				if  utils.string_util.changeStringToInt(userValue)+1 > maxNumVar :                                                              
					maxNumVar =  utils.string_util.parseInt(userValue) + 1                                                                
		                                                                                                                              
				sb = headChar                                                                                                      
		                                                                                                                              
				iZeroCnt = iNumLen - len(utils.string_util.ChangeIntToString(maxNumVar))                                               
				for i in range(0,iZeroCnt) :                                                                                       
					sb += "0"                                                                                                   
				                                                                                                                          
				sb += utils.string_util.ChangeIntToString(maxNumVar)                                                                      
			returnVal = sb                                                                                                         
			self.uptrecordfieldautotosysrecfldauto(RecordID, FieldID, utils.string_util.ChangeIntToString(maxNumVar))                                                      
		except Exception as e:                                                                                                                   
			utils.config.global_log.error("SQL文を取得時にエラー：%s", e)                                                                                    
		return returnVal                                                                                                                         
	def getsysrecfldautorecordfieldauto(self,RecordID,FieldID) :                          
		returnVal = []                                                              
		returnValStr = []                                                               
		maxNum = []
		try :                                                                                                       
			maxNum = Getmaxnumvaluedao.getsysrecfldautorecordfieldauto(RecordID, FieldID)                     
			if maxNum != None :
				for  maxnums in maxNum :
					returnValStr.insert(len(returnValStr),utils.string_util.dict_get(maxnums, "NUM_VAR"))
					returnVal.insert(len(returnVal),returnValStr)
		except Exception as e:                                                                                   
			utils.config.global_log.error("ﾚｺｰﾄﾞ定義(管理用)取得時にエラー：%s", e)                                          
			returnValStr = None
			maxNum = None
		return returnVal                                                                                           
	def insertrecordfieldautointosysrecfldauto(self,RecordID,FieldID) :                                                                                                                        
		try :                                                                                                                                                                                
			Getmaxnumvaluedao.insertrecordfieldautointosysrecfldauto("AI000000105", RecordID, FieldID, utils.date_util.getPatternDateForDb(), "", utils.date_util.getPatternDateForDb(), "");
		except Exception as e:                                                                                                                                                            
			utils.config.global_log.error("ﾚｺｰﾄﾞ定義(管理用)取得時にエラー：%s", e)                                                                                                                       
                                                                                                                                                                                 
	def uptrecordfieldautotosysrecfldauto(self,RecordID,FieldID, NUM_VAR) :                                           
	                                                                                         
		# ﾒｯｾｰｼﾞ一覧の取得                                                                      
		try :                                                                                    
			Getmaxnumvaluedao.uptrecordfieldautotosysrecfldauto(NUM_VAR, utils.date_util.getPatternDateForDb(), "", RecordID, FieldID);
		except Exception as e:                                                                
			utils.config.global_log.error("ﾚｺｰﾄﾞ定義(管理用)取得時にエラー：%s", e)               
	def getlastnumfronusertablecontent(self,headStr, FieldID, RECORD_ID) :                                                                                                               
		alData = []                                                                                                                                          
		# ﾒｯｾｰｼﾞ一覧の取得                                                                                                                                                                  
		returnValStr = []                                                              
		maxNum = []
		fieldID = ""                                                                                                                                                                 
		                                                                                                                                                                                     
		try :                                                                                                                                                                                
			                                                                                                                                                                             
			if FieldID.find(",") != -1 :                                                                                                                                            
				fieldID = FieldID[0,FieldID.find(",")]                                                                                                               
			else:                                                                                                                                                                     
				fieldID = FieldID                                                                                                                                                   
			                                                                                                                                                                             
			maxNum = Getmaxnumvaluedao.getlastnumfronusertablecontent(fieldID, RECORD_ID, fieldID, headStr)                     
			if maxNum != None :
				for  maxnums in maxNum :
					returnValStr.insert(len(returnValStr),utils.string_util.dict_get(maxnums, "numString"))
					alData.insert(len(alData),returnValStr)
			                                                                                                                                                                             
			if alData != None and len(alData) > 0 :                                                                                                                                     
				return alData[0][0]                                                                                                                                       
			else :                                                                                                                                                                    
				return utils.string_const.STRING_OF_BLANK                                                                                                                                  
		except Exception as e:                                                                                                                                                            
			utils.config.global_log.error("レコードのフィールド情報を更新時にエラー：%s", e)                                                                                                           

