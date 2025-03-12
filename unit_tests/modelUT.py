from model import train_or_update_model, predict_price

train_or_update_model()
print("✅ Model trained successfully.")

prediction = predict_price()
if prediction:
    print(f"✅ Model prediction successful: {prediction}")
else:
    print("❌ Model prediction failed.")