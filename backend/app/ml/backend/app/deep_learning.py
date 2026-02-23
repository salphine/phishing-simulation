import tensorflow as tf
import numpy as np
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime, timedelta
import joblib
import logging
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

logger = logging.getLogger(__name__)

class DeepLearningRiskPredictor:
    """
    Advanced neural network model for predicting user risk and behavior patterns
    """
    
    def __init__(self):
        self.model = None
        self.sequence_model = None
        self.autoencoder = None
        self.feature_dim = 50
        self.sequence_length = 30  # Days of historical data
        
    def build_models(self):
        """Build ensemble of deep learning models"""
        
        # 1. Main Risk Prediction Model (Multi-layer Perceptron)
        self.model = models.Sequential([
            layers.Dense(256, activation='relu', input_shape=(self.feature_dim,)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC(), tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
        
        # 2. Sequence Model for Temporal Patterns (LSTM)
        self.sequence_model = models.Sequential([
            layers.LSTM(128, return_sequences=True, input_shape=(self.sequence_length, self.feature_dim)),
            layers.Dropout(0.2),
            layers.LSTM(64, return_sequences=False),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        self.sequence_model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # 3. Anomaly Detection Autoencoder
        self.autoencoder = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(self.feature_dim,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),  # Bottleneck
            layers.Dense(64, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(self.feature_dim, activation='sigmoid')
        ])
        
        self.autoencoder.compile(
            optimizer='adam',
            loss='mse'
        )
        
        logger.info("Deep learning models built successfully")
    
    def prepare_features(self, user_data: List[Dict]) -> np.ndarray:
        """
        Advanced feature engineering for neural networks
        """
        features = []
        
        for data in user_data:
            # Base features
            base_features = [
                data.get('risk_score', 50) / 100,
                min(data.get('click_count', 0) / 50, 1.0),
                min(data.get('training_count', 0) / 20, 1.0),
                min(data.get('hours_since_last_click', 720) / 720, 1.0),
                data.get('phishing_prone_percentage', 0) / 100,
            ]
            
            # Temporal features
            time_features = self._extract_temporal_features(data)
            
            # Behavioral features
            behavioral_features = self._extract_behavioral_features(data)
            
            # Interaction features
            interaction_features = self._extract_interaction_features(data)
            
            # Combine all features
            all_features = base_features + time_features + behavioral_features + interaction_features
            
            # Pad or truncate to feature_dim
            if len(all_features) < self.feature_dim:
                all_features.extend([0] * (self.feature_dim - len(all_features)))
            else:
                all_features = all_features[:self.feature_dim]
            
            features.append(all_features)
        
        return np.array(features)
    
    def _extract_temporal_features(self, data: Dict) -> List[float]:
        """Extract time-based features"""
        features = []
        
        # Time of day patterns
        click_times = data.get('click_times', [])
        if click_times:
            # Convert to hour of day (0-23) and normalize
            hour_patterns = [dt.hour / 23 for dt in click_times[-10:]]
            features.extend([
                np.mean(hour_patterns),
                np.std(hour_patterns),
                len([h for h in hour_patterns if 9 <= h*23 <= 17]) / len(hour_patterns)  # Work hours
            ])
        else:
            features.extend([0.5, 0, 0.5])
        
        # Day of week patterns
        days = data.get('click_days', [])
        if days:
            weekend_ratio = sum(1 for d in days if d >= 5) / len(days)
            features.append(weekend_ratio)
        else:
            features.append(0.2)
        
        return features
    
    def _extract_behavioral_features(self, data: Dict) -> List[float]:
        """Extract behavioral patterns"""
        features = []
        
        # Click patterns
        clicks = data.get('click_history', [])
        if len(clicks) > 1:
            # Inter-click intervals
            intervals = np.diff([c['timestamp'] for c in clicks])
            avg_interval = np.mean(intervals) / 86400  # Convert to days
            features.append(min(avg_interval / 7, 1.0))  # Normalize to week
            
            # Click type preferences
            link_types = [c.get('link_type', 'generic') for c in clicks]
            invoice_ratio = sum(1 for t in link_types if t == 'invoice') / len(link_types)
            security_ratio = sum(1 for t in link_types if t == 'security') / len(link_types)
            features.extend([invoice_ratio, security_ratio])
        else:
            features.extend([0.5, 0.3, 0.3])
        
        return features
    
    def _extract_interaction_features(self, data: Dict) -> List[float]:
        """Extract interaction patterns"""
        features = []
        
        # Training interaction
        trainings = data.get('training_history', [])
        if trainings:
            completion_rate = sum(1 for t in trainings if t.get('completed')) / len(trainings)
            avg_score = np.mean([t.get('score', 0) for t in trainings]) / 100
            features.extend([completion_rate, avg_score])
        else:
            features.extend([0, 0])
        
        # Response time patterns
        response_times = data.get('response_times', [])
        if response_times:
            avg_response = np.mean(response_times) / 3600  # Convert to hours
            features.append(min(avg_response / 24, 1.0))
        else:
            features.append(0.5)
        
        return features
    
    def train_models(self, historical_data: List[Dict], labels: List[int]):
        """
        Train all deep learning models
        """
        if len(historical_data) < 100:
            logger.warning("Insufficient data for deep learning")
            return
        
        # Prepare features
        X = self.prepare_features(historical_data)
        y = np.array(labels)
        
        # Split data
        split = int(0.8 * len(X))
        X_train, X_val = X[:split], X[split:]
        y_train, y_val = y[:split], y[split:]
        
        # Train main model
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=100,
            batch_size=32,
            callbacks=[early_stopping],
            verbose=0
        )
        
        # Train autoencoder (unsupervised)
        self.autoencoder.fit(
            X_train, X_train,
            epochs=50,
            batch_size=32,
            validation_split=0.1,
            verbose=0
        )
        
        logger.info("Deep learning models trained successfully")
    
    def predict_risk(self, user_features: Dict) -> Dict[str, float]:
        """
        Ensemble prediction using all models
        """
        # Prepare features
        X = self.prepare_features([user_features])
        
        predictions = {}
        
        # Main model prediction
        if self.model:
            risk_score = float(self.model.predict(X, verbose=0)[0][0])
            predictions['risk_score'] = risk_score
        
        # Anomaly detection
        if self.autoencoder:
            reconstructed = self.autoencoder.predict(X, verbose=0)
            mse = np.mean(np.square(X - reconstructed))
            anomaly_score = float(1 / (1 + np.exp(-mse)))  # Sigmoid transform
            predictions['anomaly_score'] = anomaly_score
        
        # Confidence score based on model agreement
        if len(predictions) > 1:
            confidence = 1 - np.std(list(predictions.values()))
            predictions['confidence'] = float(confidence)
        
        return predictions
    
    def detect_anomalies(self, user_data: List[Dict], threshold: float = 0.8) -> List[int]:
        """
        Detect anomalous user behavior using autoencoder
        """
        if not self.autoencoder:
            return []
        
        X = self.prepare_features(user_data)
        reconstructed = self.autoencoder.predict(X, verbose=0)
        
        # Calculate reconstruction errors
        mse = np.mean(np.square(X - reconstructed), axis=1)
        
        # Normalize errors
        normalized_errors = (mse - mse.min()) / (mse.max() - mse.min() + 1e-8)
        
        # Identify anomalies
        anomalies = np.where(normalized_errors > threshold)[0].tolist()
        
        return anomalies

class EnsembleRiskModel:
    """
    Ensemble of multiple ML models for robust prediction
    """
    
    def __init__(self):
        self.deep_learner = DeepLearningRiskPredictor()
        self.random_forest = None
        self.gradient_boost = None
        self.xgboost_model = None
        self.weights = [0.4, 0.2, 0.2, 0.2]  # Model weights
        
    def initialize_models(self):
        """Initialize all ensemble models"""
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        import xgboost as xgb
        
        self.deep_learner.build_models()
        
        self.random_forest = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42
        )
        
        self.gradient_boost = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5
        )
        
        self.xgboost_model = xgb.XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            use_label_encoder=False
        )
    
    def train_ensemble(self, X_train, y_train, X_val, y_val):
        """Train all ensemble models"""
        
        # Train deep learning
        self.deep_learner.train_models(X_train, y_train)
        
        # Train traditional ML models
        self.random_forest.fit(X_train, y_train)
        self.gradient_boost.fit(X_train, y_train)
        self.xgboost_model.fit(X_train, y_train)
        
        # Optimize weights using validation set
        self._optimize_weights(X_val, y_val)
    
    def _optimize_weights(self, X_val, y_val):
        """Optimize ensemble weights using validation performance"""
        from scipy.optimize import minimize
        
        # Get individual predictions
        dl_pred = self.deep_learner.model.predict(X_val)
        rf_pred = self.random_forest.predict_proba(X_val)[:, 1]
        gb_pred = self.gradient_boost.predict_proba(X_val)[:, 1]
        xgb_pred = self.xgboost_model.predict_proba(X_val)[:, 1]
        
        predictions = np.column_stack([dl_pred, rf_pred, gb_pred, xgb_pred])
        
        # Objective function to minimize (negative accuracy)
        def objective(weights):
            weights = weights / weights.sum()
            ensemble_pred = np.dot(predictions, weights)
            ensemble_pred = (ensemble_pred > 0.5).astype(int)
            accuracy = np.mean(ensemble_pred == y_val)
            return -accuracy
        
        # Optimize
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        bounds = [(0, 1) for _ in range(4)]
        
        result = minimize(
            objective,
            self.weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        self.weights = result.x / result.x.sum()
    
    def predict_ensemble(self, X) -> Dict[str, Any]:
        """Get ensemble prediction"""
        
        # Get individual predictions
        dl_pred = self.deep_learner.model.predict(X)[0][0]
        rf_pred = self.random_forest.predict_proba(X)[0][1]
        gb_pred = self.gradient_boost.predict_proba(X)[0][1]
        xgb_pred = self.xgboost_model.predict_proba(X)[0][1]
        
        # Weighted ensemble
        weighted_pred = (
            self.weights[0] * dl_pred +
            self.weights[1] * rf_pred +
            self.weights[2] * gb_pred +
            self.weights[3] * xgb_pred
        )
        
        # Calculate prediction uncertainty
        predictions = [dl_pred, rf_pred, gb_pred, xgb_pred]
        uncertainty = np.std(predictions)
        
        return {
            'risk_score': float(weighted_pred),
            'uncertainty': float(uncertainty),
            'individual_predictions': {
                'deep_learning': float(dl_pred),
                'random_forest': float(rf_pred),
                'gradient_boost': float(gb_pred),
                'xgboost': float(xgb_pred)
            },
            'model_weights': self.weights.tolist()
        }

class RealTimeLearner:
    """
    Online learning system that adapts in real-time
    """
    
    def __init__(self):
        self.model = None
        self.experience_buffer = []
        self.buffer_size = 1000
        self.learning_rate = 0.01
        
    def update_from_feedback(self, user_data: Dict, actual_outcome: int):
        """
        Update model in real-time based on actual outcomes
        """
        # Add to experience buffer
        self.experience_buffer.append((user_data, actual_outcome))
        
        # Maintain buffer size
        if len(self.experience_buffer) > self.buffer_size:
            self.experience_buffer.pop(0)
        
        # Perform online learning update
        if len(self.experience_buffer) >= 100:
            self._online_training_step()
    
    def _online_training_step(self):
        """
        One step of online learning using recent experiences
        """
        # Sample recent experiences
        import random
        batch = random.sample(self.experience_buffer, min(32, len(self.experience_buffer)))
        
        # Prepare batch data
        X_batch = []
        y_batch = []
        
        for data, outcome in batch:
            features = self._extract_features(data)
            X_batch.append(features)
            y_batch.append(outcome)
        
        X_batch = np.array(X_batch)
        y_batch = np.array(y_batch)
        
        # Online gradient descent update
        if self.model:
            with tf.GradientTape() as tape:
                predictions = self.model(X_batch, training=True)
                loss = tf.keras.losses.binary_crossentropy(y_batch, predictions)
            
            gradients = tape.gradient(loss, self.model.trainable_variables)
            optimizer = tf.keras.optimizers.SGD(learning_rate=self.learning_rate)
            optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
    
    def _extract_features(self, data: Dict) -> np.ndarray:
        """Extract features for online learning"""
        # Simplified feature extraction for speed
        return np.array([
            data.get('risk_score', 50) / 100,
            data.get('click_count', 0) / 50,
            data.get('training_count', 0) / 20,
            data.get('hours_since_last_click', 24) / 168,  # Week
        ])
