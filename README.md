# FT Seller

This application assists in selling keys from specified wallet addresses. Before running the application, ensure that necessary configurations are set in the `config.py` file.

## Configuration (`config.py`)

- `wallets_file_path : Path to the file containing wallet addresses to sell. (Do not modify this)
- `private_key : Private key of your FT account.
- `address : Address of your FT account.
- `rpc : Your RPC endpoint.
- `Authorization : Check the instruction below to obtain this.

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup `config.py`**: Configure the settings as per the instruction above.
3. **Launch `portfolio.py`**: To export your portfolio.
   ```bash
   python portfolio.py
   ```
4. **Update `wallets.txt`**: Put addresses in `wallets.txt` (If you press 'y' to save, you don’t need to do this manually).
5. **Launch `main.py`**:
   ```bash
   python main.py
   ```

## Instruction to Get Authorization

1. Go to [Friend Tech](https://www.friend.tech/) and log into your account.
2. Press `F12` and go to the Network tab.
3. Press `F5` and find the "used-code" request, then go to headers and copy the Authorization token.

## Note

Ensure that your `config.py` is correctly setup with the necessary details for the application to run successfully.
