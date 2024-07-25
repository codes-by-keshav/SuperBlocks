import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import joblib

# Load and preprocess the dataset
csv_file_path1 = 'Amazon Sale Report.csv'
df1 = pd.read_csv(csv_file_path1)

df1['Date'] = pd.to_datetime(df1['Date'])
df1['ship-postal-code'].fillna('00000', inplace=True)

label_encoders = {}
categorical_cols = ['Status', 'Fulfilment', 'Sales Channel ', 'ship-service-level', 'Style', 'Category', 'Size', 'ASIN', 'ship-city', 'ship-state', 'ship-country', 'promotion-ids', 'fulfilled-by']
for col in categorical_cols:
    le = LabelEncoder()
    df1[col] = le.fit_transform(df1[col].astype(str))
    label_encoders[col] = le

imputer = SimpleImputer(strategy='mean')
df1['Amount'] = imputer.fit_transform(df1[['Amount']])

scaler = StandardScaler()
df1[['Qty', 'Amount']] = scaler.fit_transform(df1[['Qty', 'Amount']])

df1.drop(['index', 'Order ID', 'currency', 'B2B', 'Courier Status', 'Unnamed: 22', 'SKU'], axis=1, inplace=True)
df1['ship-postal-code'] = df1['ship-postal-code'].astype('int32')

X = df1.drop(['Amount'], axis=1)
y = df1['Amount']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train[['Qty', 'ship-postal-code']] = scaler.fit_transform(X_train[['Qty', 'ship-postal-code']])
X_test[['Qty', 'ship-postal-code']] = scaler.transform(X_test[['Qty', 'ship-postal-code']])

# Train and save the ML model
ml_model = LinearRegression()
ml_model.fit(X_train, y_train)
joblib.dump(ml_model, 'ml_model.pkl')

# Train and save the DL model
dl_model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1)
])

dl_model.compile(optimizer='adam', loss='mean_squared_error')
dl_model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)
dl_model.save('dl_model.h5')

print("Models have been trained and saved.")
