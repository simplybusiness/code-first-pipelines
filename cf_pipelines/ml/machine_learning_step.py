from enum import Enum


class MachineLearningStep(Enum):
    DATA_INGESTION = "data_ingestion"
    DATA_VALIDATION = "data_validation"
    FEATURE_ENGINEERING = "feature_engineering"
    MODEL_TRAINING = "model_training"
    MODEL_TESTING = "model_testing"
    MODEL_DEPLOYMENT = "model_deployment"
