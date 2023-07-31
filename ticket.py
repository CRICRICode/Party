import qrcode
from PIL import Image
import os

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(filename)

def create_ticket(ticket_template, qr_folder, output_folder):
    qr_x1, qr_y1 = map(int, input("Inserisci le coordinate (x,y) del punto in alto a sinistra del riquadro: ").split(','))
    qr_x2, qr_y2 = map(int, input("Inserisci le coordinate (x,y) del punto in basso a destra del riquadro: ").split(','))

    # Creazione della cartella di destinazione se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    qr_files = [f for f in os.listdir(qr_folder) if f.endswith(".png")]

    for qr_file in qr_files:
        qr_image = Image.open(os.path.join(qr_folder, qr_file))
        qr_image = qr_image.resize((qr_x2 - qr_x1, qr_y2 - qr_y1))

        ticket_image = Image.open(ticket_template)
        ticket_image.paste(qr_image, (qr_x1, qr_y1))

        qr_filename_without_extension = os.path.splitext(qr_file)[0]
        output_filename = f"{qr_filename_without_extension}.png"

        ticket_image.save(os.path.join(output_folder, output_filename))

if __name__ == "__main__":
    ticket_template = input("Inserisci il percorso del template del biglietto: ")
    qr_folder = input("Inserisci l'indirizzo della cartella con i codici QR: ")
    output_folder = input("Inserisci l'indirizzo della cartella di destinazione dei biglietti generati: ")

    create_ticket(ticket_template, qr_folder, output_folder)
    print("Biglietti generati con successo!")
