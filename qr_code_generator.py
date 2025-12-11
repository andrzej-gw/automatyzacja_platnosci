import qrcode
from PIL import Image, ImageTk
import tkinter as tk

def create_qr_transaction_and_show(bank_account, value, to, title):
    data = f"||{bank_account}|{''.join(value.split(','))}|{to}|{title}|||"

    # Generate QR
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()

    # --- Tkinter window ---
    root = tk.Tk()
    root.title("QR Code – press ENTER to close"+data)

    # Convert image for Tkinter
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=tk_img)
    label.pack()

    # Enter key closes window
    root.bind("<Return>", lambda e: root.destroy())

    root.mainloop()


if __name__ == "__main__":
    create_qr_transaction_and_show(
        91114020040000331221199478,
        '5,37',
        'Andrzej Gwiazda',
        'przelew testowy'
    )
