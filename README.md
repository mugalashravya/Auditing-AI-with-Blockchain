# Auditing AI with Blockchain

This project integrates AI-driven anomaly detection with blockchain technology to ensure secure and transparent auditing.

## Project Structure
```
AuditingAI_Blockchain/
├── blockchain/
│   ├── contracts/
│   │   ├── AuditContract.sol
│   │   └── Migration.sol
│   ├── migrations/
│   ├── node_modules/
│   ├── package.json
│   ├── truffle-config.js
│   └── build/
│
├── flask_app/
│   ├── templates/
│   │   ├── index.html
│   │   ├── audit.html
│   │   └── result.html
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── model/
│   │   ├── anomaly_model.pkl
│   │   └── train_model.py
│   │
│   ├── app.py
│   ├── blockchain_utils.py
│   └── requirements.txt
│
├── dataset/
│   └── data.csv
│
├── README.md
└── .gitignore
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/AuditingAI_Blockchain.git
   cd AuditingAI_Blockchain
   ```

2. Install dependencies for the Flask application:
   ```bash
   pip install -r flask_app/requirements.txt
   ```

3. Install dependencies for the blockchain setup:
   ```bash
   cd blockchain
   npm install
   ```

## Usage
### Step 1: Train the AI Model
Run the model training script to create the anomaly detection model:
```bash
python flask_app/model/train_model.py
```

### Step 2: Compile and Deploy the Smart Contracts
1. Compile contracts:
   ```bash
   truffle compile
   ```
2. Migrate contracts:
   ```bash
   truffle migrate --network development
   ```

### Step 3: Start the Flask Application
1. Navigate to the `flask_app` folder:
   ```bash
   cd flask_app
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```

### Step 4: Access the Application
Open your browser and visit: [http://localhost:5000](http://localhost:5000)

## Features
✅ AI-based anomaly detection for audits  
✅ Blockchain integration for immutable record storage  
✅ Secure and transparent audit tracking  

## Future Improvements
- Add email notifications for suspicious activities
- Improve UI design for better user experience

## License
This project is licensed under the MIT License.

