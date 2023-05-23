from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('mymodel')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Define digit dictionary
        digit_dict = {
            0: 'zero',
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine'
        }

        # Get image from request
        file = request.files['image']
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28,28)) # Resize - important!
        img = cv2.bitwise_not(img)
        img = (img / 255) - 0.5
        img = img.reshape((1, 28, 28, 1))

        # Print out input image data for debugging
        print('Input image:', img)

        # Make prediction
        prediction = model.predict(img)
        predicted_digit_digit = np.argmax(prediction[0])

        # Get written-out digit from dictionary
        predicted_digit = digit_dict[predicted_digit_digit]

        # Print out output prediction for debugging
        print('Output prediction:', predicted_digit)

        # Return prediction as JSON
        return jsonify({'digit': predicted_digit})

    except Exception as e:
        print('Error processing image:', e)
        return jsonify({'error': 'Error processing image'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


