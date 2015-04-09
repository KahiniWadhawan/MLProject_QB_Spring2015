# -*- coding: utf-8 -*-
import numpy as np
from user import User
from question import Question
from parent_feature_extractor import FeatureExtractor
    
class CategoryFeatureExtractor(FeatureExtractor):
    def __init__(self, user_id, qid):
        self.user = User(user_id)
        self.question = Question(qid)
        self.user_id = self.user.user_id