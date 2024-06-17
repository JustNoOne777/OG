from ext import app

from routes import home,login,register,product,profile,create_product,edit_product,delete_product,save_command,buy_product,search

if __name__ == '__main__':
    app.run(debug=True)