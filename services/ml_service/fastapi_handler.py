from sklearn.pipeline import Pipeline
import joblib
from sklearn.pipeline import Pipeline
import pandas as pd
# from catboost import CatboostRegressor


class FastApiHandler:
    def __init__(self):
        self.param_types={'user_id' : str, 'model_params' : dict}
        self.model_path = 'baseline.pkl'
        self.load_flat_price_model(model_path = self.model_path)
        self.required_model_params = ['age', 'building_type_int', 'latitude', 'longitude',
                                       'ceiling_height','flats_count', 'floors_total', 'has_elevator',
                                       'floor','kitchen_area','living_area', 'rooms', 'is_apartment',
                                        'studio', 'total_area']
        self.bool_features = ['has_elevator', 'is_apartment', 'studio']
        
    def load_flat_price_model(self, model_path : str):
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f'возникла ошибка {e} при загрузке модели..')
    
    def price_predict(self, model_params : dict):
        for feature in self.bool_features:
            if feature in model_params:
                model_params[feature] = bool(model_params[feature])
        df = pd.DataFrame([model_params])
        prediction = self.model.predict(df)[0]
        return float(prediction)
    
    def check_required_query_params(self, query_params: dict) -> bool:
        if 'user_id' not in query_params or 'model_params' not in query_params:
            return False
        if not isinstance(query_params['user_id'], self.param_types['user_id']):
            return False
        if not isinstance(query_params['model_params'], self.param_types['model_params']):
            return False
        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:
        missing = set(self.required_model_params) - set(model_params.keys())
        if missing:
            print(f'Отсутствуют параметры: {missing}')
            return False
        return True
    
    def validate_params(self, params : dict) -> bool:
        if self.check_required_query_params(params):
            print('')
        else:
            return False
        
        if self.check_required_model_params(params['model_params']):
            print('')
        else:
            return False
        
        return True
        
    def handle(self, params):
        try:
            if not self.validate_params(params):
                return {'ошибка' : 'проблема с параметрами'}
            prediction = self.price_predict(params['model_params'])
            response = {'user_id' : params['user_id'], 'prediction' : prediction}
            return response
        except Exception as e:
            print(f'ошибка : {e}')
            return {'ошибка' : str(e)}

        

        