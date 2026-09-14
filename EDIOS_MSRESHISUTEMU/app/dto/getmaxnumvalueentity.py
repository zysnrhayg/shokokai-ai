from utils.base_entity import BaseEntity
class GetMaxNumValueEntity(BaseEntity) :

	def __init__(self,mode,actflg,trigger,NUM_VAR) : 
		super().__init__(mode,actflg,trigger)
		self.NUM_VAR = NUM_VAR
	def get_NUM_VAR(self) : 
	 	return self.NUM_VAR

