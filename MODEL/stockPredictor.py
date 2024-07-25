import pandas as pd
import numpy as np
import mysql.connector
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler, RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from tensorflow import keras
from tensorflow.keras import layers
import joblib

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sunDay01@new",
    database="blockchain_user_data"
)
cursor = conn.cursor()

def fetch_data_to_dataframe(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    return df

table_names = [
    "BlockchainTransactions",
    "UserProfile",
    "BehavioralPatterns",
    "CreditAndFinancialHistory",
    "NetworkAnalysis",
    "SentimentAnalysis",
    "CommunityBehavior",
    "SystemAndPlatformScores",
    "DeviceAndIPInformation",
    "MachineLearningFeatures",
    "HistoricalFraudData",
    "ExternalDataSources"
]

dataframes = {}
for table_name in table_names:
    dataframes[table_name] = fetch_data_to_dataframe(table_name)

conn.close()

def droper(data_frames, table_name, col_arr):
    data_frames[table_name] = data_frames[table_name].drop(columns=col_arr)

def handle_dates(data, column_names):
    df = data.copy()
    for column_name in column_names:
        df[column_name] = pd.to_datetime(df[column_name])
    return df

def apply_nlp_label_encoding(df, column_names):
    stemmer = PorterStemmer()
    for column in column_names:
        if column in df.columns and df[column].dtype == 'object':
            df[column] = df[column].apply(lambda x: ' '.join([stemmer.stem(word) for word in word_tokenize(x.lower())]))

    label_encoder = LabelEncoder()
    for column in column_names:
        if column in df.columns and df[column].dtype == 'object':
            df[column] = label_encoder.fit_transform(df[column])
    return df

def apply_feature_scaling(dataframe, column_names):
    X = dataframe[column_names].values
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
    y_train = np.random.rand(X_train.shape[0])
    y_test = np.random.rand(X_test.shape[0])
    scaling_results = {}

    for scaler in [StandardScaler(), MinMaxScaler(), RobustScaler()]:
        scaled_X_train = scaler.fit_transform(X_train)
        scaled_X_test = scaler.transform(X_test)
        model = LinearRegression()
        model.fit(scaled_X_train, y_train)
        y_pred = model.predict(scaled_X_test)
        mse = mean_squared_error(y_test, y_pred)
        scaling_results[str(scaler)] = mse

    best_scaling = min(scaling_results, key(scaling_results.get))
    return best_scaling

def OnehotcodeEncoding(df, categorical_columns):
    df = pd.get_dummies(df, columns=categorical_columns)
    return df

def numerical_preprocessing(data_frames, table_name, columns):
    if table_name in data_frames:
        scaler = StandardScaler()
        data_frames[table_name][columns] = scaler.fit_transform(data_frames[table_name][columns])

def lableEncoding(df, categorical_columns):
    label_encoder = LabelEncoder()
    for column in categorical_columns:
        df[column] = label_encoder.fit_transform(df[column])
    return df

def apply_mice(data, max_iter=10, random_state=None):
    if hasattr(data, 'to_numpy'):
        data = data.to_numpy()
    mice_imputer = IterativeImputer(max_iter=max_iter, random_state=random_state)
    filled_data = mice_imputer.fit_transform(data)
    return filled_data

def combiner(dataframes, table_names):
    combined_dataframes = {table_name: dataframes[table_name] for table_name in table_names}
    combined_df = pd.concat(combined_dataframes.values(), axis=1)
    return combined_df

dataframes['BlockchainTransactions'] = handle_dates(dataframes['BlockchainTransactions'], ['Timestamp'])
dataframes['UserProfile'] = handle_dates(dataframes['UserProfile'], ['AccountCreationDate'])
dataframes["UserProfile"] = apply_nlp_label_encoding(dataframes["UserProfile"], ['KYCStatus'])
columns_to_drop = ['Name', 'Address', 'Email', 'UserID', 'PhoneNumber']
droper(dataframes, 'UserProfile', columns_to_drop)

best_scaling = apply_feature_scaling(dataframes['BlockchainTransactions'], ['AmountTransferred', 'TransactionFee', 'BlockHeight'])
scaler = MinMaxScaler()
dataframes['BlockchainTransactions'][['AmountTransferred', 'TransactionFee', 'BlockHeight']] = scaler.fit_transform(dataframes['BlockchainTransactions'][['AmountTransferred', 'TransactionFee', 'BlockHeight']])
dataframes['BlockchainTransactions'] = OnehotcodeEncoding(dataframes['BlockchainTransactions'], ['ReceiverAddress'])
droper(dataframes, 'BlockchainTransactions', ['TransactionID', 'SenderAddress'])

dataframes['BehavioralPatterns'] = apply_nlp_label_encoding(dataframes['BehavioralPatterns'], ['TransactionSizeDistribution', 'GeographicInconsistencies', 'TimeOfDayPatterns', 'RegularVsIrregularBehavior', 'ChangesInBehaviorOverTime'])
numerical_preprocessing(dataframes, "BehavioralPatterns", ['TransactionFrequency'])
droper(dataframes, 'BehavioralPatterns', ['UserID'])

best_scaling = apply_feature_scaling(dataframes['CreditAndFinancialHistory'], ['CreditScore', 'CreditCardUtilization', 'IncomeLevel', 'DebtToIncomeRatio'])
scaler = RobustScaler()
dataframes['CreditAndFinancialHistory'][['CreditScore', 'CreditCardUtilization', 'IncomeLevel', 'DebtToIncomeRatio']] = scaler.fit_transform(dataframes['CreditAndFinancialHistory'][['CreditScore', 'CreditCardUtilization', 'IncomeLevel', 'DebtToIncomeRatio']])
dataframes['CreditAndFinancialHistory'] = apply_nlp_label_encoding(dataframes['CreditAndFinancialHistory'], ['LoanRepaymentHistory', 'PastFraudulentActivity'])
droper(dataframes, 'CreditAndFinancialHistory', ['UserID'])

best_scaling = apply_feature_scaling(dataframes['NetworkAnalysis'], ['DegreeCentrality', 'ClusteringCoefficients'])
scaler = StandardScaler()
dataframes['NetworkAnalysis'][['DegreeCentrality', 'ClusteringCoefficients']] = scaler.fit_transform(dataframes['NetworkAnalysis'][['DegreeCentrality', 'ClusteringCoefficients']])
dataframes['NetworkAnalysis'] = lableEncoding(dataframes['NetworkAnalysis'], ['AnomaliesInNetwork'])
droper(dataframes, 'NetworkAnalysis', ['SenderUserID', 'ReceiverUserID'])

dataframes['SentimentAnalysis'] = apply_nlp_label_encoding(dataframes['SentimentAnalysis'], ['SocialMediaSentiment', 'TransactionSentiment', 'FinancialTransactionSentiment'])
droper(dataframes, 'SentimentAnalysis', ['UserID'])

best_scaling = apply_feature_scaling(dataframes['SystemAndPlatformScores'], ['SystemTrustScore', 'PlatformReliabilityScore'])
scaler = MinMaxScaler()
dataframes['SystemAndPlatformScores'][['SystemTrustScore', 'PlatformReliabilityScore']] = scaler.fit_transform(dataframes['SystemAndPlatformScores'][['SystemTrustScore', 'PlatformReliabilityScore']])
dataframes['SystemAndPlatformScores'] = lableEncoding(dataframes['SystemAndPlatformScores'], ['PastSecurityIncidents'])
droper(dataframes, 'SystemAndPlatformScores', ['UserID'])

droper(dataframes, 'DeviceAndIPInformation', ['UserID', 'IPAddress', 'DeviceLocation', 'DeviceID', 'DeviceTypeAndVersion'])
dataframes['DeviceAndIPInformation'] = lableEncoding(dataframes['DeviceAndIPInformation'], ['ProxyOrVPNUsage'])

dataframes['MachineLearningFeatures'] = lableEncoding(dataframes['MachineLearningFeatures'], ['HistoricalFraudData', 'AnomalyDetectionFeatures', 'ClusteringFeatures', 'DeepLearningModelFeatures'])
droper(dataframes, 'MachineLearningFeatures', ['UserID'])

droper(dataframes, 'HistoricalFraudData', ['TransactionID', 'BlacklistedEntities'])
dataframes['HistoricalFraudData'] = lableEncoding(dataframes['HistoricalFraudData'], ['FraudulentTransactions', 'PreviousFraudulentActivity'])

combine_df = combiner(dataframes, table_names)
combine_df.drop(columns=['Timestamp', 'AccountCreationDate'], inplace=True)

X = combine_df.drop(columns=['FraudulentTransactions'])
y = combine_df['FraudulentTransactions']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, y_train)
y_pred = logistic_regression.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Logistic Regression Accuracy:", accuracy)

joblib.dump(logistic_regression, 'logistic_regression_model.pkl')

model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[X_test.shape[1]]),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
neural_net_accuracy = model.evaluate(X_test, y_test, verbose=0)[1]
print("Neural Network Accuracy:", neural_net_accuracy)

model.save('neural_network_model.h5')
